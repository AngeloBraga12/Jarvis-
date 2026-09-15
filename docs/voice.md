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

## Windows native STT

Windows can optionally use `Windows.Media.SpeechRecognition` through the PyWinRT package `winrt-Windows.Media.SpeechRecognition`:

```powershell
pip install -e ".[windows]"
```

The adapter is `app.voice_windows_stt.WindowsSpeechRecognizer`. Its `recognize_once()` method starts one explicit recognition session, waits for one utterance, returns bounded text, and then ends the session. Constructing the provider does not activate the microphone.

This provider intentionally does not accept arbitrary raw audio bytes. Windows owns the microphone capture for this API, so the provider exposes an explicit recognition operation instead of pretending a byte buffer can be passed through unchanged.

The dependency is optional so Linux/macOS CI and development do not need Windows-specific packages.

## STT status

Native Windows STT is implemented as an optional provider but is not yet the automatic default. The browser implementation remains the fallback until the desktop push-to-talk path is integrated and tested on a real Windows machine.

Microsoft documents `Windows.Media.SpeechRecognition` for speech input and notes that its use requires package identity for the Windows application API. The current JARVIS adapter therefore remains an optional integration and does not claim universal compatibility with every Python launch mode.

## Safety rules

1. No always-on microphone capture.
2. No audio persistence unless a future feature explicitly requires it and the user enables it.
3. Capability detection never activates an audio device.
4. Native recognition is initiated only by an explicit call.
5. Recognized text is bounded before returning to the assistant.
6. Native providers are optional and isolated from the core application.
7. Wake-word support remains disabled until false-activation and privacy behavior are tested.
