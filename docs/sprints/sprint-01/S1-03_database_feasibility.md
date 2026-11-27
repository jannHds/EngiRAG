
# S1-03 — Database Feasibility & Initial Contracts

## Task Information

- Project: EngiRAG
- Sprint: Sprint 1
- Task ID: S1-03
- Owner: Jana
- Reviewer: Asma
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
---

## S1-03 — Team Review and Contract Validation Update

### 1. Team Review Summary

Alzahraa reviewed the document processing and evidence requirements. Leen reviewed the indexing and retrieval requirements.

Their feedback was incorporated into the preliminary logical ERD and Pydantic contracts.

#### Alzahraa — Document Processing

The following design decisions were incorporated:

- Preserve engineering relationships between equipment, parameters, values, and units.
- Support structured engineering facts alongside original evidence text.
- Retain source locations, including pages, sections, tables, and cell references.
- Distinguish DocumentVersion from ContentRevision.
- Define validation states: PENDING, NEEDS_REVIEW, APPROVED, and REJECTED.
- Record extraction methods, optional confidence scores, and extraction issues.

#### Leen — Indexing and Retrieval

The following design decisions were incorporated:

- Use a many-to-many logical relationship between EvidenceUnit and IndexedChunk through ChunkEvidence.
- Keep Evidence IDs independent of Chunk IDs.
- Introduce EmbeddingProfile to describe embedding configurations.
- Extend IndexGeneration to describe indexing configurations.
- Preserve document version, content revision, and access scope information.
- Extend retrieval contracts with language, retrieval mode, index generation, and retrieval profile information.
- Separate dense, lexical, and fusion scores.
- Define a preliminary RetrievedChunk contract.
- Require reindexing and active-index eligibility updates when approved content changes.

These decisions define the preliminary interface and logical design. They do not represent complete physical database or retrieval implementation.

### 2. Updated Contract Validation

The following files were updated:

- backend/contracts/schemas.py
- tests/test_contracts.py
- docs/architecture/initial_erd.md

Validation coverage includes:

- Private and shared document reference validation.
- Required document ownership and conversation identifiers.
- Engineering facts with parameters, values, and units.
- Source location validation.
- Approved evidence source-location requirements.
- Extraction confidence boundaries.
- Validation status restrictions.
- Rejection of unapproved evidence in retrieval results.
- Rejection of mixed document versions and content revisions within retrieved chunks.
- Retrieval request configuration validation.

### 3. Automated Test Results

Environment:
- Python: 3.12.10
- Django: 5.2.19
- pytest: 9.2.0

Command:

    python -m pytest -v

Result:

    20 passed in 0.32s

Django validation command:

    python backend\manage.py check

Result:

    System check identified no issues (0 silenced).

### 4. Database Feasibility Status

Previously verified:

- Django connectivity to Supabase PostgreSQL.
- PostgreSQL/pgvector extension availability.
- Basic vector similarity functionality.
- Local SQLite migration testing for the Custom User Model.

Important limitations:

- Django migrations have not been applied to the shared Supabase database.
- The expanded logical ERD has not been implemented as Django models.
- The many-to-many ChunkEvidence relationship is a logical design decision, not a tested database relationship.
- Isolated PostgreSQL migration testing remains pending.

### 5. Security and Integration Limitations

Pydantic validation does not establish user authorization.

The following requirements still need backend implementation and integration testing:

- Conversation ownership enforcement.
- Cross-user and cross-conversation access isolation.
- Private/shared retrieval filtering.
- Administrative publication permissions.
- Index activation and revision eligibility.
- Citation authorization and verification.

### 6. Outstanding Reviews

- Student 4: Citation structure and answering contract review.
- Student 5: Custom User Model, ownership rules, authorization boundaries, and final pull request review.

### 7. Review Status

Alzahraa: Feedback received and incorporated into the preliminary design.

Leen: Feedback received and incorporated into the preliminary design.

Lujain: Pending review.

Asma: Pending review.

Overall status: Implementation and contract tests updated; final review and isolated PostgreSQL migration validation remain pending.


### Local PostgreSQL Migration Validation

Environment:
- PostgreSQL: 17.12
- Database: engirag_test
- Database User: engirag_test_user
- Django Settings: config.settings_pgtest
- Connection: localhost:5432

Results:
- Django successfully connected to the isolated PostgreSQL database.
- Django migrations were executed against the local test database.
- accounts.0001_initial was confirmed as applied.
- The accounts_user table was confirmed to exist in PostgreSQL.
- The shared Supabase database was not used for this migration test.

Evidence:

    accounts
     [X] 0001_initial

    SELECT to_regclass('public.accounts_user');

    Result: accounts_user

Conclusion:
The initial Custom User Model migration was successfully
validated on PostgreSQL 17.12 in an isolated local environment.

Status: PASSED
