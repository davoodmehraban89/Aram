# Jules Task Template

Copy this template for one focused task. Replace every placeholder.

## Objective

[One measurable outcome.]

## Verified starting point

- Repository: `davoodmehraban89/Aram`
- Base branch: `[BASE_BRANCH]`
- Required base SHA: `[FULL_SHA]`

Fetch the remote and verify the SHA before editing. If it differs, stop and report the actual SHA. Do not guess or continue.

## Strict scope

Allowed paths:

- `[PATH]`

Required implementation:

1. [Requirement]
2. [Requirement]

## Prohibited actions

- Do not merge the PR.
- Do not modify files outside the allowed paths.
- Do not modify canonical XLSX/PDF or financial source data.
- Do not add unrelated refactors, generated binaries, releases, or dependency changes.
- Do not claim success without remote evidence.

## Tests and verification

Run:

```text
[EXACT COMMANDS]
```

Also run `git diff --check` and inspect the complete diff against the required base SHA.

## GitHub evidence

Create a dedicated branch and a focused PR into `[BASE_BRANCH]`. Return:

- verified base SHA;
- remote branch;
- full head commit SHA;
- PR number and real URL;
- exact changed-file list;
- exact test commands/results;
- GitHub Actions run URLs/results;
- artifacts/releases and checksums, or `NONE`;
- confirmation of canonical-data status;
- remaining risks.

## Documentation updates

Update `PROJECT_STATUS.md` if current status changes. Append one complete entry to `docs/PROJECT_LOG.md`. Never rewrite accepted log history.

## Completion statement

End with: `Ready for independent GitHub review; not merged.`

## Stop conditions

Stop without edits if repository state differs from this task, the scope is ambiguous, required evidence is unavailable, protected data would change, or publication to GitHub fails.
