
import pytest
from aram_backend.mapping_access import AuthenticatedPrincipal, MappingAccess
from aram_backend.mapping_workflow import (
    MappingDecision,
    MappingWorkflowError,
    MappingWorkspace,
)


def decision():
    return MappingDecision("M1", "001", 1405, "0010", "BS", "Assets",
                           "01", None, 1, "Draft", None, "Manual")


def test_authenticated_scoped_segregation_and_revisions():
    identities = {
        "token-maker": AuthenticatedPrincipal("maker", frozenset({"001"}), frozenset({"maker"})),
        "token-review": AuthenticatedPrincipal("reviewer", frozenset({"001"}), frozenset({"reviewer"})),
        "token-approve": AuthenticatedPrincipal("approver", frozenset({"001"}), frozenset({"approver"})),
        "token-foreign": AuthenticatedPrincipal("foreign", frozenset({"002"}), frozenset({"approver"})),
    }
    access = MappingAccess(identities.get)
    space = MappingWorkspace("001", 1405)
    for credential in ("", "maker", "token-foreign", "token-review"):
        with pytest.raises(MappingWorkflowError):
            access.propose(credential, space, decision())
    access.propose("token-maker", space, decision())
    with pytest.raises(MappingWorkflowError, match="access denied"):
        access.approve("token-maker", space, "M1")
    access.review("token-review", space, "M1")
    access.approve("token-approve", space, "M1")
    assert space.decisions[0].status == "Approved"
    assert [e.actor for e in space.audit] == ["maker", "reviewer", "approver"]
    access.revise("token-maker", space, "M1", target_statement="IS",
                  statement_section="Revenue", note_number="02", subnote_code=None)
    assert space.decisions[0].status == "Draft"


def test_identity_resolver_failure_is_fail_closed():
    access = MappingAccess(lambda _: None)
    with pytest.raises(MappingWorkflowError, match="access denied"):
        access.propose("anything", MappingWorkspace("001", 1405), decision())


def test_maker_with_approver_role_cannot_approve_own_mapping():
    users = {
        "a": AuthenticatedPrincipal("a", frozenset({"001"}), frozenset({"maker", "approver"})),
        "b": AuthenticatedPrincipal("b", frozenset({"001"}), frozenset({"reviewer"})),
    }
    access = MappingAccess(users.get)
    space = MappingWorkspace("001", 1405)
    access.propose("a", space, decision())
    access.review("b", space, "M1")
    with pytest.raises(MappingWorkflowError, match="independent"):
        access.approve("a", space, "M1")
