# Contributing

## Workflow

1. Create a focused branch.
2. Make the smallest coherent change.
3. Add or update tests.
4. Run `ruff check .` and `python -m pytest` locally.
5. Update documentation when behavior or architecture changes.
6. Open a pull request with a concise description and risk notes.

## Security-sensitive changes

Changes involving filesystem access, process execution, credentials, network access, browser sessions, or user data require explicit security reasoning and tests for denial/failure paths.

Do not include secrets, personal tokens, private data or real credentials in commits, examples or tests.
