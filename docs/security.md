# Security Baseline

Security is a first-class subsystem, not a final cleanup task.

## Rules

1. Bind local services to localhost unless remote access is explicitly designed and authenticated.
2. Never commit API keys, passwords, cookies, private keys or personal tokens.
3. Validate every tool argument before execution.
4. Use allowlists for applications, directories and commands where possible.
5. Require explicit approval for impactful operations.
6. Keep dangerous capabilities disabled by default.
7. Record authorization and execution events without storing unnecessary sensitive payloads.
8. Fail closed when a tool or permission cannot be identified.
9. Separate planning from privileged execution.
10. Test denial paths as seriously as success paths.

## Threat model

The main risks are prompt injection, malicious or compromised external content, accidental destructive commands, excessive permissions, secret leakage, unsafe file access and unauthorized network exposure.

## Planned controls

- Structured tool schemas.
- Path canonicalization and directory boundaries.
- Command allowlists rather than arbitrary shell execution.
- Per-tool capability tokens.
- Approval UI with clear action summaries.
- Secret management through environment/configuration providers.
- Security-focused CI checks.
- Red-team tests for prompt injection and privilege escalation.

## Current limitation

Version 0.1 is a foundation. It does not yet provide LLM execution, voice, browser control or privileged Windows automation. Those capabilities must not be added by simply calling `subprocess` from a model-generated string.
