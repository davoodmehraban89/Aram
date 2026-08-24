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
