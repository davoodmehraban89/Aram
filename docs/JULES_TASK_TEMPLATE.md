# Jules Task Specification & Prompt Template

This template defines the mandatory structure for assigning tasks to Jules (implementation AI agent) in the Aram repository.

---

## TASK TEMPLATE STRUCTURE

```markdown
### TASK TITLE: [Phase / Sub-phase Name]

#### 1. OBJECTIVE
[Succinct description of the goal for this task]

#### 2. VERIFIED STARTING POINT
- Base Branch: source-data-cleanup
- Expected Base Commit SHA: [Exact Commit SHA verified in PROJECT_STATUS.md]

#### 3. STRICT SCOPE & BOUNDARIES
- Allowed Files / Directories: [List exact paths allowed for modification/creation]
- Prohibited Actions:
  - Do NOT modify any canonical financial XLSX/CSV/PDF files under `data/`.
  - Do NOT modify legacy `index.html` unless explicitly authorized.
  - Do NOT commit generated database files (`*.db`, `*.sqlite`) or binary build artifacts (`*.exe`, `*.zip`).
  - Do NOT implement multi-phase changes outside this task's scope.

#### 4. REQUIRED IMPLEMENTATION
- [Item 1]
- [Item 2]

#### 5. TESTING REQUIREMENTS
- Run relevant unit/integration tests using `pytest`.
- Expected test output / coverage criteria.

#### 6. REQUIRED GITHUB EVIDENCE
- Exact changed files list (`git status`).
- Clean whitespace diff check (`git diff --check`).
- Dedicated working branch name (e.g., `jules/task-name`).

#### 7. DOCUMENTATION UPDATES
- Update `PROJECT_STATUS.md` with PR link and state classification.
- Add append-only entry to `docs/PROJECT_LOG.md`.

#### 8. MANDATORY STOP CONDITION
**STOP & REPORT IMMEDIATELY** if:
1. The actual repository HEAD commit SHA differs from the expected Base Commit SHA.
2. A required file or directory is missing.
3. Unexplained test failures occur on baseline code before your changes.
Do NOT guess or attempt to bypass mismatched baseline commits.
```
