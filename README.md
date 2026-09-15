# JARVIS

Personal AI assistant designed around voice interaction, memory, vision, automation and secure tool execution, with Windows as the initial execution host and Android as a native client.

> The project is intentionally built as a modular local-first assistant. Actions that can affect the system are permissioned and audited instead of being blindly executed by an LLM.

## Status

**Version:** 0.6.1 — Voice foundation + Android client foundation

JARVIS has a provider-neutral voice layer, explicit speech-to-text and text-to-speech contracts, capability detection, push-to-talk behavior and privacy-safe defaults. A native Android client foundation now lives under `android/`.

## Platform architecture

Windows remains the primary execution host. Android is a client and will use the same orchestration, model, tool registry, permission and approval boundaries through a dedicated authenticated gateway.

```text
                    JARVIS Core / Host
          LLM | Memory | Permissions | Tools
                    /            \
               Windows         Android
             execution host       client
```

The Android client does not receive the LLM API key and does not connect directly to the current localhost-only Windows service. Secure pairing and an authenticated gateway must exist before remote command execution is enabled.

## Voice foundation

The current voice model is explicit push-to-talk. Microphone access is requested only during an active listening interaction and the stream is stopped when recognition ends. There is no continuous capture, audio persistence or audio content in audit logs.

Browser speech remains the cross-platform fallback. Native Windows and Android voice adapters are isolated from the core application.

See [Voice architecture](docs/voice.md) and [Android client](docs/android.md).

## Interface

The Command Center provides listening, processing and speaking visual states, a central processing visualization, activity feed, system diagnostics and explicit approval dialogs.

The Android client uses Jetpack Compose and currently provides a native Command Center foundation with explicit push-to-talk, Android speech recognition and local text-to-speech.

## Language model

The backend uses the OpenAI Responses API through a provider abstraction. The browser and Android client never receive the API key. Configure `OPENAI_API_KEY` and `JARVIS_MODEL` in the host environment before starting the service.

The current conversation remains in bounded process memory and is cleared on restart. Responses API requests use `store=False`.

## Tool and approval model

The model can only see tools explicitly returned by `app.core.tool_registry`. Tool execution always passes through the authorization layer.

Current tools are read-only system status, read-only system health, current time and an allowlisted Windows application launcher that requires confirmation. Arbitrary shell execution, file deletion and unregistered tools remain blocked.

## Requirements

- Python 3.11+
- OpenAI API key for conversational mode
- Modern browser for the current voice fallback
- Windows for the current native execution and Windows voice targets
- Android Studio for the native Android client

## Development

### Host

```bash
python -m venv .venv
# Windows PowerShell
.\\.venv\\Scripts\\Activate.ps1
pip install -e ".[dev]"
python -m pytest
python -m app.api.server
```

The service is intentionally bound to `127.0.0.1`.

### Android

Open the `android/` directory in Android Studio and sync the Gradle project. The current client is intentionally not paired with the Windows host yet.

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

### Parallel Android track

- A0 | Native Android project and Command Center foundation — started
- A1 | Authenticated device identity and pairing
- A2 | Secure Windows gateway
- A3 | Command and response transport through the existing permission boundary
- A4 | Android approval flow and notifications
- A5 | Device management, revocation and connection health
- A6 | Android-specific integrations and wake-word research

## Documentation

- [Architecture](docs/architecture.md)
- [Security](docs/security.md)
- [Development](docs/development.md)
- [LLM integration](docs/llm.md)
- [Voice architecture](docs/voice.md)
- [Android client](docs/android.md)
- [Tools](docs/tools.md)
- [Roadmap](docs/roadmap.md)
- [Changelog](CHANGELOG.md)

## License

MIT. See [LICENSE](LICENSE).
