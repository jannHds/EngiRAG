# EngiRAG — Development Environment Setup Guide

## 1. Overview

This guide explains how to clone, configure, run, and test the EngiRAG backend development environment on Windows.

EngiRAG is a bilingual engineering knowledge assistant built using Django and Retrieval-Augmented Generation (RAG).

The project uses a shared PostgreSQL database hosted on Supabase, while each team member maintains a separate local Python development environment.

This guide covers the development setup completed during S1-01, S1-02, and S1-03.

## 2. Technology Stack

The current development environment includes:

- **Python:** 3.12.10
- **Django:** 5.2.19 LTS
- **pytest:** 9.2.0
- **pytest-django:** 4.14.0
- **Pydantic:** Version 2
- **python-dotenv:** Environment variable management
- **psycopg:** PostgreSQL database driver
- **PostgreSQL:** 17, hosted on Supabase
- **pgvector:** 0.8.2
- **Git and GitHub:** Version control and collaboration
- **Visual Studio Code:** Development environment

The versions listed above reflect the initially verified setup. The dependency manifest in `requirements/dev.txt` should be used when installing the project.

## 3. Prerequisites

Install the following tools before starting:

1. Python 3.12 — https://www.python.org/downloads/
2. Git — https://git-scm.com/
3. Visual Studio Code — https://code.visualstudio.com/
4. Python extension for VS Code

Open Windows Command Prompt (CMD) and verify the installations:

```cmd
py -3.12 --version
git --version
```

Make sure Python 3.12 is installed.

Each team member must also have access to the private EngiRAG GitHub repository.

## 4. Clone the Repository

### 4.1 Download the Project

1. Sign in to GitHub.
2. Open the private `EngiRAG` repository.
3. Click **Code → HTTPS**.
4. Copy the repository URL.
5. Open CMD in the location where you want to store the project.

Run:

```cmd
git clone REPOSITORY_URL
```

Replace `REPOSITORY_URL` with the HTTPS URL copied from GitHub.

Navigate into the project folder:

```cmd
cd EngiRAG
```

### 4.2 Switch to the Development Branch

The team uses the following branching structure:

- `main`: Stable, reviewed code.
- `develop`: Integration branch.
- `feature/...`: Individual task development.

To access the latest integrated development version, run:

```cmd
git switch develop
git pull origin develop
```

If `develop` is not available locally, verify that it exists on the remote repository and has been fetched.

**Important:** Features that have not yet been merged into `develop` will not appear in the integrated branch.

### 4.3 Open the Project in VS Code

Run:

```cmd
code .
```

Alternatively, open VS Code, select **File → Open Folder**, and choose the EngiRAG repository folder.

The terminal should be opened at the project root, where `backend`, `requirements`, `tests`, and `docs` are located.

## 5. Create a Virtual Environment

Each team member must create their own local virtual environment.

From the project root, run:

```cmd
py -3.12 -m venv .venv
```

Activate it using Windows CMD:

```cmd
.venv\Scripts\activate.bat
```

The terminal should display `(.venv)` before the project path.

Verify the Python version:

```cmd
python --version
```

Expected version:

```text
Python 3.12.x
```

In VS Code, select the Python interpreter located at:

```text
.venv\Scripts\python.exe
```

The `.venv` folder is local and must not be committed to GitHub.

## 6. Install Dependencies

With the virtual environment activated, install the project dependencies:

```cmd
python -m pip install -r requirements\dev.txt
```

Check dependency compatibility:

```cmd
python -m pip check
```

Verify Django:

```cmd
python -m django --version
```

All team members should use the shared dependency configuration rather than independently selecting package versions.

## 7. Configure Environment Variables

EngiRAG uses environment variables to keep sensitive configuration outside the source code.

### 7.1 Create the Local Environment File

From the project root, run:

```cmd
copy .env.example .env
```

If a local `.env` file already exists, do not overwrite it without checking its contents.

Open `.env` in VS Code.

### 7.2 Django Configuration

Make sure the following variables are configured:

```dotenv
DJANGO_SECRET_KEY=your-generated-secret-key
DJANGO_DEBUG=True
```

Generate a Django secret key using:

```cmd
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Replace the placeholder with the generated key.

`DJANGO_DEBUG=True` is intended for local development only.

### 7.3 Supabase PostgreSQL Configuration

Add the database configuration to the same `.env` file:

```dotenv
DB_NAME=postgres
DB_USER=your-supabase-pooler-username
DB_PASSWORD=your-database-password
DB_HOST=your-supabase-session-pooler-host
DB_PORT=5432
DB_SSLMODE=require
```

The database connection information must be obtained through the team's authorized channel.

The current Django configuration uses PostgreSQL as the default database. Missing database environment variables may prevent Django from starting.

**Security requirements:**

- Never commit `.env` to GitHub.
- Never share actual database passwords through Pull Requests or screenshots.
- Do not place credentials inside `.env.example`.
- Use the Supabase Session Pooler connection information agreed upon by the team.
- Do not change the shared database configuration without coordination.

## 8. Verify the Database Connection

The backend uses PostgreSQL through the `psycopg` driver.

After configuring `.env`, check Django:

```cmd
python backend\manage.py check
```

Then test the actual database connection:

```cmd
python backend\manage.py shell -c "from django.db import connection; connection.ensure_connection(); print('Connected successfully to Supabase!')"
```

Expected successful output:

```text
Connected successfully to Supabase!
```

During S1-03, the team successfully verified:

- Django connectivity to Supabase PostgreSQL.
- PostgreSQL 17 compatibility.
- pgvector extension availability.
- Sample vector storage and cosine similarity search.

These checks confirm initial database feasibility, not the completion of the final application schema or retrieval system.

## 9. Run Django

Start the development server:

```cmd
python backend\manage.py runserver
```

The server should start at:

```text
http://127.0.0.1:8000/
```

Open the backend health endpoint:

http://127.0.0.1:8000/api/health/

Expected response:

```json
{
  "status": "ok",
  "service": "EngiRAG Backend"
}
```

The root URL `/` may display a 404 response because the main user interface has not yet been implemented.

A successful health-check response confirms that the basic Django endpoint is operating.

To stop the server, press `Ctrl + C` in the terminal.

## 10. Run Automated Tests

From the project root, with `.venv` activated, run:

```cmd
python -m pytest -v
```

The initial test suite includes:

**Health Endpoint Testing**
- Verify successful HTTP response.
- Verify the expected response content.

**Pydantic Contract Testing**
- Validate private document references.
- Reject private documents without ownership information.
- Reject invalid shared-document ownership fields.
- Reject empty evidence content.
- Validate retrieval request parameters.

The latest verified S1-03 test execution produced:

```text
8 passed in 0.14s
```

This includes seven contract tests and one health endpoint test.

Additional tests will be introduced as the remaining modules are implemented.

## 11. Custom User Model and Database Migrations

### 11.1 Custom User Model

The project includes a Django application named `accounts`.

The initial user model is defined in:

```text
backend/accounts/models.py
```

It extends Django's `AbstractUser` and is configured using:

```python
AUTH_USER_MODEL = "accounts.User"
```

This provides an extensible foundation for future user authentication and authorization.

The initial migration is located at:

```text
backend/accounts/migrations/0001_initial.py
```

### 11.2 Migration Safety

The team uses a shared Supabase development database.

**Do not run migrations against the shared database without coordination and approval.**

To inspect the planned migrations without applying them:

```cmd
python backend\manage.py migrate --plan
```

During S1-03, the Custom User Model migration was tested using an isolated local SQLite configuration.

The initial migration has not been applied to the shared Supabase database.

An isolated PostgreSQL migration test is still required before shared schema changes are approved.

## 12. Initial Data Contracts

EngiRAG uses Pydantic to validate data exchanged between system modules.

The preliminary contracts are defined in:

```text
backend/contracts/schemas.py
```

The initial contracts include:

- **DocumentReference:** Identifies a document, version, and visibility scope.
- **EvidenceRecord:** Represents extracted evidence with source references.
- **AuthorizedRetrievalRequest:** Represents an internal retrieval request with an intended authorized document scope.
- **VisibilityScope:** Distinguishes private conversation documents from shared knowledge documents.

Two visibility categories are currently defined:

```text
PRIVATE_CONVERSATION
SHARED
```

Private conversation documents must remain associated with the correct owner and conversation.

Shared knowledge documents follow separate administrative publication rules.

These contracts validate data structure. Actual user authorization must be enforced by the backend.

The contracts and logical database design are preliminary and require review by the relevant module owners.

## 13. Project Structure

The main repository structure includes:

```text
EngiRAG/
├── backend/
│   ├── accounts/
│   ├── config/
│   ├── contracts/
│   └── manage.py
├── docs/
│   ├── architecture/
│   └── sprints/
├── experiments/
├── requirements/
├── scripts/
├── tests/
├── README.md
├── CONTRIBUTING.md
├── pytest.ini
├── .env.example
└── .gitignore
```

Important documentation files:

- `README.md` — Project overview.
- `CONTRIBUTING.md` — Team development workflow.
- `docs/ENVIRONMENT_SETUP.md` — Development setup instructions.
- `docs/architecture/initial_erd.md` — Preliminary database relationships.
- `docs/sprints/sprint-01/S1-03_database_feasibility.md` — Database feasibility results and limitations.

## 14. Daily Development Workflow

Before starting a new task, synchronize your local repository.

For a clean working tree:

```cmd
git switch develop
git pull origin develop
```

Create a feature branch for your assigned task:

```cmd
git switch -c feature/YOUR-TASK-ID-description
```

Implement the changes and run the relevant tests.

Check modified files:

```cmd
git status
git diff --check
```

Stage only the files required for the task:

```cmd
git add path/to/changed-file
```

Commit:

```cmd
git commit -m "type: short description"
```

Push the feature branch:

```cmd
git push -u origin feature/YOUR-TASK-ID-description
```

Then open a Pull Request targeting `develop`.

Use the repository's Pull Request template and request the assigned peer reviewer.

Do not merge unreviewed changes or include credentials in commits.

If you have uncommitted changes, save or resolve them before switching branches or pulling updates.

## 15. Known Issues and Troubleshooting

### Incorrect Python Version

Activate `.venv` and verify:

```cmd
python --version
```

If the environment was created using the wrong Python version, recreate it using Python 3.12.

### Missing Python Module

Verify the virtual environment is active and run:

```cmd
python -m pip install -r requirements\dev.txt
```

### Missing DJANGO_SECRET_KEY

Verify that `.env` exists in the project root and includes `DJANGO_SECRET_KEY`.

### Missing Database Variable

If Django reports `KeyError: 'DB_NAME'` or another missing database variable, check the `.env` configuration.

### Database Connection Failure

Verify the Supabase Session Pooler host, username, password, port, SSL mode, and internet connection.

### Port 8000 Already in Use

Stop the other development server or start Django on a different local port:

```cmd
python backend\manage.py runserver 8001
```

### Unapplied Migrations Warning

Some migrations may remain unapplied during initial development.

Do not execute shared-database migrations without approval.

### Root URL Returns 404

This is expected while the main application interface is under development.

Use `/api/health/` to verify the backend.

### Git Branch Does Not Contain Expected Files

Verify that the relevant Pull Request has been merged into `develop`.

Unmerged feature branches are not automatically included in the integration branch.

## 16. Current Implementation Status

### Implemented or Initially Verified

- Private GitHub repository and development workflow.
- Python 3.12 virtual environment.
- Django 5.2 backend.
- Health-check API.
- pytest-based automated testing.
- Supabase PostgreSQL connection.
- Basic pgvector similarity search.
- Initial Custom User Model.
- Preliminary database ERD.
- Initial Pydantic contracts.
- Eight passing automated tests.

### Pending Work

- Cross-team ERD and contract approval.
- Isolated PostgreSQL migration verification.
- Shared database schema migration approval.
- Full authentication and authorization workflows.
- Document processing and evidence extraction integration.
- Embedding generation and retrieval integration.
- Complete RAG question-answering pipeline.
- End-to-end private/shared document isolation tests.

## 17. Development Notes and Team Rules

- Use feature branches for assigned tasks.
- Submit changes through Pull Requests.
- Keep credentials outside version control.
- Do not modify the shared database schema without approval.
- Use only public, synthetic, or authorized engineering documents.
- Maintain source references and document version metadata.
- Run relevant automated tests before requesting review.
- Document configuration changes, limitations, and test results.
- Coordinate changes to shared module contracts with affected team members.
