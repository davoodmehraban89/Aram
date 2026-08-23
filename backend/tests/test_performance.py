import time
import pytest
from backend.app.models import Company, FiscalYear, FiscalYearStatus, SourceDocument, NormalizedFinancialRecord
from backend.app.normalization.service import normalize_and_persist_records
from backend.app.accounting.service import generate_financial_statements


def test_performance_realistic_data_volume(db_session):
    comp = Company(code="PERF_01", name="Performance Test Corp")
    db_session.add(comp)
    db_session.commit()

    fy = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.DRAFT)
    db_session.add(fy)
    db_session.commit()

    doc = SourceDocument(year_id=fy.id, filename="large_ledger.csv", file_hash="perf_hash", doc_type="ledger")
    db_session.add(doc)
    db_session.commit()

    # Generate 1,000 realistic transaction rows
    raw_rows = []
    for i in range(1, 1001):
        code = f"{1100 + (i % 50)}"
        raw_rows.append({
            "account_code": code,
            "account_name": f"Account {code}",
            "debit": str(i * 100.0),
            "credit": "0.00",
        })

    # Test normalization throughput
    start_norm = time.time()
    records, logs = normalize_and_persist_records(db_session, fy.id, doc.id, raw_rows)
    norm_duration = time.time() - start_norm

    assert len(records) == 1000
    assert norm_duration < 3.0  # Must process 1000 records under 3 seconds

    # Test accounting calculation throughput on 1,000 records
    start_calc = time.time()
    calc_results = generate_financial_statements(db_session, fy.id)
    calc_duration = time.time() - start_calc

    assert calc_results["record_count"] == 1000
    assert calc_duration < 1.0  # Calculation on 1000 records under 1 second
