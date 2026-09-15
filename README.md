# JARVIS

Personal AI assistant for Windows, designed around voice interaction, memory, vision, automation and secure tool execution.

> The project is intentionally built as a modular local-first assistant. Actions that can affect the system are permissioned and audited instead of being blindly executed by an LLM.

## Status

**Version:** 0.6.0 — Voice Foundation

JARVIS now has a provider-neutral voice layer with explicit speech-to-text and text-to-speech contracts, capability detection, push-to-talk behavior and privacy-safe defaults. Browser speech remains the current fallback while native Windows adapters are developed separately.

## Voice foundation

The current voice model is explicit push-to-talk. Microphone access is requested only during an active listening interaction and the stream is stopped when recognition ends. There is no continuous capture, audio persistence or audio content in audit logs.

Native Windows STT/TTS are not claimed as available until their adapters are actually implemented. Wake-word processing is also disabled until a future explicit preference flow exists.

The read-only `GET /voice/capabilities` endpoint reports the implemented voice targets without opening audio devices.

See [Voice architecture](docs/voice.md).

## Interface

The Command Center provides listening, processing and speaking visual states, a central processing visualization, activity feed, system diagnostics and explicit approval dialogs. Voice recognition and speech synthesis currently use browser capabilities when available.

## Language model

The backend uses the OpenAI Responses API through a provider abstraction. The browser never receives the API key. Configure `OPENAI_API_KEY` and `JARVIS_MODEL` in the environment before starting the service.

The current conversation remains in bounded process memory and is cleared on restart. Responses API requests use `store=False`.

## Tool and approval model

The model can only see tools explicitly returned by `app.core.tool_registry`. Tool execution always passes through the authorization layer.

Current tools are read-only system status, read-only system health, current time and an allowlisted Windows application launcher that requires confirmation. Arbitrary shell execution, file deletion and unregistered tools remain blocked.

## Requirements

- Python 3.11+
- OpenAI API key for conversational mode
- Modern browser for the current voice fallback
- Windows is the primary target for native voice and application automation

## Development

```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
python -m pytest
python -m app.api.server
```

The service is intentionally bound to `127.0.0.1`.

## Roadmap

| Version | Focus |
|---|---|
| 0.1 | Core, permissions, audit, diagnostics |
| 0.2 | Command Center UI and voice-state foundation |
| 0.3 | LLM adapter and conversational orchestration |
| 0.4 | Permissioned tool calls and approval UI |
| 0.5 | Rich read-only system diagnostics |
| 0.6 | Voice abstraction, privacy-safe push-to-talk and capability detection |
| 0.7 | Persistent memory with privacy controls |
| 0.8 | Screen capture and vision |
| 0.9 | Windows automation, Git, GitHub and browser tools |
| 1.0 | Stable personal assistant platform |

## Documentation

- [Architecture](docs/architecture.md)
- [Security](docs/security.md)
- [Development](docs/development.md)
- [LLM integration](docs/llm.md)
- [Voice architecture](docs/voice.md)
- [Tools](docs/tools.md)
- [Roadmap](docs/roadmap.md)
- [Changelog](CHANGELOG.md)

## License

MIT. See [LICENSE](LICENSE).
