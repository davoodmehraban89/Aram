"""Synthetic tests of non-official, explicit-policy balance sheet presentation."""
from __future__ import annotations

import json
from io import BytesIO

import pytest
from openpyxl import Workbook

from aram_backend.balance_sheet_candidate import (
    BalanceSheetLinePolicy, build_balance_sheet_candidate,
)
from aram_backend.coverage_preview import CoverageError
from aram_backend.pilot_workbook import SHEET_HEADERS
from aram_backend.reconciliation_review import NoteReference


def workbook(*, liability="-60", equity="-40", omit_mapping=False, add_income=False):
    book = Workbook()
    book.remove(book.active)
    for name, headers in SHEET_HEADERS.items():
        book.create_sheet(name).append(list(headers))

    def add(name, **record):
        book[name].append([record.get(column) for column in SHEET_HEADERS[name]])

    add("Company", company_code="001", company_name="Synthetic only",
        fiscal_year=1404, status="Draft")
    amounts = [("A", "100", "A1", "Assets"), ("L", liability, "L1", "Liabilities"),
               ("E", equity, "E1", "Equity")]
    if add_income:
        amounts.append(("I", "0", "I1", "Revenue"))
    for i, (code, amount, note, section) in enumerate(amounts, 1):
        add("Accounts", company_code="001", fiscal_year=1404,
            general_code=code, general_name=section, account_full_code=code,
            account_name=section + " Synthetic", opening=amount,
            debit="0", credit="0", closing=amount, source_row=i + 1,
            row_status="Draft", closing_delta="0")
        statement = "IS" if code == "I" else "BS"
        add("Notes", company_code="001", fiscal_year=1404,
            statement=statement, statement_section=section,
            note_number=note, note_title=section)
        if omit_mapping and code == "E":
            continue
        add("Mapping", mapping_id="M" + code, company_code="001",
            fiscal_year=1404, account_full_code=code, account_level="General",
            general_code=code, target_statement=statement,
            statement_section=section, note_number=note, mapping_version=1,
            approval_status="Approved", reviewer="Synthetic reviewer",
            review_date="2026-10-31", validation_status="Valid", source="Synthetic")
    output = BytesIO()
    book.save(output)
    book.close()
    return output.getvalue()


def references(*, liability="-60", equity="-40", add_income=False):
    rows = [
        NoteReference("BS", "Assets", "A1", "", "100", "SYNTH-TB-ASSET"),
        NoteReference("BS", "Liabilities", "L1", "", liability, "SYNTH-TB-DEBT"),
        NoteReference("BS", "Equity", "E1", "", equity, "SYNTH-TB-EQUITY"),
    ]
    if add_income:
        rows.append(NoteReference("IS", "Revenue", "I1", "", "0", "SYNTH-IS"))
    return rows


def policies(*, liabilities_sign=-1, equity_sign=-1):
    return [
        BalanceSheetLinePolicy("Assets", "A1", "", "ASSETS", 1,
                               "Synthetic assets", "SYNTH-POLICY-A"),
        BalanceSheetLinePolicy("Liabilities", "L1", "", "LIABILITIES", liabilities_sign,
                               "Synthetic liabilities", "SYNTH-POLICY-L"),
        BalanceSheetLinePolicy("Equity", "E1", "", "EQUITY", equity_sign,
                               "Synthetic equity", "SYNTH-POLICY-E"),
    ]


def build(*, source=None, refs=None, policy=None):
    return build_balance_sheet_candidate(
        source if source is not None else workbook(),
        company_code="001", fiscal_year=1404,
        references=references() if refs is None else refs,
        policies=policies() if policy is None else policy,
    )


def test_balanced_candidate_is_not_an_approved_financial_statement():
    result = build()
    assert result.eligible_for_analyst_review
    assert result.arithmetically_balanced
    assert result.assets_total == "100"
    assert result.liabilities_total == "60"
    assert result.equity_total == "40"
    assert result.balance_difference == "0"
    assert not result.findings
    assert len(result.lines) == 3
    assert not result.official_financial_statement
    assert not result.accounting_policy_authorized
    assert not result.independently_reviewed
    assert not result.export_authorized
    assert not result.releasable
    assert all(item.policy_evidence_ref for item in result.lines)


def test_mismatched_accounting_equation_is_flagged():
    result = build(source=workbook(liability="-59"), refs=references(liability="-59"))
    assert not result.eligible_for_analyst_review
    assert not result.arithmetically_balanced
    assert result.balance_difference == "1"
    assert "BALANCE_SHEET_DOES_NOT_BALANCE" in result.findings


def test_missing_presentation_policy_is_blocking():
    result = build(policy=policies()[:2])
    assert not result.eligible_for_analyst_review
    assert "MISSING_EXPLICIT_PRESENTATION_POLICY" in result.findings
    assert "NO_EQUITY_LINES" in result.findings


def test_extra_policy_is_blocking_even_if_equation_balances():
    p = policies()
    p.append(BalanceSheetLinePolicy("Equity", "Z9", "", "EQUITY", 1, "Ghost", "SYNTH"))
    result = build(policy=p)
    assert not result.eligible_for_analyst_review
    assert "ORPHAN_PRESENTATION_POLICY" in result.findings
    assert result.arithmetically_balanced


def test_unmapped_account_makes_statement_candidate_ineligible():
    result = build(source=workbook(omit_mapping=True),
                   refs=references()[:2])
    assert not result.eligible_for_analyst_review
    assert "UPSTREAM_RECONCILIATION_BLOCKED" in result.findings


def test_unmatched_reference_always_blocks_presentation():
    r = references()
    r[0] = NoteReference("BS", "Assets", "A1", "", "100.01", "SYNTH-OTHER")
    result = build(refs=r)
    assert not result.eligible_for_analyst_review
    assert "UPSTREAM_RECONCILIATION_BLOCKED" in result.findings


def test_wrong_sign_is_not_silently_corrected():
    result = build(policy=policies(liabilities_sign=1))
    assert not result.eligible_for_analyst_review
    assert result.liabilities_total == "-60"
    assert "NEGATIVE_PRESENTATION_AMOUNT" in result.findings
    assert "BALANCE_SHEET_DOES_NOT_BALANCE" in result.findings


def test_non_bs_notes_do_not_become_bs_lines_but_must_be_reconciled():
    result = build(source=workbook(add_income=True),
                   refs=references(add_income=True))
    assert result.eligible_for_analyst_review
    assert len(result.lines) == 3
    assert all(line.note_number != "I1" for line in result.lines)


def test_non_bs_missing_reference_still_blocks_the_gate():
    result = build(source=workbook(add_income=True))
    assert not result.eligible_for_analyst_review
    assert "UPSTREAM_RECONCILIATION_BLOCKED" in result.findings


def test_identical_policies_in_different_order_hash_identically():
    source = workbook()
    p = policies()
    r = build(source=source, policy=p)
    reverse = build(source=source, policy=list(reversed(p)))
    assert r.presentation_policies_sha256 == reverse.presentation_policies_sha256
    assert r.lines == reverse.lines
    assert r.source_sha256 == reverse.source_sha256


def test_policy_change_changes_provenance_and_flags_wrong_sign():
    original = build()
    edited = build(policy=policies(equity_sign=1))
    assert original.presentation_policies_sha256 != edited.presentation_policies_sha256
    assert not edited.eligible_for_analyst_review


def test_source_bytes_never_modified():
    data = workbook()
    original = bytes(data)
    build(source=data)
    assert data == original


@pytest.mark.parametrize("invalid", [
    "not a sequence", [object()], [None],
    [policies()[0]] * 10001,
])
def test_invalid_policy_collection_is_rejected(invalid):
    with pytest.raises(CoverageError):
        build(policy=invalid)


@pytest.mark.parametrize("bad", [
    BalanceSheetLinePolicy("Assets", "A1", "", "ASSETS", True, "Synthetic assets", "P"),
    BalanceSheetLinePolicy("Assets", "A1", "", "ASSETS", 0, "Synthetic assets", "P"),
    BalanceSheetLinePolicy("Assets", "A1", "", "OTHER", 1, "Synthetic assets", "P"),
    BalanceSheetLinePolicy("Assets", "", "", "ASSETS", 1, "Synthetic assets", "P"),
    BalanceSheetLinePolicy("Assets", "A1", "", "ASSETS", 1, "Bad\\nLine", "P"),
    BalanceSheetLinePolicy("Assets", "A1", "", "ASSETS", 1, " ", "P"),
    BalanceSheetLinePolicy("Assets", "A1", "", "ASSETS", 1, "Synthetic assets", ""),
])
def test_invalid_presentation_policy_rejected(bad):
    with pytest.raises(CoverageError):
        build(policy=[bad])


def test_duplicate_policies_rejected_even_when_identical():
    with pytest.raises(CoverageError) as e:
        build(policy=[policies()[0], policies()[0]])
    assert e.value.code == "DUPLICATE_PRESENTATION_POLICY"


def test_json_only_contains_string_amounts_and_no_approved_flags():
    candidate = json.loads(json.dumps(build().to_dict()))
    assert candidate["kind"] == "UNAPPROVED_BALANCE_SHEET_PRESENTATION_CANDIDATE"
    assert candidate["assets_total"] == "100"
    assert candidate["official_financial_statement"] is False
    assert candidate["releasable"] is False


def test_wrong_company_or_year_fails_closed():
    with pytest.raises(CoverageError):
        build_balance_sheet_candidate(workbook(), company_code="999",
                                      fiscal_year=1404,
                                      references=references(), policies=policies())
    with pytest.raises(CoverageError):
        build_balance_sheet_candidate(workbook(), company_code="001",
                                      fiscal_year=1403,
                                      references=references(), policies=policies())


def test_missing_source_fails_closed():
    with pytest.raises(CoverageError):
        build(source=b"not a valid workbook")
