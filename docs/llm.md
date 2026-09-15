# JARVIS language-model integration

The Command Center sends natural-language commands to the JARVIS backend. The browser never receives the provider API key.

## Configuration

Set the following environment variables before starting the server:

```text
OPENAI_API_KEY=...
JARVIS_MODEL=gpt-5.6-luna
```

The default model can be changed without modifying source code.

## Data flow

```text
Browser UI
   ↓ POST /command
Local JARVIS API
   ↓
Deterministic safe-command router
   ↓ if not a local tool
Bounded in-memory conversation
   ↓
OpenAI Responses API
   ↓ store=false
JARVIS response
   ↓
Browser speech synthesis
```

Conversation context is held only in memory by the local process and is bounded to the most recent turns. The OpenAI request explicitly uses `store=False` so the application does not ask the Responses API to persist response state.

## Security boundary

- `OPENAI_API_KEY` is read only by the Python backend.
- The key is never sent to browser JavaScript.
- The local HTTP server remains bound to `127.0.0.1` by default.
- Unknown natural-language requests are sent only to the configured language provider; they do not become shell commands.
- Operating-system tools remain behind the existing permission layer.
- LLM failures fail closed and do not execute a fallback operating-system command.
- Audit events record the provider response boundary without writing the prompt or API key to the audit log.
