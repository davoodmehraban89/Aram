"""Offline CLI for UNAPPROVED ARAM balance sheet presentation candidates.

Reads three local authorized files and writes JSON to stdout only. Exit 0 is
an arithmetic analyst-preview match, NEVER regulatory or reviewer approval.
Exit 3 means blocked/unbalanced; 2 means malformed or unsafe input.
"""
from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from aram_backend.balance_sheet_candidate import (
    BalanceSheetLinePolicy,
    build_balance_sheet_candidate,
)
from aram_backend.coverage_preview import CoverageError
from aram_backend.coverage_preview_cli import safe_read_workbook
from aram_backend.reconciliation_review_cli import (
    MAX_MANIFEST_BYTES, _strict_pairs, parse_manifest, safe_read_manifest,
)

POLICY_KEYS = frozenset({
    "statement_section", "note_number", "subnote_code",
    "category", "sign_multiplier", "line_label", "policy_evidence_ref",
})
ROOT_KEYS = frozenset({
    "schema_version", "company_code", "fiscal_year", "policies",
})


def parse_presentation_manifest(
    content: bytes,
) -> tuple[str, int, tuple[BalanceSheetLinePolicy, ...]]:
    if not isinstance(content, bytes) or not 0 < len(content) <= MAX_MANIFEST_BYTES:
        raise CoverageError("PRESENTATION_MANIFEST_SIZE_INVALID")
    try:
        payload = json.loads(content.decode("utf-8"), object_pairs_hook=_strict_pairs)
    except CoverageError:
        raise
    except (UnicodeError, ValueError, RecursionError) as exc:
        raise CoverageError("PRESENTATION_MANIFEST_JSON_INVALID") from exc
    if not isinstance(payload, dict) or set(payload) != ROOT_KEYS:
        raise CoverageError("PRESENTATION_MANIFEST_SCHEMA_INVALID")
    if type(payload["schema_version"]) is not int or payload["schema_version"] != 1:
        raise CoverageError("PRESENTATION_MANIFEST_VERSION_INVALID")
    company = payload["company_code"]
    if (not isinstance(company, str) or not company or company != company.strip()
            or len(company) > 64 or any(ord(char) < 32 for char in company)):
        raise CoverageError("PRESENTATION_COMPANY_INVALID")
    year = payload["fiscal_year"]
    if type(year) is not int or year <= 0:
        raise CoverageError("PRESENTATION_YEAR_INVALID")
    items = payload["policies"]
    if not isinstance(items, list) or len(items) > 10_000:
        raise CoverageError("PRESENTATION_POLICIES_INVALID")
    result: list[BalanceSheetLinePolicy] = []
    for item in items:
        if not isinstance(item, dict) or set(item) != POLICY_KEYS:
            raise CoverageError("PRESENTATION_POLICY_SCHEMA_INVALID")
        result.append(BalanceSheetLinePolicy(**item))
    return company, year, tuple(result)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="ARAM offline unsigned balance-sheet candidate diagnostic"
    )
    parser.add_argument("--file", required=True, help="Local Pilot workbook XLSX")
    parser.add_argument("--references", required=True, help="Local note totals JSON")
    parser.add_argument("--policies", required=True, help="Local BS sign/presentation JSON")
    options = parser.parse_args(argv)

    try:
        company, year, references = parse_manifest(
            safe_read_manifest(options.references)
        )
        policy_company, policy_year, policies = parse_presentation_manifest(
            safe_read_manifest(options.policies)
        )
        if (company, year) != (policy_company, policy_year):
            raise CoverageError("PRESENTATION_SCOPE_MISMATCH")
        snapshot = safe_read_workbook(options.file)
        result = build_balance_sheet_candidate(
            snapshot, company_code=company, fiscal_year=year,
            references=references, policies=policies,
        )
    except CoverageError as exc:
        print("ARAM unsigned BS candidate blocked: " + exc.code, file=sys.stderr)
        return 2

    print(json.dumps(result.to_dict(), ensure_ascii=True, sort_keys=True))
    return 0 if result.eligible_for_analyst_review else 3


if __name__ == "__main__":
    raise SystemExit(main())
