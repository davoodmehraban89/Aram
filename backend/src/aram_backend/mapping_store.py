"""Durable SQLite mapping store with serialized writes and optimistic concurrency."""
from __future__ import annotations

import json
import sqlite3
from contextlib import closing
from dataclasses import asdict
from pathlib import Path

from aram_backend.mapping_workflow import (
    MappingAuditEvent,
    MappingDecision,
    MappingWorkflowError,
    MappingWorkspace,
)


class MappingStore:
    def __init__(self, path: str | Path):
        self.path = str(path)
        if self.path == ":memory:":
            raise MappingWorkflowError("durable store requires a filesystem path")
        with closing(self._connect()) as db:
            db.execute("PRAGMA journal_mode=WAL")
            db.executescript("""
                CREATE TABLE IF NOT EXISTS mapping_state (
                    company TEXT NOT NULL, year INTEGER NOT NULL,
                    revision INTEGER NOT NULL, payload TEXT NOT NULL,
                    PRIMARY KEY(company, year)
                );
                CREATE TABLE IF NOT EXISTS mapping_audit (
                    sequence INTEGER PRIMARY KEY AUTOINCREMENT,
                    company TEXT NOT NULL, year INTEGER NOT NULL,
                    revision INTEGER NOT NULL, payload TEXT NOT NULL,
                    UNIQUE(company, year, revision)
                );
            """)

    def _connect(self):
        db = sqlite3.connect(self.path, timeout=15, isolation_level=None)
        db.execute("PRAGMA busy_timeout=15000")
        db.execute("PRAGMA synchronous=FULL")
        return db

    def load(self, company: str, year: int) -> tuple[MappingWorkspace, int]:
        workspace = MappingWorkspace(company, year)
        with closing(self._connect()) as db:
            row = db.execute(
                "SELECT revision, payload FROM mapping_state WHERE company=? AND year=?",
                (workspace.company_code, year),
            ).fetchone()
            if row is None:
                return workspace, 0
            revision, payload = row
            state = json.loads(payload)
            for item in state["decisions"]:
                decision = MappingDecision(**item)
                workspace._check_scope(decision)
                if decision.mapping_id in workspace._decisions:
                    raise MappingWorkflowError("duplicate persisted mapping")
                workspace._decisions[decision.mapping_id] = decision
            for item in state["audit"]:
                event = MappingAuditEvent(**item)
                if (event.company_code, event.fiscal_year) != (workspace.company_code, year):
                    raise MappingWorkflowError("foreign audit entry")
                workspace._audit.append(event)
            return workspace, revision

    def save(self, workspace: MappingWorkspace, expected_revision: int) -> int:
        if isinstance(expected_revision, bool) or not isinstance(expected_revision, int) or expected_revision < 0:
            raise MappingWorkflowError("invalid expected revision")
        for decision in workspace.decisions:
            workspace._check_scope(decision)
        for event in workspace.audit:
            if (event.company_code, event.fiscal_year) != (workspace.company_code, workspace.fiscal_year):
                raise MappingWorkflowError("foreign audit event")
        # Reject forged state and invalid audit sequences before starting a write.
        latest = {}
        for event in workspace.audit:
            prior = latest.get(event.mapping_id)
            if prior is None:
                valid = (event.previous_status is None and
                         event.previous_version is None and
                         event.new_status == "Draft" and event.new_version == 1)
            else:
                previous_status, previous_version = prior
                valid = (event.previous_status == previous_status and
                         event.previous_version == previous_version and
                         event.new_version == previous_version + 1 and
                         ((previous_status == "Draft" and event.new_status == "Reviewed") or
                          (previous_status == "Reviewed" and event.new_status == "Approved") or
                          event.new_status == "Draft"))
            if not valid or not event.actor.strip():
                raise MappingWorkflowError("invalid audit transition or version chain")
            latest[event.mapping_id] = (event.new_status, event.new_version)
        if {d.mapping_id: (d.status, d.version) for d in workspace.decisions} != latest:
            raise MappingWorkflowError("mapping state and audit history diverged")
        payload = json.dumps({
            "decisions": [asdict(item) for item in workspace.decisions],
            "audit": [asdict(item) for item in workspace.audit],
        }, ensure_ascii=False, sort_keys=True)
        db = self._connect()
        try:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute(
                "SELECT revision, payload FROM mapping_state WHERE company=? AND year=?",
                (workspace.company_code, workspace.fiscal_year),
            ).fetchone()
            current = row[0] if row else 0
            if current != expected_revision:
                raise MappingWorkflowError("concurrent update: stale revision")
            if row:
                previous = json.loads(row[1])
                old_events = previous["audit"]
                new_events = [asdict(e) for e in workspace.audit]
                if new_events[:len(old_events)] != old_events:
                    raise MappingWorkflowError("audit history must be append-only")
                if len(new_events) == len(old_events) and payload != row[1]:
                    raise MappingWorkflowError("state changed without audit event")
                appended = new_events[len(old_events):]
                if appended and not all(
                    event["mapping_id"] in {d.mapping_id for d in workspace.decisions}
                    for event in appended
                ):
                    raise MappingWorkflowError("audit event references unknown mapping")
            else:
                appended = [asdict(e) for e in workspace.audit]
                if workspace.decisions and not appended:
                    raise MappingWorkflowError("decisions require audit events")
            new_revision = current + 1
            db.execute(
                "INSERT INTO mapping_state(company,year,revision,payload) VALUES(?,?,?,?) "
                "ON CONFLICT(company,year) DO UPDATE SET revision=excluded.revision,payload=excluded.payload",
                (workspace.company_code, workspace.fiscal_year, new_revision, payload),
            )
            for index, event in enumerate(appended):
                db.execute(
                    "INSERT INTO mapping_audit(company,year,revision,payload) VALUES(?,?,?,?)",
                    (workspace.company_code, workspace.fiscal_year,
                     new_revision * 1000000 + index, json.dumps(event, ensure_ascii=False)),
                )
            db.commit()
            return new_revision
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

    def audit_log(self, company: str, year: int) -> tuple[MappingAuditEvent, ...]:
        with closing(self._connect()) as db:
            rows = db.execute(
                "SELECT payload FROM mapping_audit WHERE company=? AND year=? ORDER BY sequence",
                (company, year),
            ).fetchall()
        return tuple(MappingAuditEvent(**json.loads(row[0])) for row in rows)


    def verify_integrity(self) -> None:
        """Detect corruption and state/audit disagreement; not privileged tamper-proof."""
        with closing(self._connect()) as db:
            if db.execute("PRAGMA quick_check").fetchone()[0] != "ok":
                raise MappingWorkflowError("SQLite integrity check failed")
            rows = db.execute(
                "SELECT company, year, payload FROM mapping_state ORDER BY company, year"
            ).fetchall()
            for company, year, payload in rows:
                state = json.loads(payload)
                audit = [json.loads(r[0]) for r in db.execute(
                    "SELECT payload FROM mapping_audit WHERE company=? AND year=? ORDER BY sequence",
                    (company, year),
                )]
                if state["audit"] != audit:
                    raise MappingWorkflowError("persisted audit/state mismatch")
                workspace, _ = self.load(company, year)
                latest = {}
                for event in workspace.audit:
                    prior = latest.get(event.mapping_id)
                    if prior is None:
                        valid = (event.previous_status is None
                                 and event.previous_version is None
                                 and event.new_status == "Draft"
                                 and event.new_version == 1)
                    else:
                        valid = (event.previous_status == prior[0]
                                 and event.previous_version == prior[1]
                                 and event.new_version == prior[1] + 1
                                 and ((prior[0] == "Draft" and event.new_status == "Reviewed")
                                      or (prior[0] == "Reviewed" and event.new_status == "Approved")
                                      or event.new_status == "Draft"))
                    if not valid:
                        raise MappingWorkflowError("invalid persisted audit chain")
                    latest[event.mapping_id] = (event.new_status, event.new_version)
                if latest != {d.mapping_id: (d.status, d.version)
                              for d in workspace.decisions}:
                    raise MappingWorkflowError("persisted mapping state diverged")
            orphan = db.execute(
                "SELECT 1 FROM mapping_audit a WHERE NOT EXISTS "
                "(SELECT 1 FROM mapping_state s WHERE s.company=a.company AND s.year=a.year) "
                "LIMIT 1"
            ).fetchone()
            if orphan:
                raise MappingWorkflowError("orphan audit events")

    def backup_to(self, destination: str | Path) -> None:
        """Create consistent SQLite snapshot; never overwrite an existing backup."""
        target = Path(destination)
        if target.exists() or target.resolve() == Path(self.path).resolve():
            raise MappingWorkflowError("backup destination must be new and distinct")
        self.verify_integrity()
        try:
            with closing(self._connect()) as source, closing(sqlite3.connect(target)) as backup:
                source.backup(backup)
            MappingStore(target).verify_integrity()
        except Exception:
            target.unlink(missing_ok=True)
            raise
