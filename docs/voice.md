# Voice architecture

JARVIS 0.6 introduces a provider-neutral voice foundation. The current browser Speech Recognition and Speech Synthesis path remains the fallback because it requires no Windows-only dependency in CI.

Voice input is explicit: push-to-talk starts recognition, the microphone stream is stopped after recognition ends, and there is no always-on capture. Wake-word support is intentionally not enabled yet.

The next voice increment will add native Windows STT/TTS adapters behind optional dependencies. Windows-only packages must never become mandatory for the cross-platform test suite.

Privacy rules:

- microphone access is opt-in per interaction;
- no continuous recording is stored;
- audio is not written to audit logs;
- capability detection never opens an audio device;
- wake-word processing will require an explicit user preference before activation.
