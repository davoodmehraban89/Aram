# Aram Acceptance Policy & Mandatory Phase Gates

This policy governs the criteria required before any task, phase, Pull Request, or release is formally accepted into the Aram repository.

---

## CORE MANDATE
> **“An agent’s written success report is not acceptance evidence.”**

All claims made by AI agents or human developers must be independently backed by verifiable GitHub evidence.

---

## Mandatory Acceptance Gates

Every Pull Request submitted to Aram must satisfy all of the following gates prior to merge approval:

### Gate 1: Baseline Integrity
- Must branch from the current accepted baseline branch (`source-data-cleanup`) and commit SHA.
- Must NOT start from unmerged feature branches or stale working directories.

### Gate 2: Dedicated & Focused Scope
- Must be submitted on a dedicated branch (e.g. `jules/task-description`).
- Must maintain a strict, narrow scope addressing a single objective or sub-phase.
- Must NOT combine unrelated features, multi-phase rewrites, or broad refactors into a single PR.

### Gate 3: Changed Files Verification
- PR must include an exact, verified list of modified and created files.
- Must NOT modify or delete canonical financial source files under `data/` (`.xlsx`, `.csv`, `.pdf`).
- Must NOT commit binary build artifacts (`*.exe`, `*.zip`, `*.db`) into source code branches unless explicitly instructed.

### Gate 4: Automated Testing & GitHub CI Verification
- Unit and integration tests relevant to the change must be executed and passing.
- Must pass the official GitHub Actions CI pipeline (`.github/workflows/ai-review.yml`).
- Local sandbox test runs alone do NOT satisfy this gate.

### Gate 5: Documentation & Control Updates
- `PROJECT_STATUS.md` must be updated to reflect current state, PR links, and state categorizations.
- `docs/PROJECT_LOG.md` must receive an append-only entry recording the task, commit SHA, PR URL, and CI status.

### Gate 6: Artifact & Release Verification (When Applicable)
- Any claimed release asset (ZIP, EXE) or GitHub Release MUST be independently verified via tag, release URL, and asset download on GitHub.

### Gate 7: Independent Review & Approval
- Code review must be conducted by the ChatGPT Project Manager / human reviewer.
- Pull Requests must remain unmerged until formal approval is granted.

---

## State Classification Standards

Work in the repository must be classified using these exact terms:

- **`VERIFIED_AND_MERGED`**: Code/docs merged into default branch with passing GitHub CI.
- **`VERIFIED_BUT_UNMERGED`**: Code tested locally but pending PR review/merge on GitHub.
- **`PRESENT_BUT_UNVERIFIED`**: Artifacts/code present in working tree or PR without GitHub CI evidence.
- **`CLAIMED_BUT_NOT_PROVEN`**: Agent reports asserting completion without verifiable GitHub links/logs.
- **`IN_PROGRESS`**: Open PR or active development task currently underway.
- **`NOT_IMPLEMENTED`**: Feature or phase planned for future development but not yet started.
- **`BLOCKED`**: Progress halted due to unresolved technical or governance blockers.
