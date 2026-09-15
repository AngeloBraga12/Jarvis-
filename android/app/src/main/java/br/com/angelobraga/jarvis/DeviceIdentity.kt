package br.com.angelobraga.jarvis

import android.security.keystore.KeyGenParameterSpec
import android.security.keystore.KeyProperties
import java.security.KeyPairGenerator
import java.security.KeyStore
import java.security.MessageDigest
import java.util.Base64

class DeviceIdentity {
    private val alias = "jarvis-device-identity"
    private val keyStoreName = "AndroidKeyStore"

    fun publicKeyFingerprint(): String {
        val publicKey = loadOrCreateKeyPair().public.encoded
        val digest = MessageDigest.getInstance("SHA-256").digest(publicKey)
        return digest.joinToString(":") { "%02X".format(it) }
    }

    fun publicKeyBase64(): String = Base64.getEncoder().encodeToString(loadOrCreateKeyPair().public.encoded)

    private fun loadOrCreateKeyPair(): java.security.KeyPair {
        val keyStore = KeyStore.getInstance(keyStoreName).apply { load(null) }
        val existing = keyStore.getCertificate(alias)?.publicKey
        if (existing != null) {
            return java.security.KeyPair(existing, keyStore.getKey(alias, null) as java.security.PrivateKey)
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
