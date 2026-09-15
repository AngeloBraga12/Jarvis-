package br.com.angelobraga.jarvis

import android.Manifest
import android.content.pm.PackageManager
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.core.content.ContextCompat

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            JarvisTheme {
                JarvisScreen()
            }
        }
    }
}

@androidx.compose.runtime.Composable
private fun JarvisTheme(content: @androidx.compose.runtime.Composable () -> Unit) {
    MaterialTheme(content = content)
}

@androidx.compose.runtime.Composable
private fun JarvisScreen() {
    val context = androidx.compose.ui.platform.LocalContext.current
    val voice = remember { AndroidVoice(context) }
    val deviceIdentity = remember { DeviceIdentity() }
    val fingerprint = remember { deviceIdentity.publicKeyFingerprint() }
    var status by remember { mutableStateOf("Não conectado ao host JARVIS") }
    var transcript by remember { mutableStateOf("") }
    var listening by remember { mutableStateOf(false) }

    fun startListening() {
        listening = true
        status = "Ouvindo..."
        voice.listen(
            onResult = {
                transcript = it
                listening = false
                status = "Comando reconhecido. Aguardando conexão segura."
            },
            onError = {
                listening = false
                status = it
            },
        )
    }

    val permissionLauncher = rememberLauncherForActivityResult(
        ActivityResultContracts.RequestPermission()
    ) { granted ->
        if (granted) startListening()
        else status = "Permissão de microfone negada"
    }

    DisposableEffect(Unit) {
        onDispose { voice.release() }
    }

    Surface(modifier = Modifier.fillMaxSize()) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(24.dp),
            verticalArrangement = Arrangement.spacedBy(20.dp),
        ) {
            Text("JARVIS", style = MaterialTheme.typography.headlineLarge)
            Text("Android Command Center", style = MaterialTheme.typography.titleMedium)

            Card(modifier = Modifier.fillMaxWidth()) {
                Column(
                    modifier = Modifier.padding(18.dp),
                    verticalArrangement = Arrangement.spacedBy(8.dp),
                ) {
                    Text("Estado", style = MaterialTheme.typography.labelLarge)
                    Text(status)
                    Text("Backend: não pareado", style = MaterialTheme.typography.bodyMedium)
                    Text(
                        "Identidade local: ${fingerprint.take(23)}…",
                        style = MaterialTheme.typography.bodySmall,
                    )
                }
            }

            Spacer(modifier = Modifier.height(8.dp))

            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.Center,
                verticalAlignment = Alignment.CenterVertically,
            ) {
                Button(
                    modifier = Modifier.size(150.dp),
                    shape = CircleShape,
                    enabled = !listening,
                    onClick = {
                        if (ContextCompat.checkSelfPermission(
                                context,
                                Manifest.permission.RECORD_AUDIO,
                            ) == PackageManager.PERMISSION_GRANTED
                        ) {
                            startListening()
                        } else {
                            permissionLauncher.launch(Manifest.permission.RECORD_AUDIO)
                        }
                    },
                ) {
                    Text(if (listening) "Ouvindo" else "Falar")
                }
            }

            if (transcript.isNotBlank()) {
                Card(modifier = Modifier.fillMaxWidth()) {
                    Column(modifier = Modifier.padding(18.dp)) {
                        Text("Último comando", style = MaterialTheme.typography.labelLarge)
                        Text(transcript)
                        TextButton(
                            onClick = {
                                voice.speak(
                                    "Comando recebido. O canal seguro ainda não está pareado.",
                                )
                            },
                        ) {
                            Text("Testar voz")
                        }
                    }
                }
            }

            Text(
                "A conexão com o Windows só será habilitada depois do pareamento autenticado. O app não expõe nem recebe a chave da API do modelo.",
                style = MaterialTheme.typography.bodySmall,
            )
        }
    }
}
