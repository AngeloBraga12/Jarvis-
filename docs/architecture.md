# Architecture

## Overview

JARVIS separates reasoning from execution. The model may propose an action, but deterministic application code decides whether the requested tool exists, what risk it carries, whether approval is required and how the action is executed.

## Layers

### Interface
Receives text, voice or future multimodal input and presents results.

### Orchestrator
Maintains conversation state, selects tools and coordinates execution. It must not bypass security policy.

### Tool manager
Exposes narrowly scoped capabilities with typed inputs and predictable outputs.

### Security
Applies least privilege, approval gates and audit logging.

### Memory
Stores only information needed for useful continuity. Sensitive memory should be minimized, protected and removable.

## Execution contract

```text
User intent
   ↓
LLM / planner
   ↓
Tool request
   ↓
Schema validation
   ↓
Risk policy
   ├── safe → execute
   ├── confirm → request approval → execute/deny
   └── dangerous → deny by default
   ↓
Audit event
   ↓
Result
```

## Non-goals

JARVIS will not begin as an unrestricted autonomous agent, a remote administration service, or a process that silently executes arbitrary shell commands. Those designs are convenient until the first typo deletes something important, which is a remarkably human way to discover access control.
