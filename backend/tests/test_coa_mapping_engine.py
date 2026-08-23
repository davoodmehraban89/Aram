import pytest
from backend.app.models import (
    Company,
    FiscalYear,
    FiscalYearStatus,
    StatementType,
    AccountHierarchyLevel,
    NormalizedFinancialRecord,
    SourceDocument,
    COAMappingRule,
)
from backend.app.normalization.mapping_engine import COAMappingEngine
from backend.app.ingestion.ledger_validator import classify_account_hierarchy, validate_excel_ledger_structure


def test_account_hierarchy_classification():
    assert classify_account_hierarchy("11") == AccountHierarchyLevel.GENERAL_LEDGER
    assert classify_account_hierarchy("1101") == AccountHierarchyLevel.SUBSIDIARY_LEDGER
    assert classify_account_hierarchy("110101") == AccountHierarchyLevel.DETAIL_1
    assert classify_account_hierarchy("11010101") == AccountHierarchyLevel.DETAIL_2


def test_unmapped_account_detection(db_session):
    comp = Company(code="COA_1", name="COA Corp 1")
    db_session.add(comp)
    db_session.commit()

    fy = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.DRAFT)
    db_session.add(fy)
    db_session.commit()

    doc = SourceDocument(year_id=fy.id, filename="ledger.csv", file_hash="h_coa1", doc_type="ledger")
    db_session.add(doc)
    db_session.commit()

    rec = NormalizedFinancialRecord(
        year_id=fy.id,
        source_document_id=doc.id,
        row_index=1,
        account_code="110101",
        account_name="Cash Account Detail",
        debit=100.0,
        credit=0.0,
        net_amount=100.0,
    )
    db_session.add(rec)
    db_session.commit()

    engine = COAMappingEngine(db_session, fy.id)
    unmapped = engine.detect_unmapped_accounts()

    assert len(unmapped) == 1
    assert unmapped[0]["account_code"] == "110101"


def test_save_coa_mapping_rule(db_session):
    comp = Company(code="COA_2", name="COA Corp 2")
    db_session.add(comp)
    db_session.commit()

    fy = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.DRAFT)
    db_session.add(fy)
    db_session.commit()

    engine = COAMappingEngine(db_session, fy.id)
    rule = engine.save_mapping_rule(
        account_code="110101",
        account_name="Cash Detail",
        target_statement=StatementType.BS,
        statement_section="Current Assets",
        group_name="Cash and Cash Equivalents",
        is_approved=True,
    )

    assert rule.id is not None
    assert rule.is_approved is True

    # Confirm unmapped account list is now empty
    unmapped = engine.detect_unmapped_accounts()
    assert len(unmapped) == 0


def test_template_reuse_across_fiscal_years(db_session):
    comp = Company(code="COA_3", name="COA Corp 3")
    db_session.add(comp)
    db_session.commit()

    fy1402 = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.DRAFT)
    fy1403 = FiscalYear(company_id=comp.id, year=1403, status=FiscalYearStatus.DRAFT)
    db_session.add_all([fy1402, fy1403])
    db_session.commit()

    engine1402 = COAMappingEngine(db_session, fy1402.id)
    engine1402.save_mapping_rule(
        account_code="1101",
        account_name="Cash",
        target_statement=StatementType.BS,
        statement_section="Current Assets",
        group_name="Cash",
        is_approved=True,
    )

    engine1403 = COAMappingEngine(db_session, fy1403.id)
    copied = engine1403.copy_template_from_year(fy1402.id)

    assert copied == 1
    rules1403 = db_session.query(COAMappingRule).filter_by(year_id=fy1403.id).all()
    assert len(rules1403) == 1
    assert rules1403[0].account_code == "1101"


def test_company_isolation_in_coa_mapping(db_session):
    comp1 = Company(code="COA_C1", name="COA Corp C1")
    comp2 = Company(code="COA_C2", name="COA Corp C2")
    db_session.add_all([comp1, comp2])
    db_session.commit()

    fy1 = FiscalYear(company_id=comp1.id, year=1402, status=FiscalYearStatus.DRAFT)
    fy2 = FiscalYear(company_id=comp2.id, year=1402, status=FiscalYearStatus.DRAFT)
    db_session.add_all([fy1, fy2])
    db_session.commit()

    engine1 = COAMappingEngine(db_session, fy1.id)
    engine1.save_mapping_rule("1101", "Cash", StatementType.BS, "Assets", "Cash", True)

    rules_c2 = db_session.query(COAMappingRule).filter_by(year_id=fy2.id).all()
    assert len(rules_c2) == 0


def test_fiscal_year_isolation_in_coa_mapping(db_session):
    comp = Company(code="COA_ISO", name="COA Iso Corp")
    db_session.add(comp)
    db_session.commit()

    fy1402 = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.DRAFT)
    fy1403 = FiscalYear(company_id=comp.id, year=1403, status=FiscalYearStatus.DRAFT)
    db_session.add_all([fy1402, fy1403])
    db_session.commit()

    engine1402 = COAMappingEngine(db_session, fy1402.id)
    engine1402.save_mapping_rule("1101", "Cash 1402", StatementType.BS, "Assets", "Cash", True)

    rules_1403 = db_session.query(COAMappingRule).filter_by(year_id=fy1403.id).all()
    assert len(rules_1403) == 0


def test_api_unmapped_accounts_endpoint(client, db_session):
    comp = Company(code="API_UNMAP", name="API Unmap Corp")
    db_session.add(comp)
    db_session.commit()

    fy = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.DRAFT)
    db_session.add(fy)
    db_session.commit()

    res = client.get(f"/api/v1/coa/unmapped?year_id={fy.id}")
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_api_save_coa_mapping_rule_endpoint(client, db_session):
    comp = Company(code="API_RULE", name="API Rule Corp")
    db_session.add(comp)
    db_session.commit()

    fy = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.DRAFT)
    db_session.add(fy)
    db_session.commit()

    rule_payload = {
        "account_code": "1101",
        "account_name": "Cash",
        "target_statement": "BS",
        "statement_section": "Current Assets",
        "group_name": "Cash Equivalents",
        "is_approved": True,
    }

    res = client.post(f"/api/v1/coa/rules?year_id={fy.id}", json=rule_payload)
    assert res.status_code == 200
    assert res.json()["account_code"] == "1101"


def test_api_copy_template_endpoint(client, db_session):
    comp = Company(code="API_COPY", name="API Copy Corp")
    db_session.add(comp)
    db_session.commit()

    fy1402 = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.DRAFT)
    fy1403 = FiscalYear(company_id=comp.id, year=1403, status=FiscalYearStatus.DRAFT)
    db_session.add_all([fy1402, fy1403])
    db_session.commit()

    res = client.post(f"/api/v1/coa/copy-template?year_id={fy1403.id}&source_year_id={fy1402.id}")
    assert res.status_code == 200
    assert res.json()["copied_rules_count"] == 0


def test_validate_excel_ledger_structure_valid_csv(tmp_path):
    csv_file = tmp_path / "valid_ledger.csv"
    csv_file.write_text("account_code,account_name,debit,credit\n1101,Cash,100,0")

    result = validate_excel_ledger_structure(str(csv_file))
    assert result["has_valid_headers"] is True
    assert result["format"] == "csv"


def test_validate_excel_ledger_structure_not_found():
    with pytest.raises(FileNotFoundError):
        validate_excel_ledger_structure("non_existent_ledger.csv")


def test_validate_excel_ledger_structure_unsupported_format(tmp_path):
    invalid_file = tmp_path / "invalid.docx"
    invalid_file.write_text("dummy docx")

    with pytest.raises(ValueError):
        validate_excel_ledger_structure(str(invalid_file))


def test_detail_level_hierarchy_classification():
    assert classify_account_hierarchy("1101010101") == AccountHierarchyLevel.DETAIL_3
    assert classify_account_hierarchy("110101010101") == AccountHierarchyLevel.DETAIL_4


def test_unmapped_account_suggestion_generation(db_session):
    comp = Company(code="SUGG_1", name="Suggestion Corp")
    db_session.add(comp)
    db_session.commit()

    fy = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.DRAFT)
    db_session.add(fy)
    db_session.commit()

    doc = SourceDocument(year_id=fy.id, filename="ledger.csv", file_hash="h_sugg", doc_type="ledger")
    db_session.add(doc)
    db_session.commit()

    rec = NormalizedFinancialRecord(
        year_id=fy.id,
        source_document_id=doc.id,
        row_index=1,
        account_code="2101",
        account_name="Property Plant Equipment",
        debit=500.0,
        credit=0.0,
        net_amount=500.0,
    )
    db_session.add(rec)
    db_session.commit()

    engine = COAMappingEngine(db_session, fy.id)
    unmapped = engine.detect_unmapped_accounts()

    assert len(unmapped) == 1
    assert "Property" in unmapped[0]["suggested_statement"]


def test_coa_mapping_rule_update_existing(db_session):
    comp = Company(code="UPDATE_COA", name="Update COA Corp")
    db_session.add(comp)
    db_session.commit()

    fy = FiscalYear(company_id=comp.id, year=1402, status=FiscalYearStatus.DRAFT)
    db_session.add(fy)
    db_session.commit()

    engine = COAMappingEngine(db_session, fy.id)
    engine.save_mapping_rule("1101", "Old Name", StatementType.BS, "Current Assets", "Cash", False)
    updated = engine.save_mapping_rule("1101", "Updated Cash Name", StatementType.BS, "Current Assets", "Cash Equivalents", True)

    assert updated.account_name == "Updated Cash Name"
    assert updated.is_approved is True
