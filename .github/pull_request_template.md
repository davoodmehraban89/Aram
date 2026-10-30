## Objective

<!-- One measurable outcome. -->

## Base branch and base SHA

- Base branch:
- Verified base SHA:

## Scope

### Included

-

### Excluded

-

## Changed files

<!-- Exact list; explain every binary/generated file. -->

-

## Tests

| Command | Result |
|---|---|
|  |  |

## GitHub Actions evidence

- Run URL:
- Result:

## Canonical data verification

- [ ] No canonical XLSX/PDF or financial source changed.
- [ ] Any approved exception is listed with before/after hashes and recovery steps.

## Binary / artifact changes

- [ ] None
- [ ] Present and explained below with workflow URL and checksums:

## Documentation updates

- [ ] `PROJECT_STATUS.md` updated, or no current-status change explained.
- [ ] `docs/PROJECT_LOG.md` appended; historical entries were not rewritten.
- [ ] Decision changes recorded as a new ADR, if applicable.

## Risks

-

## Rollback / recovery

-

## Acceptance checklist

- [ ] Correct base branch and SHA
- [ ] Focused PR
- [ ] Exact changed-file list
- [ ] No unexplained binary or data changes
- [ ] Tests executed
- [ ] Required CI successful
- [ ] Documentation updated
- [ ] Independent review pending/completed
- [ ] Artifact/release evidence verified when applicable
- [ ] Explicit acceptance decision recorded

**Agent reports are not acceptance evidence. Do not merge until remote evidence is independently reviewed.**

## Proposed ADR-013 5+1+3 evidence fields (Draft PR #34)

This block becomes mandatory **only when ADR-013 is accepted and merged**.

- Operational manager / actual implementation agent:
- Applicable specialist roles A1–A5 and actual executors:
- Base SHA / final head SHA / dependent PRs:
- Exact original source-to-output trace and financial fixtures (when relevant):
- Scope exceptions and owner approvals (if any):

| Independent gate | Actual reviewer (not author) | Reviewed full SHA | Evidence URLs | Decision / unresolved findings |
|---|---|---|---|---|
| C1 technical/security | | | | PASS / FAIL / BLOCKED |
| C2 financial/integrity | | | | PASS / FAIL / BLOCKED; justified N/A if applicable |
| C3 acceptance/release | | | | ACCEPT / REVISE / REJECT / BLOCKED |

C1/C2/C3 must be reviewed by **three distinct, verifiable identities**, none of whom authored the change. A green check does not replace reviewer independence. A change to head SHA requires re-verification. Missing reviewer or evidence = `BLOCKED`, not `PASS`. No self-merge, unapproved Production release or canonical-data change.
