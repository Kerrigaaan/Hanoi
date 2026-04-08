#!/usr/bin/env python3
"""
TP Tours de Hanoï
Usage : python tp_hanoi.py
"""
import os, sys, webbrowser, threading

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

PORT      = 5678
NUM_DISKS = 3

# État serveur : ex3 validé ou non — repart à zéro à chaque démarrage du serveur
_server_state = {"ex3_unlocked": False, "ex4_unlocked": False}

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