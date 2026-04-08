# Serveur HTTP
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from urllib.parse import urlparse

from tp.exercises import EXERCISES
from tp.pages     import WELCOME, DOCS, HTML
from tp.logic     import run_test, launch_pygame
import __main__ as _main

def _get_server_state():
    return _main._server_state

class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a): pass

    def _send_json(self, data):
        body = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        p = urlparse(self.path).path

        if p == "/api/state":
            self._send_json({"ex3_unlocked": _get_server_state()["ex3_unlocked"], "ex4_unlocked": _get_server_state()["ex4_unlocked"]})
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
                    _get_server_state()["ex3_unlocked"] = True
                elif ex_id == "ex4":
                    _get_server_state()["ex4_unlocked"] = True
            self._send_json({"ok": ok, "message": msg, "game_success": game_ok})
        else:
            self.send_response(404); self.end_headers()