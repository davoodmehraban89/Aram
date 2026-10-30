"""Local-only CLI for unapproved, read-only Mapping coverage preview.

python -m aram_backend.coverage_preview_cli --file pilot.xlsx \
    --company-code 001 --fiscal-year 1404
Prints JSON to stdout. No files are written and no financial action is taken.
"""
from __future__ import annotations

import argparse
import json
import os
import stat
import sys
from pathlib import Path

from aram_backend.coverage_preview import (
    CoverageError, MAX_INPUT_BYTES, preview_mapping_coverage,
)


def safe_read_workbook(file_name: str) -> bytes:
    """Read a bounded regular-file snapshot, detecting replacement and edits."""
    path = Path(file_name)
    if path.suffix.lower() != ".xlsx":
        raise CoverageError("XLSX_REQUIRED")
    try:
        before = path.lstat()
        if not stat.S_ISREG(before.st_mode):
            raise CoverageError("NOT_REGULAR_FILE")
        if not 0 < before.st_size <= MAX_INPUT_BYTES:
            raise CoverageError("WORKBOOK_SIZE_INVALID")

        flags = os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0)
        fd = os.open(path, flags)
        with os.fdopen(fd, "rb") as stream:
            opened = os.fstat(stream.fileno())
            if (not stat.S_ISREG(opened.st_mode)
                    or (opened.st_dev, opened.st_ino) != (before.st_dev, before.st_ino)):
                raise CoverageError("FILE_REPLACED")
            content = stream.read(MAX_INPUT_BYTES + 1)
            finished = os.fstat(stream.fileno())

        after = path.lstat()
        if (not stat.S_ISREG(after.st_mode)
                or (after.st_dev, after.st_ino) != (opened.st_dev, opened.st_ino)
                or opened.st_size != finished.st_size
                or opened.st_mtime_ns != finished.st_mtime_ns
                or after.st_size != finished.st_size
                or after.st_mtime_ns != finished.st_mtime_ns):
            raise CoverageError("FILE_CHANGED_DURING_READ")
    except CoverageError:
        raise
    except OSError as exc:
        raise CoverageError("WORKBOOK_READ_FAILED") from exc
    if not 0 < len(content) <= MAX_INPUT_BYTES:
        raise CoverageError("WORKBOOK_SIZE_INVALID")
    return content


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="ARAM read-only non-official Mapping coverage diagnostic"
    )
    parser.add_argument("--file", required=True)
    parser.add_argument("--company-code", required=True)
    parser.add_argument("--fiscal-year", required=True, type=int)
    args = parser.parse_args(argv)
    try:
        content = safe_read_workbook(args.file)
        result = preview_mapping_coverage(
            content, company_code=args.company_code, fiscal_year=args.fiscal_year,
        )
    except CoverageError as exc:
        print("ARAM diagnostic blocked: " + exc.code, file=sys.stderr)
        return 2
    print(json.dumps(result.to_dict(), sort_keys=True, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
