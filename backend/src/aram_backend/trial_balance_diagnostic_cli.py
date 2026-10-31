"""Local-only read-only trial balance CLI, with explicit company/year scope.

Exit 0 = arithmetic totals balance for analyst review; NOT a verified source.
Exit 3 = totals mismatch; 2 = malformed/unreadable input.
"""
from __future__ import annotations

import argparse
import json
import sys

from aram_backend.coverage_preview import CoverageError
from aram_backend.coverage_preview_cli import safe_read_workbook
from aram_backend.trial_balance_diagnostic import analyze_trial_balance


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="ARAM nonofficial read-only trial balance diagnostic"
    )
    parser.add_argument("--file", required=True)
    parser.add_argument("--company-code", required=True)
    parser.add_argument("--fiscal-year", required=True, type=int)
    args = parser.parse_args(argv)
    try:
        source = safe_read_workbook(args.file)
        result = analyze_trial_balance(
            source, company_code=args.company_code, fiscal_year=args.fiscal_year,
        )
    except CoverageError as exc:
        print("ARAM trial balance blocked: " + exc.code, file=sys.stderr)
        return 2
    print(json.dumps(result.to_dict(), sort_keys=True, ensure_ascii=True))
    return 0 if result.balanced_for_analyst_review else 3


if __name__ == "__main__":
    raise SystemExit(main())
