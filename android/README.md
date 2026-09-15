# JARVIS Android

Native Android client for JARVIS.

The Android app is a client, not the execution host. It will use the same permissioned JARVIS backend and will never receive the LLM API key.

Initial scope:

- Jetpack Compose Command Center
- explicit push-to-talk
- Android SpeechRecognizer STT
- Android TextToSpeech TTS
- secure device pairing protocol
- authenticated communication with the JARVIS host

Remote access is intentionally not enabled by this first scaffold. The Windows service currently binds to localhost, so exposing it directly to a phone would bypass the security boundary. A dedicated authenticated gateway will be added before network commands are enabled.
