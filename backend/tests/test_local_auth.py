import pytest

from aram_backend.local_auth import LocalSessionAuthority, create_credential


def test_local_auth_password_session_revocation():
    credential = create_credential("owner", "correct horse battery staple", frozenset({"001"}), frozenset({"maker"}))
    authority = LocalSessionAuthority(credential)
    assert authority.login("wrong password") is None
    token = authority.login("correct horse battery staple")
    assert token and len(token) >= 32
    assert authority.resolve("owner") is None
    assert authority.resolve(token).subject == "owner"
    authority.revoke(token)
    assert authority.resolve(token) is None
    assert LocalSessionAuthority(credential).resolve(token) is None


def test_local_auth_rejects_weak_provisioning():
    with pytest.raises(ValueError):
        create_credential("owner", "short", frozenset({"001"}), frozenset({"maker"}))
    with pytest.raises(ValueError):
        LocalSessionAuthority(create_credential("owner", "correct horse battery staple", frozenset({"001"}), frozenset({"maker"})), lifetime_seconds=0)

def test_local_auth_lockout_and_recovery(monkeypatch):
    import aram_backend.local_auth as auth

    now = [100.0]
    monkeypatch.setattr(auth.time, "monotonic", lambda: now[0])
    credential = create_credential("owner", "correct horse battery staple",
                                   frozenset({"001"}), frozenset({"owner"}))
    authority = LocalSessionAuthority(credential, max_failed_attempts=2, lockout_seconds=30)
    assert authority.login("wrong") is None
    assert authority.login("wrong") is None
    assert authority.login("correct horse battery staple") is None
    now[0] += 31
    token = authority.login("correct horse battery staple")
    assert token is not None


def test_local_auth_session_limit_and_revoke_all():
    credential = create_credential("owner", "correct horse battery staple",
                                   frozenset({"001"}), frozenset({"owner"}))
    authority = LocalSessionAuthority(credential, max_sessions=1)
    token = authority.login("correct horse battery staple")
    assert token is not None
    assert authority.login("correct horse battery staple") is None
    authority.revoke_all()
    assert authority.resolve(token) is None
    assert authority.login("correct horse battery staple") is not None


def test_local_auth_rejects_unknown_roles_and_oversized_password():
    with pytest.raises(ValueError):
        create_credential("owner", "correct horse battery staple",
                          frozenset({"001"}), frozenset({"superadmin"}))
    credential = create_credential("owner", "correct horse battery staple",
                                   frozenset({"001"}), frozenset({"owner"}))
    authority = LocalSessionAuthority(credential)
    assert authority.login("x" * 1025) is None
    assert authority.resolve("x" * 1000) is None
