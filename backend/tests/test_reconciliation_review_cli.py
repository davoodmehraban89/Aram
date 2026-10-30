"""CLI tests use only ephemeral synthetic workbooks and control references."""
from __future__ import annotations

import json

import pytest

from aram_backend.coverage_preview import CoverageError
from aram_backend.reconciliation_review_cli import (
    MAX_MANIFEST_BYTES, main, parse_manifest, safe_read_manifest,
)
from test_reconciliation_review import workbook


def manifest(*, expected="126.00", company="001", year=1404):
    return {
        "schema_version": 1, "company_code": company, "fiscal_year": year,
        "references": [{
            "statement": "BS", "section": "Assets",
            "note_number": "N01", "subnote_code": "",
            "expected_closing_exposure": expected,
            "evidence_ref": "SYNTHETIC-REFERENCE-1",
        }],
    }


def run(tmp_path, capsys, *, expected="126.00", company="001", data=None):
    xlsx = tmp_path / "synthetic.xlsx"
    controls = tmp_path / "synthetic.json"
    xlsx.write_bytes(workbook() if data is None else data)
    controls.write_text(json.dumps(manifest(expected=expected, company=company)),
                        encoding="utf-8")
    code = main(["--file", str(xlsx), "--references", str(controls)])
    captured = capsys.readouterr()
    return code, captured, xlsx, controls


def test_cli_matched_is_still_unapproved(tmp_path, capsys):
    source_bytes = workbook()
    code, captured, xlsx, controls = run(tmp_path, capsys, data=source_bytes)
    assert code == 0
    result = json.loads(captured.out)
    assert result["matched_for_analyst_review"]
    assert not result["approved"]
    assert not result["releasable"]
    assert len(result["reference_sha256"]) == 64
    assert captured.err == ""
    assert xlsx.read_bytes() == source_bytes
    assert json.loads(controls.read_text()) == manifest()


def test_cli_mismatch_returns_three_and_json_findings(tmp_path, capsys):
    code, captured, _, _ = run(tmp_path, capsys, expected="127.00")
    assert code == 3
    result = json.loads(captured.out)
    assert not result["matched_for_analyst_review"]
    assert any(f["code"] == "NOTE_EXPOSURE_MISMATCH" for f in result["findings"])


def test_cli_wrong_scope_returns_two_without_leaking_workbook(tmp_path, capsys):
    code, captured, _, _ = run(tmp_path, capsys, company="999")
    assert code == 2
    assert captured.out == ""
    assert "COMPANY_SCOPE_NOT_FOUND" in captured.err


def test_duplicate_json_keys_rejected():
    content = b'{"schema_version":1,"schema_version":1}'
    with pytest.raises(CoverageError) as error:
        parse_manifest(content)
    assert error.value.code == "DUPLICATE_MANIFEST_KEY"


@pytest.mark.parametrize("content", [
    b"[]", b"null", b"{}", b"{not json", b"\xff",
    json.dumps({**manifest(), "extra": 1}).encode("utf-8"),
    json.dumps({**manifest(), "schema_version": True}).encode("utf-8"),
    json.dumps({**manifest(), "fiscal_year": True}).encode("utf-8"),
    json.dumps({**manifest(), "references": "not list"}).encode("utf-8"),
    json.dumps({**manifest(), "references": [{"note_number": "N01"}]}).encode("utf-8"),
])
def test_invalid_manifest_blocks(content):
    with pytest.raises(CoverageError):
        parse_manifest(content)


def test_large_manifest_bytes_rejected():
    with pytest.raises(CoverageError) as error:
        parse_manifest(b" " * (MAX_MANIFEST_BYTES + 1))
    assert error.value.code == "MANIFEST_SIZE_INVALID"


def test_cli_invalid_reference_type_blocks_safely(tmp_path, capsys):
    xlsx = tmp_path / "synthetic.xlsx"
    controls = tmp_path / "synthetic.json"
    xlsx.write_bytes(workbook())
    payload = manifest()
    payload["references"][0]["expected_closing_exposure"] = 126.0
    controls.write_text(json.dumps(payload), encoding="utf-8")
    assert main(["--file", str(xlsx), "--references", str(controls)]) == 2
    assert capsys.readouterr().out == ""


def test_manifest_symlink_rejected(tmp_path):
    target = tmp_path / "reference.json"
    target.write_text(json.dumps(manifest()), encoding="utf-8")
    alias = tmp_path / "alias.json"
    try:
        alias.symlink_to(target)
    except (OSError, NotImplementedError):
        pytest.skip("No symlinks on this filesystem")
    with pytest.raises(CoverageError) as error:
        safe_read_manifest(str(alias))
    assert error.value.code == "MANIFEST_NOT_REGULAR_FILE"


def test_manifest_directory_and_missing_path_are_rejected(tmp_path):
    folder = tmp_path / "folder.json"
    folder.mkdir()
    with pytest.raises(CoverageError):
        safe_read_manifest(str(folder))
    with pytest.raises(CoverageError):
        safe_read_manifest(str(tmp_path / "missing.json"))


def test_manifest_size_checked_before_read(tmp_path):
    source = tmp_path / "large.json"
    with source.open("wb") as stream:
        stream.truncate(MAX_MANIFEST_BYTES + 1)
    with pytest.raises(CoverageError) as error:
        safe_read_manifest(str(source))
    assert error.value.code == "MANIFEST_SIZE_INVALID"


def test_no_snapshot_written_or_input_edited_on_mismatch(tmp_path, capsys):
    source_bytes = workbook()
    code, _, xlsx, controls = run(tmp_path, capsys, expected="-100.00", data=source_bytes)
    assert code == 3
    assert sorted(path.name for path in tmp_path.iterdir()) == [
        "synthetic.json", "synthetic.xlsx",
    ]
    assert xlsx.read_bytes() == source_bytes
    assert json.loads(controls.read_text()) == manifest(expected="-100.00")
