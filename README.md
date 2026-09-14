# JARVIS

Personal AI assistant for Windows, designed around voice interaction, memory, vision, automation and secure tool execution.

> The project is intentionally built as a modular local-first assistant. Actions that can affect the system are permissioned and audited instead of being blindly executed by an LLM.

## Status

**Version:** 0.1.0 — Foundation

The current release establishes the orchestration core, permission model, audit trail, local API and system diagnostics. Voice, LLM integration, persistent memory, vision and Windows automation are planned for subsequent milestones.

## Goals

- Natural interaction through text and, later, voice.
- A tool-based architecture instead of unrestricted shell access.
- Explicit risk classification for every tool.
- Approval gates for sensitive operations.
- Auditability of assistant actions.
- Local-first handling of personal data wherever practical.
- Automated tests and security checks from the beginning.
- A clean architecture that can grow without turning into a pile of scripts.

## Architecture

```text
JARVIS
├── Orchestrator
│   ├── LLM adapter
│   ├── Memory
│   ├── Vision
│   └── Tool manager
│       ├── Windows
│       ├── Files
│       ├── Browser
│       ├── Git/GitHub
│       └── Terminal
├── Security
│   ├── Permission policy
│   ├── Approval flow
│   └── Audit log
└── Interfaces
    ├── CLI
    ├── Local API
    └── Voice UI (planned)
```

## Security model

Tools are classified as `safe`, `confirm` or `dangerous`.

- **Safe:** can execute without interactive approval.
- **Confirm:** requires an explicit approval decision.
- **Dangerous:** blocked by default and only becomes available through a future, deliberately designed authorization flow.

The assistant must never treat an LLM-generated instruction as equivalent to user authorization.

## Repository layout

```text
app/
  api/       Local HTTP interface
  core/      Agent orchestration and policies
  tools/     Controlled system capabilities
  memory/    Memory subsystem (planned)
  voice/     Speech subsystem (planned)
  vision/    Visual subsystem (planned)
tests/
  unit/      Isolated behavior tests
  security/  Permission and abuse-case tests
docs/        Architecture, security, development and roadmap
.github/     CI and repository automation
config/      Non-secret configuration examples
scripts/     Developer utilities
```

## Requirements

- Python 3.11+
- Windows is the primary target for automation; the foundation currently remains cross-platform.

## Development

Create a virtual environment and install the project in editable mode:

```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

Run the tests:

```bash
python -m pytest
```

Run the local API:

```bash
python -m app.api.server
```

The API listens on `127.0.0.1:8765` by default. It is intentionally bound to localhost.

## Roadmap

| Version | Focus |
|---|---|
| 0.1 | Core, permissions, audit, diagnostics |
| 0.2 | LLM adapter and conversational orchestration |
| 0.3 | Speech-to-text, text-to-speech and wake word |
| 0.4 | Persistent memory and user preferences |
| 0.5 | Screen capture and vision |
| 0.6 | Windows automation |
| 0.7 | Git and GitHub tools |
| 0.8 | Browser automation |
| 0.9 | Multimodal agent workflows |
| 1.0 | Stable personal assistant platform |

## Design principles

1. Least privilege.
2. Explicit authorization for impactful actions.
3. Observable behavior.
4. Deterministic tools around probabilistic reasoning.
5. Small modules with clear contracts.
6. Tests before expanding capabilities.
7. No secrets committed to Git.

## Documentation

- [Architecture](docs/architecture.md)
- [Security](docs/security.md)
- [Development](docs/development.md)
- [Tools](docs/tools.md)
- [Roadmap](docs/roadmap.md)
- [Changelog](CHANGELOG.md)

## License

MIT. See [LICENSE](LICENSE).
