"""Adversarial validation of the strictly typed five-statement JSON manifest.

Synthetic data only. No financial documents or account information in fixtures.
"""
from __future__ import annotations

import json
from copy import deepcopy

import pytest

from aram_backend.coverage_preview import CoverageError
from aram_backend.five_statement_pipeline_cli import parse_pipeline_manifest
from test_five_statement_pipeline_integration import pipeline_manifest


def parse(document):
    return parse_pipeline_manifest(json.dumps(document, ensure_ascii=True).encode("utf-8"))


def test_synthetic_manifest_is_accepted_with_exact_money_strings_and_signs():
    document = pipeline_manifest()
    result = parse(document)
    assert result.company_code == "001"
    assert result.fiscal_year == 1404
    assert result.references[0].expected_closing_exposure == "50"
    assert result.balance_sheet_policies[0].sign_multiplier == 1
    assert result.transactions[0].cash_debit == "30"


@pytest.mark.parametrize("section, index, field, bad", [
    ("references", 0, "expected_closing_exposure", 50),
    ("references", 0, "expected_closing_exposure", True),
    ("references", 0, "expected_closing_exposure", "NaN"),
    ("references", 0, "expected_closing_exposure", "Infinity"),
    ("references", 0, "expected_closing_exposure", "1e200"),
    ("references", 0, "expected_closing_exposure", " 50"),
    ("transactions", 0, "cash_debit", 30),
    ("transactions", 0, "cash_debit", False),
    ("transactions", 0, "cash_debit", "NaN"),
    ("transactions", 0, "cash_debit", "1e500"),
    ("transactions", 0, "cash_credit", 0.0),
    ("transactions", 0, "counterpart_credit", " 30"),
    ("balance_sheet_policies", 0, "sign_multiplier", True),
    ("balance_sheet_policies", 0, "sign_multiplier", 1.0),
    ("income_statement_policies", 0, "sign_multiplier", "1"),
    ("equity_movement_policies", 0, "sign_multiplier", 0),
    ("equity_movement_policies", 0, "sign_multiplier", False),
])
def test_invalid_amounts_or_signs_fail_before_engine_runs(section, index, field, bad):
    document = pipeline_manifest()
    document[section][index][field] = bad
    with pytest.raises(CoverageError) as exc:
        parse(document)
    assert exc.value.code == "PIPELINE_MANIFEST_" + section.upper() + "_ROW_INVALID"


@pytest.mark.parametrize("section, field, bad", [
    ("references", "statement", None),
    ("references", "note_number", ""),
    ("references", "evidence_ref", "REF\nBAD"),
    ("balance_sheet_policies", "line_label", ""),
    ("balance_sheet_policies", "category", 3),
    ("income_statement_policies", "policy_evidence_ref", "   "),
    ("equity_movement_policies", "movement_category", False),
    ("cash_accounts", "account_code", ""),
    ("cash_accounts", "evidence_ref", "REF\tBAD"),
    ("counterpart_policies", "activity", None),
    ("counterpart_policies", "evidence_ref", " SRC "),
    ("transactions", "line_id", 1),
    ("transactions", "posting_date", ""),
    ("transactions", "evidence_ref", "SRC\nBAD"),
    ("cash_balance_notes", "statement_section", None),
    ("cash_balance_notes", "note_number", ""),
    ("cash_balance_notes", "evidence_ref", "  "),
])
def test_invalid_identity_and_evidence_fields_fail_closed(section, field, bad):
    document = pipeline_manifest()
    document[section][0][field] = bad
    with pytest.raises(CoverageError) as exc:
        parse(document)
    assert exc.value.code == "PIPELINE_MANIFEST_" + section.upper() + "_ROW_INVALID"


@pytest.mark.parametrize("field, bad", [
    ("company_code", "002"),
    ("fiscal_year", 1403),
    ("fiscal_year", "1404"),
    ("fiscal_year", True),
])
def test_transaction_scope_mismatch_is_rejected(field, bad):
    document = pipeline_manifest()
    document["transactions"][0][field] = bad
    with pytest.raises(CoverageError) as exc:
        parse(document)
    assert exc.value.code == "PIPELINE_MANIFEST_TRANSACTION_SCOPE_MISMATCH"


def test_zero_and_negative_reference_values_remain_exact_strings():
    document = pipeline_manifest()
    document["references"][0]["expected_closing_exposure"] = "-0.0001"
    document["transactions"][0]["cash_debit"] = "0.0000000001"
    parsed = parse(document)
    assert parsed.references[0].expected_closing_exposure == "-0.0001"
    assert parsed.transactions[0].cash_debit == "0.0000000001"


def test_subnote_code_remains_optionally_blank_without_affecting_validation():
    document = pipeline_manifest()
    assert all(item["subnote_code"] == "" for item in document["references"])
    parsed = parse(document)
    assert len(parsed.references) == len(document["references"])


def test_manifest_fields_are_not_mutated_during_parsing():
    original = pipeline_manifest()
    snapshot = deepcopy(original)
    parsed = parse(original)
    assert original == snapshot
    assert parsed.company_code == snapshot["company_code"]
