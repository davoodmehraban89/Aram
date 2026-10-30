"""Synthetic tests for independent reference reconciliation; no real finance data."""
from __future__ import annotations

from io import BytesIO
import json

import pytest
from openpyxl import Workbook

from aram_backend.coverage_preview import CoverageError
from aram_backend.pilot_workbook import SHEET_HEADERS
from aram_backend.reconciliation_review import (
    NoteReference, reconcile_workbook_for_review,
)


def workbook(*, include_second_mapping=True, second_draft=False,
             split_notes=False, second_amount="15.75") -> bytes:
    book = Workbook()
    book.remove(book.active)
    for sheet_name, columns in SHEET_HEADERS.items():
        book.create_sheet(sheet_name).append(list(columns))

    def add(name, **values):
        book[name].append([values.get(key) for key in SHEET_HEADERS[name]])

    add("Company", company_code="001", company_name="Synthetic",
        fiscal_year=1404, status="Draft")
    for code, amount in [("0010", "110.25"), ("0020", second_amount)]:
        add("Accounts", company_code="001", fiscal_year=1404,
            general_code=code, general_name="General", account_full_code=code,
            account_name="Synthetic " + code, opening=amount,
            debit="0", credit="0", closing=amount, source_row=7,
            row_status="Draft", closing_delta="0")
    add("Notes", company_code="001", fiscal_year=1404,
        statement="BS", statement_section="Assets",
        note_number="N01", note_title="Cash")
    if split_notes:
        add("Notes", company_code="001", fiscal_year=1404,
            statement="BS", statement_section="Assets",
            note_number="N02", note_title="Other")

    for index, code in enumerate(["0010", "0020"]):
        if index == 1 and not include_second_mapping:
            continue
        add("Mapping", mapping_id=f"M{index + 1}", company_code="001",
            fiscal_year=1404, account_full_code=code, account_level="General",
            general_code=code, target_statement="BS",
            statement_section="Assets", note_number="N02" if split_notes
            and index == 1 else "N01", mapping_version=1,
            approval_status="Draft" if index == 1 and second_draft else "Approved",
            reviewer="Synthetic reviewer" if index == 0 or not second_draft else None,
            review_date="2026-10-31" if index == 0 or not second_draft else None,
            validation_status="Valid", source="Synthetic")

    output = BytesIO()
    book.save(output)
    book.close()
    return output.getvalue()


def ref(amount="126.00", note="N01", statement="BS",
        section="Assets", evidence="SYNTHETIC-TB-1") -> NoteReference:
    return NoteReference(
        statement=statement, section=section, note_number=note, subnote_code="",
        expected_closing_exposure=amount, evidence_ref=evidence,
    )


def evaluate(content=None, references=None, company="001", year=1404):
    return reconcile_workbook_for_review(
        content if content is not None else workbook(),
        company_code=company, fiscal_year=year,
        references=[ref()] if references is None else references,
    )


def test_fully_reconciled_is_still_not_financial_approval():
    reviewed = evaluate()
    assert reviewed.matched_for_analyst_review
    assert not reviewed.findings
    assert reviewed.account_count == reviewed.candidate_mapped_accounts == 2
    assert reviewed.blocked_accounts == 0
    assert len(reviewed.notes) == 1
    assert reviewed.notes[0].difference == "0.00"
    assert reviewed.notes[0].candidate_closing_exposure == "126.00"
    assert not reviewed.financial_statement
    assert not reviewed.trusted_approvals
    assert not reviewed.approved
    assert not reviewed.releasable


def test_mismatch_blocks_without_tolerance_or_rounding():
    reviewed = evaluate(references=[ref("126.01")])
    assert not reviewed.matched_for_analyst_review
    assert reviewed.notes[0].difference == "-0.01"
    assert reviewed.findings[0].code == "NOTE_EXPOSURE_MISMATCH"


def test_missing_account_mapping_blocks_even_with_matching_reference():
    reviewed = evaluate(content=workbook(include_second_mapping=False),
                        references=[ref("110.25")])
    assert not reviewed.matched_for_analyst_review
    assert reviewed.blocked_accounts == 1
    assert any(e.code == "BLOCKED_ACCOUNT_UNMAPPED_ACCOUNT"
               and e.account_code == "0020" for e in reviewed.findings)


def test_workbook_marked_draft_is_not_silently_approved():
    reviewed = evaluate(content=workbook(second_draft=True),
                        references=[ref("110.25")])
    assert not reviewed.matched_for_analyst_review
    assert any("NOT_FILE_MARKED_APPROVED" in e.code for e in reviewed.findings)


def test_missing_reference_blocks_and_does_not_invent_a_total():
    reviewed = evaluate(references=[])
    assert not reviewed.matched_for_analyst_review
    assert reviewed.notes[0].reference_closing_exposure is None
    assert reviewed.notes[0].difference is None
    assert reviewed.findings[0].code == "MISSING_NOTE_REFERENCE"


def test_extra_reference_blocks_without_creating_a_note():
    reviewed = evaluate(references=[ref(), ref("1", note="N99")])
    assert not reviewed.matched_for_analyst_review
    extra = next(note for note in reviewed.notes if note.note_number == "N99")
    assert extra.candidate_closing_exposure is None
    assert extra.reference_closing_exposure == "1"
    assert any(f.code == "UNKNOWN_REFERENCE_TARGET" for f in reviewed.findings)


def test_separate_notes_reference_order_is_irrelevant():
    data = workbook(split_notes=True)
    left = evaluate(content=data, references=[ref("110.25"), ref("15.75", note="N02")])
    right = evaluate(content=data, references=[ref("15.75", note="N02"), ref("110.25")])
    assert left.matched_for_analyst_review and right.matched_for_analyst_review
    assert left.reference_sha256 == right.reference_sha256
    assert left.notes == right.notes


def test_duplicate_reference_rejected_not_deduplicated():
    with pytest.raises(CoverageError) as err:
        evaluate(references=[ref(), ref("126.00", evidence="ANOTHER")])
    assert str(err.value) == "DUPLICATE_NOTE_REFERENCE"


@pytest.mark.parametrize("refs", [
    "not a list", (item for item in []), [object()],
    [ref()] * 10_001,
])
def test_reference_collection_fails_closed(refs):
    with pytest.raises(CoverageError):
        evaluate(references=refs)


@pytest.mark.parametrize("bad", [
    ref(statement="OTHER"), ref(note=""), ref(note=" N01"),
    ref(section="Assets\nInjected"), ref(evidence=""),
    ref(amount="NaN"), ref(amount="Infinity"), ref(amount="1E+999"),
    ref(amount="0E-99999999"), ref(amount="nonsense"),
    ref(amount="1" * 151),
])
def test_invalid_reference_rejected(bad):
    with pytest.raises(CoverageError):
        evaluate(references=[bad])


def test_reference_amount_must_be_text_not_float_or_bool():
    with pytest.raises(CoverageError):
        evaluate(references=[ref(126.0)])
    with pytest.raises(CoverageError):
        evaluate(references=[ref(True)])


def test_wrong_company_or_year_has_no_fallback():
    with pytest.raises(CoverageError):
        evaluate(company="002")
    with pytest.raises(CoverageError):
        evaluate(year=1403)


def test_provenance_hashes_bind_input_and_reference():
    source = workbook()
    original = bytes(source)
    left = evaluate(content=source, references=[ref()])
    right = evaluate(content=source, references=[ref("126.00", evidence="SYNTHETIC-TB-2")])
    assert left.source_sha256 == right.source_sha256
    assert left.reference_sha256 != right.reference_sha256
    assert len(left.source_sha256) == len(left.reference_sha256) == 64
    assert source == original


def test_signed_negative_amount_is_compared_without_faking_statement_signs():
    reviewed = evaluate(content=workbook(second_amount="-15.75"),
                        references=[ref("94.50")])
    assert reviewed.matched_for_analyst_review
    assert reviewed.source_closing_exposure == "94.50"


def test_read_only_packet_is_json_safe_and_explicitly_provisional():
    result = evaluate()
    data = json.loads(json.dumps(result.to_dict(), sort_keys=True))
    assert data["kind"] == "UNAPPROVED_NOTE_RECONCILIATION_REVIEW"
    assert data["matched_for_analyst_review"]
    assert data["releasable"] is False


def test_untrusted_invalid_excel_fails_before_comparison():
    with pytest.raises(CoverageError):
        evaluate(content=b"invalid xlsx")


def test_unmatched_cents_do_not_disappear_in_decimal_context():
    reviewed = evaluate(references=[ref("126.000000000000001")])
    assert reviewed.notes[0].difference == "-1E-15"
    assert not reviewed.matched_for_analyst_review
