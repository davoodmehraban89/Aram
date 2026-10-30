"""Read-only desktop preflight controller; no database or financial postings.

Native Tk window is a presentation adapter. No source is ever mutated,
uploaded, auto-imported, or used to generate statements.
"""
from __future__ import annotations

from pathlib import Path

from aram_backend.pilot_workbook import PilotPreflightResult, preflight_pilot_workbook

MAX_WORKBOOK_BYTES = 20 * 1024 * 1024


class PilotInputError(ValueError):
    """Refuse unsafe, absent or unsupported local input without side effects."""


class DesktopPilotController:
    """Small, GUI-independent application state for native desktop tests."""

    def __init__(self) -> None:
        self.selected_path: Path | None = None
        self.result: PilotPreflightResult | None = None
        self.state = "EMPTY"

    def clear(self) -> None:
        self.selected_path = None
        self.result = None
        self.state = "EMPTY"

    def choose_file(self, file_path: str | Path) -> None:
        # An attempted invalid switch must not leave the earlier workbook
        # looking like the currently selected and successfully checked one.
        self.clear()
        try:
            path = Path(file_path)
            if path.suffix.lower() != ".xlsx" or not path.is_file():
                raise PilotInputError("Only an existing local .xlsx file is supported")
            if path.is_symlink():
                raise PilotInputError("Symbolic links are not accepted")
            size = path.stat().st_size
            if size <= 0 or size > MAX_WORKBOOK_BYTES:
                raise PilotInputError("Workbook must be nonempty and at most 20 MiB")
        except (OSError, ValueError) as exc:
            raise PilotInputError("Cannot select the workbook") from exc
        self.selected_path = path
        self.state = "SELECTED"

    def validate(self) -> PilotPreflightResult:
        """Read bounded bytes and run the existing governed in-memory contract."""
        if self.selected_path is None:
            raise PilotInputError("Select an .xlsx Pilot workbook first")
        self.result = None
        self.state = "SELECTED"
        try:
            # Bound the *actual* bytes read, not just an earlier stat, to
            # reject a changing file and avoid unbounded memory consumption.
            with self.selected_path.open("rb") as handle:
                content = handle.read(MAX_WORKBOOK_BYTES + 1)
        except OSError as exc:
            raise PilotInputError("Selected workbook cannot be read") from exc
        if not content or len(content) > MAX_WORKBOOK_BYTES:
            raise PilotInputError("Workbook is empty or exceeds the 20 MiB limit")
        checked = preflight_pilot_workbook(content)
        self.result = checked
        self.state = "VALID" if checked.valid else "INVALID"
        return checked
