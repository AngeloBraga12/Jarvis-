# Changelog

All notable changes to this project are documented here.

## [0.6.0] - 2026-09-15

### Added
- Provider-neutral speech-to-text and text-to-speech interfaces.
- Voice capability detection that does not open audio devices.
- Explicit push-to-talk interaction model and browser voice fallback.
- Voice privacy policy with no continuous capture and no audio storage by default.
- Read-only `/voice/capabilities` endpoint.
- Voice architecture documentation and automated interface/capability tests.

### Security
- Native voice integrations are not falsely reported as available before their adapters exist.
- Microphone activation remains explicit and interaction-scoped.
- Wake-word processing is disabled until a future explicit preference flow exists.
- Audio content is not sent to audit logs or persisted by the voice foundation.

## [0.5.0] - 2026-09-15

### Added
- Read-only `system_health` tool for richer local diagnostics.
- CPU count, architecture, Python version, disk capacity and load-average reporting where the platform provides it.
- Security tests covering the new diagnostic tool and model-visible registry.

### Security
- `system_health` is classified as safe and accepts no arguments.
- Diagnostic output is limited to technical runtime information and does not collect user files, prompts or secrets.
- The model still cannot access arbitrary shell, file deletion or unregistered capabilities.

## [0.4.0] - 2026-09-15

### Added
- Explicit model-visible tool registry.
- Read-only `current_time` tool.
- Allowlisted Windows application launcher for Notepad, Calculator and Explorer.
- Ephemeral, single-use approval requests.
- Local `/approval` endpoint for approve/deny decisions.
- Command Center approval dialog for confirm-risk actions.
- Security tests covering approval bypass and dangerous-tool blocking.

### Security
- Confirm-risk tools cannot execute without an explicit approval decision.
- Approval requests are stored only in process memory and are consumed once.
- The application launcher accepts an enum of fixed application names, never arbitrary paths or shell strings.
- Dangerous tools remain blocked even when `approved=True` is supplied.
- The model receives only explicitly registered tools.

## [0.3.0] - 2026-09-15

### Added
- OpenAI Responses API provider behind a vendor-neutral LLM interface.
- Server-side model configuration through `OPENAI_API_KEY` and `JARVIS_MODEL`.
- Bounded in-memory conversation context for multi-turn interaction.
- Natural-language routing from the Command Center to the language model.
- Live LLM connection status in the UI.
- Fail-closed behavior when the LLM is unavailable or not configured.
- Unit tests for provider routing, context preservation and missing-provider behavior.

### Security
- API credentials remain exclusively in the Python backend.
- Browser code never receives the provider API key.
- OpenAI Responses requests explicitly use `store=False`.
- Conversation memory is not persisted to disk.
- Conversation reset is exposed only as an explicit POST action.
- LLM failures cannot fall through to arbitrary operating-system commands.

## [0.2.0] - 2026-09-15

### Added
- Clean JARVIS Command Center interface served locally by the Python backend.
- Voice-state visualizer with listening and speaking waveform states.
- Animated brain visualization with stimulated regions during processing.
- Browser Speech Recognition integration when supported by the client.
- Browser Speech Synthesis integration for spoken responses.
- Safe `/command` endpoint with bounded request size and deterministic routing.
- Live system diagnostics in the interface.
- Activity feed for commands and system events.
- Unit coverage for safe command routing.

### Security
- UI is served only by the existing localhost service.
- Command requests are size-limited and validated before routing.
- Unsupported commands never execute arbitrary operating-system actions.
- Existing permission and audit layers remain in force.

## [0.1.0] - 2026-09-14

### Added
- Modular JARVIS foundation.
- Permission and risk policy.
- Append-only JSONL audit log.
- Read-only system diagnostics.
- Localhost HTTP API with health and system endpoints.
- Initial unit tests for authorization behavior.
- Architecture, security, development, tools and roadmap documentation.
