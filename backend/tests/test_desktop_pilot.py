"""Desktop pilot safety and command tests; all source data is synthetic."""
from hashlib import sha256
from io import BytesIO

import pytest
from openpyxl import Workbook

from aram_backend.desktop_pilot_core import (
    MAX_WORKBOOK_BYTES, DesktopPilotController, PilotInputError,
)


def workbook_bytes():
    from aram_backend.pilot_workbook import SHEET_HEADERS
    wb = Workbook()
    wb.remove(wb.active)
    for sheet_name, headers in SHEET_HEADERS.items():
        wb.create_sheet(sheet_name).append(list(headers))
    stream = BytesIO()
    wb.save(stream)
    return stream.getvalue()


def test_selection_uses_local_xlsx_only_and_does_not_write(tmp_path):
    original = workbook_bytes()
    selected = tmp_path / "pilot.xlsx"
    selected.write_bytes(original)
    before = sha256(selected.read_bytes()).hexdigest()
    controller = DesktopPilotController()
    controller.choose_file(selected)
    assert controller.selected_path == selected
    assert controller.result is None
    result = controller.validate()
    assert result is controller.result
    assert isinstance(result.valid, bool)
    assert sha256(selected.read_bytes()).hexdigest() == before
    assert not any(path.name.endswith(".db") for path in tmp_path.iterdir())


def test_selection_does_not_validate_implicitly(tmp_path):
    selected = tmp_path / "pilot.xlsx"
    selected.write_bytes(b"not a workbook")
    controller = DesktopPilotController()
    controller.choose_file(selected)
    assert controller.result is None
    assert controller.state == "SELECTED"
    result = controller.validate()
    assert not result.valid
    assert any(issue.code == "INVALID_WORKBOOK" for issue in result.issues)
    assert controller.state == "INVALID"


@pytest.mark.parametrize("name", ["budget.csv", "mapping.xls", "scan.pdf", "backup.xlsx.exe", "not_file"])
def test_rejects_non_xlsx_paths_and_fails_closed(tmp_path, name):
    controller = DesktopPilotController()
    selected = tmp_path / name
    selected.write_bytes(b"x")
    with pytest.raises(PilotInputError):
        controller.choose_file(selected)
    assert controller.selected_path is None
    assert controller.result is None
    assert controller.state == "EMPTY"


def test_rejects_missing_or_directory_and_cannot_validate_without_selection(tmp_path):
    controller = DesktopPilotController()
    with pytest.raises(PilotInputError):
        controller.validate()
    with pytest.raises(PilotInputError):
        controller.choose_file(tmp_path / "missing.xlsx")
    directory = tmp_path / "folder.xlsx"
    directory.mkdir()
    with pytest.raises(PilotInputError):
        controller.choose_file(directory)


def test_file_over_limit_rejected_without_reading_payload(tmp_path):
    selected = tmp_path / "oversized.xlsx"
    with selected.open("wb") as stream:
        stream.truncate(MAX_WORKBOOK_BYTES + 1)
    controller = DesktopPilotController()
    with pytest.raises(PilotInputError):
        controller.choose_file(selected)
    assert controller.selected_path is None


def test_modified_file_becomes_invalid_and_never_uses_stale_result(tmp_path):
    selected = tmp_path / "original.xlsx"
    selected.write_bytes(workbook_bytes())
    controller = DesktopPilotController()
    controller.choose_file(selected)
    controller.validate()
    selected.write_bytes(b"broken")
    changed = controller.validate()
    assert not changed.valid
    assert controller.result is changed
    assert controller.state == "INVALID"


def test_removed_file_clears_prior_validation(tmp_path):
    selected = tmp_path / "pilot.xlsx"
    selected.write_bytes(workbook_bytes())
    controller = DesktopPilotController()
    controller.choose_file(selected)
    controller.validate()
    selected.unlink()
    with pytest.raises(PilotInputError):
        controller.validate()
    assert controller.result is None
    assert controller.state == "SELECTED"


def test_clearing_never_mutates_the_selected_workbook(tmp_path):
    selected = tmp_path / "pilot.xlsx"
    selected.write_bytes(workbook_bytes())
    before = sha256(selected.read_bytes()).hexdigest()
    controller = DesktopPilotController()
    controller.choose_file(selected)
    controller.validate()
    controller.clear()
    assert controller.selected_path is None
    assert controller.result is None
    assert controller.state == "EMPTY"
    assert sha256(selected.read_bytes()).hexdigest() == before


def test_selecting_new_file_discards_previous_issue_list(tmp_path):
    invalid = tmp_path / "invalid.xlsx"
    invalid.write_bytes(b"bad")
    valid_shape = tmp_path / "new.xlsx"
    valid_shape.write_bytes(workbook_bytes())
    controller = DesktopPilotController()
    controller.choose_file(invalid)
    controller.validate()
    assert controller.result.issues
    controller.choose_file(valid_shape)
    assert controller.result is None
    assert controller.state == "SELECTED"


def test_headless_self_diagnostic_uses_real_validator_without_financial_write():
    from aram_backend.desktop_pilot import self_test
    assert self_test() == 0


def test_all_enabled_controls_are_backed_by_implemented_callbacks():
    from aram_backend.desktop_pilot import PILOT_ACTIONS, PilotWindow
    assert set(PILOT_ACTIONS) == {
        "file.open", "file.validate", "file.clear",
        "file.exit", "help.about",
    }
    for action, method_name in PILOT_ACTIONS.items():
        assert callable(getattr(PilotWindow, method_name)), action


def test_bounded_zip_metadata_rejects_expansion_and_many_entries():
    from types import SimpleNamespace
    from aram_backend.desktop_pilot_core import (
        MAX_ZIP_ENTRIES, MAX_UNCOMPRESSED_BYTES, _check_archive_limits,
    )
    with pytest.raises(PilotInputError):
        _check_archive_limits([
            SimpleNamespace(file_size=MAX_UNCOMPRESSED_BYTES + 1),
        ])
    with pytest.raises(PilotInputError):
        _check_archive_limits([
            SimpleNamespace(file_size=1) for _ in range(MAX_ZIP_ENTRIES + 1)
        ])
    with pytest.raises(PilotInputError):
        _check_archive_limits([
            SimpleNamespace(file_size=MAX_UNCOMPRESSED_BYTES // 2 + 1),
            SimpleNamespace(file_size=MAX_UNCOMPRESSED_BYTES // 2 + 1),
        ])


def test_symlink_cannot_be_selected_for_financial_preflight(tmp_path):
    target = tmp_path / "trusted.xlsx"
    target.write_bytes(workbook_bytes())
    link = tmp_path / "untrusted.xlsx"
    try:
        link.symlink_to(target)
    except (NotImplementedError, OSError):
        pytest.skip("Symlinks are not available on this test filesystem")
    controller = DesktopPilotController()
    with pytest.raises(PilotInputError):
        controller.choose_file(link)
    assert controller.state == "EMPTY"
