
# S1-03 — Database Feasibility & Initial Contracts

## Task Information

- Project: EngiRAG
- Sprint: Sprint 1
- Task ID: S1-03
- Owner: Student 1
- Reviewer: Student 5
- Status: In Progress — Pending Peer Review

## 1. Objective

Verify PostgreSQL and pgvector feasibility and
prepare initial database relationships and module
contracts for EngiRAG.

## 2. Database Feasibility

Database: Supabase PostgreSQL 17.12
Extension: pgvector 0.8.2
Backend: Django 5.2.19
Python: 3.12.10

Results:
- PostgreSQL connection: PASSED
- Django database connection: PASSED
- pgvector similarity query: PASSED
- Initial migration plan inspection: PASSED

Note:
No Django migrations have been applied to the
shared Supabase database.

## 3. Custom User Model

- Created accounts application.
- Implemented accounts.User using AbstractUser.
- Configured AUTH_USER_MODEL.
- Generated accounts.0001_initial.
- Verified migrations using isolated SQLite.
- Confirmed expected user table: accounts_user.

## 4. Initial Database Design

Drafted:
- Logical ERD
- Entity definitions and relationships
- Primary and Foreign Key strategy
- Database integrity rules
- Private/shared document separation
- Document version and citation relationships

Reference:
docs/architecture/initial_erd.md

## 5. Pydantic Contracts

Implemented:
- DocumentReference
- EvidenceRecord
- AuthorizedRetrievalRequest
- VisibilityScope

Location:
backend/contracts/schemas.py

## 6. Test Results

Command:
python -m pytest tests/test_contracts.py -v

Observed Result:
7 passed in 0.15s

Verified:
- Valid private document accepted.
- Missing private owner rejected.
- Missing conversation rejected.
- Shared document with private owner rejected.
- Empty evidence content rejected.
- Invalid top_k values rejected.

## 7. Remaining Work

- Review contracts with Students 2, 3 and 5.
- Align EvidenceRecord with Student 2.
- Align retrieval/index metadata with Student 3.
- Review account isolation with Student 5.
- Test migrations in isolated PostgreSQL.
- Finalize logical design decisions.
- Complete peer review and Pull Request.

## 8. Limitations

- Contracts are preliminary.
- Authorization rules are not yet tested end-to-end.
- Shared database migrations remain pending.
- Final physical schema has not been approved.

## 9. Review Status

Pending cross-team review and approval.
