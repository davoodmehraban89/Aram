"""Synthetic-only tests for unsigned income statement presentation."""
from __future__ import annotations

from dataclasses import replace
from io import BytesIO
from decimal import Decimal, localcontext
import json

import pytest
from openpyxl import Workbook

from aram_backend.coverage_preview import CoverageError
from aram_backend.income_statement_candidate import (
    IncomeStatementLinePolicy,
    build_income_statement_candidate,
)
from aram_backend.pilot_workbook import SHEET_HEADERS
from aram_backend.reconciliation_review import NoteReference


ITEMS = (
    ("REV", "200", "Revenue", "R01", "REVENUE", -1),
    ("COS", "110", "Cost", "C01", "COST_OF_REVENUE", 1),
    ("OPE", "40", "Operating", "O01", "OPERATING_EXPENSE", 1),
    ("OIN", "10", "Other income", "I01", "OTHER_INCOME", -1),
    ("OEX", "5", "Other expense", "X01", "OTHER_EXPENSE", 1),
    ("TAX", "10", "Taxes", "T01", "TAX_EXPENSE", 1),
)


def workbook(*, costs="110", missing_mapping=False, include_bs=False,
             revenue="200") -> bytes:
    book = Workbook()
    book.remove(book.active)
    for name, columns in SHEET_HEADERS.items():
        book.create_sheet(name).append(list(columns))

    def add(name, **values):
        book[name].append([values.get(key) for key in SHEET_HEADERS[name]])

    add("Company", company_code="001", company_name="Synthetic test only",
        fiscal_year=1404, status="Draft")
    items = tuple(
        (code, revenue if code == "REV" else costs if code == "COS" else amount,
         section, note, category, sign)
        for code, amount, section, note, category, sign in ITEMS
    )
    if include_bs:
        items += (("AST", "0", "Assets", "A01", "BS", 1),)
    for index, (code, amount, section, note, category, sign) in enumerate(items, 2):
        closing = str(-Decimal(amount)) if sign == -1 else amount
        add("Accounts", company_code="001", fiscal_year=1404,
            general_code=code, general_name=section, account_full_code=code,
            account_name="Synthetic " + section, opening=closing, debit="0",
            credit="0", closing=closing, closing_delta="0",
            source_row=index, row_status="Draft")
        statement = "BS" if category == "BS" else "IS"
        add("Notes", company_code="001", fiscal_year=1404,
            statement=statement, statement_section=section,
            note_number=note, note_title=section)
        if missing_mapping and code == "TAX":
            continue
        add("Mapping", mapping_id="M-" + code, company_code="001",
            fiscal_year=1404, account_full_code=code, account_level="General",
            general_code=code, target_statement=statement,
            statement_section=section, note_number=note, mapping_version=1,
            approval_status="Approved", reviewer="Synthetic reviewer",
            review_date="2026-10-31", validation_status="Valid", source="Synthetic")
    stream = BytesIO()
    book.save(stream)
    book.close()
    return stream.getvalue()


def references(*, costs="110", include_bs=False, revenue="200"):
    result = []
    for code, amount, section, note, category, sign in ITEMS:
        replacement = revenue if code == "REV" else costs if code == "COS" else amount
        closing = str(-Decimal(replacement)) if sign == -1 else replacement
        result.append(NoteReference("IS", section, note, "", closing, "SYNTH-" + code))
    if include_bs:
        result.append(NoteReference("BS", "Assets", "A01", "", "0", "SYNTH-BS"))
    return result


def policies():
    return [
        IncomeStatementLinePolicy(section, note, "", category, sign,
                                  "Synthetic " + section, "SYNTH-POL-" + code)
        for code, _, section, note, category, sign in ITEMS
    ]


def build(*, data=None, refs=None, pol=None):
    return build_income_statement_candidate(
        workbook_bytes=workbook() if data is None else data,
        company_code="001", fiscal_year=1404,
        references=references() if refs is None else refs,
        policies=policies() if pol is None else pol,
    )


def test_complete_profit_bridge_never_claims_approval():
    result = build()
    assert result.eligible_for_analyst_review
    assert not result.findings
    assert result.revenue_total == "200"
    assert result.cost_of_revenue_total == "110"
    assert result.gross_profit == "90"
    assert result.operating_expense_total == "40"
    assert result.operating_profit == "50"
    assert result.other_income_total == "10"
    assert result.other_expense_total == "5"
    assert result.profit_before_tax == "55"
    assert result.tax_expense_total == "10"
    assert result.net_result == "45"
    assert len(result.lines) == 6
    assert result.kind == "UNAPPROVED_INCOME_STATEMENT_PRESENTATION_CANDIDATE"
    assert not result.official_financial_statement
    assert not result.accounting_policy_authorized
    assert not result.independently_reviewed
    assert not result.export_authorized
    assert not result.releasable
    assert all(line.policy_evidence_ref for line in result.lines)


def test_real_loss_is_not_false_positive_if_expense_exceeds_income():
    result = build(data=workbook(costs="290"), refs=references(costs="290"))
    assert result.eligible_for_analyst_review
    assert result.net_result == "-135"
    assert result.gross_profit == "-90"
    assert not result.findings


def test_zero_cost_of_revenue_is_valid_with_explicit_reference():
    # Source and reference keep the same input amount; no unseen tax estimate.
    result = build(data=workbook(costs="0"), refs=references(costs="0"))
    assert result.cost_of_revenue_total == "0"
    assert result.net_result == "155"
    assert result.eligible_for_analyst_review


def test_other_statement_reconciled_but_excluded_from_income_rows():
    result = build(data=workbook(include_bs=True), refs=references(include_bs=True))
    assert result.eligible_for_analyst_review
    assert len(result.lines) == 6
    assert all(l.note_number != "A01" for l in result.lines)


def test_other_statement_missing_reference_blocks_income_preview():
    result = build(data=workbook(include_bs=True))
    assert not result.eligible_for_analyst_review
    assert "UPSTREAM_RECONCILIATION_BLOCKED" in result.findings


def test_unmapped_tax_account_blocks_even_with_other_matching_notes():
    result = build(data=workbook(missing_mapping=True),
                   refs=references()[:-1])
    assert not result.eligible_for_analyst_review
    assert "UPSTREAM_RECONCILIATION_BLOCKED" in result.findings


def test_reference_mismatch_blocks_even_when_profit_bridge_can_be_computed():
    refs = references()
    refs[0] = replace(refs[0], expected_closing_exposure="-201")
    result = build(refs=refs)
    assert not result.eligible_for_analyst_review
    assert "UPSTREAM_RECONCILIATION_BLOCKED" in result.findings


def test_missing_income_policy_blocks():
    result = build(pol=policies()[:-1])
    assert not result.eligible_for_analyst_review
    assert "MISSING_INCOME_POLICY" in result.findings


def test_orphan_income_policy_blocks():
    p = policies()
    p.append(IncomeStatementLinePolicy("Extra", "Z1", "", "REVENUE", 1,
                                       "Synthetic extra", "SYNTH-POL"))
    result = build(pol=p)
    assert "ORPHAN_INCOME_POLICY" in result.findings
    assert not result.eligible_for_analyst_review


def test_negative_presentation_value_blocked_without_sign_guessing():
    p = policies()
    p[0] = replace(p[0], sign_multiplier=1)
    result = build(pol=p)
    assert "NEGATIVE_INCOME_PRESENTATION_AMOUNT" in result.findings
    assert not result.eligible_for_analyst_review
    assert result.revenue_total == "-200"


def test_policy_order_does_not_change_hash_or_rows():
    p = policies()
    first = build(pol=p)
    second = build(pol=list(reversed(p)))
    assert first.lines == second.lines
    assert first.presentation_policies_sha256 == second.presentation_policies_sha256


def test_policy_change_changes_evidence_hash():
    p = policies()
    first = build(pol=p)
    p[0] = replace(p[0], line_label="Synthetic revenues revised")
    second = build(pol=p)
    assert first.presentation_policies_sha256 != second.presentation_policies_sha256


@pytest.mark.parametrize("invalid", [
    "invalid", [None], [object()], [policies()[0]] * 10001,
])
def test_policy_collection_invalid(invalid):
    with pytest.raises(CoverageError):
        build(pol=invalid)


@pytest.mark.parametrize("invalid", [
    IncomeStatementLinePolicy("Revenue", "R01", "", "REVENUE", True, "Revenue", "P"),
    IncomeStatementLinePolicy("Revenue", "R01", "", "REVENUE", 0, "Revenue", "P"),
    IncomeStatementLinePolicy("Revenue", "R01", "", "OTHER", 1, "Revenue", "P"),
    IncomeStatementLinePolicy("Revenue", "", "", "REVENUE", -1, "Revenue", "P"),
    IncomeStatementLinePolicy("Revenue", "R01", "", "REVENUE", -1, "", "P"),
    IncomeStatementLinePolicy("Revenue", "R01", "", "REVENUE", -1, "Revenue", ""),
    IncomeStatementLinePolicy("Revenue", "R01", "", "REVENUE", -1, "Bad" + chr(10) + "Label", "P"),
])
def test_invalid_policy_blocked(invalid):
    with pytest.raises(CoverageError):
        build(pol=[invalid])


def test_duplicate_policy_is_never_deduplicated():
    p = policies()
    with pytest.raises(CoverageError) as error:
        build(pol=p + [p[0]])
    assert error.value.code == "DUPLICATE_INCOME_POLICY"


def test_missing_income_notes_is_nonreleasable():
    from test_balance_sheet_candidate import workbook as bs_workbook
    from test_balance_sheet_candidate import references as bs_references
    result = build(data=bs_workbook(), refs=bs_references(), pol=[])
    assert not result.eligible_for_analyst_review
    assert "NO_INCOME_STATEMENT_NOTES" in result.findings
    assert result.net_result == "0"


def test_source_bytes_preserved_and_results_json_safe():
    content = workbook()
    snapshot = bytes(content)
    result = json.loads(json.dumps(build(data=content).to_dict()))
    assert content == snapshot
    assert result["releasable"] is False
    assert isinstance(result["net_result"], str)
    assert len(result["source_sha256"]) == 64
    assert len(result["note_references_sha256"]) == 64
    assert len(result["presentation_policies_sha256"]) == 64


def test_company_and_year_strict_scoping():
    with pytest.raises(CoverageError):
        build_income_statement_candidate(
            workbook(), company_code="999", fiscal_year=1404,
            references=references(), policies=policies(),
        )
    with pytest.raises(CoverageError):
        build_income_statement_candidate(
            workbook(), company_code="001", fiscal_year=1403,
            references=references(), policies=policies(),
        )


def test_invalid_xlsx_fails_closed():
    with pytest.raises(CoverageError):
        build(data=b"not XLSX")


def test_tiny_exact_decimal_is_not_rounded_away():
    small = "0." + "0" * 30 + "1"
    result = build(
        data=workbook(costs=small),
        refs=references(costs=small),
    )
    assert result.eligible_for_analyst_review
    assert Decimal(result.cost_of_revenue_total) == Decimal(small)
    with localcontext() as context:
        context.prec = 400
        expected = str(Decimal("155") - Decimal(small))
    assert result.net_result == expected
