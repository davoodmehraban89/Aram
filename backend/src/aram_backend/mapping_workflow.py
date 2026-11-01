"""Governed, isolated mapping decisions for a single company and fiscal year.

No approval is inferred from an imported workbook. All transitions are explicit
and append-only audit entries; caller owns durable storage and transactionality.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime, timezone
from io import BytesIO
from typing import Iterable

from openpyxl import Workbook, load_workbook

from aram_backend.pilot_workbook import SHEET_HEADERS, preflight_pilot_workbook


class MappingWorkflowError(ValueError):
    pass


@dataclass(frozen=True)
class MappingDecision:
    mapping_id: str
    company_code: str
    fiscal_year: int
    account_full_code: str
    target_statement: str
    statement_section: str
    note_number: str
    subnote_code: str | None
    version: int
    status: str
    reviewer: str | None
    source: str


@dataclass(frozen=True)
class MappingAuditEvent:
    mapping_id: str
    company_code: str
    fiscal_year: int
    previous_status: str | None
    new_status: str
    actor: str
    timestamp: str
    previous_version: int | None
    new_version: int


class MappingWorkspace:
    """In-memory transaction boundary; never crosses the selected company/year."""

    def __init__(self, company_code: str, fiscal_year: int):
        if not isinstance(company_code, str) or not company_code.strip():
            raise MappingWorkflowError("company_code is required")
        if isinstance(fiscal_year, bool) or not isinstance(fiscal_year, int) or fiscal_year <= 0:
            raise MappingWorkflowError("fiscal_year must be a positive integer")
        self.company_code = company_code.strip()
        self.fiscal_year = fiscal_year
        self._decisions: dict[str, MappingDecision] = {}
        self._audit: list[MappingAuditEvent] = []

    @property
    def decisions(self) -> tuple[MappingDecision, ...]:
        return tuple(self._decisions[key] for key in sorted(self._decisions))

    @property
    def audit(self) -> tuple[MappingAuditEvent, ...]:
        return tuple(self._audit)

    def _check_scope(self, decision: MappingDecision) -> None:
        if (decision.company_code, decision.fiscal_year) != (self.company_code, self.fiscal_year):
            raise MappingWorkflowError("company/year isolation violation")

    def _record(self, old: MappingDecision | None, new: MappingDecision, actor: str) -> None:
        self._decisions[new.mapping_id] = new
        self._audit.append(MappingAuditEvent(
            new.mapping_id, new.company_code, new.fiscal_year,
            old.status if old else None, new.status, actor,
            datetime.now(timezone.utc).isoformat(),
            old.version if old else None, new.version,
        ))

    def propose(self, decision: MappingDecision, *, actor: str) -> MappingDecision:
        self._check_scope(decision)
        if not actor.strip() or not decision.mapping_id.strip() or not decision.account_full_code.strip():
            raise MappingWorkflowError("actor, mapping_id and account are required")
        if decision.status != "Draft" or decision.version != 1 or decision.reviewer is not None:
            raise MappingWorkflowError("new decisions must begin as unreviewed Draft v1")
        if decision.mapping_id in self._decisions:
            raise MappingWorkflowError("mapping_id already exists; use revise")
        if not decision.note_number or not decision.target_statement or not decision.statement_section:
            raise MappingWorkflowError("target statement, section and note are required")
        self._record(None, decision, actor)
        return decision

    def transition(self, mapping_id: str, status: str, *, actor: str) -> MappingDecision:
        old = self._decisions.get(mapping_id)
        if old is None:
            raise MappingWorkflowError("unknown mapping_id")
        allowed = {"Draft": "Reviewed", "Reviewed": "Approved"}
        if allowed.get(old.status) != status:
            raise MappingWorkflowError("invalid mapping lifecycle transition")
        if not actor.strip():
            raise MappingWorkflowError("reviewer identity required")
        if status == "Approved" and actor == old.reviewer:
            raise MappingWorkflowError("approval requires independent reviewer")
        new = replace(old, status=status, reviewer=actor, version=old.version + 1)
        self._record(old, new, actor)
        return new

    def revise(self, mapping_id: str, *, actor: str, target_statement: str,
               statement_section: str, note_number: str, subnote_code: str | None) -> MappingDecision:
        old = self._decisions.get(mapping_id)
        if old is None:
            raise MappingWorkflowError("unknown mapping_id")
        if not actor.strip() or not target_statement or not statement_section or not note_number:
            raise MappingWorkflowError("actor and complete target are required")
        new = replace(old, target_statement=target_statement,
                      statement_section=statement_section, note_number=note_number,
                      subnote_code=subnote_code, status="Draft", reviewer=None,
                      version=old.version + 1)
        self._record(old, new, actor)
        return new

    def carry_forward(self, previous: Iterable[MappingDecision], *, actor: str) -> int:
        if not actor.strip():
            raise MappingWorkflowError("actor required")
        candidates = tuple(previous)
        ids = [d.mapping_id for d in candidates]
        if len(ids) != len(set(ids)) or any(i in self._decisions for i in ids):
            raise MappingWorkflowError("duplicate carry-forward mapping_id")
        for d in candidates:
            if d.company_code != self.company_code or d.fiscal_year != self.fiscal_year - 1:
                raise MappingWorkflowError("carry-forward source company/year mismatch")
            if d.status != "Approved":
                raise MappingWorkflowError("only approved mappings may be carried forward")
        for d in candidates:
            self.propose(replace(d, fiscal_year=self.fiscal_year, status="Draft",
                                 reviewer=None, version=1, source="CarryForward"), actor=actor)
        return len(candidates)


def import_mapping_workbook(content: bytes, company_code: str, fiscal_year: int) -> tuple[MappingDecision, ...]:
    """Read only preflight-valid mapping rows; reject any out-of-scope rows."""
    report = preflight_pilot_workbook(content)
    if not report.valid:
        raise MappingWorkflowError(f"workbook preflight failed: {report.issues[0].code}")
    workbook = load_workbook(BytesIO(content), read_only=True, data_only=False)
    try:
        columns = SHEET_HEADERS["Mapping"]
        decisions: list[MappingDecision] = []
        for values in workbook["Mapping"].iter_rows(min_row=2, values_only=True):
            if not any(v is not None for v in values):
                continue
            row = dict(zip(columns, values))
            if (row["company_code"], row["fiscal_year"]) != (company_code, fiscal_year):
                raise MappingWorkflowError("import includes foreign company/year")
            decisions.append(MappingDecision(
                row["mapping_id"], row["company_code"], row["fiscal_year"],
                row["account_full_code"], row["target_statement"],
                row["statement_section"], row["note_number"], row["subnote_code"],
                row["mapping_version"], row["approval_status"], row["reviewer"], row["source"],
            ))
        return tuple(decisions)
    finally:
        workbook.close()


def export_mapping_rows(decisions: Iterable[MappingDecision]) -> bytes:
    """Export mapping decisions to a standalone review sheet (not an approved Pilot input)."""
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Mapping"
    columns = ("mapping_id", "company_code", "fiscal_year", "account_full_code",
               "target_statement", "statement_section", "note_number", "subnote_code",
               "mapping_version", "approval_status", "reviewer", "source")
    sheet.append(columns)
    for decision in decisions:
        sheet.append((decision.mapping_id, decision.company_code, decision.fiscal_year,
                      decision.account_full_code, decision.target_statement,
                      decision.statement_section, decision.note_number, decision.subnote_code,
                      decision.version, decision.status, decision.reviewer, decision.source))
    buffer = BytesIO()
    workbook.save(buffer)
    workbook.close()
    return buffer.getvalue()
