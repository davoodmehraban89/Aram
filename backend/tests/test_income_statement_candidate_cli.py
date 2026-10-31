"""End-to-end synthetic CLI tests for unapproved IS preview and invalid inputs."""
from __future__ import annotations

import json

import pytest

from aram_backend.coverage_preview import CoverageError
from aram_backend.income_statement_candidate_cli import main, parse_income_manifest
from test_income_statement_candidate import workbook, references, policies


def references_doc():
    return {
        "schema_version": 1, "company_code": "001", "fiscal_year": 1404,
        "references": [
            {
                "statement": r.statement, "section": r.section,
                "note_number": r.note_number, "subnote_code": r.subnote_code,
                "expected_closing_exposure": r.expected_closing_exposure,
                "evidence_ref": r.evidence_ref,
            }
            for r in references()
        ],
    }


def policies_doc():
    return {
        "schema_version": 1, "company_code": "001", "fiscal_year": 1404,
        "policies": [
            {
                "statement_section": p.statement_section,
                "note_number": p.note_number, "subnote_code": p.subnote_code,
                "category": p.category, "sign_multiplier": p.sign_multiplier,
                "line_label": p.line_label, "policy_evidence_ref": p.policy_evidence_ref,
            }
            for p in policies()
        ],
    }


def fixtures(tmp_path, *, refs=None, pols=None, data=None):
    data = workbook() if data is None else data
    ref = references_doc() if refs is None else refs
    pol = policies_doc() if pols is None else pols
    excel = tmp_path / "synthetic.xlsx"
    control = tmp_path / "control.json"
    policy = tmp_path / "policy.json"
    excel.write_bytes(data)
    control.write_text(json.dumps(ref), encoding="utf-8")
    policy.write_text(json.dumps(pol), encoding="utf-8")
    return excel, control, policy, data


def argv(paths):
    return [
        "--file", str(paths[0]), "--references", str(paths[1]),
        "--policies", str(paths[2]),
    ]


def test_cli_profit_is_unapproved_and_does_not_mutate_inputs(tmp_path, capsys):
    original = workbook()
    paths = fixtures(tmp_path, data=original)
    assert main(argv(paths)) == 0
    output = capsys.readouterr()
    result = json.loads(output.out)
    assert result["net_result"] == "45"
    assert result["eligible_for_analyst_review"]
    assert not result["official_financial_statement"]
    assert not result["releasable"]
    assert output.err == ""
    assert paths[0].read_bytes() == original
    assert sorted(item.name for item in tmp_path.iterdir()) == [
        "control.json", "policy.json", "synthetic.xlsx",
    ]


def test_cli_loss_is_not_a_failure(tmp_path, capsys):
    data = workbook(costs="290")
    doc = references_doc()
    next(r for r in doc["references"] if r["note_number"] == "C01")[
        "expected_closing_exposure"
    ] = "290"
    paths = fixtures(tmp_path, refs=doc, data=data)
    assert main(argv(paths)) == 0
    assert json.loads(capsys.readouterr().out)["net_result"] == "-135"


def test_cli_missing_policy_blocks_and_reports_findings(tmp_path, capsys):
    doc = policies_doc()
    doc["policies"].pop()
    paths = fixtures(tmp_path, pols=doc)
    assert main(argv(paths)) == 3
    output = json.loads(capsys.readouterr().out)
    assert "MISSING_INCOME_POLICY" in output["findings"]
    assert not output["export_authorized"]


def test_cli_company_mismatch_blocks_without_json_data(tmp_path, capsys):
    doc = policies_doc()
    doc["company_code"] = "002"
    paths = fixtures(tmp_path, pols=doc)
    assert main(argv(paths)) == 2
    output = capsys.readouterr()
    assert not output.out.strip()
    assert "INCOME_SCOPE_MISMATCH" in output.err


@pytest.mark.parametrize("raw", [
    b"null", b"[]", b"{}", b"not-json", b"\xff",
    b'{"schema_version":1,"schema_version":1}',
    json.dumps({**policies_doc(), "unexpected": "value"}).encode("utf-8"),
    json.dumps({**policies_doc(), "schema_version": True}).encode("utf-8"),
    json.dumps({**policies_doc(), "company_code": " 001"}).encode("utf-8"),
    json.dumps({**policies_doc(), "fiscal_year": True}).encode("utf-8"),
    json.dumps({**policies_doc(), "policies": "not-list"}).encode("utf-8"),
    json.dumps({**policies_doc(), "policies": [{"category": "REVENUE"}]}).encode("utf-8"),
])
def test_invalid_json_manifest_blocked(raw):
    with pytest.raises(CoverageError):
        parse_income_manifest(raw)


def test_boolean_sign_cannot_pass_through_json(tmp_path, capsys):
    doc = policies_doc()
    doc["policies"][0]["sign_multiplier"] = True
    paths = fixtures(tmp_path, pols=doc)
    assert main(argv(paths)) == 2
    assert capsys.readouterr().out == ""


def test_symlink_to_policy_file_is_rejected(tmp_path, capsys):
    paths = fixtures(tmp_path)
    link = tmp_path / "alias.json"
    try:
        link.symlink_to(paths[2])
    except (OSError, NotImplementedError):
        pytest.skip("Symlinks unavailable")
    params = argv(paths)
    params[-1] = str(link)
    assert main(params) == 2
    assert capsys.readouterr().out == ""


def test_invalid_excel_rejected_before_processing(tmp_path, capsys):
    paths = fixtures(tmp_path, data=b"broken")
    assert main(argv(paths)) == 2
    assert capsys.readouterr().out == ""


def test_missing_reference_file_is_rejected(tmp_path, capsys):
    paths = fixtures(tmp_path)
    paths[1].unlink()
    assert main(argv(paths)) == 2
    assert capsys.readouterr().out == ""


def test_manifest_size_limit_applies_before_json_parsing():
    from aram_backend.reconciliation_review_cli import MAX_MANIFEST_BYTES
    with pytest.raises(CoverageError) as exc:
        parse_income_manifest(b" " * (MAX_MANIFEST_BYTES + 1))
    assert exc.value.code == "INCOME_MANIFEST_SIZE_INVALID"
