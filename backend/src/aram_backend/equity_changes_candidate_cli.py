"""Offline CLI for unsigned equity changes analyst preview."""
from __future__ import annotations

import argparse
import json
import sys

from aram_backend.coverage_preview import CoverageError
from aram_backend.coverage_preview_cli import safe_read_workbook
from aram_backend.equity_changes_candidate import (
    EquityMovementPolicy, build_equity_changes_candidate,
)
from aram_backend.reconciliation_review_cli import (
    MAX_MANIFEST_BYTES, _strict_pairs, parse_manifest, safe_read_manifest,
)

POLICY_FIELDS = frozenset({
    "statement_section", "note_number", "subnote_code", "equity_component",
    "movement_category", "sign_multiplier", "line_label", "policy_evidence_ref",
})
ROOT_FIELDS = frozenset({"schema_version", "company_code", "fiscal_year", "policies"})


def parse_equity_manifest(content: bytes):
    if not isinstance(content, bytes) or not 0 < len(content) <= MAX_MANIFEST_BYTES:
        raise CoverageError("EQUITY_MANIFEST_SIZE_INVALID")
    try:
        payload = json.loads(content.decode("utf-8"), object_pairs_hook=_strict_pairs)
    except CoverageError:
        raise
    except (UnicodeError, ValueError, RecursionError) as exc:
        raise CoverageError("EQUITY_MANIFEST_JSON_INVALID") from exc
    if not isinstance(payload, dict) or set(payload) != ROOT_FIELDS:
        raise CoverageError("EQUITY_MANIFEST_SCHEMA_INVALID")
    if type(payload["schema_version"]) is not int or payload["schema_version"] != 1:
        raise CoverageError("EQUITY_MANIFEST_VERSION_INVALID")
    company = payload["company_code"]
    if (not isinstance(company, str) or not company
            or company != company.strip() or len(company) > 64
            or any(ord(char) < 32 for char in company)):
        raise CoverageError("EQUITY_MANIFEST_COMPANY_INVALID")
    year = payload["fiscal_year"]
    if type(year) is not int or year <= 0:
        raise CoverageError("EQUITY_MANIFEST_YEAR_INVALID")
    items = payload["policies"]
    if not isinstance(items, list) or len(items) > 10_000:
        raise CoverageError("EQUITY_MANIFEST_POLICIES_INVALID")
    policies = []
    for item in items:
        if not isinstance(item, dict) or set(item) != POLICY_FIELDS:
            raise CoverageError("EQUITY_MANIFEST_POLICY_SCHEMA_INVALID")
        policies.append(EquityMovementPolicy(**item))
    return company, year, tuple(policies)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="ARAM offline NONOFFICIAL statement-of-changes-in-equity preview"
    )
    parser.add_argument("--file", required=True)
    parser.add_argument("--references", required=True)
    parser.add_argument("--policies", required=True)
    args = parser.parse_args(argv)
    try:
        company, year, references = parse_manifest(
            safe_read_manifest(args.references)
        )
        policy_company, policy_year, policies = parse_equity_manifest(
            safe_read_manifest(args.policies)
        )
        if (company, year) != (policy_company, policy_year):
            raise CoverageError("EQUITY_SCOPE_MISMATCH")
        source = safe_read_workbook(args.file)
        result = build_equity_changes_candidate(
            source, company_code=company, fiscal_year=year,
            references=references, policies=policies,
        )
    except CoverageError as exc:
        print("ARAM unsigned equity changes candidate blocked: " + exc.code,
              file=sys.stderr)
        return 2
    print(json.dumps(result.to_dict(), sort_keys=True, ensure_ascii=True))
    return 0 if result.eligible_for_analyst_review else 3


if __name__ == "__main__":
    raise SystemExit(main())
