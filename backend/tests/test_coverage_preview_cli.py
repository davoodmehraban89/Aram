"""Safety and integration tests for the read-only CLI; synthetic files only."""
from __future__ import annotations

import json
from io import BytesIO

import pytest
from openpyxl import Workbook

from aram_backend.coverage_preview import CoverageError, MAX_INPUT_BYTES
from aram_backend.coverage_preview_cli import main, safe_read_workbook
from aram_backend.pilot_workbook import SHEET_HEADERS


def synthetic_book() -> bytes:
    book = Workbook()
    book.remove(book.active)
    for name, columns in SHEET_HEADERS.items():
        book.create_sheet(name).append(list(columns))

    def add(name, **values):
        book[name].append([values.get(column) for column in SHEET_HEADERS[name]])

    add("Company", company_code="001", company_name="Synthetic",
        fiscal_year=1404, status="Draft")
    add("Accounts", company_code="001", fiscal_year=1404,
        general_code="01", general_name="Assets", account_full_code="01",
        account_name="Cash", opening="100", debit="0", credit="0",
        closing="100", source_row=2, row_status="Draft", closing_delta="0")
    add("Notes", company_code="001", fiscal_year=1404, statement="BS",
        statement_section="Assets", note_number="N1", note_title="Cash")
    add("Mapping", mapping_id="M1", company_code="001", fiscal_year=1404,
        account_full_code="01", account_level="General", general_code="01",
        target_statement="BS", statement_section="Assets",
        note_number="N1", mapping_version=1, approval_status="Approved",
        reviewer="Synthetic reviewer", review_date="2026-10-31",
        validation_status="Valid", source="Manual")
    buffer = BytesIO()
    book.save(buffer)
    book.close()
    return buffer.getvalue()


def test_safe_read_preserves_bytes(tmp_path):
    data = synthetic_book()
    file = tmp_path / "pilot.xlsx"
    file.write_bytes(data)
    assert safe_read_workbook(str(file)) == data
    assert file.read_bytes() == data


def test_cli_outputs_explicitly_unapproved_json(tmp_path, capsys):
    file = tmp_path / "pilot.xlsx"
    file.write_bytes(synthetic_book())
    assert main(["--file", str(file), "--company-code", "001",
                 "--fiscal-year", "1404"]) == 0
    result = json.loads(capsys.readouterr().out)
    assert result["candidate_mapped_accounts"] == 1
    assert result["source_closing_exposure"] == "100"
    assert result["releasable"] is False
    assert result["trusted_approvals"] is False
    assert result["financial_statement"] is False


@pytest.mark.parametrize("name,body", [
    ("pilot.csv", b"content"),
    ("bad.xlsx.exe", b"content"),
    ("empty.xlsx", b""),
])
def test_rejects_disallowed_or_empty_file(tmp_path, name, body):
    file = tmp_path / name
    file.write_bytes(body)
    with pytest.raises(CoverageError):
        safe_read_workbook(str(file))


def test_rejects_missing_path_and_directory(tmp_path):
    with pytest.raises(CoverageError):
        safe_read_workbook(str(tmp_path / "absent.xlsx"))
    folder = tmp_path / "folder.xlsx"
    folder.mkdir()
    with pytest.raises(CoverageError):
        safe_read_workbook(str(folder))


def test_rejects_file_beyond_limit_without_full_read(tmp_path):
    file = tmp_path / "huge.xlsx"
    with file.open("wb") as stream:
        stream.truncate(MAX_INPUT_BYTES + 1)
    with pytest.raises(CoverageError) as exc:
        safe_read_workbook(str(file))
    assert exc.value.code == "WORKBOOK_SIZE_INVALID"


def test_symlink_never_followed(tmp_path):
    target = tmp_path / "good.xlsx"
    target.write_bytes(synthetic_book())
    link = tmp_path / "alias.xlsx"
    try:
        link.symlink_to(target)
    except (NotImplementedError, OSError):
        pytest.skip("Symlink creation unavailable")
    with pytest.raises(CoverageError) as exc:
        safe_read_workbook(str(link))
    assert exc.value.code == "NOT_REGULAR_FILE"


def test_cli_invalid_workbook_has_no_stdout_success(tmp_path, capsys):
    file = tmp_path / "invalid.xlsx"
    file.write_bytes(b"not a workbook")
    assert main(["--file", str(file), "--company-code", "001",
                 "--fiscal-year", "1404"]) == 2
    result = capsys.readouterr()
    assert not result.out.strip()
    assert "blocked" in result.err


def test_wrong_company_never_falls_back(tmp_path, capsys):
    file = tmp_path / "pilot.xlsx"
    file.write_bytes(synthetic_book())
    assert main(["--file", str(file), "--company-code", "002",
                 "--fiscal-year", "1404"]) == 2
    captured = capsys.readouterr()
    assert not captured.out.strip()
    assert "COMPANY_SCOPE_NOT_FOUND" in captured.err
