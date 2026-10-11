"""Offline dev server: stdlib http.server wrapping the pure handlers. No pip, no AWS.

Run: python3 backend/api/local_server.py   (from repo root; port 8787)
Endpoints: GET /state · GET /routes?origin&dest&mode · GET /aws/status · GET /aws/panel?origin&dest&mode
"""

import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))   # repo root on sys.path

from backend.api import handler as hp        # noqa: E402
from backend.api import aws_handler as ah    # noqa: E402


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/state":
            return self._json(hp.handle_state())
        if parsed.path == "/routes":
            q = parse_qs(parsed.query)
            payload = hp.handle_routes(
                _first(q, "origin", "ashok_vihar"),
                _first(q, "dest", "pitampura"),
                _first(q, "mode", "jog"),
                trip=_first(q, "trip", None),
                budget=_first(q, "budget", None),
                city=_first(q, "city", None),
            )
            return self._json(payload, status=200 if payload.get("ok") else 400)
        if parsed.path == "/aws/status":
            return self._json(ah.handle_aws_status())
        if parsed.path == "/aws/panel":
            q = parse_qs(parsed.query)
            payload = ah.handle_aws_panel(
                _first(q, "origin", "ashok_vihar"),
                _first(q, "dest", "pitampura"),
                _first(q, "mode", "jog"),
            )
            return self._json(payload, status=200 if payload.get("ok") else 400)
        return self._json({"ok": False, "error": "unknown path"}, status=404)

    def _json(self, payload, status=200):
        body = json.dumps(payload, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        sys.stderr.write("[local-api] " + (fmt % args) + "\n")


def _first(q, key, default):
    return (q.get(key) or [default])[0]


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8787
    print(f"ecoroute local api on http://127.0.0.1:{port}  (fix mode: no AWS needed)")
    HTTPServer(("127.0.0.1", port), Handler).serve_forever()
