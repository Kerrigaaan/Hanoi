"""Tests de non-régression : verrouillent les bugs corrigés.

Lancer :  python -m pytest test_regressions.py -q
(Placé à la racine — PAS dans un dossier 'tests/' pour ne pas masquer tests.py.)
"""
import pytest

import tp.logic as L
from tp.exercises import EXERCISES


# ──────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────
def _capture_launch_script(codes, ex_id, monkeypatch):
    """Capture le script pygame généré sans lancer de sous-processus."""
    holder = []

    class _FakeFile:
        name = "/tmp/_hanoi_test.py"
        def write(self, d): holder.append(d)
        def __enter__(self): return self
        def __exit__(self, *a): pass

    monkeypatch.setattr(L.tempfile, "NamedTemporaryFile", lambda *a, **k: _FakeFile())
    monkeypatch.setattr(L.subprocess, "run", lambda *a, **k: type("R", (), {"returncode": 0})())
    monkeypatch.setattr(L.os, "unlink", lambda p: None)
    L.launch_pygame(codes, ex_id=ex_id)
    return "".join(holder)


IS_GAME_OVER_LENIENT = (
    'def is_game_over(poles):\n'
    '    t = poles["A"].num_disks + poles["B"].num_disks + poles["C"].num_disks\n'
    '    return poles["B"].num_disks == t or poles["C"].num_disks == t\n'
)
IS_GAME_OVER_STRICT = (
    'def is_game_over(poles):\n'
    '    t = poles["A"].num_disks + poles["B"].num_disks + poles["C"].num_disks\n'
    '    return poles["C"].num_disks == t\n'
)
IS_MOVE_VALID = 'def is_move_valid(poles, s, d):\n    return True\n'
PLAY = 'def play(num_disks, poles):\n    yield ("A", "C")\n'
PLAY_REC = "def play_rec(num_disks, poles, start='A', middle='B', end='C'):\n    yield (start, end)\n"


# ──────────────────────────────────────────────────────────────────────────
# Bug : imports de l'élève perdus au lancement (NameError: name 'cycle' ...)
# ──────────────────────────────────────────────────────────────────────────
def test_extract_imports_preserved():
    code = "from itertools import cycle\n\ndef play(n, p):\n    yield next(cycle([1]))\n"
    imports = L._extract_imports(code)
    assert any("from itertools import cycle" in i for i in imports)


def test_launch_keeps_student_imports(monkeypatch):
    codes = {
        "ex1": IS_GAME_OVER_LENIENT, "ex2": IS_MOVE_VALID,
        "ex3": ("from itertools import cycle\n\n"
                "def play(num_disks, poles):\n"
                "    for s, d in cycle([('A','C')]):\n        yield (s, d)\n"),
    }
    script = _capture_launch_script(codes, "ex3", monkeypatch)
    assert "from itertools import cycle" in script


# ──────────────────────────────────────────────────────────────────────────
# Bug : exercice lancé avec ses propres fonctions encore vides
# ──────────────────────────────────────────────────────────────────────────
def test_starter_function_names():
    ex4 = next(e for e in EXERCISES if e["id"] == "ex4")
    assert set(L._starter_function_names(ex4["starter"])) == {"is_game_over", "play"}


def test_launch_refuses_empty_exercise():
    codes = {
        "ex1": IS_GAME_OVER_LENIENT, "ex2": IS_MOVE_VALID, "ex3": PLAY,
        "ex4": "def is_game_over(poles):\n    pass\n\ndef play(num_disks, poles):\n    pass\n",
    }
    ok, msg, game = L.launch_pygame(codes, ex_id="ex4")
    assert ok is False and game is False
    assert "is_game_over" in msg and "play" in msg


# ──────────────────────────────────────────────────────────────────────────
# Bug : lancer l'exo 3 utilisait le is_game_over strict de l'exo 4
# ──────────────────────────────────────────────────────────────────────────
def test_ex3_launch_ignores_later_ex4(monkeypatch):
    codes = {"ex1": IS_GAME_OVER_LENIENT, "ex2": IS_MOVE_VALID, "ex3": PLAY,
             "ex4": IS_GAME_OVER_STRICT + "\n" + PLAY}
    script = _capture_launch_script(codes, "ex3", monkeypatch)
    body = script.split("def is_game_over")[1].split("def ")[0]
    assert " or " in body                   # version souple (B ou C) bien présente


def test_ex4_launch_uses_strict(monkeypatch):
    codes = {"ex1": IS_GAME_OVER_LENIENT, "ex2": IS_MOVE_VALID, "ex3": PLAY,
             "ex4": IS_GAME_OVER_STRICT + "\n" + PLAY}
    script = _capture_launch_script(codes, "ex4", monkeypatch)
    body = script.split("def is_game_over")[1].split("def ")[0]
    assert " or " not in body               # strict : pas de "B ou C", seulement C


# ──────────────────────────────────────────────────────────────────────────
# Bug : exo 5 utilisait play() au lieu de play_rec() ; victoire pas bornée à C
# ──────────────────────────────────────────────────────────────────────────
def test_ex5_uses_play_rec_and_win_pole(monkeypatch):
    codes = {"ex1": IS_GAME_OVER_STRICT, "ex2": IS_MOVE_VALID, "ex3": PLAY,
             "ex4": IS_GAME_OVER_STRICT + "\n" + PLAY, "ex5": PLAY_REC}
    script = _capture_launch_script(codes, "ex5", monkeypatch)
    assert "_generator = play_rec if EX_ID == 'ex5' else play" in script
    assert "win_pole=('C' if EX_ID in ('ex4', 'ex5') else None)" in script


# ──────────────────────────────────────────────────────────────────────────
# Messages d'erreur clairs (un à la fois)
# ──────────────────────────────────────────────────────────────────────────
def test_syntax_error_message():
    ok, msg = L.run_test("ex1", {"ex1": "def is_game_over(poles)\n    return True\n"})
    assert ok is False and "criture" in msg          # "Erreur d'écriture ..."


def test_name_error_for_misnamed_function():
    ok, msg = L.run_test("ex1", {"ex1": "def is_gameover(poles):\n    return True\n"})
    assert ok is False and "is_game_over" in msg


# ──────────────────────────────────────────────────────────────────────────
# Test strict côté tests.py : tout sur B ne compte PAS comme fini
# ──────────────────────────────────────────────────────────────────────────
def test_strict_is_game_over_rejects_B():
    import tests as student_tests
    strict = lambda poles: poles["C"].num_disks == 3
    student_tests.test_is_game_over(strict, strict=True)        # ne doit pas lever
    lenient = lambda poles: poles["B"].num_disks == 3 or poles["C"].num_disks == 3
    with pytest.raises(AssertionError):
        student_tests.test_is_game_over(lenient, strict=True)


# ──────────────────────────────────────────────────────────────────────────
# Progression persistée par élève
# ──────────────────────────────────────────────────────────────────────────
def test_progress_persists(tmp_path, monkeypatch):
    import tp.progress as P
    monkeypatch.setattr(P, "PROGRESS_FILE", str(tmp_path / "p.json"))
    monkeypatch.setattr(P, "_data", None)
    P.set_unlocked("eleve1", "ex3_unlocked")
    assert P.get_state("eleve1")["ex3_unlocked"] is True
    monkeypatch.setattr(P, "_data", None)                       # simule un redémarrage
    assert P.get_state("eleve1")["ex3_unlocked"] is True
    assert P.get_state("eleve2")["ex3_unlocked"] is False
