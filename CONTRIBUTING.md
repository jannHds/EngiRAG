
# EngiRAG — Contribution Guidelines

## 1. Branching Strategy

- main: Stable, reviewed code.
- develop: Integration branch.
- feature/: New features and sprint tasks.
- fix/: Bug fixes.
- experiment/: AI research experiments.

## 2. Development Workflow

1. Pull the latest changes from develop.
2. Create a new branch from develop.
3. Implement the assigned task.
4. Test changes locally.
5. Commit changes with a descriptive message.
6. Push the branch to GitHub.
7. Open a Pull Request targeting develop.
8. Request a review from another team member.
9. Merge only after approval and successful tests.

## 3. Commit Naming

Use descriptive messages with task IDs.

Examples:
- feat(S1-02): initialize Django project
- test(S1-03): verify pgvector similarity search
- docs(S1-01): add contribution guidelines

## 4. Pull Request Rules

- Link the relevant Sprint task ID.
- Explain the changes made.
- Include testing evidence.
- Request at least one peer review.
- Resolve review comments before merging.
- Do not merge code with failing tests.

## 5. Security

- Never commit API keys or passwords.
- Never commit .env files.
- Use .env.example for configuration examples.
- Do not upload confidential engineering documents.
- Keep private conversation data separate from shared data.

## 6. Integration

- Feature branches target develop.
- Only reviewed, tested changes move to main.
- Avoid direct commits to main.
- Coordinate database migrations before applying them
  to the shared Supabase database.
