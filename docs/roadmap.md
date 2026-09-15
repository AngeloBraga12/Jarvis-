# Roadmap

## 0.1 Foundation
- [x] Modular Python application
- [x] Risk classification
- [x] Approval gate model
- [x] Audit logging
- [x] Read-only system diagnostics
- [x] Local API
- [x] Unit tests

## 0.2 Command Center
- [x] Desktop-style local interface
- [x] Listening/thinking/speaking visual states
- [x] Browser speech recognition and synthesis
- [x] Bounded command API
- [x] Approval dialog

## 0.3 LLM
- [x] Provider-neutral LLM adapter
- [x] OpenAI Responses API integration
- [x] Structured tool calling
- [x] Bounded conversation state
- [x] Model failure handling
- [x] Server-side API key isolation

## 0.4 Permissioned tools
- [x] Explicit model-visible tool registry
- [x] Safe/confirm/dangerous risk classes
- [x] Allowlisted application launch
- [x] Single-use approval requests
- [x] Approval expiration
- [x] Fail-closed unknown-tool handling
- [x] Security tests for model/tool boundary

## 0.5 System diagnostics
- [x] Basic OS and disk diagnostics
- [x] Read-only system health metrics
- [x] CPU, architecture and Python runtime information
- [x] Load-average reporting where supported
- [x] `/system/health` endpoint

## 0.6 Voice foundation
- [x] Provider-neutral speech-to-text interface
- [x] Provider-neutral text-to-speech interface
- [x] Voice capability detection without opening audio devices
- [x] Push-to-talk as the explicit interaction model
- [x] Browser STT/TTS fallback remains available
- [x] Privacy-safe defaults: no continuous capture or audio storage
- [x] `/voice/capabilities` endpoint
- [ ] Native Windows speech-to-text adapter
- [ ] Native Windows text-to-speech adapter
- [ ] User-approved voice preferences
- [ ] Wake-word adapter

## 0.7 Persistent memory
- [ ] Explicit memory opt-in
- [ ] Local encrypted storage
- [ ] Memory deletion and export
- [ ] Per-category retention controls
- [ ] Memory audit events without storing unnecessary content

## 0.8 Vision
- [ ] Screenshot capture
- [ ] OCR
- [ ] Visual reasoning adapter
- [ ] Explicit screen-sharing boundaries

## 0.9 Windows automation and integrations
- [ ] Application discovery
- [ ] Safe window management
- [ ] Controlled filesystem operations
- [ ] Git/GitHub tools
- [ ] Browser session isolation
- [ ] Confirmation for purchases, submissions and account changes

## 1.0 Multimodal assistant
- [ ] Combined voice + vision + tools
- [ ] Long-running task state
- [ ] Recovery and retry policies
- [ ] Security review
- [ ] Reliability benchmark
- [ ] Full test suite
- [ ] Documentation review
- [ ] Stable release
