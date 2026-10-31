"""GUI-independent read-only controller for ARAM's five-statement Windows pilot.

All financial calculations are delegated to the audited pipeline CLI function.
Selection never reads or writes the selected files. Execution revalidates both
files using the CLI's bounded, no-symlink, stable-read guards.
"""
from __future__ import annotations

from pathlib import Path
import stat

from aram_backend.coverage_preview import CoverageError, MAX_INPUT_BYTES
from aram_backend.cash_flow_direct_candidate_cli import MAX_CASH_MANIFEST_BYTES
from aram_backend.five_statement_pipeline import FiveStatementPipelineResult
from aram_backend.five_statement_pipeline_cli import run_pipeline_cli


class DesktopFiveInputError(ValueError):
    """Local selection or source validation was refused."""


def _select_regular_file(path_value: str, *, suffix: str, limit: int) -> Path:
    if not isinstance(path_value, str) or not path_value:
        raise DesktopFiveInputError("FILE_REQUIRED")
    path = Path(path_value)
    if path.suffix.lower() != suffix:
        raise DesktopFiveInputError("FILE_EXTENSION_INVALID")
    try:
        info = path.lstat()
    except OSError as exc:
        raise DesktopFiveInputError("FILE_NOT_READABLE") from exc
    if not stat.S_ISREG(info.st_mode):
        raise DesktopFiveInputError("FILE_NOT_REGULAR")
    if not 0 < info.st_size <= limit:
        raise DesktopFiveInputError("FILE_SIZE_INVALID")
    return path


class DesktopFiveStatementController:
    """No stale approval, financial posting, database or export state."""

    def __init__(self) -> None:
        self.workbook_path: Path | None = None
        self.manifest_path: Path | None = None
        self.result: FiveStatementPipelineResult | None = None
        self.error_code: str | None = None
        self.state = "EMPTY"
        self.generation = 0

    @property
    def can_run(self) -> bool:
        return self.workbook_path is not None and self.manifest_path is not None

    def _invalidate(self) -> None:
        self.generation += 1
        self.result = None
        self.error_code = None
        self.state = "SELECTED" if self.can_run else "EMPTY"

    def select_workbook(self, path_value: str) -> None:
        self.workbook_path = None
        self._invalidate()
        self.workbook_path = _select_regular_file(
            path_value, suffix=".xlsx", limit=MAX_INPUT_BYTES,
        )
        self._invalidate()

    def select_manifest(self, path_value: str) -> None:
        self.manifest_path = None
        self._invalidate()
        self.manifest_path = _select_regular_file(
            path_value, suffix=".json", limit=MAX_CASH_MANIFEST_BYTES,
        )
        self._invalidate()

    def clear(self) -> None:
        self.workbook_path = None
        self.manifest_path = None
        self._invalidate()

    def validate(self) -> FiveStatementPipelineResult:
        self.result = None
        self.error_code = None
        self.state = "RUNNING"
        if not self.can_run:
            self.state = "EMPTY"
            raise DesktopFiveInputError("TWO_INPUT_FILES_REQUIRED")
        try:
            outcome = run_pipeline_cli(
                str(self.workbook_path), str(self.manifest_path),
            )
        except CoverageError as exc:
            self.error_code = exc.code
            self.state = "INPUT_ERROR"
            raise DesktopFiveInputError(exc.code) from exc
        self.result = outcome
        self.state = "ELIGIBLE" if outcome.eligible_for_analyst_review else "BLOCKED"
        return outcome
