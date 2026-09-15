# Voice subsystem

JARVIS 0.6 uses a provider-neutral voice layer with explicit microphone access and privacy-first defaults.

## Current behavior

- Browser Speech Recognition remains the cross-platform STT fallback.
- Browser Speech Synthesis remains the cross-platform TTS fallback.
- Push-to-talk is explicit and enabled by default.
- Capability detection never opens an audio device.
- Audio is not persisted by the voice layer.
- Wake-word listening is not enabled yet.

## Windows TTS

Windows can optionally use the local SAPI5 synthesizer through `pyttsx3`:

```powershell
pip install -e ".[windows]"
```

The adapter is `app.voice_windows.WindowsSapiTTS`. It uses the installed Windows SAPI5 voice and does not send speech text to an external service.

The dependency is optional so Linux/macOS CI and development do not need Windows-specific packages.

## STT status

Native Windows speech recognition is intentionally not marked as available yet. The next implementation will use a bounded, explicit capture session and must preserve the same privacy guarantees before becoming the default.

## Safety rules

1. No always-on microphone capture.
2. No audio persistence unless a future feature explicitly requires it and the user enables it.
3. Capability detection never activates an audio device.
4. Voice providers receive bounded input.
5. Native providers are optional and isolated from the core application.
6. Wake-word support remains disabled until false-activation and privacy behavior are tested.
