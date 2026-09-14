"""Small localhost-only HTTP API for the foundation release."""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json

from app.core.agent import Agent


class Handler(BaseHTTPRequestHandler):
    agent = Agent()

    def _send(self, status: int, payload: dict[str, object]) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/health":
            self._send(200, {"status": "ok", "version": "0.1.0"})
        elif self.path == "/system":
            self._send(200, self.agent.run("system_status"))
        else:
            self._send(404, {"error": "not found"})

    def log_message(self, *_args: object) -> None:
        return


def run(host: str = "127.0.0.1", port: int = 8765) -> None:
    ThreadingHTTPServer((host, port), Handler).serve_forever()


if __name__ == "__main__":
    run()
