import pytest
from backend.app.models import Company, FiscalYear, FiscalYearStatus, SourceDocument, NormalizedFinancialRecord


def test_csv_export_endpoint(client, db_session):
    comp = Company(code="EXP1", name="Export Corp 1")
    db_session.add(comp)
    db_session.commit()

    fy = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.DRAFT)
    db_session.add(fy)
    db_session.commit()

    doc = SourceDocument(year_id=fy.id, filename="ledger.csv", file_hash="hex1", doc_type="ledger")
    db_session.add(doc)
    db_session.commit()

    rec = NormalizedFinancialRecord(
        year_id=fy.id,
        source_document_id=doc.id,
        row_index=1,
        account_code="1101",
        account_name="Cash",
        debit=1000.0,
        credit=0.0,
        net_amount=1000.0,
    )
    db_session.add(rec)
    db_session.commit()

    res = client.get(f"/api/v1/export/csv?year_id={fy.id}&statement_type=TB")
    assert res.status_code == 200
    assert "text/csv" in res.headers["content-type"]
    assert "1101" in res.text
    assert "Cash" in res.text


def test_pdf_structure_export_endpoint(client, db_session):
    comp = Company(code="EXP2", name="Export Corp 2")
    db_session.add(comp)
    db_session.commit()

    fy = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.DRAFT)
    db_session.add(fy)
    db_session.commit()

    res = client.get(f"/api/v1/export/pdf-structure?year_id={fy.id}&statement_type=TB")
    assert res.status_code == 200
    data = res.json()
    assert "title" in data
    assert "formatted_totals" in data
    assert "raw_data" in data
