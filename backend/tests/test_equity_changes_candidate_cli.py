"""Synthetic-only CLI tests for equity changes preview and safe input handling."""
from __future__ import annotations

import json

import pytest

from aram_backend.coverage_preview import CoverageError
from aram_backend.equity_changes_candidate_cli import main, parse_equity_manifest
from test_equity_changes_candidate import workbook, references, policies


def reference_document():
    return {
        "schema_version": 1, "company_code": "001", "fiscal_year": 1404,
        "references": [
            {
                "statement": item.statement, "section": item.section,
                "note_number": item.note_number, "subnote_code": item.subnote_code,
                "expected_closing_exposure": item.expected_closing_exposure,
                "evidence_ref": item.evidence_ref,
            }
            for item in references()
        ],
    }


def policy_document():
    return {
        "schema_version": 1, "company_code": "001", "fiscal_year": 1404,
        "policies": [
            {
                "statement_section": item.statement_section,
                "note_number": item.note_number, "subnote_code": item.subnote_code,
                "equity_component": item.equity_component,
                "movement_category": item.movement_category,
                "sign_multiplier": item.sign_multiplier,
                "line_label": item.line_label,
                "policy_evidence_ref": item.policy_evidence_ref,
            }
            for item in policies()
        ],
    }


def files(tmp_path, *, ref=None, policy=None, data=None):
    data = workbook() if data is None else data
    ref = reference_document() if ref is None else ref
    policy = policy_document() if policy is None else policy
    xlsx = tmp_path / "synthetic.xlsx"
    references_path = tmp_path / "references.json"
    policies_path = tmp_path / "equity-policies.json"
    xlsx.write_bytes(data)
    references_path.write_text(json.dumps(ref), encoding="utf-8")
    policies_path.write_text(json.dumps(policy), encoding="utf-8")
    return xlsx, references_path, policies_path, data


def command(paths):
    return [
        "--file", str(paths[0]), "--references", str(paths[1]),
        "--policies", str(paths[2]),
    ]


def test_cli_prints_equity_rollforward_and_preserves_source(tmp_path, capsys):
    paths = files(tmp_path)
    original = paths[3]
    assert main(command(paths)) == 0
    captured = capsys.readouterr()
    result = json.loads(captured.out)
    assert result["opening_equity_total"] == "150"
    assert result["total_movement"] == "5"
    assert result["closing_equity_total"] == "155"
    assert result["eligible_for_analyst_review"]
    assert not result["official_financial_statement"]
    assert not result["releasable"]
    assert captured.err == ""
    assert paths[0].read_bytes() == original
    assert sorted(p.name for p in tmp_path.iterdir()) == [
        "equity-policies.json", "references.json", "synthetic.xlsx"
    ]


def test_cli_missing_policy_returns_three_and_findings(tmp_path, capsys):
    policy = policy_document()
    policy["policies"].pop()
    paths = files(tmp_path, policy=policy)
    assert main(command(paths)) == 3
    result = json.loads(capsys.readouterr().out)
    assert "MISSING_EQUITY_POLICY" in result["findings"]
    assert not result["export_authorized"]


def test_cli_wrong_company_scope_blocks_without_stdout(tmp_path, capsys):
    policy = policy_document()
    policy["company_code"] = "002"
    paths = files(tmp_path, policy=policy)
    assert main(command(paths)) == 2
    output = capsys.readouterr()
    assert output.out == ""
    assert "EQUITY_SCOPE_MISMATCH" in output.err


@pytest.mark.parametrize("raw", [
    b"null", b"[]", b"{}", b"not json", b"\xff",
    b'{"schema_version":1,"schema_version":1}',
    json.dumps({**policy_document(), "extra": 1}).encode("utf-8"),
    json.dumps({**policy_document(), "schema_version": True}).encode("utf-8"),
    json.dumps({**policy_document(), "company_code": " 001"}).encode("utf-8"),
    json.dumps({**policy_document(), "fiscal_year": True}).encode("utf-8"),
    json.dumps({**policy_document(), "policies": "bad"}).encode("utf-8"),
    json.dumps({**policy_document(), "policies": [{}]}).encode("utf-8"),
])
def test_invalid_policy_manifest_fails_closed(raw):
    with pytest.raises(CoverageError):
        parse_equity_manifest(raw)


def test_json_boolean_sign_is_not_accepted(tmp_path, capsys):
    policy = policy_document()
    policy["policies"][0]["sign_multiplier"] = True
    paths = files(tmp_path, policy=policy)
    assert main(command(paths)) == 2
    assert capsys.readouterr().out == ""


def test_symlinked_policy_file_is_rejected(tmp_path, capsys):
    paths = files(tmp_path)
    alias = tmp_path / "alias.json"
    try:
        alias.symlink_to(paths[2])
    except (OSError, NotImplementedError):
        pytest.skip("Symlinks unavailable")
    args = command(paths)
    args[-1] = str(alias)
    assert main(args) == 2
    assert capsys.readouterr().out == ""


def test_missing_workbook_is_rejected(tmp_path, capsys):
    paths = files(tmp_path)
    paths[0].unlink()
    assert main(command(paths)) == 2
    assert capsys.readouterr().out == ""


def test_bad_xlsx_is_rejected(tmp_path, capsys):
    paths = files(tmp_path, data=b"not xlsx")
    assert main(command(paths)) == 2
    assert capsys.readouterr().out == ""


def test_manifest_size_limit_is_enforced():
    from aram_backend.reconciliation_review_cli import MAX_MANIFEST_BYTES
    with pytest.raises(CoverageError) as error:
        parse_equity_manifest(b" " * (MAX_MANIFEST_BYTES + 1))
    assert error.value.code == "EQUITY_MANIFEST_SIZE_INVALID"
