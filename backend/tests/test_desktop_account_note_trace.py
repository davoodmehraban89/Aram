"""Source-account -> note trace tests on one synthetic XLSX snapshot."""
from dataclasses import replace

import pytest

from aram_backend.coverage_preview import CoverageError
from aram_backend.desktop_five_statement_details import build_preview_details
from aram_backend.desktop_five_statement_integrity import validate_desktop_pipeline_result
from test_five_statement_pipeline_integration import build_pipeline


def test_all_account_to_statement_mappings_are_visible_without_double_counting():
    result = build_pipeline()
    coverage = result.mapping_coverage
    assert coverage.account_count == len(result.trial_balance.accounts) == 6
    assert len(coverage.mappings) == 11
    assert coverage.source_sha256 == result.source_sha256
    assert all(not getattr(coverage, flag) for flag in (
        "financial_statement", "trusted_approvals", "releasable",
    ))
    valid = validate_desktop_pipeline_result(result)
    assert valid is None
    details = build_preview_details(result)
    revenue_rows = [
        row for row in details if row.item == "حساب REV / Revenue"
    ]
    assert len(revenue_rows) == 3
    assert {row.statement for row in revenue_rows} == {
        "سود و زیان", "ترازنامه", "تغییرات حقوق مالکانه",
    }
    assert all("ردیف نگاشت" in row.trace for row in revenue_rows)
    assert all("اکسل" in row.source_detail for row in revenue_rows)
    assert all(row.opening_or_source == "-40" for row in revenue_rows)
    assert all(row.closing_or_presentation == "" for row in revenue_rows)
    assert all("فاقد تأیید مستقل" in row.trace for row in revenue_rows)


def test_serialized_pipeline_contains_nonofficial_mapping_coverage_with_source_rows():
    payload = build_pipeline().to_dict()
    trace = payload["mapping_coverage"]
    assert trace["source_sha256"] == payload["source_sha256"]
    assert trace["financial_statement"] is False
    assert trace["releasable"] is False
    assert len(trace["mappings"]) == 11
    assert any(row["mapping_id"] == "SYNTH-M-06" for row in trace["mappings"])


@pytest.mark.parametrize("field,corrupt", [
    ("closing_exposure", "999999"),
    ("source_row", 999999),
    ("account_excel_row", 999999),
    ("mapping_excel_row", 1),
    ("mapping_id", ""),
    ("included", 1),
])
def test_mapping_trace_corruption_is_rejected_before_display(field, corrupt):
    result = build_pipeline()
    trace = result.mapping_coverage
    mapping = replace(trace.mappings[0], **{field: corrupt})
    changed = replace(result, mapping_coverage=replace(
        trace, mappings=(mapping,) + trace.mappings[1:],
    ))
    with pytest.raises(CoverageError, match="DESKTOP_PREVIEW_MAPPING"):
        build_preview_details(changed)


def test_note_exposure_inconsistent_with_included_account_mappings_is_rejected():
    result = build_pipeline()
    coverage = result.mapping_coverage
    altered = replace(coverage.notes[0], closing_exposure="1.000000001")
    changed = replace(result, mapping_coverage=replace(
        coverage, notes=(altered,) + coverage.notes[1:],
    ))
    with pytest.raises(CoverageError, match="DESKTOP_PREVIEW_MAPPING_NOTE"):
        validate_desktop_pipeline_result(changed)


def test_mismatched_account_name_and_closing_against_trial_balance_is_rejected():
    result = build_pipeline()
    coverage = result.mapping_coverage
    corrupted = replace(coverage.accounts[0], closing_exposure="999")
    changed = replace(result, mapping_coverage=replace(
        coverage, accounts=(corrupted,) + coverage.accounts[1:],
    ))
    with pytest.raises(CoverageError, match="DESKTOP_PREVIEW_MAPPING_SOURCE"):
        validate_desktop_pipeline_result(changed)


def test_mismatched_source_file_digest_and_scope_rejected():
    result = build_pipeline()
    coverage = result.mapping_coverage
    for changed_coverage in (
        replace(coverage, source_sha256="f" * 64),
        replace(coverage, company_code="002"),
        replace(coverage, fiscal_year=1403),
        replace(coverage, financial_statement=True),
    ):
        with pytest.raises(CoverageError, match="DESKTOP_PREVIEW_MAPPING_PROVENANCE"):
            validate_desktop_pipeline_result(
                replace(result, mapping_coverage=changed_coverage)
            )


def test_presentation_source_exposure_cannot_disagree_with_account_mapping():
    result = build_pipeline()
    wrong = replace(result.balance_sheet.lines[0], source_closing_exposure="999")
    changed = replace(result, balance_sheet=replace(
        result.balance_sheet,
        lines=(wrong,) + result.balance_sheet.lines[1:],
    ))
    with pytest.raises(CoverageError, match="DESKTOP_PREVIEW_NOTE_SOURCE_MISMATCH"):
        validate_desktop_pipeline_result(changed)


def test_duplicate_mapping_id_fails_closed():
    result = build_pipeline()
    coverage = result.mapping_coverage
    duplicated = replace(
        coverage.mappings[1], mapping_id=coverage.mappings[0].mapping_id,
    )
    changed = replace(result, mapping_coverage=replace(
        coverage, mappings=(
            coverage.mappings[0], duplicated,
            *coverage.mappings[2:],
        ),
    ))
    with pytest.raises(CoverageError, match="DESKTOP_PREVIEW_MAPPING_ROW"):
        validate_desktop_pipeline_result(changed)


def test_account_note_mappings_remain_diagnostic_when_cash_transactions_missing():
    from aram_backend.synthetic_five_statement_demo import cash_transactions

    result = build_pipeline(transactions=cash_transactions()[:-1])
    assert not result.eligible_for_analyst_review
    rows = build_preview_details(result)
    mapping_rows = [row for row in rows if "ردیف نگاشت" in row.trace]
    assert len(mapping_rows) == 11
    assert all("مسدود" in row.state for row in mapping_rows)
