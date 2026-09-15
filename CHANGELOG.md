# Changelog

All notable changes to this project are documented here.

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
