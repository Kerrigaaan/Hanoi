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
# Vraie solution récursive : play_rec s'appelle elle-même.
PLAY_REC = (
    "def play_rec(num_disks, poles, start='A', middle='B', end='C'):\n"
    "    if num_disks == 0:\n"
    "        return\n"
    "    yield from play_rec(num_disks - 1, poles, start, end, middle)\n"
    "    yield (start, end)\n"
    "    yield from play_rec(num_disks - 1, poles, middle, start, end)\n"
)
# Solution itérative déguisée : aucun appel à play_rec → doit être refusée pour l'ex. 5.
PLAY_REC_ITERATIVE = (
    "def play_rec(num_disks, poles, start='A', middle='B', end='C'):\n"
    "    yield (start, end)\n"
)


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
# Bug : l'exo 5 acceptait une solution itérative (play_rec sans récursion)
# ──────────────────────────────────────────────────────────────────────────
def test_is_recursive_detection():
    assert L._is_recursive(PLAY_REC, "play_rec") is True
    assert L._is_recursive(PLAY_REC_ITERATIVE, "play_rec") is False


def test_ex5_refuses_iterative_play_rec():
    codes = {"ex1": IS_GAME_OVER_STRICT, "ex2": IS_MOVE_VALID, "ex3": PLAY,
             "ex4": IS_GAME_OVER_STRICT + "\n" + PLAY, "ex5": PLAY_REC_ITERATIVE}
    ok, msg, game = L.launch_pygame(codes, ex_id="ex5")
    assert ok is False and game is False
    assert "récursive" in msg


def test_ex5_accepts_recursive_play_rec(monkeypatch):
    codes = {"ex1": IS_GAME_OVER_STRICT, "ex2": IS_MOVE_VALID, "ex3": PLAY,
             "ex4": IS_GAME_OVER_STRICT + "\n" + PLAY, "ex5": PLAY_REC}
    # Ne doit pas être refusé : le script de lancement est bien généré.
    script = _capture_launch_script(codes, "ex5", monkeypatch)
    assert "play_rec" in script


# ──────────────────────────────────────────────────────────────────────────
# Logique de victoire du jeu (sans fenêtre) — anti-triche et robustesse
# ──────────────────────────────────────────────────────────────────────────
def _make_scene(iv, go, play, win_pole):
    from engine.scene import HanoiScene
    return HanoiScene(iv, go, play, num_disks=3, win_pole=win_pole)


def _drive_scene(sc):
    """Joue tous les coups du générateur (sans rendu) et renvoie l'état final."""
    g = sc._reset_game()
    sc._anim = None
    guard = 0
    while g["state"] == "playing" and guard < 500:
        guard += 1
        sc._start_next_move(g)
        if g["state"] != "playing" or sc._anim is None:
            break
        while sc._anim is not None:
            if sc._advance_anim(1.0):
                sc._anim = None
                sc._check_win(g)
    return g


_IV_OK = (lambda p, s, d: p[s].num_disks > 0
          and (p[d].num_disks == 0 or p[d].upper_disk.width > p[s].upper_disk.width))


def test_ex3_rejects_always_true_is_game_over():
    # is_game_over toujours vrai + 8 coups légaux mais inutiles : ne doit PAS gagner,
    # car la tour n'est jamais réellement reconstruite sur B ou C.
    def pingpong(n, p):
        for _ in range(4):
            yield ("A", "B"); yield ("B", "A")
    g = _drive_scene(_make_scene(_IV_OK, lambda p: True, pingpong, None))
    assert g["state"] != "win"


def test_ex3_wins_when_tower_actually_rebuilt():
    # Solution correcte qui finit sur C : victoire acceptée en mode libre (win_pole=None).
    def solve(n, p):
        def rec(n, s, m, e):
            if n == 0: return
            yield from rec(n - 1, s, e, m); yield (s, e); yield from rec(n - 1, m, s, e)
        yield from rec(n, "A", "B", "C")
    g = _drive_scene(_make_scene(_IV_OK, lambda p: p["C"].num_disks == 3, solve, None))
    assert g["state"] == "win"


def test_illegal_move_is_handled_without_crash():
    # is_move_valid toujours vrai + coup illégal : message « mouvement impossible »,
    # pas de IllegalMoveError qui remonte.
    def play_illegal(n, p):
        yield ("A", "B"); yield ("A", "B")   # le 2e pose un gros disque sur un petit
    g = _drive_scene(_make_scene(lambda p, s, d: True, lambda p: False, play_illegal, None))
    assert g["state"] == "wrong move"


def test_student_is_game_over_exception_shows_error():
    def go_crash(p):
        return p["D"].num_disks == 3          # KeyError 'D'
    g = _drive_scene(_make_scene(_IV_OK, go_crash, lambda n, p: iter([("A", "C")]), None))
    assert g["state"] == "error" and "is_game_over" in g["error_msg"]


def test_student_is_move_valid_exception_shows_error():
    def iv_crash(p, s, d):
        return p["Z"].num_disks > 0           # KeyError 'Z'
    g = _drive_scene(_make_scene(iv_crash, lambda p: False, lambda n, p: iter([("A", "C")]), None))
    assert g["state"] == "error" and "is_move_valid" in g["error_msg"]


def test_student_play_exception_shows_error():
    def play_crash(n, p):
        yield ("A", "C")
        raise ValueError("boom")
    g = _drive_scene(_make_scene(_IV_OK, lambda p: False, play_crash, None))
    assert g["state"] == "error" and "play()" in g["error_msg"]


# ──────────────────────────────────────────────────────────────────────────
# Bug : l'assemblage du code cassait sur les fonctions imbriquées / classes,
# et perdait les constantes de niveau module de l'élève
# ──────────────────────────────────────────────────────────────────────────
def test_extract_functions_ignores_nested_and_methods():
    nested = ("def play(num_disks, poles):\n"
              "    def helper(s, d):\n"
              "        return (s, d)\n"
              "    yield helper('A', 'C')\n")
    method = ("def play(num_disks, poles):\n"
              "    class Aide:\n"
              "        def m(self):\n"
              "            return 1\n"
              "    yield ('A', 'C')\n")
    assert set(L._extract_functions(nested)) == {"play"}
    assert set(L._extract_functions(method)) == {"play"}


def test_launch_with_class_method_is_valid_python(monkeypatch):
    play = ("def play(num_disks, poles):\n"
            "    class Aide:\n"
            "        def m(self):\n"
            "            return 1\n"
            "    yield ('A', 'C')\n")
    codes = {"ex1": IS_GAME_OVER_LENIENT, "ex2": IS_MOVE_VALID, "ex3": play}
    script = _capture_launch_script(codes, "ex3", monkeypatch)
    compile(script, "<launch>", "exec")       # ne doit plus lever IndentationError


def test_launch_keeps_student_module_constants(monkeypatch):
    play = ("SEQUENCE = [('A', 'C')]\n"
            "def play(num_disks, poles):\n"
            "    for m in SEQUENCE:\n"
            "        yield m\n")
    assert L._extract_assignments(play)        # l'affectation est bien repérée
    codes = {"ex1": IS_GAME_OVER_LENIENT, "ex2": IS_MOVE_VALID, "ex3": play}
    script = _capture_launch_script(codes, "ex3", monkeypatch)
    assert "SEQUENCE = [('A', 'C')]" in script


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
