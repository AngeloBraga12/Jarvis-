# JARVIS

Personal AI assistant for Windows, designed around voice interaction, memory, vision, automation and secure tool execution.

> The project is intentionally built as a modular local-first assistant. Actions that can affect the system are permissioned and audited instead of being blindly executed by an LLM.

## Status

**Version:** 0.4.0 — Permissioned Tools

The current release connects the Command Center to an OpenAI Responses API provider and adds a real tool boundary. JARVIS can use read-only system tools and can request allowlisted application launches, but impactful actions stop at an explicit approval dialog before execution.

## Interface

The Command Center is designed to feel like a real desktop assistant rather than a generic AI chat screen:

- When JARVIS is listening, the interface shows an animated voice waveform driven by microphone amplitude.
- While JARVIS is processing, the central brain visualization activates individual regions.
- While JARVIS speaks, the visual state returns to the output waveform.
- Approval-required actions appear as a focused confirmation dialog instead of silently running.
- System status and recent activity stay visible without taking over the main interaction.
- Voice recognition and speech synthesis use browser capabilities when available.
- The UI is served by the same localhost-only Python service.
- The connection indicator reports whether the language model is configured.

## Language model

The backend uses the OpenAI Responses API through a small provider abstraction. The browser never receives the API key.

Set the environment before starting JARVIS:

```text
OPENAI_API_KEY=your_key_here
JARVIS_MODEL=gpt-5.6-luna
```

Run:

```bash
python -m app.api.server
```

Then open `http://127.0.0.1:8765/`.

The current conversation is kept only in bounded process memory. The Responses API request uses `store=False`. Restarting JARVIS clears the conversation.

See [LLM integration](docs/llm.md) for the data flow and security boundary.

## Tool and approval model

The model can only see tools explicitly returned by `app.core.tool_registry`. Tool execution always passes through `Agent.authorize()`.

Current tools:

- `system_status`: read-only diagnostics, safe.
- `current_time`: read-only local/UTC time, safe.
- `open_application`: allowlisted Windows applications only, confirmation required.

The application launcher accepts only `notepad`, `calculator` and `explorer`. It never accepts arbitrary executable paths, shell fragments or command strings. Approval requests live only in process memory and are single-use.

Dangerous tools such as arbitrary shell execution and file deletion remain blocked and are not exposed to the model.

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
│   ├── LLM provider
│   ├── Conversation memory
│   ├── Vision
│   └── Tool manager
│       ├── Windows
│       ├── Files
│       ├── Browser
│       ├── Git/GitHub
│       └── Terminal
├── Security
│   ├── Permission policy
│   ├── Approval store
│   └── Audit log
└── Interfaces
    ├── Command Center
    ├── Local API
    └── Voice subsystem
```

## Security model

Tools are classified as `safe`, `confirm` or `dangerous`.

- **Safe:** can execute without interactive approval.
- **Confirm:** creates a short-lived approval request and waits for an explicit user decision.
- **Dangerous:** blocked by default and never becomes executable merely because an LLM requested it.

The assistant must never treat an LLM-generated instruction as equivalent to user authorization.

The `/command` endpoint validates and bounds requests before routing them. Natural-language requests go to the configured language provider and never become shell commands automatically. The `/approval` endpoint consumes a server-generated request ID and can execute only the exact pending, allowlisted operation.

## Repository layout

```text
app/
  api/       Local HTTP interface and static UI server
  core/      Agent orchestration, command routing, conversation, approvals and policies
  providers/ LLM provider adapters
  tools/     Controlled system capabilities
  ui/        JARVIS Command Center
  memory/    Persistent memory subsystem (planned)
  voice/     Speech subsystem
  vision/    Visual subsystem (planned)
tests/
  unit/      Isolated behavior tests
  security/  Permission and abuse-case tests
docs/        Architecture, security, development, LLM and roadmap documentation
.github/     CI and repository automation
config/      Non-secret configuration examples
scripts/     Developer utilities
```

## Requirements

- Python 3.11+
- An OpenAI API key for conversational mode.
- A modern browser for voice recognition and speech synthesis.
- Windows is the primary target for application automation; the foundation remains cross-platform.

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
| 0.4 | Permissioned tool calls and explicit approval UI |
| 0.5 | Native speech pipeline, wake word and richer Windows diagnostics |
| 0.6 | Persistent memory and user preferences |
| 0.7 | Screen capture and vision |
| 0.8 | Windows automation, Git and GitHub tools |
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
- [LLM integration](docs/llm.md)
- [Tools](docs/tools.md)
- [Roadmap](docs/roadmap.md)
- [Changelog](CHANGELOG.md)

## License

MIT. See [LICENSE](LICENSE).
