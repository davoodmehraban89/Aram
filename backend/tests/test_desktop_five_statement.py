"""Synthetic-only safety and lifecycle checks for the native Windows pilot."""
from __future__ import annotations

from hashlib import sha256
import json
import sys
import time

import pytest

from aram_backend.desktop_five_statement_core import (
    DesktopFiveInputError, DesktopFiveStatementController,
    MAX_INPUT_BYTES, MAX_CASH_MANIFEST_BYTES,
)
from aram_backend.desktop_five_statement import ACTIONS, FiveStatementWindow, main, self_test
from test_five_statement_pipeline_integration import (
    cash_transactions, pipeline_manifest, source_workbook,
)


def fixtures(tmp_path, *, manifest=None):
    xlsx = tmp_path / "synthetic.xlsx"
    jsonfile = tmp_path / "synthetic.json"
    xlsx.write_bytes(source_workbook())
    jsonfile.write_text(
        json.dumps(pipeline_manifest() if manifest is None else manifest),
        encoding="utf-8",
    )
    return xlsx, jsonfile


def controller_with_files(paths):
    ctl = DesktopFiveStatementController()
    ctl.select_workbook(str(paths[0]))
    ctl.select_manifest(str(paths[1]))
    return ctl


def test_full_five_statement_preview_is_local_and_never_writes_source_files(tmp_path):
    paths = fixtures(tmp_path)
    workbook_digest = sha256(paths[0].read_bytes()).hexdigest()
    manifest_digest = sha256(paths[1].read_bytes()).hexdigest()
    ctl = controller_with_files(paths)
    assert ctl.can_run
    assert ctl.state == "SELECTED"
    assert ctl.result is None
    result = ctl.validate()
    assert result.eligible_for_analyst_review
    assert result.reconciliation.eligible_for_analyst_review
    assert not result.releasable and not result.official_financial_statement
    assert ctl.result is result
    assert ctl.state == "ELIGIBLE"
    assert sha256(paths[0].read_bytes()).hexdigest() == workbook_digest
    assert sha256(paths[1].read_bytes()).hexdigest() == manifest_digest
    assert {p.name for p in tmp_path.iterdir()} == {
        "synthetic.xlsx", "synthetic.json",
    }


def test_missing_cash_transaction_blocks_without_creating_approved_state(tmp_path):
    manifest = pipeline_manifest(transactions=cash_transactions()[:-1])
    ctl = controller_with_files(fixtures(tmp_path, manifest=manifest))
    result = ctl.validate()
    assert not result.eligible_for_analyst_review
    assert ctl.state == "BLOCKED"
    assert "CASH_FLOW_CANDIDATE_BLOCKED" in result.findings


def test_invalid_manifest_clears_previous_eligible_result(tmp_path):
    paths = fixtures(tmp_path)
    ctl = controller_with_files(paths)
    assert ctl.validate().eligible_for_analyst_review
    paths[1].write_text("not-json", encoding="utf-8")
    with pytest.raises(DesktopFiveInputError):
        ctl.validate()
    assert ctl.state == "INPUT_ERROR"
    assert ctl.result is None
    assert ctl.error_code is not None


def test_changing_selected_file_invalidates_previous_result(tmp_path):
    paths = fixtures(tmp_path)
    ctl = controller_with_files(paths)
    assert ctl.validate().eligible_for_analyst_review
    old_generation = ctl.generation
    ctl.select_manifest(str(paths[1]))
    assert ctl.generation > old_generation
    assert ctl.result is None
    assert ctl.state == "SELECTED"
    ctl.select_workbook(str(paths[0]))
    assert ctl.result is None


def test_invalid_switch_does_not_leave_old_financial_preview_visible(tmp_path):
    paths = fixtures(tmp_path)
    ctl = controller_with_files(paths)
    ctl.validate()
    with pytest.raises(DesktopFiveInputError):
        ctl.select_manifest(str(tmp_path / "missing.json"))
    assert ctl.manifest_path is None
    assert not ctl.can_run
    assert ctl.result is None
    assert ctl.state == "EMPTY"


def test_removed_source_before_execution_refuses_stale_previously_eligible_file(tmp_path):
    paths = fixtures(tmp_path)
    ctl = controller_with_files(paths)
    ctl.validate()
    paths[0].unlink()
    with pytest.raises(DesktopFiveInputError):
        ctl.validate()
    assert ctl.result is None
    assert ctl.state == "INPUT_ERROR"


@pytest.mark.parametrize("selection, name", [
    ("workbook", "invalid.xls"),
    ("workbook", "fake.xlsx.exe"),
    ("manifest", "invalid.txt"),
    ("manifest", "fake.json.bak"),
])
def test_selection_requires_expected_extension(tmp_path, selection, name):
    target = tmp_path / name
    target.write_bytes(b"bad")
    ctl = DesktopFiveStatementController()
    with pytest.raises(DesktopFiveInputError) as exc:
        getattr(ctl, "select_" + selection)(str(target))
    assert exc.value.args[0] == "FILE_EXTENSION_INVALID"
    assert ctl.result is None


@pytest.mark.parametrize("selection, extension", [
    ("workbook", ".xlsx"), ("manifest", ".json"),
])
def test_selection_rejects_symlinks_and_directories(tmp_path, selection, extension):
    target = tmp_path / ("target" + extension)
    target.write_bytes(b"test")
    link = tmp_path / ("alias" + extension)
    try:
        link.symlink_to(target)
    except (OSError, NotImplementedError):
        pytest.skip("No symlink support on test runner")
    ctl = DesktopFiveStatementController()
    with pytest.raises(DesktopFiveInputError):
        getattr(ctl, "select_" + selection)(str(link))
    folder = tmp_path / ("folder" + extension)
    folder.mkdir()
    with pytest.raises(DesktopFiveInputError):
        getattr(ctl, "select_" + selection)(str(folder))


@pytest.mark.parametrize("selection,extension,limit", [
    ("workbook", ".xlsx", MAX_INPUT_BYTES),
    ("manifest", ".json", MAX_CASH_MANIFEST_BYTES),
])
def test_selection_blocks_empty_and_oversized_files(tmp_path, selection, extension, limit):
    target = tmp_path / ("oversize" + extension)
    ctl = DesktopFiveStatementController()
    target.write_bytes(b"")
    with pytest.raises(DesktopFiveInputError):
        getattr(ctl, "select_" + selection)(str(target))
    with target.open("wb") as stream:
        stream.truncate(limit + 1)
    with pytest.raises(DesktopFiveInputError):
        getattr(ctl, "select_" + selection)(str(target))


def test_controller_clear_discards_both_files_and_all_prior_results(tmp_path):
    ctl = controller_with_files(fixtures(tmp_path))
    ctl.validate()
    ctl.clear()
    assert ctl.state == "EMPTY"
    assert ctl.workbook_path is None and ctl.manifest_path is None
    assert ctl.result is None and ctl.error_code is None
    assert not ctl.can_run
    with pytest.raises(DesktopFiveInputError):
        ctl.validate()


def test_headless_executable_smoke_and_all_enabled_actions_have_methods():
    assert self_test() == 0
    assert main(["--self-test"]) == 0
    assert main(["--unexpected"]) == 2
    assert set(ACTIONS) == {
        "file.workbook", "file.manifest", "file.run",
        "file.clear", "file.exit", "help.about",
    }
    for key, method in ACTIONS.items():
        assert callable(getattr(FiveStatementWindow, method)), key


@pytest.mark.skipif(sys.platform != "win32", reason="Native Tk smoke requires Windows runner")
def test_native_window_shows_real_successful_five_statement_result(tmp_path):
    paths = fixtures(tmp_path)
    file_names = {"workbook": str(paths[0]), "manifest": str(paths[1])}
    window = FiveStatementWindow(picker=lambda kind: file_names[kind])
    try:
        window.withdraw()
        window.update_idletasks()
        assert str(window.run_button.cget("state")) == "disabled"
        window.workbook_button.invoke()
        window.manifest_button.invoke()
        assert str(window.run_button.cget("state")) == "normal"
        window.run_button.invoke()
        for _ in range(500):
            window.update()
            if not window._busy:
                break
            time.sleep(0.02)
        assert not window._busy
        assert window.controller.state == "ELIGIBLE"
        assert window.controller.result is not None
        assert window.controller.result.eligible_for_analyst_review
        rows = window.outcome_tree.get_children()
        assert len(rows) == 5
        assert all(
            window.outcome_tree.item(row, "values")[1] == "قابل بررسی"
            for row in rows
        )
        amounts = [
            window.figures_tree.item(row, "values")
            for row in window.figures_tree.get_children()
        ]
        assert len(amounts) == 28
        assert ("ترازنامه", "دارایی‌ها", "100", "پیش‌نویس قابل بررسی؛ غیررسمی") in amounts
        assert ("سود و زیان", "سود خالص", "20", "پیش‌نویس قابل بررسی؛ غیررسمی") in amounts
        expected_details = (
            len(window.controller.result.balance_sheet.lines)
            + len(window.controller.result.income_statement.lines)
            + len(window.controller.result.equity_changes.note_movements)
            + len(window.controller.result.equity_changes.account_movements)
            + len(window.controller.result.cash_flow.cash_flow_lines)
            + len(window.controller.result.cash_flow.account_reconciliations)
            + len(window.controller.result.trial_balance.accounts)
        )
        assert len(window._detail_rows) == expected_details
        assert any(row.item == "Revenue" for row in window._detail_rows)
        window.detail_filter_var.set("سود و زیان")
        window.detail_search_var.set("یادداشت R01")
        window._apply_detail_filter()
        assert window._filtering
        assert str(window.detail_search_button.cget("state")) == "disabled"
        window.update_idletasks()
        for _ in range(500):
            window.update()
            if not window._filtering:
                break
            time.sleep(0.01)
        assert not window._filtering
        assert len(window.detail_tree.get_children()) == 1
        assert window.detail_tree.item(
            window.detail_tree.get_children()[0], "values",
        )[1] == "Revenue"
        window.clear_button.invoke()
        assert not window.outcome_tree.get_children()
        assert not window.figures_tree.get_children()
        assert not window.detail_tree.get_children()
        assert not window._detail_rows
        assert window.controller.result is None
        assert str(window.run_button.cget("state")) == "disabled"
    finally:
        if window.winfo_exists():
            window.destroy()


@pytest.mark.skipif(sys.platform != "win32", reason="Native Tk requires Windows runner")
def test_new_detail_query_supersedes_inflight_search_and_ignores_stale_reply(
    tmp_path, monkeypatch,
):
    """The initial all-rows filter cannot overwrite a newer exact note query."""
    import threading
    import aram_backend.desktop_five_statement as desktop_module

    release_old = threading.Event()
    started_old = threading.Event()
    real_filter = desktop_module.filter_preview_details

    def delayed_filter(rows, *, statement, query):
        if statement == "همه" and query == "":
            started_old.set()
            if not release_old.wait(30):
                raise RuntimeError("Synthetic old filter was not released")
        return real_filter(rows, statement=statement, query=query)

    monkeypatch.setattr(desktop_module, "filter_preview_details", delayed_filter)
    paths = fixtures(tmp_path)
    file_names = {"workbook": str(paths[0]), "manifest": str(paths[1])}
    window = FiveStatementWindow(picker=lambda kind: file_names[kind])
    try:
        window.withdraw()
        window.workbook_button.invoke()
        window.manifest_button.invoke()
        window.run_button.invoke()
        for _ in range(2000):
            window.update()
            if not window._busy and started_old.is_set():
                break
            time.sleep(0.01)
        assert not window._busy
        assert started_old.is_set()
        assert window._filtering
        window.detail_filter_var.set("سود و زیان")
        window.detail_search_var.set("یادداشت R01")
        window._apply_detail_filter()
        assert window._filtering
        for _ in range(500):
            window.update()
            if not window._filtering:
                break
            time.sleep(0.01)
        assert not window._filtering
        rows = window.detail_tree.get_children()
        assert len(rows) == 1
        assert window.detail_tree.item(rows[0], "values")[1] == "Revenue"

        release_old.set()
        for _ in range(30):
            window.update()
            time.sleep(0.01)
        # A superseded full-dataset search must not retain private rows
        # in the pending event queue after the newer search finishes.
        assert window._filter_events.empty()
        rows = window.detail_tree.get_children()
        assert len(rows) == 1
        assert window.detail_tree.item(rows[0], "values")[1] == "Revenue"
        window.clear_button.invoke()
        assert not window.detail_tree.get_children()
        assert not window._detail_rows
    finally:
        release_old.set()
        if window.winfo_exists():
            window.destroy()
