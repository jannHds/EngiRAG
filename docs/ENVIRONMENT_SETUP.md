# EngiRAG — Development Environment Setup Guide

## 1. Overview

This guide explains how to set up the EngiRAG backend
development environment on Windows.

## 2. Technology Stack

- Python 3.12.10
- Django 5.2.19 LTS
- pytest 9.2.0
- pytest-django 4.14.0
- Pydantic
- python-dotenv
- PostgreSQL 17 with pgvector (Supabase)

## 3. Prerequisites

Install the following tools:

- Python 3.12
- Git
- Visual Studio Code

## 4. Clone the Repository

Clone the private EngiRAG repository from GitHub.

Open the project folder in VS Code.

## 5. Create a Virtual Environment

From the project root, run:

    py -3.12 -m venv .venv

Activate the environment in Windows CMD:

    .venv\Scripts\activate.bat

Verify the Python version:

    python --version

## 6. Install Dependencies

Install the required packages:

    python -m pip install -r requirements\dev.txt

Check dependency compatibility:

    python -m pip check

## 7. Configure Environment Variables

Create a .env file in the project root.

Add the following configuration:

    DJANGO_SECRET_KEY=your-generated-secret-key
    DJANGO_DEBUG=True

Generate a secret key using:

    python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

Replace the placeholder with the generated key.

Never commit the .env file to GitHub.

Database credentials will be configured separately
when the shared PostgreSQL connection is integrated.

## 8. Run Django

Check the Django configuration:

    python backend\manage.py check

Start the development server:

    python backend\manage.py runserver

Open:

http://127.0.0.1:8000/api/health/

Expected response:

    {"status": "ok", "service": "EngiRAG Backend"}

## 9. Run Automated Tests

From the project root, run:

    python -m pytest -v

The initial smoke test verifies the health endpoint.

## 10. Database Configuration

The team uses a shared PostgreSQL database hosted
on Supabase, with the pgvector extension enabled.

Database connectivity and Django migrations will
be tested separately during S1-03.

## 11. Known Issues and Troubleshooting

- Wrong Python version:
  Activate the virtual environment.

- Missing module:
  Install packages from requirements/dev.txt.

- Missing DJANGO_SECRET_KEY:
  Check the local .env file.

- Port 8000 already in use:
  Stop the other development server.

- Unapplied migrations:
  Complete database configuration before applying
  migrations to the shared database.

## 12. Development Notes

- Use feature branches for development tasks.
- Submit changes through Pull Requests.
- Keep credentials outside version control.
- Use only public, synthetic, or authorized documents.
- Document configuration changes and test results.