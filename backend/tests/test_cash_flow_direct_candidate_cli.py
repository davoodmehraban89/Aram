"""Synthetic CLI tests for direct cash flow manifests and local file safety."""
from __future__ import annotations

import json

import pytest

from aram_backend.cash_flow_direct_candidate_cli import (
    MAX_CASH_MANIFEST_BYTES, main, parse_cash_manifest,
)
from aram_backend.coverage_preview import CoverageError
from test_cash_flow_direct_candidate import (
    cash_accounts, counterpart_policies, transactions, workbook,
)


def cash_manifest():
    return {
        "schema_version": 1,
        "company_code": "001",
        "fiscal_year": 1404,
        "currency": "IRR",
        "unit": "Rial",
        "cash_accounts": [
            {"account_code": p.account_code, "evidence_ref": p.evidence_ref}
            for p in cash_accounts()
        ],
        "counterpart_policies": [
            {"account_code": p.account_code, "activity": p.activity,
             "evidence_ref": p.evidence_ref}
            for p in counterpart_policies()
        ],
        "transactions": [
            {
                "company_code": t.company_code, "fiscal_year": t.fiscal_year,
                "line_id": t.line_id, "transaction_id": t.transaction_id,
                "posting_date": t.posting_date,
                "cash_account_code": t.cash_account_code,
                "counterpart_account_code": t.counterpart_account_code,
                "cash_debit": t.cash_debit, "cash_credit": t.cash_credit,
                "counterpart_debit": t.counterpart_debit,
                "counterpart_credit": t.counterpart_credit,
                "evidence_ref": t.evidence_ref,
            }
            for t in transactions()
        ],
    }


def files(tmp_path, *, manifest=None, data=None):
    data = workbook() if data is None else data
    manifest = cash_manifest() if manifest is None else manifest
    xlsx = tmp_path / "synthetic.xlsx"
    json_file = tmp_path / "cash-manifest.json"
    xlsx.write_bytes(data)
    json_file.write_text(json.dumps(manifest), encoding="utf-8")
    return xlsx, json_file, data


def command(paths):
    return ["--file", str(paths[0]), "--manifest", str(paths[1])]


def test_cli_direct_cash_flow_json_and_source_are_unchanged(tmp_path, capsys):
    paths = files(tmp_path)
    original = paths[2]
    assert main(command(paths)) == 0
    output = capsys.readouterr()
    result = json.loads(output.out)
    assert result["operating_net_cash_flow"] == "10"
    assert result["investing_net_cash_flow"] == "-10"
    assert result["financing_net_cash_flow"] == "10"
    assert result["net_change_in_cash"] == "10"
    assert result["closing_cash_and_equivalents"] == "130"
    assert result["eligible_for_analyst_review"]
    assert not result["official_financial_statement"]
    assert not result["releasable"]
    assert output.err == ""
    assert paths[0].read_bytes() == original
    assert sorted(p.name for p in tmp_path.iterdir()) == [
        "cash-manifest.json", "synthetic.xlsx"
    ]


def test_cli_blocked_transaction_manifest_returns_three(tmp_path, capsys):
    manifest = cash_manifest()
    manifest["transactions"].pop()
    paths = files(tmp_path, manifest=manifest)
    assert main(command(paths)) == 3
    result = json.loads(capsys.readouterr().out)
    assert not result["eligible_for_analyst_review"]
    assert "CASH_ACCOUNT_CREDIT_TURNOVER_MISMATCH" in result["findings"]


def test_cli_wrong_transaction_scope_returns_two_without_stdout(tmp_path, capsys):
    manifest = cash_manifest()
    manifest["transactions"][0]["company_code"] = "002"
    paths = files(tmp_path, manifest=manifest)
    assert main(command(paths)) == 2
    output = capsys.readouterr()
    assert output.out == ""
    assert "CASH_FLOW_TRANSACTION_SCOPE_MISMATCH" in output.err


@pytest.mark.parametrize("raw", [
    b"null", b"[]", b"{}", b"not-json", b"\xff",
    b'{"schema_version":1,"schema_version":1}',
    json.dumps({**cash_manifest(), "extra": True}).encode("utf-8"),
    json.dumps({**cash_manifest(), "schema_version": True}).encode("utf-8"),
    json.dumps({**cash_manifest(), "company_code": " 001"}).encode("utf-8"),
    json.dumps({**cash_manifest(), "fiscal_year": True}).encode("utf-8"),
    json.dumps({**cash_manifest(), "cash_accounts": "bad"}).encode("utf-8"),
    json.dumps({**cash_manifest(), "cash_accounts": [{}]}).encode("utf-8"),
    json.dumps({**cash_manifest(), "counterpart_policies": [{}]}).encode("utf-8"),
    json.dumps({**cash_manifest(), "transactions": [{}]}).encode("utf-8"),
])
def test_invalid_cash_manifest_schema_fails_closed(raw):
    with pytest.raises(CoverageError):
        parse_cash_manifest(raw)


def test_duplicate_nested_transaction_key_fails_closed():
    raw = (
        '{"schema_version":1,"company_code":"001","fiscal_year":1404,'
        '"currency":"IRR","unit":"Rial","cash_accounts":[],"counterpart_policies":[],'
        '"transactions":[{"line_id":"A","line_id":"B"}]}'
    ).encode("utf-8")
    with pytest.raises(CoverageError) as error:
        parse_cash_manifest(raw)
    assert error.value.code == "DUPLICATE_MANIFEST_KEY"


def test_manifest_transaction_limit_is_enforced():
    manifest = cash_manifest()
    manifest["transactions"] = manifest["transactions"] * 5001
    with pytest.raises(CoverageError) as error:
        parse_cash_manifest(json.dumps(manifest).encode("utf-8"))
    assert error.value.code == "CASH_MANIFEST_TRANSACTIONS_INVALID"


def test_manifest_size_limit_is_enforced():
    with pytest.raises(CoverageError) as error:
        parse_cash_manifest(b" " * (MAX_CASH_MANIFEST_BYTES + 1))
    assert error.value.code == "CASH_MANIFEST_SIZE_INVALID"


def test_symlink_manifest_rejected(tmp_path, capsys):
    paths = files(tmp_path)
    alias = tmp_path / "alias.json"
    try:
        alias.symlink_to(paths[1])
    except (OSError, NotImplementedError):
        pytest.skip("Symlinks unavailable")
    args = command(paths)
    args[-1] = str(alias)
    assert main(args) == 2
    assert capsys.readouterr().out == ""


def test_missing_manifest_or_workbook_rejected(tmp_path, capsys):
    paths = files(tmp_path)
    paths[1].unlink()
    assert main(command(paths)) == 2
    assert capsys.readouterr().out == ""
    paths = files(tmp_path)
    paths[0].unlink()
    assert main(command(paths)) == 2
    assert capsys.readouterr().out == ""


def test_invalid_workbook_rejected_before_json_success(tmp_path, capsys):
    paths = files(tmp_path, data=b"broken")
    assert main(command(paths)) == 2
    assert capsys.readouterr().out == ""
