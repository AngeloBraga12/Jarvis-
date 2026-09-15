package br.com.angelobraga.jarvis

import java.security.SecureRandom
import java.util.Base64

private const val PROTOCOL_VERSION = "1"
private const val NONCE_SIZE_BYTES = 32

/** Builds pairing material locally; it performs no network operation. */
class PairingHandshake(
    private val identity: DeviceIdentity,
    private val secureRandom: SecureRandom = SecureRandom(),
) {
    fun createRequest(): PairingRequest {
        val deviceId = identity.publicKeyFingerprint()
        val nonce = ByteArray(NONCE_SIZE_BYTES)
        secureRandom.nextBytes(nonce)
        val nonceBase64 = Base64.getEncoder().encodeToString(nonce)
        return PairingRequest(
            protocolVersion = PROTOCOL_VERSION,
            deviceId = deviceId,
            publicKeyBase64 = identity.publicKeyBase64(),
            nonceBase64 = nonceBase64,
        )
    }

    fun createProof(request: PairingRequest): PairingProof {
        val payload = pairingPayload(
            request.protocolVersion,
            request.deviceId,
            request.nonceBase64,
        )
        return PairingProof(
            deviceId = request.deviceId,
            nonceBase64 = request.nonceBase64,
            signatureBase64 = identity.signPairingPayload(payload),
        )
    }
}
