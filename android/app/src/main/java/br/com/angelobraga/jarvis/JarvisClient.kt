package br.com.angelobraga.jarvis

import java.net.URI

class JarvisClient(private val endpoint: String) {
    init {
        val uri = URI(endpoint)
        require(uri.scheme == "https") { "JARVIS Android requires HTTPS for remote communication" }
    }

    fun isConfigured(): Boolean = endpoint.isNotBlank()
}
