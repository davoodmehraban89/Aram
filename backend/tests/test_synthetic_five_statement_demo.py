"""Synthetic inspection package creation and safety tests."""
from __future__ import annotations

from hashlib import sha256
import json

import pytest

from aram_backend.five_statement_pipeline_cli import run_pipeline_cli
from aram_backend.synthetic_five_statement_demo import (
    DEMO_MANIFEST, DEMO_NOTICE, DEMO_WORKBOOK,
    main, pipeline_manifest, source_workbook, write_demo_bundle,
)


def test_generated_demo_bundle_runs_real_five_statement_pipeline(tmp_path):
    destination = tmp_path / "ARAM-DEMO-SYNTHETIC-ONLY"
    workbook, manifest = write_demo_bundle(destination)
    assert workbook.name == DEMO_WORKBOOK
    assert manifest.name == DEMO_MANIFEST
    assert (destination / DEMO_NOTICE).is_file()
    assert "SYNTHETIC" in (destination / DEMO_NOTICE).read_text(encoding="utf-8")
    assert len(tuple(destination.iterdir())) == 3

    original_workbook = sha256(workbook.read_bytes()).hexdigest()
    original_manifest = sha256(manifest.read_bytes()).hexdigest()
    result = run_pipeline_cli(str(workbook), str(manifest))
    assert result.eligible_for_analyst_review, result.findings
    assert result.balance_sheet.assets_total == "100"
    assert result.income_statement.net_result == "20"
    assert result.equity_changes.closing_equity_total == "90"
    assert result.cash_flow.closing_cash_and_equivalents == "50"
    assert not result.releasable and not result.official_financial_statement
    assert sha256(workbook.read_bytes()).hexdigest() == original_workbook
    assert sha256(manifest.read_bytes()).hexdigest() == original_manifest


def test_example_manifest_is_structurally_parseable_and_not_real_company_data():
    document = pipeline_manifest()
    assert document["schema_version"] == 1
    assert document["company_code"] == "001"
    assert all(str(item["evidence_ref"]).startswith("SYNTH-") for item in document["references"])
    assert all(str(item["line_id"]).startswith("CF-") for item in document["transactions"])
    assert source_workbook()[:2] == b"PK"


def test_generator_never_overwrites_an_existing_directory_or_file(tmp_path):
    destination = tmp_path / "EXISTING-DATA"
    destination.mkdir()
    original = destination / "private.xlsx"
    original.write_bytes(b"private untouched")
    before = sha256(original.read_bytes()).hexdigest()
    with pytest.raises(FileExistsError):
        write_demo_bundle(destination)
    assert sha256(original.read_bytes()).hexdigest() == before
    assert list(destination.iterdir()) == [original]


def test_generator_never_overwrites_existing_demo_bundle(tmp_path):
    directory = tmp_path / "ARAM-DEMO"
    workbook, manifest = write_demo_bundle(directory)
    digests = (
        sha256(workbook.read_bytes()).hexdigest(),
        sha256(manifest.read_bytes()).hexdigest(),
    )
    with pytest.raises(FileExistsError):
        write_demo_bundle(directory)
    assert (
        sha256(workbook.read_bytes()).hexdigest(),
        sha256(manifest.read_bytes()).hexdigest(),
    ) == digests


def test_generator_rejects_symlink_directory(tmp_path):
    destination = tmp_path / "SENSITIVE"
    destination.mkdir()
    link = tmp_path / "ALIAS"
    try:
        link.symlink_to(destination, target_is_directory=True)
    except (OSError, NotImplementedError):
        pytest.skip("Symlinks unavailable on this runner")
    with pytest.raises(FileExistsError):
        write_demo_bundle(link)
    assert not list(destination.iterdir())


def test_module_cli_requires_explicit_output_directory(tmp_path):
    with pytest.raises(SystemExit):
        main([])
    destination = tmp_path / "FIRST-DEMO"
    assert main(["--output-dir", str(destination)]) == 0
    assert (destination / DEMO_WORKBOOK).is_file()
    with pytest.raises(SystemExit) as exc:
        main(["--output-dir", str(destination)])
    assert exc.value.code == 2
