"""Server-side mapping authorization boundary.

The identity resolver MUST verify the request against an external identity
provider; never accept a user-supplied username as authenticated identity.
"""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Literal

from aram_backend.mapping_workflow import (
    MappingDecision,
    MappingWorkflowError,
    MappingWorkspace,
)

Role = Literal["maker", "reviewer", "approver"]


@dataclass(frozen=True)
class AuthenticatedPrincipal:
    subject: str
    company_scopes: frozenset[str]
    roles: frozenset[Role]


class MappingAccess:
    """Fail-closed role/scope checks; resolver is a trusted server dependency."""

    def __init__(self, resolve_identity: Callable[[str], AuthenticatedPrincipal | None]):
        self._resolve = resolve_identity

    def _authorize(self, credential: str, workspace: MappingWorkspace, role: Role) -> str:
        if not isinstance(credential, str) or not credential:
            raise MappingWorkflowError("authenticated credential required")
        principal = self._resolve(credential)
        if (principal is None or not isinstance(principal, AuthenticatedPrincipal)
                or not principal.subject.strip()
                or workspace.company_code not in principal.company_scopes
                or role not in principal.roles):
            raise MappingWorkflowError("mapping access denied")
        return principal.subject

    def propose(self, credential: str, workspace: MappingWorkspace,
                decision: MappingDecision) -> MappingDecision:
        actor = self._authorize(credential, workspace, "maker")
        return workspace.propose(decision, actor=actor)

    def review(self, credential: str, workspace: MappingWorkspace,
               mapping_id: str) -> MappingDecision:
        actor = self._authorize(credential, workspace, "reviewer")
        return workspace.transition(mapping_id, "Reviewed", actor=actor)

    def approve(self, credential: str, workspace: MappingWorkspace,
                mapping_id: str) -> MappingDecision:
        actor = self._authorize(credential, workspace, "approver")
        return workspace.transition(mapping_id, "Approved", actor=actor)

    def revise(self, credential: str, workspace: MappingWorkspace, mapping_id: str,
               *, target_statement: str, statement_section: str, note_number: str,
               subnote_code: str | None) -> MappingDecision:
        actor = self._authorize(credential, workspace, "maker")
        return workspace.revise(mapping_id, actor=actor, target_statement=target_statement,
                                statement_section=statement_section, note_number=note_number,
                                subnote_code=subnote_code)

    def carry_forward(self, credential: str, workspace: MappingWorkspace,
                      previous: tuple[MappingDecision, ...]) -> int:
        actor = self._authorize(credential, workspace, "maker")
        return workspace.carry_forward(previous, actor=actor)
