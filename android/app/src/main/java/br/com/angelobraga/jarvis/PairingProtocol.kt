package br.com.angelobraga.jarvis

import java.util.Base64

private const val MAX_NONCE_BYTES = 64
private const val MAX_VERSION_LENGTH = 16
private const val MAX_DEVICE_ID_LENGTH = 128

/** Data exchanged during the authenticated device-pairing handshake. */
data class PairingRequest(
    val protocolVersion: String,
    val deviceId: String,
    val publicKeyBase64: String,
    val nonceBase64: String,
) {
    init {
        require(protocolVersion.isNotBlank() && protocolVersion.length <= MAX_VERSION_LENGTH)
        require(deviceId.isNotBlank() && deviceId.length <= MAX_DEVICE_ID_LENGTH)
        require(publicKeyBase64.isNotBlank())
        require(nonceBase64.isNotBlank())
        val nonce = Base64.getDecoder().decode(nonceBase64)
        require(nonce.isNotEmpty() && nonce.size <= MAX_NONCE_BYTES)
    }
}

data class PairingProof(
    val deviceId: String,
    val nonceBase64: String,
    val signatureBase64: String,
) {
    init {
        require(deviceId.isNotBlank() && deviceId.length <= MAX_DEVICE_ID_LENGTH)
        require(nonceBase64.isNotBlank())
        require(signatureBase64.isNotBlank())
        Base64.getDecoder().decode(nonceBase64)
        Base64.getDecoder().decode(signatureBase64)
    }
}

fun pairingPayload(protocolVersion: String, deviceId: String, nonceBase64: String): ByteArray {
    require(protocolVersion.isNotBlank() && protocolVersion.length <= MAX_VERSION_LENGTH)
    require(deviceId.isNotBlank() && deviceId.length <= MAX_DEVICE_ID_LENGTH)
    require(nonceBase64.isNotBlank())
    return "$protocolVersion\n$deviceId\n$nonceBase64".toByteArray(Charsets.UTF_8)
}
