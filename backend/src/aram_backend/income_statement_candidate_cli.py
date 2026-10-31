"""Offline CLI for the UNAPPROVED ARAM income statement candidate.

Reads local authorized XLSX and two strict JSON manifests; writes only JSON to
stdout. Exit 0 = analyst preview, 3 = blocked review, 2 = unsafe input.
It does not authorize financial reports or any database/filesystem mutation.
"""
from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from aram_backend.coverage_preview import CoverageError
from aram_backend.coverage_preview_cli import safe_read_workbook
from aram_backend.income_statement_candidate import (
    IncomeStatementLinePolicy, build_income_statement_candidate,
)
from aram_backend.reconciliation_review_cli import (
    MAX_MANIFEST_BYTES, _strict_pairs, parse_manifest, safe_read_manifest,
)

POLICY_FIELDS = frozenset({
    "statement_section", "note_number", "subnote_code", "category",
    "sign_multiplier", "line_label", "policy_evidence_ref",
})
ROOT_FIELDS = frozenset({"schema_version", "company_code", "fiscal_year", "policies"})


def parse_income_manifest(
    content: bytes,
) -> tuple[str, int, tuple[IncomeStatementLinePolicy, ...]]:
    if not isinstance(content, bytes) or not 0 < len(content) <= MAX_MANIFEST_BYTES:
        raise CoverageError("INCOME_MANIFEST_SIZE_INVALID")
    try:
        payload = json.loads(content.decode("utf-8"), object_pairs_hook=_strict_pairs)
    except CoverageError:
        raise
    except (UnicodeError, ValueError, RecursionError) as exc:
        raise CoverageError("INCOME_MANIFEST_JSON_INVALID") from exc
    if not isinstance(payload, dict) or set(payload) != ROOT_FIELDS:
        raise CoverageError("INCOME_MANIFEST_SCHEMA_INVALID")
    if type(payload["schema_version"]) is not int or payload["schema_version"] != 1:
        raise CoverageError("INCOME_MANIFEST_VERSION_INVALID")
    company = payload["company_code"]
    if (not isinstance(company, str) or not company
            or company != company.strip() or len(company) > 64
            or any(ord(char) < 32 for char in company)):
        raise CoverageError("INCOME_MANIFEST_COMPANY_INVALID")
    year = payload["fiscal_year"]
    if type(year) is not int or year <= 0:
        raise CoverageError("INCOME_MANIFEST_YEAR_INVALID")
    items = payload["policies"]
    if not isinstance(items, list) or len(items) > 10_000:
        raise CoverageError("INCOME_MANIFEST_POLICIES_INVALID")
    result = []
    for item in items:
        if not isinstance(item, dict) or set(item) != POLICY_FIELDS:
            raise CoverageError("INCOME_MANIFEST_POLICY_SCHEMA_INVALID")
        result.append(IncomeStatementLinePolicy(**item))
    return company, year, tuple(result)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="ARAM offline NONOFFICIAL income statement analyst preview"
    )
    parser.add_argument("--file", required=True)
    parser.add_argument("--references", required=True)
    parser.add_argument("--policies", required=True)
    options = parser.parse_args(argv)
    try:
        company, year, references = parse_manifest(
            safe_read_manifest(options.references)
        )
        policy_company, policy_year, policies = parse_income_manifest(
            safe_read_manifest(options.policies)
        )
        if (company, year) != (policy_company, policy_year):
            raise CoverageError("INCOME_SCOPE_MISMATCH")
        data = safe_read_workbook(options.file)
        result = build_income_statement_candidate(
            data, company_code=company, fiscal_year=year,
            references=references, policies=policies,
        )
    except CoverageError as exc:
        print("ARAM unsigned income candidate blocked: " + exc.code, file=sys.stderr)
        return 2
    print(json.dumps(result.to_dict(), ensure_ascii=True, sort_keys=True))
    return 0 if result.eligible_for_analyst_review else 3


if __name__ == "__main__":
    raise SystemExit(main())
