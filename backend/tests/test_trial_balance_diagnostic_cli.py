"""Synthetic CLI regression tests; no customer data or database writes."""
from __future__ import annotations

import json

import pytest

from aram_backend.trial_balance_diagnostic_cli import main
from test_trial_balance_diagnostic import edit, workbook


def command(tmp_path, *, content=None, company="001", year="1404"):
    file = tmp_path / "synthetic.xlsx"
    data = workbook() if content is None else content
    file.write_bytes(data)
    argv = [
        "--file", str(file),
        "--company-code", company,
        "--fiscal-year", year,
    ]
    return argv, file, data


def test_cli_balance_zero_exit_and_never_modifies_source(tmp_path, capsys):
    args, file, original = command(tmp_path)
    assert main(args) == 0
    output = capsys.readouterr()
    result = json.loads(output.out)
    assert result["balanced_for_analyst_review"]
    assert result["debit_turnover_total"] == "50"
    assert result["credit_turnover_total"] == "50"
    assert not result["releasable"]
    assert not result["source_ledger_completeness_verified"]
    assert file.read_bytes() == original
    assert output.err == ""


def test_cli_unbalanced_returns_three_with_structured_findings(tmp_path, capsys):
    def change(book):
        book["Accounts"]["R2"] = "41"
        book["Accounts"]["T2"] = "121"
    args, _, _ = command(tmp_path, content=edit(workbook(), change))
    assert main(args) == 3
    result = json.loads(capsys.readouterr().out)
    assert "DEBIT_CREDIT_TURNOVER_UNBALANCED" in result["findings"]
    assert result["balanced_for_analyst_review"] is False


def test_cli_wrong_company_scope_no_fallback_or_stdout(tmp_path, capsys):
    args, _, _ = command(tmp_path, company="002")
    assert main(args) == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "TRIAL_BALANCE_COMPANY_NOT_FOUND" in captured.err


def test_cli_rejects_invalid_year(tmp_path, capsys):
    args, _, _ = command(tmp_path, year="0")
    assert main(args) == 2
    assert not capsys.readouterr().out.strip()


def test_cli_rejects_nonworkbook_bytes(tmp_path, capsys):
    args, _, _ = command(tmp_path, content=b"not xlsx")
    assert main(args) == 2
    assert not capsys.readouterr().out.strip()


def test_cli_rejects_missing_input(tmp_path, capsys):
    args, file, _ = command(tmp_path)
    file.unlink()
    assert main(args) == 2
    assert capsys.readouterr().out == ""


def test_cli_rejects_symlink_without_touching_target(tmp_path, capsys):
    args, file, original = command(tmp_path)
    alias = tmp_path / "alias.xlsx"
    try:
        alias.symlink_to(file)
    except (OSError, NotImplementedError):
        pytest.skip("No local symlink support")
    args[1] = str(alias)
    assert main(args) == 2
    assert capsys.readouterr().out == ""
    assert file.read_bytes() == original


def test_cli_rejects_oversized_file_before_loading(tmp_path, capsys):
    args, file, _ = command(tmp_path)
    with file.open("wb") as stream:
        stream.truncate(20 * 1024 * 1024 + 1)
    assert main(args) == 2
    assert capsys.readouterr().out == ""
