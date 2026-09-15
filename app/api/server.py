"""Local-only HTTP API and static UI for the JARVIS service."""

from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

from app.core.agent import Agent
from app.core.commands import handle_command
from app.core.conversation import Conversation
from app.providers.openai import OpenAIProvider
from app.voice_capabilities import detect_capabilities

UI_DIR = Path(__file__).resolve().parent.parent / "ui"
MAX_BODY_BYTES = 4096
VERSION = "0.6.1"


class Handler(BaseHTTPRequestHandler):
    agent = Agent()
    provider = OpenAIProvider.from_env()
    conversation = Conversation()

    def _send(
        self,
        status: int,
        payload: dict[str, object],
        content_type: str = "application/json; charset=utf-8",
    ) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _send_file(self, path: Path, content_type: str) -> None:
        if not path.is_file() or UI_DIR not in path.parents:
            self._send(HTTPStatus.NOT_FOUND, {"error": "not found"})
            return
        body = path.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self) -> dict[str, object] | None:
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self._send(HTTPStatus.BAD_REQUEST, {"error": "invalid content length"})
            return None
        if length <= 0 or length > MAX_BODY_BYTES:
            self._send(
                HTTPStatus.REQUEST_ENTITY_TOO_LARGE,
                {"error": "request body too large or empty"},
            )
            return None
        try:
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            self._send(HTTPStatus.BAD_REQUEST, {"error": "invalid JSON"})
            return None
        if not isinstance(payload, dict):
            self._send(HTTPStatus.BAD_REQUEST, {"error": "JSON object required"})
            return None
        return payload

    def do_GET(self) -> None:
        path = urlsplit(self.path).path
        if path in {"/", "/ui/"}:
            self._send_file(UI_DIR / "index.html", "text/html; charset=utf-8")
        elif path == "/ui/styles.css":
            self._send_file(UI_DIR / "styles.css", "text/css; charset=utf-8")
        elif path == "/ui/app.js":
            self._send_file(UI_DIR / "app.js", "text/javascript; charset=utf-8")
        elif path == "/health":
            self._send(
                HTTPStatus.OK,
                {
                    "status": "ok",
                    "version": VERSION,
                    "llm_configured": self.provider is not None,
                },
            )
        elif path == "/system":
            self._send(HTTPStatus.OK, self.agent.run("system_status"))
        elif path == "/system/health":
            self._send(HTTPStatus.OK, self.agent.run("system_health"))
        elif path == "/voice/capabilities":
            self._send(HTTPStatus.OK, {"ok": True, "capabilities": detect_capabilities()})
        else:
            self._send(HTTPStatus.NOT_FOUND, {"error": "not found"})

    def do_POST(self) -> None:
        path = urlsplit(self.path).path
        if path == "/conversation/clear":
            self.conversation.clear()
            self._send(HTTPStatus.OK, {"ok": True})
            return

        if path == "/approval":
            payload = self._read_json()
            if payload is None:
                return
            request_id = payload.get("request_id")
            decision = payload.get("decision")
            if not isinstance(request_id, str) or len(request_id) != 32:
                self._send(HTTPStatus.BAD_REQUEST, {"error": "invalid request_id"})
                return
            if decision == "approve":
                result = self.agent.approve(request_id)
            elif decision == "deny":
                result = self.agent.deny(request_id)
            else:
                self._send(HTTPStatus.BAD_REQUEST, {"error": "decision must be approve or deny"})
                return
            status = HTTPStatus.OK if result.get("ok") else HTTPStatus.NOT_FOUND
            self._send(status, result)
            return

        if path != "/command":
            self._send(HTTPStatus.NOT_FOUND, {"error": "not found"})
            return

        payload = self._read_json()
        if payload is None:
            return
        command = payload.get("command")
        if not isinstance(command, str) or len(command) > 1000:
            self._send(
                HTTPStatus.BAD_REQUEST,
                {"error": "command must be a string up to 1000 characters"},
            )
            return

        result = handle_command(command, self.agent, self.provider, self.conversation)
        status = HTTPStatus.OK if result.get("ok") else HTTPStatus.SERVICE_UNAVAILABLE
        self._send(status, result)

    def log_message(self, *_args: object) -> None:
        return


def run(host: str = "127.0.0.1", port: int = 8765) -> None:
    """Start the localhost-only JARVIS service."""
    ThreadingHTTPServer((host, port), Handler).serve_forever()


if __name__ == "__main__":
    run()
