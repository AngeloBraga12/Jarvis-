# Tool Registry

| Tool | Risk | Status | Purpose |
|---|---|---|---|
| `system_status` | safe | active | Read-only runtime diagnostics |
| `open_application` | confirm | planned | Launch an approved application |
| `read_file` | confirm | planned | Read a user-approved file |
| `write_file` | confirm | planned | Write to a user-approved location |
| `execute_command` | dangerous | blocked | Arbitrary command execution |
| `delete_file` | dangerous | blocked | Destructive filesystem operation |

Unknown tools default to `confirm` rather than being treated as safe.

## Adding a tool

1. Implement the smallest possible capability.
2. Register its risk level.
3. Validate all arguments.
4. Add tests for allowed, denied and malformed requests.
5. Add audit events.
6. Document data access and side effects.
7. Keep dangerous behavior disabled until its authorization model is complete.
