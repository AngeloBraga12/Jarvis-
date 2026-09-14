# Development Guide

## Local setup

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

## Quality checks

```bash
python -m pytest
ruff check .
```

## Principles for new tools

Every tool should have:

- A narrow responsibility.
- Typed inputs and outputs.
- A declared risk level.
- Validation before execution.
- Unit tests for success and denial cases.
- No implicit privilege escalation.
- Minimal logging of sensitive information.

## Branching

Use short-lived branches named by purpose, for example:

```text
feat/voice-input
feat/windows-tools
fix/path-validation
security/prompt-injection-tests
```

Commit messages should describe the change clearly and avoid mixing unrelated modifications.

## Definition of done

A capability is not considered complete until its implementation, tests, security behavior, documentation and failure paths have been reviewed.
