# Serveur HTTP
import json
import os
import uuid
from http.cookies import SimpleCookie
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from urllib.parse import urlparse

from tp.exercises import EXERCISES
from tp.pages     import WELCOME, DOCS, HTML
from tp.logic     import run_test, launch_pygame
from tp           import progress

STATIC_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static")
_CTYPES = {".css": "text/css; charset=utf-8", ".js": "application/javascript; charset=utf-8",
           ".png": "image/png", ".svg": "image/svg+xml"}

class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a): pass

    def _sid(self):
        """Identifiant d'élève lu dans le cookie hanoi_sid (ou 'default')."""
        raw = self.headers.get("Cookie")
        if raw:
            ck = SimpleCookie()
            ck.load(raw)
            if "hanoi_sid" in ck:
                return ck["hanoi_sid"].value
        return "default"

    def _send_json(self, data):
        body = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    def _serve_static(self, p):
        name = os.path.basename(p)                       # pas de remontée de dossier
        path = os.path.join(STATIC_DIR, name)
        if not os.path.isfile(path):
            self.send_response(404); self.end_headers(); return
        with open(path, "rb") as f:
            body = f.read()
        ctype = _CTYPES.get(os.path.splitext(name)[1], "application/octet-stream")
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        p = urlparse(self.path).path

        if p.startswith("/static/"):
            self._serve_static(p)
            return

        if p == "/api/state":
            st = progress.get_state(self._sid())
            self._send_json({"ex3_unlocked": st["ex3_unlocked"], "ex4_unlocked": st["ex4_unlocked"]})
            return

        if p == "/" or p == "":
            self.send_response(302)
            self.send_header("Location", "/tp")
            self.end_headers()
            return

        if p == "/docs":
            # Documentation intégrée dans /tp — redirige
            self.send_response(302)
            self.send_header("Location", "/tp")
            self.end_headers()
            return

        if p == "/tp":
            # Page des exercices
            ex_json = json.dumps(
                [{k: ex[k] for k in
                  ("id","num","title","instructions","starter","check_call","unlock_after","has_launch","code_label")}
                 for ex in EXERCISES], ensure_ascii=False)
            page = HTML.replace("%EXERCISES_JSON%", ex_json).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", len(page))
            # Donne un identifiant d'élève persistant au premier passage
            if self._sid() == "default":
                sid = uuid.uuid4().hex
                self.send_header("Set-Cookie", f"hanoi_sid={sid}; Path=/; Max-Age=31536000; SameSite=Lax")
            self.end_headers()
            self.wfile.write(page)
            return

        self.send_response(404); self.end_headers()

    def do_POST(self):
        n    = int(self.headers.get("Content-Length", 0))
        data = json.loads(self.rfile.read(n))
        path = urlparse(self.path).path
        if path == "/api/test":
            ok, msg = run_test(data["ex_id"], data["codes"])
            self._send_json({"ok": ok, "message": msg})
        elif path == "/api/launch":
            ok, msg, game_ok = launch_pygame(data["codes"], ex_id=data.get("ex_id", ""))
            ex_id = data.get("ex_id", "")
            if game_ok:
                if ex_id == "ex3":
                    progress.set_unlocked(self._sid(), "ex3_unlocked")
                elif ex_id == "ex4":
                    progress.set_unlocked(self._sid(), "ex4_unlocked")
            self._send_json({"ok": ok, "message": msg, "game_success": game_ok})
        else:
            self.send_response(404); self.end_headers()