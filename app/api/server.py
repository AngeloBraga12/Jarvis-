"""Local-only HTTP API and static UI for the JARVIS foundation."""

from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

from app.core.agent import Agent
from app.core.commands import handle_command

UI_DIR = Path(__file__).resolve().parent.parent / "ui"
MAX_BODY_BYTES = 4096


class Handler(BaseHTTPRequestHandler):
    agent = Agent()

    def _send(self, status: int, payload: dict[str, object], content_type: str = "application/json; charset=utf-8") -> None:
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

    def do_GET(self) -> None:
        path = urlsplit(self.path).path
        if path in {"/", "/ui/"}:
            self._send_file(UI_DIR / "index.html", "text/html; charset=utf-8")
        elif path == "/ui/styles.css":
            self._send_file(UI_DIR / "styles.css", "text/css; charset=utf-8")
        elif path == "/ui/app.js":
            self._send_file(UI_DIR / "app.js", "text/javascript; charset=utf-8")
        elif path == "/health":
            self._send(HTTPStatus.OK, {"status": "ok", "version": "0.2.0"})
        elif path == "/system":
            self._send(HTTPStatus.OK, self.agent.run("system_status"))
        else:
            self._send(HTTPStatus.NOT_FOUND, {"error": "not found"})

    def do_POST(self) -> None:
        if urlsplit(self.path).path != "/command":
            self._send(HTTPStatus.NOT_FOUND, {"error": "not found"})
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self._send(HTTPStatus.BAD_REQUEST, {"error": "invalid content length"})
            return

        if length <= 0 or length > MAX_BODY_BYTES:
            self._send(HTTPStatus.REQUEST_ENTITY_TOO_LARGE, {"error": "request body too large or empty"})
            return

        try:
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            self._send(HTTPStatus.BAD_REQUEST, {"error": "invalid JSON"})
            return

        command = payload.get("command") if isinstance(payload, dict) else None
        if not isinstance(command, str) or len(command) > 1000:
            self._send(HTTPStatus.BAD_REQUEST, {"error": "command must be a string up to 1000 characters"})
            return

        self._send(HTTPStatus.OK, handle_command(command, self.agent))

    def log_message(self, *_args: object) -> None:
        return


def run(host: str = "127.0.0.1", port: int = 8765) -> None:
    """Start the localhost-only JARVIS service."""
    ThreadingHTTPServer((host, port), Handler).serve_forever()


if __name__ == "__main__":
    run()
