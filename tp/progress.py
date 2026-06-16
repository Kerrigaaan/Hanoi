# Progression des élèves, persistée dans un fichier JSON (survit aux redémarrages).
# Un "élève" = un identifiant de navigateur (cookie hanoi_sid). Chaque élève a son profil.
import json
import os
import threading

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROGRESS_FILE = os.path.join(BASE_DIR, "progress.json")

_DEFAULT = {"ex3_unlocked": False, "ex4_unlocked": False}
_lock = threading.Lock()
_data = None   # { sid: {ex3_unlocked, ex4_unlocked} }


def _load():
    global _data
    if _data is None:
        try:
            with open(PROGRESS_FILE, encoding="utf-8") as f:
                _data = json.load(f)
        except Exception:
            _data = {}
    return _data


def _save():
    try:
        with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
            json.dump(_data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def get_state(sid):
    """Retourne (en le créant au besoin) le profil de l'élève `sid`."""
    with _lock:
        d = _load()
        if sid not in d:
            d[sid] = dict(_DEFAULT)
            _save()
        # complète les clés manquantes si le format évolue
        for k, v in _DEFAULT.items():
            d[sid].setdefault(k, v)
        return dict(d[sid])


def set_unlocked(sid, key):
    """Marque `key` (ex3_unlocked / ex4_unlocked) à True pour l'élève et sauvegarde."""
    if key not in _DEFAULT:
        return
    with _lock:
        d = _load()
        d.setdefault(sid, dict(_DEFAULT))[key] = True
        _save()
