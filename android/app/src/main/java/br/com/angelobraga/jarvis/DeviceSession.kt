package br.com.angelobraga.jarvis

/** Explicit lifecycle for the Android-to-JARVIS secure session. */
sealed interface DeviceSession {
    data object Unpaired : DeviceSession
    data object Pairing : DeviceSession
    data class Paired(val deviceId: String) : DeviceSession
    data object Revoked : DeviceSession
    data class ConnectionError(val message: String) : DeviceSession
}
