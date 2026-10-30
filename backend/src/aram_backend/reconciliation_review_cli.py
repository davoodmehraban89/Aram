"""Offline CLI for non-official read-only note exposure reconciliation.

Usage: python -m aram_backend.reconciliation_review_cli \
  --file synthetic.xlsx --references synthetic_references.json

Returns 0 only for analyst-review matched exposure, 3 for a blocking
reconciliation finding, and 2 for malformed/unreadable inputs. NEVER creates
approved statements or edits source files.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import stat
import sys
from typing import Any

from aram_backend.coverage_preview import CoverageError
from aram_backend.coverage_preview_cli import safe_read_workbook
from aram_backend.reconciliation_review import (
    NoteReference, reconcile_workbook_for_review,
)

MAX_MANIFEST_BYTES = 512 * 1024
EXPECTED_ROOT_KEYS = frozenset({
    "schema_version", "company_code", "fiscal_year", "references",
})
EXPECTED_REFERENCE_KEYS = frozenset({
    "statement", "section", "note_number", "subnote_code",
    "expected_closing_exposure", "evidence_ref",
})


def _strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result = {}
    for key, value in pairs:
        if key in result:
            raise CoverageError("DUPLICATE_MANIFEST_KEY")
        result[key] = value
    return result


def safe_read_manifest(filename: str) -> bytes:
    """Read a bounded, unchanged local regular JSON file without symlinks."""
    path = Path(filename)
    if path.suffix.lower() != ".json":
        raise CoverageError("JSON_MANIFEST_REQUIRED")
    try:
        first = path.lstat()
        if not stat.S_ISREG(first.st_mode):
            raise CoverageError("MANIFEST_NOT_REGULAR_FILE")
        if not 0 < first.st_size <= MAX_MANIFEST_BYTES:
            raise CoverageError("MANIFEST_SIZE_INVALID")
        flags = os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0)
        fd = os.open(path, flags)
        with os.fdopen(fd, "rb") as stream:
            opened = os.fstat(stream.fileno())
            immediate = path.lstat()
            if (not stat.S_ISREG(opened.st_mode)
                    or not stat.S_ISREG(immediate.st_mode)
                    or (opened.st_dev, opened.st_ino) != (first.st_dev, first.st_ino)
                    or (immediate.st_dev, immediate.st_ino) != (first.st_dev, first.st_ino)):
                raise CoverageError("MANIFEST_CHANGED")
            content = stream.read(MAX_MANIFEST_BYTES + 1)
            finished = os.fstat(stream.fileno())
        last = path.lstat()
        if (not stat.S_ISREG(last.st_mode)
                or (last.st_dev, last.st_ino) != (first.st_dev, first.st_ino)
                or opened.st_size != finished.st_size
                or opened.st_mtime_ns != finished.st_mtime_ns
                or last.st_size != finished.st_size
                or last.st_mtime_ns != finished.st_mtime_ns):
            raise CoverageError("MANIFEST_CHANGED")
    except CoverageError:
        raise
    except OSError as exc:
        raise CoverageError("MANIFEST_READ_FAILED") from exc
    if not 0 < len(content) <= MAX_MANIFEST_BYTES:
        raise CoverageError("MANIFEST_SIZE_INVALID")
    return content


def parse_manifest(content: bytes) -> tuple[str, int, tuple[NoteReference, ...]]:
    if not isinstance(content, bytes) or not 0 < len(content) <= MAX_MANIFEST_BYTES:
        raise CoverageError("MANIFEST_SIZE_INVALID")
    try:
        document = json.loads(content.decode("utf-8"), object_pairs_hook=_strict_pairs)
    except CoverageError:
        raise
    except (UnicodeError, ValueError, RecursionError) as exc:
        raise CoverageError("INVALID_MANIFEST_JSON") from exc
    if not isinstance(document, dict) or set(document) != EXPECTED_ROOT_KEYS:
        raise CoverageError("INVALID_MANIFEST_SCHEMA")
    if type(document["schema_version"]) is not int or document["schema_version"] != 1:
        raise CoverageError("INVALID_MANIFEST_VERSION")
    company = document["company_code"]
    if (not isinstance(company, str) or not company or company != company.strip()
            or len(company) > 64 or any(ord(ch) < 32 for ch in company)):
        raise CoverageError("INVALID_MANIFEST_COMPANY")
    if type(document["fiscal_year"]) is not int or document["fiscal_year"] <= 0:
        raise CoverageError("INVALID_MANIFEST_YEAR")
    entries = document["references"]
    if not isinstance(entries, list) or len(entries) > 10_000:
        raise CoverageError("INVALID_MANIFEST_REFERENCES")
    refs: list[NoteReference] = []
    for item in entries:
        if not isinstance(item, dict) or set(item) != EXPECTED_REFERENCE_KEYS:
            raise CoverageError("INVALID_MANIFEST_REFERENCE")
        refs.append(NoteReference(**item))
    return document["company_code"], document["fiscal_year"], tuple(refs)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="ARAM offline UNAPPROVED note reconciliation diagnostic"
    )
    parser.add_argument("--file", required=True, help="Local authorized Pilot XLSX")
    parser.add_argument("--references", required=True, help="Local synthetic control totals JSON")
    options = parser.parse_args(argv)
    try:
        company, year, refs = parse_manifest(safe_read_manifest(options.references))
        workbook = safe_read_workbook(options.file)
        result = reconcile_workbook_for_review(
            workbook, company_code=company, fiscal_year=year,
            references=refs,
        )
    except CoverageError as exc:
        print("ARAM note review blocked: " + exc.code, file=sys.stderr)
        return 2
    print(json.dumps(result.to_dict(), ensure_ascii=True, sort_keys=True))
    return 0 if result.matched_for_analyst_review else 3


if __name__ == "__main__":
    raise SystemExit(main())
