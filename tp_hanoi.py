#!/usr/bin/env python3
"""
TP Tours de Hanoï
Usage : python tp_hanoi.py
"""
import os, sys, webbrowser, threading

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

PORT      = 5678

# La progression (ex3/ex4 débloqués) est désormais persistée par élève
# dans progress.json — voir tp/progress.py.

from tp.server import ThreadingHTTPServer, Handler


def main():
    srv = ThreadingHTTPServer(("localhost", PORT), Handler)
    url = f"http://localhost:{PORT}/tp"
    print(f"\n  TP Tours de Hanoï")
    print(f"  ─────────────────────────────")
    print(f"  → {url}")
    print(f"\n  Ctrl+C pour arrêter\n")
    threading.Timer(1.2, lambda: webbrowser.open(url)).start()
    try:    srv.serve_forever()
    except KeyboardInterrupt: print("\n  Au revoir !")

if __name__ == "__main__":
    main()