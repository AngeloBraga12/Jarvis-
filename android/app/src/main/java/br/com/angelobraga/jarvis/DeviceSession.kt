package br.com.angelobraga.jarvis

/** Explicit lifecycle for the Android-to-JARVIS secure session. */
sealed interface DeviceSession {
    data object Unpaired : DeviceSession
    data object Pairing : DeviceSession
    data class Paired(val deviceId: String) : DeviceSession
    data object Revoked : DeviceSession
    data class ConnectionError(val message: String) : DeviceSession
}

/**
 * Deterministic state machine. Transport and authorization are deliberately absent so
 * a networking failure cannot silently become an authenticated state.
 */
class DeviceSessionController(initial: DeviceSession = DeviceSession.Unpaired) {
    var state: DeviceSession = initial
        private set

    fun beginPairing() {
        require(state is DeviceSession.Unpaired || state is DeviceSession.ConnectionError) {
            "pairing can only start from an unpaired or failed session"
        }
        state = DeviceSession.Pairing
    }

    fun paired(deviceId: String) {
        require(state is DeviceSession.Pairing) { "session is not awaiting pairing" }
        require(deviceId.isNotBlank()) { "deviceId must not be blank" }
        state = DeviceSession.Paired(deviceId)
    }

    fun fail(message: String) {
        require(message.isNotBlank()) { "message must not be blank" }
        state = DeviceSession.ConnectionError(message.take(256))
    }

    fun revoke() {
        state = DeviceSession.Revoked
    }

    fun reset() {
        require(state is DeviceSession.Revoked || state is DeviceSession.ConnectionError) {
            "session can only reset after revocation or failure"
        }
        state = DeviceSession.Unpaired
    }
}
