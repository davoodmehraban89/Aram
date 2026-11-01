from dataclasses import replace
from io import BytesIO

import pytest
from openpyxl import load_workbook

from aram_backend.mapping_workflow import (
    MappingDecision, MappingWorkflowError, MappingWorkspace, export_mapping_rows,
    import_mapping_workbook,
)
from test_pilot_workbook import valid_rows, workbook_bytes


def sample(*, year=1405, company="001", status="Draft"):
    return MappingDecision("M001", company, year, "0010", "BS", "Assets",
                           "01", "001", 1, status, None, "Manual")


def test_lifecycle_requires_distinct_approver_and_records_audit():
    space = MappingWorkspace("001", 1405)
    space.propose(sample(), actor="maker")
    reviewed = space.transition("M001", "Reviewed", actor="reviewer")
    assert reviewed.version == 2
    with pytest.raises(MappingWorkflowError, match="independent"):
        space.transition("M001", "Approved", actor="reviewer")
    approved = space.transition("M001", "Approved", actor="approver")
    assert approved.version == 3
    assert [e.new_status for e in space.audit] == ["Draft", "Reviewed", "Approved"]
    assert space.audit[-1].previous_version == 2
    assert all(e.timestamp for e in space.audit)


def test_illegal_transitions_fail_closed():
    space = MappingWorkspace("001", 1405)
    with pytest.raises(MappingWorkflowError):
        space.transition("missing", "Approved", actor="a")
    space.propose(sample(), actor="a")
    for status in ("Approved", "Draft", "Deleted"):
        with pytest.raises(MappingWorkflowError):
            space.transition("M001", status, actor="b")
    with pytest.raises(MappingWorkflowError):
        space.propose(sample(), actor="a")
    assert len(space.audit) == 1


def test_revision_resets_approval_and_keeps_history():
    space = MappingWorkspace("001", 1405)
    space.propose(sample(), actor="a")
    space.transition("M001", "Reviewed", actor="b")
    space.transition("M001", "Approved", actor="c")
    updated = space.revise("M001", actor="a", target_statement="IS",
                           statement_section="Revenue", note_number="02",
                           subnote_code=None)
    assert updated.status == "Draft" and updated.reviewer is None
    assert updated.version == 4
    assert len(space.audit) == 4
    assert space.audit[-1].previous_status == "Approved"


def test_company_year_isolation_and_atomic_carry_forward_validation():
    space = MappingWorkspace("001", 1405)
    with pytest.raises(MappingWorkflowError, match="isolation"):
        space.propose(sample(company="002"), actor="a")
    with pytest.raises(MappingWorkflowError, match="isolation"):
        space.propose(sample(year=1404), actor="a")
    good = replace(sample(year=1404, status="Approved"), reviewer="r")
    bad = replace(sample(year=1404, company="002", status="Approved"),
                  mapping_id="M002")
    with pytest.raises(MappingWorkflowError):
        space.carry_forward([good, bad], actor="a")
    assert not space.decisions and not space.audit
    assert space.carry_forward([good], actor="a") == 1
    assert space.decisions[0].status == "Draft"
    assert space.decisions[0].source == "CarryForward"
    assert space.decisions[0].fiscal_year == 1405


def test_invalid_scope_and_actor():
    for company, year in (("", 1405), ("001", 0), ("001", True)):
        with pytest.raises(MappingWorkflowError):
            MappingWorkspace(company, year)
    space = MappingWorkspace("001", 1405)
    with pytest.raises(MappingWorkflowError):
        space.propose(sample(), actor="")


def test_import_preflight_and_export_review_rows():
    source = workbook_bytes(valid_rows())
    imported = import_mapping_workbook(source, "001", 1405)
    assert len(imported) == 1 and imported[0].mapping_id == "M001"
    with pytest.raises(MappingWorkflowError, match="foreign"):
        import_mapping_workbook(source, "002", 1405)
    with pytest.raises(MappingWorkflowError, match="preflight"):
        import_mapping_workbook(b"invalid", "001", 1405)
    exported = export_mapping_rows(imported)
    book = load_workbook(BytesIO(exported), read_only=True)
    try:
        assert book["Mapping"]["A2"].value == "M001"
        assert book["Mapping"]["C2"].value == 1405
    finally:
        book.close()


def test_unknown_queue_only_excludes_approved_and_is_sorted():
    from aram_backend.mapping_workflow import unknown_account_queue
    draft = sample()
    approved = replace(sample(), status="Approved")
    accounts = [("001", 1405, "0020"), ("001", 1405, "0010"),
                ("001", 1405, "0020"), ("001", 1405, "0030")]
    queue = unknown_account_queue(accounts, [draft], company_code="001", fiscal_year=1405)
    assert [item.account_full_code for item in queue] == ["0010", "0020", "0030"]
    queue = unknown_account_queue(accounts, [approved], company_code="001", fiscal_year=1405)
    assert [item.account_full_code for item in queue] == ["0020", "0030"]


def test_unknown_queue_rejects_foreign_scope():
    from aram_backend.mapping_workflow import unknown_account_queue
    with pytest.raises(MappingWorkflowError, match="foreign account"):
        unknown_account_queue([("002", 1405, "0010")], [],
                              company_code="001", fiscal_year=1405)
    with pytest.raises(MappingWorkflowError, match="foreign mapping"):
        unknown_account_queue([], [sample(company="002")],
                              company_code="001", fiscal_year=1405)


def test_maker_cannot_review_own_mapping():
    space = MappingWorkspace("001", 1405)
    space.propose(sample(), actor="maker")
    with pytest.raises(MappingWorkflowError, match="maker"):
        space.transition("M001", "Reviewed", actor="maker")
    assert len(space.audit) == 1


def test_maker_cannot_approve_own_mapping_even_after_independent_review():
    space = MappingWorkspace("001", 1405)
    space.propose(sample(), actor="maker")
    space.transition("M001", "Reviewed", actor="reviewer")
    with pytest.raises(MappingWorkflowError, match="independent"):
        space.transition("M001", "Approved", actor="maker")
    assert space.decisions[0].status == "Reviewed"
    assert len(space.audit) == 2
