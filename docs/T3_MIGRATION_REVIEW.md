# T3 explicit migration: evidence and review gates

- Accepted base: `source-data-cleanup@7dc864fd032f0c4ae4d650d89304a01286a6d914`.
- Candidate: [Draft PR #25](https://github.com/davoodmehraban89/Aram/pull/25).
- GitHub Actions [Backend CI #50](https://github.com/davoodmehraban89/Aram/actions/runs/39868963147) passed on implementation head `10dd7cc74b1b3a217eb75ddac65441629de79e7a`: pytest, Alembic upgrade/downgrade, compile. Earlier CI failures were caused by regression-test comparison mistakes (column objects vs names; unresolved FK name), corrected in later commits.
- Coverage: all nine tables, column names and nullability, unique constraints, indexes, foreign keys, and empty-database downgrade. Test uses an in-memory SQLite database, not financial source data.
- Functional review: initial schema operations are explicit and upgrade/downgrade passed in GitHub CI; no claim of external independent reviewer approval.
- Code/security review: metadata-driven migration DDL was removed; canonical XLSX/PDF and `data/` are unchanged; SQLite-only CI does not prove PostgreSQL behavior.
- Edge-case review: empty-database migration round trip is covered; upgrading a pre-existing populated production database is not covered and must be tested separately before deployment.
- Acceptance: **PENDING independent review**, Draft PR remains unmerged. No release artifact.
- Recovery: do not merge PR #25 if any review fails; accepted branch remains untouched. For a disposable database only, run `cd backend && alembic downgrade base`.
