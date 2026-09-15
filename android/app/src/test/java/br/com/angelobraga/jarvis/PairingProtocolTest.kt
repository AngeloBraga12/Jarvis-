package br.com.angelobraga.jarvis

import java.util.Base64
import org.junit.Assert.assertArrayEquals
import org.junit.Assert.assertEquals
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

    @Test
    fun sessionStateMachineRequiresPairingBeforePaired() {
        val session = DeviceSessionController()
        assertThrows(IllegalArgumentException::class.java) {
            session.paired("device-1")
        }
        session.beginPairing()
        session.paired("device-1")
        assertEquals(DeviceSession.Paired("device-1"), session.state)
    }

    @Test
    fun revokedSessionCanOnlyReturnToUnpaired() {
        val session = DeviceSessionController()
        session.revoke()
        assertEquals(DeviceSession.Revoked, session.state)
        session.reset()
        assertEquals(DeviceSession.Unpaired, session.state)
    }

    @Test
    fun failureMessageIsBounded() {
        val session = DeviceSessionController()
        session.fail("x".repeat(1000))
        val state = session.state as DeviceSession.ConnectionError
        assertEquals(256, state.message.length)
    }
}
