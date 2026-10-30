"""Synthetic end-to-end tests of the non-official BS CLI."""
from __future__ import annotations

import json

import pytest

from aram_backend.balance_sheet_candidate_cli import (
    main, parse_presentation_manifest,
)
from aram_backend.coverage_preview import CoverageError
from test_balance_sheet_candidate import workbook, policies, references


def reference_document():
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


def policy_document():
    return {
        "schema_version": 1, "company_code": "001", "fiscal_year": 1404,
        "policies": [
            {
                "statement_section": p.statement_section,
                "note_number": p.note_number,
                "subnote_code": p.subnote_code, "category": p.category,
                "sign_multiplier": p.sign_multiplier, "line_label": p.line_label,
                "policy_evidence_ref": p.policy_evidence_ref,
            }
            for p in policies()
        ],
    }


def files(tmp_path, *, reference=None, presentation=None, source=None):
    source_bytes = workbook() if source is None else source
    ref_doc = reference_document() if reference is None else reference
    policy_doc = policy_document() if presentation is None else presentation
    file = tmp_path / "sample.xlsx"
    reference_file = tmp_path / "controls.json"
    policy_file = tmp_path / "presentation.json"
    file.write_bytes(source_bytes)
    reference_file.write_text(json.dumps(ref_doc), encoding="utf-8")
    policy_file.write_text(json.dumps(policy_doc), encoding="utf-8")
    return file, reference_file, policy_file, source_bytes


def command(files):
    file, refs, pol, _ = files
    return [
        "--file", str(file), "--references", str(refs),
        "--policies", str(pol),
    ]


def test_cli_presents_three_sections_but_no_official_document(tmp_path, capsys):
    input_files = files(tmp_path)
    initial = input_files[3]
    assert main(command(input_files)) == 0
    output = capsys.readouterr()
    data = json.loads(output.out)
    assert data["assets_total"] == "100"
    assert data["liabilities_total"] == "60"
    assert data["equity_total"] == "40"
    assert data["eligible_for_analyst_review"]
    assert not data["releasable"]
    assert not data["official_financial_statement"]
    assert output.err == ""
    assert input_files[0].read_bytes() == initial
    assert sorted(p.name for p in tmp_path.iterdir()) == [
        "controls.json", "presentation.json", "sample.xlsx"
    ]


def test_cli_unbalanced_returns_code_three_with_findings(tmp_path, capsys):
    xlsx = workbook(liability="-59")
    controls = reference_document()
    controls["references"][1]["expected_closing_exposure"] = "-59"
    inputs = files(tmp_path, source=xlsx, reference=controls)
    assert main(command(inputs)) == 3
    result = json.loads(capsys.readouterr().out)
    assert result["balance_difference"] == "1"
    assert "BALANCE_SHEET_DOES_NOT_BALANCE" in result["findings"]
    assert not result["export_authorized"]


def test_cli_policy_scope_mismatch_fails_without_stdout(tmp_path, capsys):
    doc = policy_document()
    doc["fiscal_year"] = 1403
    inputs = files(tmp_path, presentation=doc)
    assert main(command(inputs)) == 2
    output = capsys.readouterr()
    assert not output.out.strip()
    assert "PRESENTATION_SCOPE_MISMATCH" in output.err


@pytest.mark.parametrize("content", [
    b"[]", b"{}", b"not json", b"null", b"\xff",
    b'{"schema_version":1,"schema_version":1}',
    json.dumps({**policy_document(), "extra": "oops"}).encode("utf-8"),
    json.dumps({**policy_document(), "schema_version": True}).encode("utf-8"),
    json.dumps({**policy_document(), "company_code": " 001"}).encode("utf-8"),
    json.dumps({**policy_document(), "fiscal_year": True}).encode("utf-8"),
    json.dumps({**policy_document(), "policies": "bad"}).encode("utf-8"),
    json.dumps({**policy_document(), "policies": [{}]}).encode("utf-8"),
])
def test_bad_policy_manifest_is_rejected(content):
    with pytest.raises(CoverageError):
        parse_presentation_manifest(content)


def test_presentation_sign_boolean_rejected_by_engine(tmp_path, capsys):
    doc = policy_document()
    doc["policies"][0]["sign_multiplier"] = True
    inputs = files(tmp_path, presentation=doc)
    assert main(command(inputs)) == 2
    output = capsys.readouterr()
    assert not output.out.strip()
    assert "INVALID_PRESENTATION_SIGN" in output.err


def test_extra_policy_and_missing_policy_block_not_silently_ignored(tmp_path, capsys):
    doc = policy_document()
    doc["policies"].pop()
    inputs = files(tmp_path, presentation=doc)
    assert main(command(inputs)) == 3
    result = json.loads(capsys.readouterr().out)
    assert "MISSING_EXPLICIT_PRESENTATION_POLICY" in result["findings"]


def test_missing_xlsx_blocks_safely(tmp_path, capsys):
    inputs = files(tmp_path)
    inputs[0].unlink()
    assert main(command(inputs)) == 2
    assert capsys.readouterr().out == ""


def test_policy_symlink_is_rejected(tmp_path, capsys):
    inputs = files(tmp_path)
    link = tmp_path / "policy_link.json"
    try:
        link.symlink_to(inputs[2])
    except (OSError, NotImplementedError):
        pytest.skip("Symlink creation unsupported")
    args = command(inputs)
    args[-1] = str(link)
    assert main(args) == 2
    assert capsys.readouterr().out == ""


def test_reference_file_scope_mismatch_no_fallback(tmp_path, capsys):
    controls = reference_document()
    controls["company_code"] = "999"
    inputs = files(tmp_path, reference=controls)
    assert main(command(inputs)) == 2
    assert capsys.readouterr().out == ""
