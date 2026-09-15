package br.com.angelobraga.jarvis

import java.util.Base64
import org.junit.Assert.assertArrayEquals
import org.junit.Assert.assertThrows
import org.junit.Test

class PairingProtocolTest {
    @Test
    fun pairingPayloadIsDeterministic() {
        val nonce = Base64.getEncoder().encodeToString(ByteArray(32) { 7 })
        val payload = pairingPayload("1", "device-1", nonce)
        val expected = "1\ndevice-1\n$nonce".toByteArray(Charsets.UTF_8)
        assertArrayEquals(expected, payload)
    }

    @Test
    fun requestRejectsOversizedNonce() {
        val nonce = Base64.getEncoder().encodeToString(ByteArray(65))
        assertThrows(IllegalArgumentException::class.java) {
            PairingRequest("1", "device-1", "public-key", nonce)
        }
    }

    @Test
    fun proofRejectsBlankSignature() {
        val nonce = Base64.getEncoder().encodeToString(ByteArray(16))
        assertThrows(IllegalArgumentException::class.java) {
            PairingProof("device-1", nonce, "")
        }
    }
}
