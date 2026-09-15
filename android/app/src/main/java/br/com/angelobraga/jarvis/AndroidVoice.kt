package br.com.angelobraga.jarvis

import android.content.Context
import android.content.Intent
import android.os.Bundle
import android.speech.RecognitionListener
import android.speech.RecognizerIntent
import android.speech.SpeechRecognizer
import android.speech.tts.TextToSpeech
import java.util.Locale

class AndroidVoice(private val context: Context) {
    private var recognizer: SpeechRecognizer? = null
    private var tts: TextToSpeech? = null

    fun speak(text: String) {
        if (text.isBlank() || text.length > 2000) return
        if (tts == null) {
            tts = TextToSpeech(context) { status ->
                if (status == TextToSpeech.SUCCESS) {
                    tts?.language = Locale("pt", "BR")
                    tts?.speak(text, TextToSpeech.QUEUE_FLUSH, null, "jarvis-response")
                }
            }
        } else {
            tts?.speak(text, TextToSpeech.QUEUE_FLUSH, null, "jarvis-response")
        }
    }

    fun listen(onResult: (String) -> Unit, onError: (String) -> Unit) {
        if (!SpeechRecognizer.isRecognitionAvailable(context)) {
            onError("Reconhecimento de voz indisponível neste dispositivo")
            return
        }
        recognizer?.destroy()
        recognizer = SpeechRecognizer.createSpeechRecognizer(context).apply {
            setRecognitionListener(object : RecognitionListener {
                override fun onReadyForSpeech(params: Bundle?) = Unit
                override fun onBeginningOfSpeech() = Unit
                override fun onRmsChanged(rmsdB: Float) = Unit
                override fun onBufferReceived(buffer: ByteArray?) = Unit
                override fun onEndOfSpeech() = Unit
                override fun onPartialResults(partialResults: Bundle?) = Unit
                override fun onEvent(eventType: Int, params: Bundle?) = Unit

                override fun onResults(results: Bundle?) {
                    val text = results?.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION)
                        ?.firstOrNull()
                    if (text.isNullOrBlank()) onError("Não foi possível reconhecer a fala")
                    else onResult(text.take(1000))
                    destroyRecognizer()
                }

                override fun onError(error: Int) {
                    onError("Falha no reconhecimento de voz: código $error")
                    destroyRecognizer()
                }
            })
            startListening(Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH).apply {
                putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
                putExtra(RecognizerIntent.EXTRA_LANGUAGE, "pt-BR")
                putExtra(RecognizerIntent.EXTRA_MAX_RESULTS, 1)
                putExtra(RecognizerIntent.EXTRA_PARTIAL_RESULTS, false)
            })
        }
    }

    private fun destroyRecognizer() {
        recognizer?.destroy()
        recognizer = null
    }

    fun release() {
        destroyRecognizer()
        tts?.stop()
        tts?.shutdown()
        tts = null
    }
}
