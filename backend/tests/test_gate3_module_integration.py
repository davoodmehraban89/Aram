"""Synthetic cross-module Gate 3 proof, not a financial-amount reconciliation.

The fixture intentionally contains no customer source workbooks or actual balances.
This is a diagnostic-only composite branch: no individual Draft PR is accepted.
"""
from io import BytesIO

import pytest
from openpyxl import Workbook
from sqlalchemy import select

from aram_backend.mapping_excel import (
    MappingEntry, export_mapping_workbook, import_mapping_workbook,
)
from aram_backend.mapping_coverage import inspect_mapping_coverage
from aram_backend.mapping_carry_forward import preview_mapping_carry_forward
from aram_backend.mapping_service import MappingValidationError
from aram_backend.models import (
    AccountVersion, Company, FiscalYear, MappingRule, NoteDefinition,
)
from aram_backend.note_mapping_review import review_note_mappings


def two_years(session):
    company = Company(code="GATE3-INTEGRATED", name="Synthetic")
    source = FiscalYear(company=company, year=1403)
    target = FiscalYear(company=company, year=1404)
    session.add_all([source, target])
    session.flush()
    source_note = NoteDefinition(year_id=source.id, note_number="1", title="Cash", version=1)
    target_note = NoteDefinition(year_id=target.id, note_number="1", title="Cash", version=1)
    session.add_all([
        AccountVersion(year_id=source.id, account_code="001", account_name="Cash", version=1),
        AccountVersion(year_id=target.id, account_code="001", account_name="Cash", version=1),
        source_note, target_note,
    ])
    session.commit()
    return source, target, source_note, target_note


def test_excel_import_to_coverage_note_review_then_explicit_carry_forward(session):
    source, target, source_note, target_note = two_years(session)
    workbook = export_mapping_workbook((
        MappingEntry("cash", "001", source_note.id, "manual", 1),
    ))
    assert import_mapping_workbook(session, year_id=source.id, content=workbook) == 1
    session.commit()

    coverage = inspect_mapping_coverage(session, year_id=source.id)
    assert coverage.mapped_accounts == ("001",)
    assert coverage.invalid_target_rules == ()
    note_review = review_note_mappings(session, year_id=source.id)
    assert note_review.stale_note_rule_keys == ()
    assert note_review.notes[0].account_codes == ("001",)

    preview = preview_mapping_carry_forward(
        session, source_year_id=source.id, target_year_id=target.id,
    )
    assert len(preview.candidates) == 1
    assert preview.candidates[0].target_note_id == target_note.id
    assert inspect_mapping_coverage(session, year_id=target.id).unmapped_accounts == ("001",)

    # Carry-forward is advisory; explicit save is required to establish a rule.
    proposed = preview.candidates[0]
    decision_workbook = export_mapping_workbook((
        MappingEntry(proposed.rule_key, proposed.account_code,
                     proposed.target_note_id, proposed.mapping_type, 1),
    ))
    assert import_mapping_workbook(session, year_id=target.id, content=decision_workbook) == 1
    session.commit()
    assert inspect_mapping_coverage(session, year_id=target.id).mapped_accounts == ("001",)
    assert review_note_mappings(session, year_id=target.id).notes[0].account_codes == ("001",)
    assert session.scalar(select(MappingRule).where(
        MappingRule.year_id == target.id
    )).target_note_id == target_note.id


def test_stale_mapping_is_rejected_by_both_diagnostics_and_carry_forward(session):
    source, target, source_note, _ = two_years(session)
    workbook = export_mapping_workbook((
        MappingEntry("cash", "001", source_note.id, "manual", 1),
    ))
    import_mapping_workbook(session, year_id=source.id, content=workbook)
    session.commit()

    session.add(NoteDefinition(
        year_id=source.id, note_number="1", title="Revised note", version=2
    ))
    session.commit()

    coverage = inspect_mapping_coverage(session, year_id=source.id)
    review = review_note_mappings(session, year_id=source.id)
    carry = preview_mapping_carry_forward(
        session, source_year_id=source.id, target_year_id=target.id
    )
    assert coverage.mapped_accounts == ()
    assert coverage.invalid_target_rules == (("cash", "001", "target_note_stale"),)
    assert review.stale_note_rule_keys == ("cash",)
    assert carry.candidates == ()
    assert carry.skipped == (("cash", "source_note_stale"),)


def test_hidden_input_is_rejected_before_mapping_persistence(session):
    source, _, source_note, _ = two_years(session)
    book = Workbook()
    sheet = book.active
    sheet.title = "Mapping"
    sheet.append(("rule_key", "account_code", "target_note_id", "mapping_type", "version"))
    sheet.append(("cash", "001", source_note.id, "manual", 1))
    sheet.row_dimensions[2].hidden = True
    stream = BytesIO()
    book.save(stream)

    with pytest.raises(MappingValidationError, match="Hidden"):
        import_mapping_workbook(session, year_id=source.id, content=stream.getvalue())
    assert session.scalars(select(MappingRule)).all() == []
