"""Bounded local-only CLI for paired direct-method cash flow preview."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import stat
import sys
from typing import Any

from aram_backend.cash_flow_direct_candidate import (
    MAX_CASH_ACCOUNTS, MAX_CASH_COUNTERPART_POLICIES,
    MAX_CASH_TRANSACTIONS, CashAccountPolicy, CashCounterpartPolicy,
    CashFlowEntry, build_direct_cash_flow_candidate,
)
from aram_backend.coverage_preview import CoverageError
from aram_backend.coverage_preview_cli import safe_read_workbook
from aram_backend.reconciliation_review_cli import _strict_pairs

MAX_CASH_MANIFEST_BYTES = 20 * 1024 * 1024
ROOT_FIELDS = frozenset({
    "schema_version", "company_code", "fiscal_year", "currency", "unit",
    "cash_accounts", "counterpart_policies", "transactions",
})
CASH_POLICY_FIELDS = frozenset({"account_code", "evidence_ref"})
COUNTERPART_POLICY_FIELDS = frozenset({"account_code", "activity", "evidence_ref"})
TRANSACTION_FIELDS = frozenset({
    "company_code", "fiscal_year", "line_id", "transaction_id", "posting_date",
    "cash_account_code", "counterpart_account_code", "cash_debit", "cash_credit",
    "counterpart_debit", "counterpart_credit", "evidence_ref",
})


def safe_read_cash_manifest(filename: str) -> bytes:
    """Read one bounded, stable regular JSON file without following symlinks."""
    path = Path(filename)
    if path.suffix.lower() != ".json":
        raise CoverageError("CASH_MANIFEST_JSON_REQUIRED")
    try:
        before = path.lstat()
        if not stat.S_ISREG(before.st_mode):
            raise CoverageError("CASH_MANIFEST_NOT_REGULAR_FILE")
        if not 0 < before.st_size <= MAX_CASH_MANIFEST_BYTES:
            raise CoverageError("CASH_MANIFEST_SIZE_INVALID")
        flags = os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0)
        fd = os.open(path, flags)
        with os.fdopen(fd, "rb") as stream:
            opened = os.fstat(stream.fileno())
            immediate = path.lstat()
            if (not stat.S_ISREG(opened.st_mode)
                    or not stat.S_ISREG(immediate.st_mode)
                    or (opened.st_dev, opened.st_ino) != (before.st_dev, before.st_ino)
                    or (immediate.st_dev, immediate.st_ino) != (before.st_dev, before.st_ino)):
                raise CoverageError("CASH_MANIFEST_CHANGED")
            content = stream.read(MAX_CASH_MANIFEST_BYTES + 1)
            finished = os.fstat(stream.fileno())
        after = path.lstat()
        if (not stat.S_ISREG(after.st_mode)
                or (after.st_dev, after.st_ino) != (opened.st_dev, opened.st_ino)
                or opened.st_size != finished.st_size
                or opened.st_mtime_ns != finished.st_mtime_ns
                or after.st_size != finished.st_size
                or after.st_mtime_ns != finished.st_mtime_ns):
            raise CoverageError("CASH_MANIFEST_CHANGED")
    except CoverageError:
        raise
    except OSError as exc:
        raise CoverageError("CASH_MANIFEST_READ_FAILED") from exc
    if not 0 < len(content) <= MAX_CASH_MANIFEST_BYTES:
        raise CoverageError("CASH_MANIFEST_SIZE_INVALID")
    return content


def parse_cash_manifest(content: bytes):
    if (not isinstance(content, bytes)
            or not 0 < len(content) <= MAX_CASH_MANIFEST_BYTES):
        raise CoverageError("CASH_MANIFEST_SIZE_INVALID")
    try:
        payload = json.loads(content.decode("utf-8"), object_pairs_hook=_strict_pairs)
    except CoverageError:
        raise
    except (UnicodeError, ValueError, RecursionError) as exc:
        raise CoverageError("CASH_MANIFEST_JSON_INVALID") from exc
    if not isinstance(payload, dict) or set(payload) != ROOT_FIELDS:
        raise CoverageError("CASH_MANIFEST_SCHEMA_INVALID")
    if type(payload["schema_version"]) is not int or payload["schema_version"] != 1:
        raise CoverageError("CASH_MANIFEST_VERSION_INVALID")
    company = payload["company_code"]
    if (not isinstance(company, str) or not company or company != company.strip()
            or len(company) > 64 or any(ord(char) < 32 for char in company)):
        raise CoverageError("CASH_MANIFEST_COMPANY_INVALID")
    year = payload["fiscal_year"]
    if type(year) is not int or year <= 0:
        raise CoverageError("CASH_MANIFEST_YEAR_INVALID")
    currency, unit = payload["currency"], payload["unit"]
    if not isinstance(currency, str) or not currency or not isinstance(unit, str) or not unit:
        raise CoverageError("CASH_MANIFEST_CURRENCY_UNIT_INVALID")

    cash_items = payload["cash_accounts"]
    if (not isinstance(cash_items, list)
            or not 0 < len(cash_items) <= MAX_CASH_ACCOUNTS):
        raise CoverageError("CASH_MANIFEST_CASH_ACCOUNTS_INVALID")
    cash_accounts = []
    for item in cash_items:
        if not isinstance(item, dict) or set(item) != CASH_POLICY_FIELDS:
            raise CoverageError("CASH_MANIFEST_CASH_POLICY_INVALID")
        cash_accounts.append(CashAccountPolicy(**item))

    counterpart_items = payload["counterpart_policies"]
    if (not isinstance(counterpart_items, list)
            or len(counterpart_items) > MAX_CASH_COUNTERPART_POLICIES):
        raise CoverageError("CASH_MANIFEST_COUNTERPART_POLICIES_INVALID")
    counterpart_policies = []
    for item in counterpart_items:
        if not isinstance(item, dict) or set(item) != COUNTERPART_POLICY_FIELDS:
            raise CoverageError("CASH_MANIFEST_COUNTERPART_POLICY_INVALID")
        counterpart_policies.append(CashCounterpartPolicy(**item))

    transaction_items = payload["transactions"]
    if (not isinstance(transaction_items, list)
            or len(transaction_items) > MAX_CASH_TRANSACTIONS):
        raise CoverageError("CASH_MANIFEST_TRANSACTIONS_INVALID")
    transactions = []
    for item in transaction_items:
        if not isinstance(item, dict) or set(item) != TRANSACTION_FIELDS:
            raise CoverageError("CASH_MANIFEST_TRANSACTION_INVALID")
        transactions.append(CashFlowEntry(**item))
    return (
        company, year, currency, unit, tuple(cash_accounts),
        tuple(counterpart_policies), tuple(transactions),
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="ARAM offline NONOFFICIAL direct-method cash flow diagnostic"
    )
    parser.add_argument("--file", required=True, help="Local Pilot XLSX snapshot")
    parser.add_argument("--manifest", required=True, help="Paired cash transaction JSON")
    args = parser.parse_args(argv)
    try:
        (
            company, year, currency, unit, cash_accounts,
            counterpart_policies, transactions,
        ) = parse_cash_manifest(safe_read_cash_manifest(args.manifest))
        source = safe_read_workbook(args.file)
        result = build_direct_cash_flow_candidate(
            source, company_code=company, fiscal_year=year,
            currency=currency, unit=unit, cash_accounts=cash_accounts,
            counterpart_policies=counterpart_policies, transactions=transactions,
        )
    except CoverageError as exc:
        print("ARAM direct cash flow candidate blocked: " + exc.code, file=sys.stderr)
        return 2
    print(json.dumps(result.to_dict(), ensure_ascii=True, sort_keys=True))
    return 0 if result.eligible_for_analyst_review else 3


if __name__ == "__main__":
    raise SystemExit(main())
