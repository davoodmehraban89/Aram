# ARAM Gate 3 identity boundary — implementation and acceptance plan

**Issue [#49](https://github.com/davoodmehraban89/Aram/issues/49)**. Child [Draft PR #55](https://github.com/davoodmehraban89/Aram/pull/55) of unmerged [Draft #54](https://github.com/davoodmehraban89/Aram/pull/54), exact parent SHA `c5e3fb7f8917433a1075ece8ad1ee95a1695dad5`; upstream #53/#52/#51/#50/#26 and schema #25 remain unmerged. Accepted `source-data-cleanup@7dc864fd032f0c4ae4d650d89304a01286a6d914` unchanged.

## Evidence collected

1. [x] Inspected the live GitHub source `backend/pyproject.toml`, `config.py`, `main.py`, existing read-only API and lack of any authenticated user directory, approver role, trusted middleware or integration to customer IdP. Verified PR #54 remained Draft and parent SHA unchanged.
2. [x] Consulted current PyJWT documentation for `decode` signature/issuer/audience validation and `options.require` mandatory claims; used `PyJWT[crypto]>=2.10,<3` as an explicitly reviewed dependency candidate.
3. [x] Added dependency declaration SHA `79da69972d01b858c876e7b42f5d8e59a34d4e9e`, then test-first `test_authenticated_identity.py` SHA `afe380fc0a2236f9eb2cdfce21168a1dbc507bfd`. [RED CI 41109024753](https://github.com/davoodmehraban89/Aram/actions/runs/41109024753): **34 expected 404 route failures and 193 preexisting passing tests** (2 warnings), proving the new read-only auth endpoint did not yet exist. No private keys committed: RSA fixtures generate ephemeral keys.
4. [x] Created read-only `authenticated_identity.py`, configured default-off issuer/audience/RSA public PEM fields, and added `GET /api/v1/auth/me` with `Depends(require_verified_principal)`. Pinned public RS256 verification, strict signed claims, max 15-minute lifetime, exact one role, rejection of forged HTTP headers, unsigned/HMAC tokens and stale credentials. No review/apply endpoint or database mutation.
5. [x] [GREEN CI 41109205928](https://github.com/davoodmehraban89/Aram/actions/runs/41109205928) on route implementation SHA `c0b6f5df64ae9235683926e1fed661dadb46be67`: **227 passed, 2 warnings**, disposable Alembic upgrade/downgrade and compileall success.
6. [x] Added four further synthetic adversarial cases at `ad66b06bab27ad61040f7a5b4f8cb81923eaf2da`: signed reviewer can use only whoami, still no approval endpoint; modified payload invalidates signature; malformed/weak RSA public keys fail closed. Await corresponding exact code-head CI.
7. [ ] Complete focused spec/plan and append-only `docs/PROJECT_LOG.md` and `docs/handoff/LATEST_HANDOFF.md`; run remote GitHub CI on **FINAL exact docs SHA**, check diff allowlist, parent, original accepted branch and actual review count. Log any CI failure, do not omit RED failures.
8. [ ] **Deferred mandatory security gates:** configure a genuinely authorized enterprise OIDC/OAuth2 issuer and access-token signer; introduce key rotation/revocation and issuer trust policy; store authenticated proposal author identity; implement real reviewer-vs-author separation, year/company authorization, signed immutable review decision and atomic lock/CAS MappingRule apply; retrofit bypassing Excel import path; verify provider-specific SQL controls and actual financial reconciliation. No deployment until real independent review and migration history reconciliation.

## Exact allowed changed paths

- New `backend/src/aram_backend/authenticated_identity.py`
- New `backend/tests/test_authenticated_identity.py`
- Modify `backend/src/aram_backend/config.py`
- Modify `backend/src/aram_backend/main.py`
- Modify `backend/pyproject.toml` (new explicit crypto verification dependency, no workflow or lockfile modification)
- Add spec/plan under `docs/superpowers/`
- Append only `docs/PROJECT_LOG.md` and `docs/handoff/LATEST_HANDOFF.md`

No canonical source XLSX/PDF, `data/`, real customer or production SQL, migration rewrite, CI workflow, binary, release, or source-data-cleanup mutation. No actual enterprise user ID, signing private key, finance signer or approval fabricated.

## Downgrade, rollout and false-completion risk

No DB schema migration introduced in this PR. If the code is rejected, close the unmerged Draft or use an independently reviewed revert if ever accepted. `GET /auth/me` is default-deny: absence of all operator-managed auth settings produces HTTP 503, never anonymous acceptance. Do not treat unit-test RSA keys as a production identity provider. The broader Gate 3 remains **0% formally accepted**, all actual human review and finance owner signoff unresolved.
