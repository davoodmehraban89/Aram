import os
import zipfile
import pytest


def test_release_package_documentation_consistency():
    docs_to_check = [
        "docs/ACCOUNTANT_USER_GUIDE.md",
        "docs/PILOT_INSTALLATION.md",
        "docs/PILOT_RELEASE_PACKAGE.md",
        "docs/PILOT_TESTING_GUIDE.md",
        "docs/ARAM_V1_READINESS_AUDIT.md",
        "docs/RELEASE_NOTES_V1.md",
    ]
    for doc_path in docs_to_check:
        assert os.path.exists(doc_path), f"Missing documentation file: {doc_path}"
        with open(doc_path, "r", encoding="utf-8") as f:
            content = f.read()
        assert len(content) > 100


def test_sample_files_consistency():
    sample_files = [
        "samples/sample_general_ledger.csv",
        "samples/sample_trial_balance.csv",
        "samples/sample_mapping_template.csv",
    ]
    for sample_path in sample_files:
        assert os.path.exists(sample_path), f"Missing sample file: {sample_path}"
        with open(sample_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        assert len(lines) >= 5


def test_release_notes_version_specification():
    with open("docs/RELEASE_NOTES_V1.md", "r", encoding="utf-8") as f:
        content = f.read()
    assert "1.0.0-pilot" in content
    assert "Aram_Accountant_Pilot.exe" in content


def test_zip_release_package_contents():
    zip_path = "dist/Aram_V1.0.0_Pilot.zip"
    assert os.path.exists(zip_path), "Release ZIP package dist/Aram_V1.0.0_Pilot.zip does not exist."
    with zipfile.ZipFile(zip_path, "r") as z:
        file_list = z.namelist()
        assert any("Aram_Accountant_Pilot.exe" in f for f in file_list)
        assert any("ACCOUNTANT_USER_GUIDE.md" in f for f in file_list)
        assert any("sample_general_ledger.csv" in f for f in file_list)
