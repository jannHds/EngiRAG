# EngiRAG

EngiRAG is a bilingual Engineering Knowledge Assistant
that uses Retrieval-Augmented Generation (RAG) to answer
engineering questions in Arabic and English.

The system retrieves information from engineering documents
and provides evidence-grounded answers with source citations.

## Technology Stack

- Python 3.12
- Django 5.2 LTS
- PostgreSQL 17 (Supabase)
- pgvector
- Multilingual Embedding Models

## Project Structure

- `backend/` - Django backend application
- `experiments/` - AI and RAG experiments
- `tests/` - Automated and integration tests
- `docs/` - Architecture and sprint documentation
- `scripts/` - Development utilities
- `requirements/` - Python dependencies

## Development Workflow

- `main` - Stable reviewed code
- `develop` - Integration branch
- `feature/*` - Individual development tasks
- `fix/*` - Bug fixes
- `experiment/*` - Research experiments

## Development Status

Sprint 1: Foundation, Dataset & Feasibility

Current focus:
- Repository and collaboration setup
- Django environment configuration
- PostgreSQL and pgvector feasibility
- Initial RAG retrieval integration

## Security

Only public, synthetic, or authorized engineering
documents may be used.

Credentials, API keys, and private environment
configuration must not be committed to Git.


## Development Setup

For installation and configuration instructions,
see [Environment Setup Guide](docs/ENVIRONMENT_SETUP.md).