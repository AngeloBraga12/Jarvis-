# JARVIS

Personal AI assistant for Windows, designed around voice interaction, memory, vision, automation and secure tool execution.

> The project is intentionally built as a modular local-first assistant. Actions that can affect the system are permissioned and audited instead of being blindly executed by an LLM.

## Status

**Version:** 0.5.0 — System Diagnostics

The current release connects the Command Center to an OpenAI Responses API provider and maintains a real tool boundary. JARVIS can inspect the local system through read-only diagnostics and can request allowlisted application launches, but impactful actions stop at an explicit approval dialog before execution.

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

- `system_status`: read-only basic diagnostics, safe.
- `system_health`: read-only technical health metrics, safe.
- `current_time`: read-only local/UTC time, safe.
- `open_application`: allowlisted Windows applications only, confirmation required.

The system-health tool reports platform, architecture, Python version, CPU count, disk capacity and load average where the operating system provides it. It does not read user files or collect prompts.

The application launcher accepts only `notepad`, `calculator` and `explorer`. It never accepts arbitrary executable paths, shell fragments or command strings. Approval requests live only in process memory, expire after five minutes and are single-use.

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
│       └── Git/GitHub
├── Security
│   ├── Permission policy
│   ├── Approval store
│   └── Audit log
└── Interfaces
    ├── Command Center
    ├── Local API
    └── Voice subsystem
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
| 0.5 | Rich read-only system diagnostics |
| 0.6 | Native speech pipeline, wake word and user preferences |
| 0.7 | Persistent memory with privacy controls |
| 0.8 | Screen capture and vision |
| 0.9 | Windows automation, Git, GitHub and browser tools |
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
