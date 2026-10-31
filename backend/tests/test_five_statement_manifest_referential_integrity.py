"""Synthetic adversarial tests for five-statement manifest referential integrity."""
from __future__ import annotations

from copy import deepcopy
import json

import pytest

from aram_backend.coverage_preview import CoverageError
from aram_backend.five_statement_pipeline_cli import parse_pipeline_manifest
from test_five_statement_pipeline_integration import pipeline_manifest


def parse(data):
    return parse_pipeline_manifest(json.dumps(data, ensure_ascii=True).encode("utf-8"))


def reject(modify, code):
    data = pipeline_manifest()
    modify(data)
    with pytest.raises(CoverageError) as exc:
        parse(data)
    assert exc.value.code == code


def test_complete_synthetic_graph_is_accepted_unchanged():
    source = pipeline_manifest()
    original = deepcopy(source)
    output = parse(source)
    assert len(output.references) == 8
    assert len(output.balance_sheet_policies) == 4
    assert len(output.cash_balance_notes) == 1
    assert source == original


def test_duplicate_reference_to_same_statement_note_rejected():
    reject(
        lambda d: d["references"].append(deepcopy(d["references"][0])),
        "PIPELINE_MANIFEST_DUPLICATE_NOTE_REFERENCE",
    )


def test_unknown_reference_statement_rejected():
    reject(
        lambda d: d["references"][0].update(statement="UNKNOWN"),
        "PIPELINE_MANIFEST_REFERENCE_STATEMENT_INVALID",
    )


@pytest.mark.parametrize("section,code", [
    ("balance_sheet_policies", "PIPELINE_MANIFEST_DUPLICATE_BS_POLICY"),
    ("income_statement_policies", "PIPELINE_MANIFEST_DUPLICATE_IS_POLICY"),
    ("equity_movement_policies", "PIPELINE_MANIFEST_DUPLICATE_EQ_POLICY"),
])
def test_duplicate_statement_policy_rejected(section, code):
    reject(lambda d: d[section].append(deepcopy(d[section][0])), code)


@pytest.mark.parametrize("section,code", [
    ("balance_sheet_policies", "PIPELINE_MANIFEST_ORPHAN_BS_POLICY"),
    ("income_statement_policies", "PIPELINE_MANIFEST_ORPHAN_IS_POLICY"),
    ("equity_movement_policies", "PIPELINE_MANIFEST_ORPHAN_EQ_POLICY"),
])
def test_policy_target_without_matching_reference_rejected(section, code):
    reject(
        lambda d: d[section][0].update(note_number="NONEXISTENT"),
        code,
    )


def test_missing_policy_remains_a_blocked_candidate_not_parse_error():
    data = pipeline_manifest()
    data["balance_sheet_policies"].pop()
    assert len(parse(data).balance_sheet_policies) == 3


def test_duplicate_cash_note_selection_rejected():
    reject(
        lambda d: d["cash_balance_notes"].append(
            deepcopy(d["cash_balance_notes"][0])
        ),
        "PIPELINE_MANIFEST_DUPLICATE_CASH_NOTE_SELECTION",
    )


def test_cash_note_selection_without_reference_rejected():
    reject(
        lambda d: d["cash_balance_notes"][0].update(note_number="MISSING"),
        "PIPELINE_MANIFEST_CASH_NOTE_REFERENCE_MISSING",
    )


def test_cash_note_cannot_select_a_liability_or_equity_policy():
    reject(
        lambda d: d["cash_balance_notes"][0].update(
            statement_section="Current liabilities", note_number="L01",
        ),
        "PIPELINE_MANIFEST_CASH_NOTE_NOT_ASSET",
    )


def test_cash_note_cannot_select_an_unmapped_asset_policy():
    reject(
        lambda d: d["balance_sheet_policies"].pop(0),
        "PIPELINE_MANIFEST_CASH_NOTE_NOT_ASSET",
    )


def test_duplicate_cash_account_registry_entry_rejected():
    reject(
        lambda d: d["cash_accounts"].append(deepcopy(d["cash_accounts"][0])),
        "PIPELINE_MANIFEST_DUPLICATE_CASH_ACCOUNT",
    )


def test_duplicate_counterpart_policy_rejected():
    reject(
        lambda d: d["counterpart_policies"].append(
            deepcopy(d["counterpart_policies"][0])
        ),
        "PIPELINE_MANIFEST_DUPLICATE_COUNTERPART_POLICY",
    )


def test_cash_account_cannot_have_non_cash_counterpart_policy():
    reject(
        lambda d: d["counterpart_policies"][0].update(account_code="CASH"),
        "PIPELINE_MANIFEST_CASH_COUNTERPART_OVERLAP",
    )


def test_duplicate_transaction_line_id_rejected():
    reject(
        lambda d: d["transactions"].append(deepcopy(d["transactions"][0])),
        "PIPELINE_MANIFEST_DUPLICATE_TRANSACTION_LINE",
    )


def test_unknown_cash_account_in_transaction_rejected():
    reject(
        lambda d: d["transactions"][0].update(cash_account_code="UNKNOWN"),
        "PIPELINE_MANIFEST_UNKNOWN_CASH_ACCOUNT",
    )


def test_unknown_counterpart_account_in_transaction_rejected():
    reject(
        lambda d: d["transactions"][0].update(counterpart_account_code="UNKNOWN"),
        "PIPELINE_MANIFEST_UNKNOWN_COUNTERPART_ACCOUNT",
    )


def test_same_cash_and_counterpart_account_rejected():
    reject(
        lambda d: d["transactions"][0].update(counterpart_account_code="CASH"),
        "PIPELINE_MANIFEST_SAME_ACCOUNT_PAIR",
    )


@pytest.mark.parametrize("section", [
    "references",
    "balance_sheet_policies",
    "income_statement_policies",
    "equity_movement_policies",
    "cash_balance_notes",
])
@pytest.mark.parametrize("bad", [None, 0, False, 1.5, "  ", "A\nB", " A"])
def test_invalid_optional_subnote_type_or_control_char_rejected(section, bad):
    reject(
        lambda d: d[section][0].update(subnote_code=bad),
        "PIPELINE_MANIFEST_" + section.upper() + "_ROW_INVALID",
    )


def test_valid_blank_subnotes_remain_valid():
    parsed = parse(pipeline_manifest())
    assert all(x.subnote_code == "" for x in parsed.references)


def test_references_for_cash_flow_may_exist_without_presentation_policy():
    data = pipeline_manifest()
    data["references"].append({
        "statement": "CF", "section": "Cash flow", "note_number": "C00",
        "subnote_code": "", "expected_closing_exposure": "0",
        "evidence_ref": "SYNTH-CF-REF",
    })
    parsed = parse(data)
    assert len(parsed.references) == 9
