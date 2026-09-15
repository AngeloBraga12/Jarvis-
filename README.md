# JARVIS

Personal AI assistant for Windows, designed around voice interaction, memory, vision, automation and secure tool execution.

> The project is intentionally built as a modular local-first assistant. Actions that can affect the system are permissioned and audited instead of being blindly executed by an LLM.

## Status

**Version:** 0.2.0 — Command Center

The current release adds the first real JARVIS interface: a clean local command center with voice-state visualization, microphone amplitude feedback, processing animation, spoken responses, system diagnostics and a safe command endpoint. The language model, persistent memory, vision and Windows automation remain deliberately separate milestones.

## Interface

The Command Center is designed to feel like a real desktop assistant rather than a generic AI chat screen:

- When JARVIS is listening, the interface shows an animated voice waveform driven by microphone amplitude.
- While JARVIS is processing, the central brain visualization activates individual regions.
- While JARVIS speaks, the visual state returns to the output waveform.
- System status and recent activity stay visible without taking over the main interaction.
- Voice recognition and speech synthesis use browser capabilities when available.
- The UI is served by the same localhost-only Python service, so there is no separate frontend server in the foundation release.

## Goals

- Natural interaction through text and voice.
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
    ├── Command Center (current)
    ├── Local API
    └── Voice subsystem (in progress)
```

## Security model

Tools are classified as `safe`, `confirm` or `dangerous`.

- **Safe:** can execute without interactive approval.
- **Confirm:** requires an explicit approval decision.
- **Dangerous:** blocked by default and only becomes available through a future, deliberately designed authorization flow.

The assistant must never treat an LLM-generated instruction as equivalent to user authorization.

The current `/command` endpoint is intentionally deterministic. Unsupported commands are acknowledged but never passed to a shell or arbitrary operating-system tool.

## Repository layout

```text
app/
  api/       Local HTTP interface and static UI server
  core/      Agent orchestration, command routing and policies
  tools/     Controlled system capabilities
  ui/        JARVIS Command Center
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
- A modern browser for voice recognition and speech synthesis.
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

Run the JARVIS Command Center:

```bash
python -m app.api.server
```

Then open `http://127.0.0.1:8765/` in a modern browser. The service is intentionally bound to localhost.

Voice input requires microphone permission in the browser. The microphone stream is requested only while listening and is stopped when recognition ends.

## Roadmap

| Version | Focus |
|---|---|
| 0.1 | Core, permissions, audit, diagnostics |
| 0.2 | Command Center UI and voice-state foundation |
| 0.3 | LLM adapter and conversational orchestration |
| 0.4 | Speech-to-text, text-to-speech and wake word |
| 0.5 | Persistent memory and user preferences |
| 0.6 | Screen capture and vision |
| 0.7 | Windows automation |
| 0.8 | Git and GitHub tools |
| 0.9 | Browser automation and multimodal workflows |
| 1.0 | Stable personal assistant platform |

## Design principles

1. Least privilege.
2. Explicit authorization for impactful actions.
3. Observable behavior.
4. Deterministic tools around probabilistic reasoning.
5. Small modules with clear contracts.
6. Tests before expanding capabilities.
7. No secrets committed to Git.
8. The interface should communicate state without pretending the assistant is magic.

## Documentation

- [Architecture](docs/architecture.md)
- [Security](docs/security.md)
- [Development](docs/development.md)
- [Tools](docs/tools.md)
- [Roadmap](docs/roadmap.md)
- [Changelog](CHANGELOG.md)

## License

MIT. See [LICENSE](LICENSE).
