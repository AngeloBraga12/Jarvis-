# Android client

JARVIS now has a native Android client foundation under `android/`.

## Architecture

Android is a client, not the execution host. The Windows/local JARVIS service remains responsible for orchestration, LLM access, permissions, approvals and system tools.

The Android client is responsible for:

- Command Center UI
- explicit push-to-talk interaction
- Android SpeechRecognizer STT
- Android TextToSpeech TTS
- device identity held by Android Keystore
- authenticated pairing proof without exporting the private key
- presenting approvals and responses without receiving provider secrets

Jetpack Compose is used for the native UI. Android's `SpeechRecognizer` requires `RECORD_AUDIO` permission and is explicitly started by the user; it is not used for continuous recognition. Android documentation also notes that the recognition implementation may stream audio to a remote service, so JARVIS treats it as an explicit user interaction rather than an always-on microphone.

## Security boundary

The current Windows service is intentionally bound to `127.0.0.1`. The Android client therefore does not attempt to connect to it yet.

The Android identity uses an EC key pair stored in Android Keystore. The public key can be identified by a SHA-256 fingerprint, while pairing challenges are signed locally with `SHA256withECDSA`; the private key is never exported to the app's network layer.

The current pairing layer is protocol material only. It performs no network operation and does not establish trust by itself. Before network commands are enabled, JARVIS will add a dedicated authenticated gateway with:

1. device identity
2. explicit pairing approval on the trusted host
3. revocable device state
4. TLS transport
5. bounded request schemas
6. server-side signature verification and authorization
7. approval propagation
8. audit events without prompts or secrets

The Android client must never receive `OPENAI_API_KEY` or any provider credential.

## Initial UX

The first Android screen deliberately exposes only the safe local voice interaction foundation. A command can be recognized and spoken back locally, but execution against Windows remains disabled until secure pairing exists. This prevents the common human tradition of calling an unauthenticated LAN endpoint a security architecture.

## Next stages

- trusted-host pairing approval and revocation
- secure gateway on the Windows host
- command transport using the existing tool/approval boundary
- Android approval notifications
- connection status and device management
- optional encrypted local preferences
- later: Android-specific integrations and wake-word research
