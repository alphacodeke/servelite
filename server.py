#!/usr/bin/env python3
"""
ServeLite — server.py
A minimal HTTP server with file upload and listing support.
No third-party frameworks required.
"""

import os
import cgi
import json
import mimetypes
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import unquote

PORT      = 8000
ROOT      = Path(__file__).parent          # serve index.html from here
UPLOAD_DIR = ROOT / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)


class ServeLiteHandler(BaseHTTPRequestHandler):

    #  suppress default request logs (we print our own)
    def log_message(self, fmt, *args):
        method = args[0].split()[0] if args else "?"
        path   = args[0].split()[1] if args else "?"
        code   = args[1] if len(args) > 1 else "?"
        print(f"  [{method}] {path} → {code}")

    # routing 
    def do_GET(self):
        p = self.path.split("?")[0]   # strip query string

        if p == "/" or p == "/index.html":
            self._serve_file(ROOT / "index.html", "text/html")

        elif p == "/files":
            self._list_files()

        elif p.startswith("/uploads/"):
            filename = unquote(p[len("/uploads/"):])
            target   = UPLOAD_DIR / Path(filename).name   # prevent traversal
            self._serve_file(target)

        else:
            # try serving a static file from ROOT (css, js, favicon…)
            target = ROOT / Path(p.lstrip("/"))
            if target.is_file():
                self._serve_file(target)
            else:
                self._send_json({"error": "Not found"}, 404)

    def do_POST(self):
        if self.path == "/upload":
            self._handle_upload()
        else:
            self._send_json({"error": "Not found"}, 404)

    # handlers
    def _handle_upload(self):
        content_type = self.headers.get("Content-Type", "")
        if "multipart/form-data" not in content_type:
            self._send_json({"error": "Expected multipart/form-data"}, 400)
            return

        # cgi.FieldStorage parses multipart bodies
        env = {
            "REQUEST_METHOD": "POST",
            "CONTENT_TYPE":   content_type,
            "CONTENT_LENGTH": self.headers.get("Content-Length", "0"),
        }
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ=env,
        )

        if "file" not in form:
            self._send_json({"error": "No file field in request"}, 400)
            return

        field = form["file"]
        if isinstance(field, list):
            field = field[0]

        filename = Path(field.filename).name   # strip directory components
        if not filename:
            self._send_json({"error": "Empty filename"}, 400)
            return

        save_path = UPLOAD_DIR / filename
        with open(save_path, "wb") as f:
            f.write(field.file.read())

        size = save_path.stat().st_size
        print(f"  Saved → uploads/{filename} ({size} bytes)")
        self._send_json({"ok": True, "filename": filename, "size": size})

    def _list_files(self):
        files = []
        for entry in sorted(UPLOAD_DIR.iterdir()):
            if entry.is_file():
                files.append({"name": entry.name, "size": entry.stat().st_size})
        self._send_json(files)

    def _serve_file(self, path: Path, mime: str = None):
        if not path.is_file():
            self._send_json({"error": f"File not found: {path.name}"}, 404)
            return

        mime = mime or mimetypes.guess_type(str(path))[0] or "application/octet-stream"
        data = path.read_bytes()

        self.send_response(200)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(data)))
        # allow downloads from other origins (useful on LAN)
        self.send_header("Access-Control-Allow-Origin", "*")
        if mime == "application/octet-stream":
            self.send_header("Content-Disposition", f'attachment; filename="{path.name}"')
        self.end_headers()
        self.wfile.write(data)

    def _send_json(self, payload, code: int = 200):
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        """Support CORS pre-flight."""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


# entry point
if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", PORT), ServeLiteHandler)
    print(f"\n  ServeLite is running")
    print(f"  ─────────────────────────────")
    print(f"  Local  →  http://localhost:{PORT}")
    print(f"  Press Ctrl+C to stop\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n  Shutting down ServeLite. Goodbye!\n")
        server.server_close()
