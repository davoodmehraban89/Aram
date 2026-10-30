# Acceptance Policy

> An agent's written success report is not acceptance evidence.

Every phase must satisfy all applicable gates below.

## Mandatory gates

- [ ] The target branch and exact base SHA match the approved starting point.
- [ ] A dedicated working branch exists remotely.
- [ ] The PR is focused and targets the approved branch.
- [ ] The PR lists every changed file and explains each change.
- [ ] No unexplained binary, generated, database, or financial-data change exists.
- [ ] Required test commands and results are recorded.
- [ ] Required GitHub Actions checks succeeded and their URLs are recorded.
- [ ] Canonical XLSX/PDF and financial source hashes or unchanged status are verified.
- [ ] `PROJECT_STATUS.md` is updated when current state changes.
- [ ] `docs/PROJECT_LOG.md` receives an append-only entry.
- [ ] An independent reviewer checks the remote commit, diff, and evidence.
- [ ] The acceptance decision is explicit: accepted, rejected, or changes requested.
- [ ] Artifact checksums, provenance, and download URLs are verified when relevant.
- [ ] Rollback or recovery instructions are recorded.

## Artifact and release gate

A local file or a file committed to an unmerged branch is not a release. Acceptance requires a reproducible workflow, successful run URL, artifact metadata/checksum, tag, release URL, correct target commit, downloadable assets, and clean-environment verification appropriate to the artifact.

## Stop conditions

Stop and report without making changes if the base SHA differs, required files are unavailable, canonical data would be changed outside explicit scope, unrelated changes are present, tests cannot run, authentication blocks remote publication, or evidence cannot be obtained.

## Decision record

The reviewer must record:

- reviewed commit SHA;
- reviewed file list;
- CI run URLs and conclusions;
- artifact/release URLs if applicable;
- detected risks;
- final decision and reviewer identity.

## Proposed extension: three independently evidenced controls (ADR-013)

This section is proposed by [Draft PR #34](https://github.com/davoodmehraban89/Aram/pull/34) and takes effect **only upon its independently accepted merge**. It supplements rather than removes the mandatory gates above.

### C1: Technical and security — `PASS | FAIL | BLOCKED`

Independent non-author reviewer checks the **complete remote diff at the final head SHA**, scope, security/auth, data access and separation, tests and failures, actual GitHub Actions jobs on that head, dependencies, migrations, protected paths and rollback. Record identity, SHA, URL(s), findings and decision.

### C2: Financial accuracy and data integrity — `PASS | FAIL | BLOCKED`

Qualified independent financial reviewer checks relevant debits/credits, opening/closing positions, company/year separation, mapping coverage and exceptions, statement-to-note consistency, comparative periods, currency/unit/rounding and source-row lineage on synthetic or explicitly approved fixtures. For unrelated documentation tasks, an independent reviewer may record `PASS (NOT_APPLICABLE)` with a documented reason and evidence. Never invent financial outcomes or imply that passing backend tests alone proves financial correctness.

### C3: Independent acceptance and release — `ACCEPT | REVISE | REJECT | BLOCKED`

Separate non-author reviewer checks requirement coverage, the base and final head SHA, complete changed files, PR and job provenance, C1/C2 evidence, unresolved risks, issue/handoff consistency, rollback and authorized merge/release boundaries. No accepted or production-ready claim without the applicable evidence.

**Separation and failure rule:** an LLM's successive internal audits do **not** count as three independent reviewers. No self-approval. If any gate fails, evidence is incomplete, reviewer identities cannot be established, or a checked SHA changes, the item is **not accepted**. Route fixes to the author; repeat every affected gate on the new SHA. No override by green CI, PR author, or manager. Existing ADR-011 routine merge delegation applies only after successful gates.

### Required work-item evidence

Each report records task ID, manager, lead A1–A5, collaborators, remote base/branch/head SHA, complete changed paths, real tests and CI URLs, C1/C2/C3 identities, checked SHA and decisions, financial-source protections, remaining risks, rollback and one final state `ACCEPTED | REVISION_REQUIRED | REJECTED | BLOCKED | UNVERIFIED`. Owner approval is separately required for accounting ambiguity, protected-data edits, material scope, destructive operations, credentials and formal release.
