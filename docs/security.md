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

## Current controls in v0.4

- The HTTP service binds to `127.0.0.1` by default.
- The browser never receives the OpenAI API key.
- The model sees only explicitly registered tools.
- Unknown tools are blocked without generating an approval request.
- Tool arguments are validated before authorization and execution.
- `open_application` uses a fixed Windows allowlist and explicit approval.
- Dangerous capabilities such as arbitrary shell execution and file deletion remain blocked.
- Approval requests are single-use, in-memory and expire after five minutes.
- Approval responses do not expose the stored tool arguments to the browser.
- Audit entries record security events without storing prompts or API keys.
- Tool execution failures are converted into safe error responses instead of escaping into the HTTP handler.

## Threat model

The main risks are prompt injection, malicious or compromised external content, accidental destructive commands, excessive permissions, secret leakage, unsafe file access and unauthorized network exposure.

## Planned controls

- Path canonicalization and directory boundaries for future file tools.
- Command allowlists rather than arbitrary shell execution.
- Per-tool capability tokens.
- Native speech/wake-word security boundaries.
- Secret management through environment/configuration providers.
- Security-focused CI checks.
- Red-team tests for prompt injection and privilege escalation.

## Important limitation

JARVIS is still a local development platform, not a general-purpose autonomous operating-system agent. The current tool surface is intentionally small. New capabilities must be added through an explicit schema, permission policy, argument validation, execution handler and security tests. A model-generated string must never become an implicit shell command or privileged operation.
