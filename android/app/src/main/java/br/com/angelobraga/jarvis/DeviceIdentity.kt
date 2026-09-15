package br.com.angelobraga.jarvis

import android.security.keystore.KeyGenParameterSpec
import android.security.keystore.KeyProperties
import java.security.KeyPair
import java.security.KeyPairGenerator
import java.security.KeyStore
import java.security.MessageDigest
import java.security.Signature
import java.util.Base64

class DeviceIdentity {
    private val alias = "jarvis-device-identity"
    private val keyStoreName = "AndroidKeyStore"

    fun publicKeyFingerprint(): String {
        val publicKey = loadOrCreateKeyPair().public.encoded
        val digest = MessageDigest.getInstance("SHA-256").digest(publicKey)
        return digest.joinToString(":") { "%02X".format(it) }
    }

    fun publicKeyBase64(): String =
        Base64.getEncoder().encodeToString(loadOrCreateKeyPair().public.encoded)

    /** Proves possession of the private key without exporting it from Android Keystore. */
    fun signPairingPayload(payload: ByteArray): String {
        require(payload.isNotEmpty()) { "payload must not be empty" }
        require(payload.size <= 4096) { "payload exceeds the signing limit" }
        val signature = Signature.getInstance("SHA256withECDSA")
        signature.initSign(loadOrCreateKeyPair().private)
        signature.update(payload)
        return Base64.getEncoder().encodeToString(signature.sign())
    }

    private fun loadOrCreateKeyPair(): KeyPair {
        val keyStore = KeyStore.getInstance(keyStoreName).apply { load(null) }
        val existing = keyStore.getCertificate(alias)?.publicKey
        if (existing != null) {
            return KeyPair(existing, keyStore.getKey(alias, null) as java.security.PrivateKey)
        }

        val generator = KeyPairGenerator.getInstance(KeyProperties.KEY_ALGORITHM_EC, keyStoreName)
        generator.initialize(
            KeyGenParameterSpec.Builder(
                alias,
                KeyProperties.PURPOSE_SIGN or KeyProperties.PURPOSE_VERIFY,
            )
                .setAlgorithmParameterSpec(java.security.spec.ECGenParameterSpec("secp256r1"))
                .setDigests(KeyProperties.DIGEST_SHA256)
                .build(),
        )
        return generator.generateKeyPair()
    }
}
