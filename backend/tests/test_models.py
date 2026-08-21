from backend.app.models import (
    Company,
    FiscalYear,
    FiscalYearStatus,
    SourceDocument,
    AccountVersion,
    MappingRule,
    NoteDefinition,
    NoteRow,
    FinancialStatement,
    StatementType,
    StatementLine,
)


def test_create_core_entities_and_relationships(db_session):
    # 1. Create Company
    company = Company(code="COMP01", name="Test Company PLC")
    db_session.add(company)
    db_session.commit()
    db_session.refresh(company)

    assert company.id is not None
    assert company.code == "COMP01"
    assert company.created_at is not None

    # 2. Create Fiscal Year
    fy1402 = FiscalYear(company_id=company.id, year=1402, status=FiscalYearStatus.DRAFT)
    db_session.add(fy1402)
    db_session.commit()
    db_session.refresh(fy1402)

    assert fy1402.id is not None
    assert fy1402.company.name == "Test Company PLC"

    # 3. Create Source Document
    doc = SourceDocument(
        year_id=fy1402.id,
        filename="ledger_1402.xlsx",
        file_hash="abc123hash",
        doc_type="ledger",
    )
    db_session.add(doc)

    # 4. Create Account Version
    acc = AccountVersion(
        year_id=fy1402.id,
        account_code="110101",
        account_name="Cash in Hand",
        nature="Debit",
    )
    db_session.add(acc)

    # 5. Create Note Definition and Row
    note = NoteDefinition(
        year_id=fy1402.id,
        note_number=5,
        title="Cash and Cash Equivalents",
        configuration_json={"section": "Current Assets"},
    )
    db_session.add(note)
    db_session.commit()
    db_session.refresh(note)

    row = NoteRow(
        note_id=note.id,
        row_order=1,
        label="Petty Cash",
        formula_logic="SUM(110101)",
    )
    db_session.add(row)

    # 6. Create Mapping Rule
    rule = MappingRule(
        year_id=fy1402.id,
        account_code="110101",
        account_version_id=acc.id,
        target_note_id=note.id,
        mapping_type="DETERMINISTIC",
    )
    db_session.add(rule)

    # 7. Create Financial Statement and Line
    stmt = FinancialStatement(year_id=fy1402.id, statement_type=StatementType.BS)
    db_session.add(stmt)
    db_session.commit()
    db_session.refresh(stmt)

    line = StatementLine(
        statement_id=stmt.id,
        line_label="Cash and Cash Equivalents",
        target_note_id=note.id,
        mapped_total=1500000.00,
    )
    db_session.add(line)
    db_session.commit()

    # Verify relationships via cascade/backref
    db_session.refresh(fy1402)
    assert len(fy1402.source_documents) == 1
    assert len(fy1402.account_versions) == 1
    assert len(fy1402.note_definitions) == 1
    assert len(fy1402.financial_statements) == 1
    assert len(note.rows) == 1
    assert len(stmt.lines) == 1
    assert stmt.lines[0].target_note.title == "Cash and Cash Equivalents"
