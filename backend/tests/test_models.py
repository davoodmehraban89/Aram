import pytest
from sqlalchemy.exc import IntegrityError

from aram_backend.models import (
    AccountVersion,
    Company,
    FinancialStatement,
    FiscalYear,
    FiscalYearStatus,
    MappingRule,
    NoteDefinition,
    NoteRow,
    SourceDocument,
    StatementLine,
    StatementType,
)


def make_year(session, year=1404):
    company = Company(code=f"CO-{year}", name="Test Company")
    fiscal_year = FiscalYear(company=company, year=year)
    session.add(company)
    session.commit()
    return fiscal_year


def test_model_relationships(session):
    year = make_year(session)
    note = NoteDefinition(year_id=year.id, note_number="10", title="Assets", version=1)
    note.rows.append(NoteRow(row_order=0, label="Tangible assets"))
    statement = FinancialStatement(year_id=year.id, statement_type=StatementType.BALANCE_SHEET)
    statement.lines.append(StatementLine(line_order=0, line_label="Assets", target_note=note))
    session.add_all([note, statement])
    session.commit()
    assert note.rows[0].note_id == note.id
    assert statement.lines[0].target_note_id == note.id


def test_version_uniqueness(session):
    year = make_year(session)
    session.add(AccountVersion(year_id=year.id, account_code="1000", account_name="Cash", version=1))
    session.commit()
    session.add(AccountVersion(year_id=year.id, account_code="1000", account_name="Cash duplicate", version=1))
    with pytest.raises(IntegrityError):
        session.commit()


def test_source_document_hash_unique_within_year(session):
    year = make_year(session)
    session.add(SourceDocument(year_id=year.id, filename="a.xlsx", file_hash="abc", document_type="ledger"))
    session.commit()
    session.add(SourceDocument(year_id=year.id, filename="b.xlsx", file_hash="abc", document_type="ledger"))
    with pytest.raises(IntegrityError):
        session.commit()


def test_fiscal_year_isolation_for_mapping(session):
    first = make_year(session, 1403)
    second = make_year(session, 1404)
    note = NoteDefinition(year_id=first.id, note_number="10", title="Assets")
    session.add(note)
    session.commit()
    session.add(MappingRule(
        year_id=second.id, rule_key="rule-1", account_code="1000",
        target_note=note, mapping_type="O"
    ))
    with pytest.raises(ValueError, match="same fiscal year"):
        session.commit()


def test_fiscal_year_isolation_cannot_be_bypassed_with_raw_ids(session):
    first = make_year(session, 1403)
    second = make_year(session, 1404)
    note = NoteDefinition(year_id=first.id, note_number="10", title="Assets")
    session.add(note)
    session.commit()
    session.add(MappingRule(
        year_id=second.id, rule_key="raw-id-rule", account_code="1000",
        target_note_id=note.id, mapping_type="O"
    ))
    with pytest.raises(ValueError, match="same fiscal year"):
        session.commit()


def test_statement_line_isolation_cannot_be_bypassed_with_raw_ids(session):
    first = make_year(session, 1403)
    second = make_year(session, 1404)
    note = NoteDefinition(year_id=first.id, note_number="10", title="Assets")
    statement = FinancialStatement(
        year_id=second.id, statement_type=StatementType.BALANCE_SHEET
    )
    session.add_all([note, statement])
    session.commit()
    session.add(StatementLine(
        statement_id=statement.id, line_order=0, line_label="Assets",
        target_note_id=note.id
    ))
    with pytest.raises(ValueError, match="same fiscal year"):
        session.commit()


def test_locked_year_blocks_mutation(session):
    year = make_year(session)
    year.status = FiscalYearStatus.APPROVED
    session.commit()
    year.status = FiscalYearStatus.LOCKED
    session.commit()
    session.add(AccountVersion(year_id=year.id, account_code="1000", account_name="Cash"))
    with pytest.raises(ValueError, match="locked"):
        session.commit()


def test_locked_year_protection_cannot_be_bypassed_with_raw_parent_id(session):
    year = make_year(session)
    statement = FinancialStatement(
        year_id=year.id, statement_type=StatementType.BALANCE_SHEET
    )
    session.add(statement)
    session.commit()
    year.status = FiscalYearStatus.APPROVED
    session.commit()
    year.status = FiscalYearStatus.LOCKED
    session.commit()
    session.add(StatementLine(
        statement_id=statement.id, line_order=0, line_label="Blocked"
    ))
    with pytest.raises(ValueError, match="locked"):
        session.commit()


def test_approved_year_blocks_silent_overwrite(session):
    year = make_year(session)
    account = AccountVersion(
        year_id=year.id, account_code="1000", account_name="Cash"
    )
    session.add(account)
    session.commit()
    year.status = FiscalYearStatus.APPROVED
    session.commit()
    account.account_name = "Silently changed cash"
    with pytest.raises(ValueError, match="approved"):
        session.commit()


def test_locked_year_cannot_be_reopened(session):
    year = make_year(session)
    year.status = FiscalYearStatus.APPROVED
    session.commit()
    year.status = FiscalYearStatus.LOCKED
    session.commit()
    year.status = FiscalYearStatus.DRAFT
    with pytest.raises(ValueError, match="Invalid fiscal-year transition"):
        session.commit()


def test_invalid_status_skip_is_rejected(session):
    year = make_year(session)
    year.status = FiscalYearStatus.LOCKED
    with pytest.raises(ValueError, match="Invalid fiscal-year transition"):
        session.commit()


# These adversarial cases reproduce the V1 audit bypasses; keep them as release gates.
@pytest.mark.parametrize("status", [FiscalYearStatus.APPROVED, FiscalYearStatus.LOCKED])
def test_protected_year_identity_cannot_be_mutated(session, status):
    year = make_year(session)
    year.status = FiscalYearStatus.APPROVED
    session.commit()
    if status is FiscalYearStatus.LOCKED:
        year.status = FiscalYearStatus.LOCKED
        session.commit()

    year.year = 1405
    with pytest.raises(ValueError, match="identity cannot be mutated"):
        session.commit()


@pytest.mark.parametrize("status", [FiscalYearStatus.APPROVED, FiscalYearStatus.LOCKED])
def test_protected_year_cannot_be_deleted(session, status):
    year = make_year(session)
    year.status = FiscalYearStatus.APPROVED
    session.commit()
    if status is FiscalYearStatus.LOCKED:
        year.status = FiscalYearStatus.LOCKED
        session.commit()

    session.delete(year)
    with pytest.raises(ValueError, match="cannot be deleted"):
        session.commit()


def test_company_with_protected_year_cannot_be_mutated(session):
    year = make_year(session)
    year.status = FiscalYearStatus.APPROVED
    session.commit()

    year.company.name = "Changed after approval"
    with pytest.raises(ValueError, match="cannot be mutated"):
        session.commit()


def test_company_with_protected_year_cannot_be_deleted(session):
    year = make_year(session)
    year.status = FiscalYearStatus.APPROVED
    session.commit()

    session.delete(year.company)
    with pytest.raises(ValueError, match="cannot be deleted"):
        session.commit()


def test_protected_year_cannot_be_reparented_through_relationship(session):
    year = make_year(session)
    replacement = Company(code="REPLACEMENT", name="Replacement Company")
    session.add(replacement)
    session.commit()
    year.status = FiscalYearStatus.APPROVED
    session.commit()

    year.company = replacement
    with pytest.raises(ValueError, match="cannot be mutated"):
        session.commit()


def test_draft_year_identity_and_deletion_remain_mutable(session):
    year = make_year(session)
    year.year = 1405
    session.commit()
    assert year.year == 1405

    session.delete(year)
    session.commit()
    assert session.get(FiscalYear, year.id) is None


@pytest.mark.parametrize("status", [FiscalYearStatus.APPROVED, FiscalYearStatus.LOCKED])
@pytest.mark.parametrize("expire_owner", [False, True])
@pytest.mark.parametrize("record_kind", ["account", "source", "note", "statement"])
def test_record_cannot_leave_protected_year(session, status, expire_owner, record_kind):
    original = make_year(session, 1403)
    destination = make_year(session, 1404)
    records = {
        "account": lambda: AccountVersion(
            year_id=original.id, account_code="1000", account_name="Cash"
        ),
        "source": lambda: SourceDocument(
            year_id=original.id, filename="synthetic.csv", file_hash="synthetic",
            document_type="general_ledger",
        ),
        "note": lambda: NoteDefinition(
            year_id=original.id, note_number="10", title="Assets"
        ),
        "statement": lambda: FinancialStatement(
            year_id=original.id, statement_type=StatementType.BALANCE_SHEET
        ),
    }
    record = records[record_kind]()
    session.add(record)
    session.commit()
    original.status = FiscalYearStatus.APPROVED
    session.commit()
    if status is FiscalYearStatus.LOCKED:
        original.status = FiscalYearStatus.LOCKED
        session.commit()
    record_id, original_id = record.id, original.id
    if expire_owner:
        session.expire(record, ["year_id"])

    record.year_id = destination.id
    with pytest.raises(ValueError, match="cannot be mutated"):
        session.commit()
    session.rollback()
    session.expire_all()
    assert session.get(type(record), record_id).year_id == original_id


@pytest.mark.parametrize("status", [FiscalYearStatus.APPROVED, FiscalYearStatus.LOCKED])
def test_mapping_cannot_leave_protected_year_with_new_target(session, status):
    original = make_year(session, 1403)
    destination = make_year(session, 1404)
    original_note = NoteDefinition(year_id=original.id, note_number="10", title="Old")
    new_note = NoteDefinition(year_id=destination.id, note_number="10", title="New")
    session.add_all([original_note, new_note])
    session.commit()
    rule = MappingRule(
        year_id=original.id, rule_key="cash", account_code="1000",
        mapping_type="O", target_note=original_note,
    )
    session.add(rule)
    session.commit()
    original.status = FiscalYearStatus.APPROVED
    session.commit()
    if status is FiscalYearStatus.LOCKED:
        original.status = FiscalYearStatus.LOCKED
        session.commit()
    original_id, rule_id, note_id = original.id, rule.id, original_note.id

    rule.year_id = destination.id
    rule.target_note = new_note
    with pytest.raises(ValueError, match="cannot be mutated"):
        session.commit()
    session.rollback()
    session.expire_all()
    stored = session.get(MappingRule, rule_id)
    assert (stored.year_id, stored.target_note_id) == (original_id, note_id)


@pytest.mark.parametrize("status", [FiscalYearStatus.APPROVED, FiscalYearStatus.LOCKED])
@pytest.mark.parametrize("child_kind", ["note_row", "statement_line"])
@pytest.mark.parametrize("assignment", ["foreign_key", "relationship"])
def test_child_cannot_leave_protected_parent(session, status, child_kind, assignment):
    original = make_year(session, 1403)
    destination = make_year(session, 1404)
    if child_kind == "note_row":
        old_parent = NoteDefinition(year_id=original.id, note_number="10", title="Old")
        new_parent = NoteDefinition(year_id=destination.id, note_number="10", title="New")
        child = NoteRow(note=old_parent, row_order=0, label="Cash")
        foreign_key, relationship = "note_id", "note"
    else:
        old_parent = FinancialStatement(
            year_id=original.id, statement_type=StatementType.BALANCE_SHEET
        )
        new_parent = FinancialStatement(
            year_id=destination.id, statement_type=StatementType.BALANCE_SHEET
        )
        child = StatementLine(statement=old_parent, line_order=0, line_label="Cash")
        foreign_key, relationship = "statement_id", "statement"
    session.add_all([old_parent, new_parent, child])
    session.commit()
    original.status = FiscalYearStatus.APPROVED
    session.commit()
    if status is FiscalYearStatus.LOCKED:
        original.status = FiscalYearStatus.LOCKED
        session.commit()
    child_id, parent_id = child.id, old_parent.id
    if assignment == "foreign_key":
        session.expire(child, [relationship])
        setattr(child, foreign_key, new_parent.id)
    else:
        setattr(child, relationship, new_parent)

    with pytest.raises(ValueError, match="cannot be mutated"):
        session.commit()
    session.rollback()
    session.expire_all()
    assert getattr(session.get(type(child), child_id), foreign_key) == parent_id


def test_draft_account_edits_and_owner_change_remain_allowed(session):
    original = make_year(session, 1403)
    destination = make_year(session, 1404)
    account = AccountVersion(year_id=original.id, account_code="1000", account_name="Cash")
    session.add(account)
    session.commit()

    account.year_id = destination.id
    account.account_name = "Reviewed cash"
    session.commit()
    session.expire_all()
    stored = session.get(AccountVersion, account.id)
    assert (stored.year_id, stored.account_name) == (destination.id, "Reviewed cash")


@pytest.mark.parametrize("same_company", [False, True])
def test_relationship_only_statement_note_cannot_cross_year(session, same_company):
    first = make_year(session, 1403)
    if same_company:
        second = FiscalYear(company=first.company, year=1404)
        session.add(second)
        session.commit()
    else:
        second = make_year(session, 1404)
    note = NoteDefinition(year_id=first.id, note_number="10", title="Assets")
    statement = FinancialStatement(
        year_id=second.id, statement_type=StatementType.BALANCE_SHEET
    )
    session.add_all([note, statement])
    session.commit()
    statement_id = statement.id
    session.add(StatementLine(
        statement=statement, target_note=note, line_order=0, line_label="Assets"
    ))

    with pytest.raises(ValueError, match="same fiscal year"):
        session.commit()
    session.rollback()
    session.expire_all()
    assert session.get(FinancialStatement, statement_id).lines == []


@pytest.mark.parametrize("record_kind", ["mapping", "statement_line"])
def test_cached_note_cannot_hide_cross_year_foreign_key_change(session, record_kind):
    first = make_year(session, 1403)
    second = make_year(session, 1404)
    old_note = NoteDefinition(year_id=first.id, note_number="10", title="Old")
    new_note = NoteDefinition(year_id=second.id, note_number="10", title="New")
    statement = FinancialStatement(
        year_id=first.id, statement_type=StatementType.BALANCE_SHEET
    )
    session.add_all([old_note, new_note, statement])
    session.commit()
    if record_kind == "mapping":
        record = MappingRule(
            year_id=first.id, rule_key="cash", account_code="1000",
            target_note=old_note, mapping_type="O",
        )
    else:
        record = StatementLine(
            statement=statement, target_note=old_note, line_order=0, line_label="Cash"
        )
    session.add(record)
    session.commit()
    assert record.target_note is old_note
    record_id, old_note_id = record.id, old_note.id

    record.target_note_id = new_note.id
    with pytest.raises(ValueError, match="same fiscal year"):
        session.commit()
    session.rollback()
    session.expire_all()
    assert session.get(type(record), record_id).target_note_id == old_note_id


def test_cached_statement_cannot_hide_move_into_locked_year(session):
    first = make_year(session, 1403)
    second = make_year(session, 1404)
    old_statement = FinancialStatement(
        year_id=first.id, statement_type=StatementType.BALANCE_SHEET
    )
    new_statement = FinancialStatement(
        year_id=second.id, statement_type=StatementType.BALANCE_SHEET
    )
    line = StatementLine(statement=old_statement, line_order=0, line_label="Cash")
    session.add_all([old_statement, new_statement, line])
    session.commit()
    second.status = FiscalYearStatus.APPROVED
    session.commit()
    second.status = FiscalYearStatus.LOCKED
    session.commit()
    assert line.statement is old_statement
    line_id, original_id = line.id, old_statement.id

    line.statement_id = new_statement.id
    with pytest.raises(ValueError, match="cannot be mutated"):
        session.commit()
    session.rollback()
    session.expire_all()
    assert session.get(StatementLine, line_id).statement_id == original_id


@pytest.mark.parametrize("record_kind", ["mapping", "statement_line"])
def test_conflicting_target_relationship_and_foreign_key_are_rejected(session, record_kind):
    year = make_year(session)
    first_note = NoteDefinition(year_id=year.id, note_number="10", title="First")
    second_note = NoteDefinition(year_id=year.id, note_number="11", title="Second")
    statement = FinancialStatement(
        year_id=year.id, statement_type=StatementType.BALANCE_SHEET
    )
    session.add_all([first_note, second_note, statement])
    session.commit()
    if record_kind == "mapping":
        record = MappingRule(
            year_id=year.id, rule_key="cash", account_code="1000", mapping_type="O",
            target_note=first_note, target_note_id=second_note.id,
        )
    else:
        record = StatementLine(
            statement=statement, line_order=0, line_label="Cash",
            target_note=first_note, target_note_id=second_note.id,
        )
    session.add(record)

    with pytest.raises(ValueError, match="Conflicting"):
        session.commit()
    session.rollback()


def test_statement_allows_same_year_relationship_and_optional_note(session):
    year = make_year(session)
    note = NoteDefinition(year_id=year.id, note_number="10", title="Assets")
    statement = FinancialStatement(
        year_id=year.id, statement_type=StatementType.BALANCE_SHEET
    )
    linked = StatementLine(
        statement=statement, target_note=note, line_order=0, line_label="Cash"
    )
    unlinked = StatementLine(statement=statement, line_order=1, line_label="Subtotal")
    session.add_all([note, statement, linked, unlinked])
    session.commit()
    note_id, linked_id, unlinked_id = note.id, linked.id, unlinked.id
    session.expire_all()
    assert session.get(StatementLine, linked_id).target_note_id == note_id
    assert session.get(StatementLine, unlinked_id).target_note_id is None

    session.get(StatementLine, linked_id).target_note = None
    session.commit()
    session.expire_all()
    assert session.get(StatementLine, linked_id).target_note_id is None


@pytest.mark.parametrize("pending_parent", ["note", "statement", "both"])
@pytest.mark.parametrize("same_year", [False, True])
def test_direct_fk_resolves_pending_explicit_id_parents(session, pending_parent, same_year):
    first = make_year(session, 1403)
    second = make_year(session, 1404)
    note = NoteDefinition(
        id=900, year_id=first.id if same_year else second.id,
        note_number="10", title="Synthetic note",
    )
    statement = FinancialStatement(
        id=901, year_id=first.id, statement_type=StatementType.BALANCE_SHEET
    )
    if pending_parent == "note":
        session.add(statement)
        session.commit()
    elif pending_parent == "statement":
        session.add(note)
        session.commit()
    line = StatementLine(
        statement_id=901, target_note_id=900, line_order=0, line_label="Synthetic"
    )
    session.add_all([note, statement, line])
    if same_year:
        session.commit()
        line_id = line.id
        session.expire_all()
        stored = session.get(StatementLine, line_id)
        assert stored.statement.year_id == first.id
        assert stored.target_note.year_id == first.id
    else:
        with pytest.raises(ValueError, match="same fiscal year"):
            session.commit()
        session.rollback()
        session.expire_all()
        assert session.query(StatementLine).count() == 0


@pytest.mark.parametrize("same_year", [False, True])
def test_mapping_direct_fk_resolves_pending_note(session, same_year):
    first = make_year(session, 1403)
    second = make_year(session, 1404)
    note = NoteDefinition(
        id=900, year_id=first.id if same_year else second.id,
        note_number="10", title="Synthetic note",
    )
    mapping = MappingRule(
        year_id=first.id, rule_key="synthetic", account_code="1000",
        target_note_id=900, mapping_type="O",
    )
    session.add_all([note, mapping])
    if same_year:
        session.commit()
        rule_id = mapping.id
        session.expire_all()
        stored = session.get(MappingRule, rule_id)
        assert stored.target_note.year_id == stored.year_id == first.id
    else:
        with pytest.raises(ValueError, match="same fiscal year"):
            session.commit()
        session.rollback()
        assert session.query(MappingRule).count() == 0


# Same-flush approval must atomically freeze the entire fiscal-year aggregate.
# Prior to this regression, checking only persisted FiscalYear.status returned DRAFT
# while a pending APPROVED transition was in the same SQLAlchemy flush.
@pytest.mark.parametrize("record_kind", [
    "account", "source", "note", "statement", "mapping", "note_row", "statement_line",
])
def test_approval_and_existing_year_record_edit_in_one_flush_are_rejected(session, record_kind):
    year = make_year(session, 1403)
    note = NoteDefinition(year_id=year.id, note_number="10", title="Existing note")
    statement = FinancialStatement(
        year_id=year.id, statement_type=StatementType.BALANCE_SHEET
    )
    account = AccountVersion(
        year_id=year.id, account_code="1000", account_name="Existing account"
    )
    source = SourceDocument(
        year_id=year.id, filename="synthetic.xlsx",
        file_hash="synthetic-sha", document_type="general_ledger",
    )
    mapping = MappingRule(
        year_id=year.id, rule_key="existing", account_code="1000",
        target_note=note, mapping_type="O",
    )
    note_row = NoteRow(note=note, row_order=0, label="Existing row")
    statement_line = StatementLine(
        statement=statement, target_note=note,
        line_order=0, line_label="Existing statement row",
    )
    session.add_all([
        note, statement, account, source, mapping, note_row, statement_line
    ])
    session.commit()
    records = {
        "account": (account, "account_name"),
        "source": (source, "filename"),
        "note": (note, "title"),
        "statement": (statement, "version"),
        "mapping": (mapping, "rule_key"),
        "note_row": (note_row, "label"),
        "statement_line": (statement_line, "line_label"),
    }
    record, field = records[record_kind]
    original = getattr(record, field)
    year_id = year.id
    record_id = record.id
    year.status = FiscalYearStatus.APPROVED
    setattr(record, field, original + "-edited" if isinstance(original, str) else original + 1)

    with pytest.raises(ValueError, match="cannot be mutated"):
        session.commit()
    session.rollback()
    session.expire_all()
    assert session.get(FiscalYear, year_id).status is FiscalYearStatus.DRAFT
    assert getattr(session.get(type(record), record_id), field) == original


def test_approval_and_new_source_registration_in_one_flush_are_rejected(session):
    year = make_year(session, 1403)
    year_id = year.id
    year.status = FiscalYearStatus.APPROVED
    session.add(SourceDocument(
        year_id=year_id, filename="new.xlsx", file_hash="synthetic-new",
        document_type="general_ledger",
    ))

    with pytest.raises(ValueError, match="cannot be mutated"):
        session.commit()
    session.rollback()
    session.expire_all()
    assert session.get(FiscalYear, year_id).status is FiscalYearStatus.DRAFT
    assert session.query(SourceDocument).filter_by(year_id=year_id).count() == 0


def test_approval_and_company_edit_in_one_flush_are_rejected(session):
    year = make_year(session, 1403)
    company_id = year.company_id
    original = year.company.name
    year_id = year.id
    year.status = FiscalYearStatus.APPROVED
    year.company.name = "Company changed during approval"

    with pytest.raises(ValueError, match="cannot be mutated"):
        session.commit()
    session.rollback()
    session.expire_all()
    assert session.get(FiscalYear, year_id).status is FiscalYearStatus.DRAFT
    assert session.get(Company, company_id).name == original


def test_draft_edit_committed_before_approval_is_still_allowed(session):
    year = make_year(session, 1403)
    account = AccountVersion(
        year_id=year.id, account_code="1000", account_name="Initial"
    )
    session.add(account)
    session.commit()
    account.account_name = "Validated"
    session.commit()
    year.status = FiscalYearStatus.APPROVED
    session.commit()
    session.expire_all()
    assert session.get(AccountVersion, account.id).account_name == "Validated"
    assert session.get(FiscalYear, year.id).status is FiscalYearStatus.APPROVED


# A parent's fiscal-year movement must not silently invalidate rows that
# were not themselves dirty and therefore escaped the ORM before_flush loop.
@pytest.mark.parametrize("same_company", [False, True])
@pytest.mark.parametrize("ref_kind", ["mapping", "statement_line"])
def test_draft_note_move_rejects_clean_cross_year_references(session, same_company, ref_kind):
    first = make_year(session, 1403)
    if same_company:
        second = FiscalYear(company=first.company, year=1404)
        session.add(second)
        session.commit()
    else:
        second = make_year(session, 1404)
    note = NoteDefinition(year_id=first.id, note_number="10", title="Synthetic note")
    if ref_kind == "mapping":
        dependent = MappingRule(
            year_id=first.id, rule_key="cash", account_code="1000",
            mapping_type="O", target_note=note,
        )
    else:
        statement = FinancialStatement(
            year_id=first.id, statement_type=StatementType.BALANCE_SHEET,
        )
        dependent = StatementLine(
            statement=statement, target_note=note,
            line_order=0, line_label="Linked assets",
        )
        session.add(statement)
    session.add_all([note, dependent])
    session.commit()
    original_year_id, note_id, dependent_id = first.id, note.id, dependent.id

    note.year_id = second.id
    with pytest.raises(ValueError, match="same fiscal year"):
        session.commit()
    session.rollback()
    session.expire_all()
    assert session.get(NoteDefinition, note_id).year_id == original_year_id
    assert session.get(type(dependent), dependent_id) is not None


@pytest.mark.parametrize("same_company", [False, True])
def test_draft_statement_move_rejects_clean_note_link(session, same_company):
    first = make_year(session, 1403)
    if same_company:
        second = FiscalYear(company=first.company, year=1404)
        session.add(second)
        session.commit()
    else:
        second = make_year(session, 1404)
    note = NoteDefinition(year_id=first.id, note_number="10", title="Existing note")
    statement = FinancialStatement(
        year_id=first.id, statement_type=StatementType.BALANCE_SHEET,
    )
    line = StatementLine(
        statement=statement, target_note=note,
        line_order=0, line_label="Assets",
    )
    session.add_all([note, statement, line])
    session.commit()
    original_id, statement_id, line_id = first.id, statement.id, line.id

    statement.year_id = second.id
    with pytest.raises(ValueError, match="same fiscal year"):
        session.commit()
    session.rollback()
    session.expire_all()
    assert session.get(FinancialStatement, statement_id).year_id == original_id
    assert session.get(StatementLine, line_id).statement_id == statement_id


def test_unreferenced_draft_parents_can_change_year(session):
    first = make_year(session, 1403)
    second = make_year(session, 1404)
    note = NoteDefinition(year_id=first.id, note_number="10", title="Free note")
    statement = FinancialStatement(
        year_id=first.id, statement_type=StatementType.BALANCE_SHEET,
    )
    session.add_all([note, statement])
    session.commit()
    note.year_id = second.id
    statement.year_id = second.id
    session.commit()
    session.expire_all()
    assert session.get(NoteDefinition, note.id).year_id == second.id
    assert session.get(FinancialStatement, statement.id).year_id == second.id


def test_draft_note_move_and_mapping_owner_move_in_one_flush(session):
    first = make_year(session, 1403)
    second = make_year(session, 1404)
    note = NoteDefinition(year_id=first.id, note_number="10", title="Synthetic note")
    mapping = MappingRule(
        year_id=first.id, rule_key="cash", account_code="1000",
        mapping_type="O", target_note=note,
    )
    session.add_all([note, mapping])
    session.commit()
    note.year_id = second.id
    mapping.year_id = second.id
    session.commit()
    session.expire_all()
    assert session.get(NoteDefinition, note.id).year_id == second.id
    assert session.get(MappingRule, mapping.id).year_id == second.id


def test_draft_statement_move_with_clean_unlinked_line_is_allowed(session):
    first = make_year(session, 1403)
    second = make_year(session, 1404)
    statement = FinancialStatement(
        year_id=first.id, statement_type=StatementType.BALANCE_SHEET,
    )
    line = StatementLine(statement=statement, line_order=0, line_label="Subtotal")
    session.add_all([statement, line])
    session.commit()

    statement.year_id = second.id
    session.commit()
    session.expire_all()
    assert session.get(FinancialStatement, statement.id).year_id == second.id
    assert session.get(StatementLine, line.id).target_note_id is None
