# Logique Python : tests, assemblage du code élève, lancement pygame
import os, sys, io, builtins, traceback, tempfile, subprocess, ast, textwrap, json

from tp.exercises   import EXERCISES
from tp.assets      import _ZERG_B64
from tp.celebration import _CELEBRATION_CODE

# Racine du projet et nombre de disques du jeu
BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NUM_DISKS = 3

# Le code de l'élève s'exécute dans un sous-process : un timeout l'empêche de
# geler le serveur (boucle infinie), et l'isole du process principal.
TEST_RUNNER    = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_test_subprocess.py")
TEST_TIMEOUT   = 5     # secondes — un test ne doit jamais durer plus longtemps
LAUNCH_TIMEOUT = 300   # secondes — partie pygame interactive (généreux), borne les runaway
_RESULT_MARKER = "__RESULT__"

def run_test(ex_id, codes_by_id):
    ex = next((e for e in EXERCISES if e["id"] == ex_id), None)
    if not ex:               return False, "Exercice introuvable."
    if not ex["check_call"]: return True,  "Testé au lancement du jeu."

    needed = list(ex.get("needs", [])) + [ex_id]
    code   = "\n\n".join(codes_by_id.get(i, "").strip() for i in needed if i in codes_by_id)

    payload = {
        "base_dir":        BASE_DIR,
        "code":            code,
        "check_setup":     ex["check_setup"],
        "check_call":      ex["check_call"],
        "expected_names":  _starter_function_names(ex["starter"]),
    }

    tmp = None
    try:
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False)
            tmp = f.name
        proc = subprocess.run(
            [sys.executable, TEST_RUNNER, tmp],
            capture_output=True, text=True, timeout=TEST_TIMEOUT,
        )
    except subprocess.TimeoutExpired:
        return False, ("❌ Ton code met trop de temps à répondre (plus de "
                       f"{TEST_TIMEOUT} s). As-tu une boucle qui ne s'arrête jamais "
                       "(par ex. « while True » sans condition de sortie) ?")
    except Exception:
        lines = traceback.format_exc().strip().splitlines()
        last  = next((l for l in reversed(lines) if l.strip()), "Erreur inconnue")
        return False, f"❌ {last}"
    finally:
        if tmp:
            try: os.unlink(tmp)
            except Exception: pass

    # Le runner écrit son résultat JSON après le marqueur. On prend la dernière
    # occurrence pour ignorer un éventuel affichage parasite du code de l'élève.
    out = proc.stdout or ""
    idx = out.rfind(_RESULT_MARKER)
    if idx == -1:
        err  = (proc.stderr or "").strip().splitlines()
        last = err[-1] if err else "Erreur inconnue lors du test."
        return False, f"❌ {last}"
    try:
        result = json.loads(out[idx + len(_RESULT_MARKER):])
    except Exception:
        return False, "❌ Erreur inattendue lors du test."
    return bool(result.get("ok")), result.get("message", "")


import ast, textwrap

def _extract_functions(code: str) -> dict:
    """
    Parse le code et retourne un dict {nom_fonction: source_complète}.
    Ignore les fonctions dont le corps est uniquement 'pass'.
    """
    funcs = {}
    try:
        tree = ast.parse(textwrap.dedent(code))
    except SyntaxError:
        return funcs
    lines = code.splitlines()
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef):
            continue
        # Corps = uniquement Pass ?
        body = [n for n in node.body if not isinstance(n, ast.Expr)]
        only_pass = all(isinstance(n, ast.Pass) for n in node.body)
        if only_pass:
            continue  # stub → ignoré
        # Extrait les lignes source de la fonction
        start = node.lineno - 1
        end   = node.end_lineno
        funcs[node.name] = "\n".join(lines[start:end])
    return funcs


def _starter_function_names(code: str) -> list:
    """Noms de toutes les fonctions déclarées dans un starter (stubs inclus)."""
    try:
        tree = ast.parse(textwrap.dedent(code))
    except SyntaxError:
        return []
    return [n.name for n in tree.body if isinstance(n, ast.FunctionDef)]


def _extract_imports(code: str) -> list:
    """
    Retourne les lignes source des imports de niveau module.
    Sans ça, un 'from itertools import cycle' écrit par l'élève serait
    perdu au lancement du jeu → NameError: name 'cycle' is not defined.
    """
    imports = []
    dedented = textwrap.dedent(code)
    try:
        tree = ast.parse(dedented)
    except SyntaxError:
        return imports
    lines = dedented.splitlines()
    for node in tree.body:   # uniquement le niveau module
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            imports.append("\n".join(lines[node.lineno - 1:node.end_lineno]))
    return imports



# ── Image Zerg embarquée en base64 ──────────────────────────────────────────
# _ZERG_B64 est importé depuis tp.assets (image chargée depuis assets/zerg.png)


def launch_pygame(codes_by_id, ex_id=''):
    """
    Assemble le code élève fonction par fonction :
    - parcourt les exercices dans l'ordre
    - pour chaque fonction trouvée, la version la plus récente NON-STUB gagne
    (ex4 peut écraser ex3 si sa version est réellement implémentée)
    """
    # Les fonctions propres à l'exercice lancé (celles de son starter) doivent être
    # réellement écrites par l'élève. Sinon, le jeu retomberait en silence sur les
    # versions des exercices précédents (ex. l'ancien play()), ce qui est déroutant.
    current = next((e for e in EXERCISES if e["id"] == ex_id), None)
    if current:
        # Noms des fonctions attendues = celles déclarées dans le starter (même en stub).
        required = _starter_function_names(current["starter"])
        # _extract_functions ignore les stubs (corps 'pass') : une fonction laissée
        # vide n'y figure pas → on la repère comme manquante.
        own = _extract_functions(codes_by_id.get(ex_id, ""))
        missing = [name for name in required if name not in own]
        if missing:
            noms = ", ".join(f"{n}()" for n in missing)
            return (False,
                    f"Tu n'as pas encore écrit {noms} dans l'exercice {current['num']}. "
                    f"Complète ton code avant de lancer le jeu.",
                    False)

    all_ids = [ex["id"] for ex in EXERCISES]
    # On ne fusionne que les exercices JUSQU'À celui qu'on lance (inclus).
    # Sinon, lancer l'exo 3 utiliserait le is_game_over strict de l'exo 4, qui ne
    # reconnaît la victoire que sur C — alors que l'algo de l'exo 3 finit sur B.
    if ex_id in all_ids:
        all_ids = all_ids[:all_ids.index(ex_id) + 1]
    merged  = {}   # nom_fonction → source
    imports = []   # imports de l'élève (dédupliqués), à conserver

    for eid in all_ids:
        code = codes_by_id.get(eid, "").strip()
        if not code:
            continue
        for imp in _extract_imports(code):
            if imp not in imports:
                imports.append(imp)
        for fname, fsrc in _extract_functions(code).items():
            merged[fname] = fsrc   # écrase seulement si non-stub

    stu_code = "\n\n".join(imports + list(merged.values()))

    script = f"""
import os
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "hide")
import sys
sys.path.insert(0, {repr(BASE_DIR)})
import pygame

# Image Zerg embarquée
_ZERG_B64 = "{_ZERG_B64}"

from engine.scene import HanoiScene
from typing import Dict, Iterator, Tuple

# ── code de l'élève ──────────────────────────
{stu_code}
# ─────────────────────────────────────────────

{_CELEBRATION_CODE}

def _show_error(title, lines):
    import pygame
    pygame.init()
    W, H = 740, 300
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption(title)
    font  = pygame.font.SysFont(None, 27)
    small = pygame.font.SysFont(None, 22)
    screen.fill((28, 6, 6))
    pygame.draw.rect(screen, (120, 20, 20), (0, 0, W, 46))
    screen.blit(font.render(title, True, (255, 120, 120)), (16, 12))
    for i, line in enumerate(lines[:8]):
        screen.blit(small.render(str(line)[:92], True, (210, 170, 100)), (16, 58 + i * 26))
    screen.blit(small.render("Appuie sur une touche ou ferme la fenêtre.", True, (110,110,110)), (16, 262))
    pygame.display.flip()
    running = True
    while running:
        for ev in pygame.event.get():
            if ev.type in (pygame.QUIT, pygame.KEYDOWN):
                running = False
    pygame.quit()

EX_ID = "{ex_id}"

try:
    # L'exo 5 demande la fonction récursive play_rec() ; les autres utilisent play().
    # Si play_rec n'est pas encore écrite, la référence lève NameError ci-dessous
    # → écran "Fonction manquante" (au lieu de gagner en silence avec l'ancien play).
    _generator = play_rec if EX_ID == 'ex5' else play
    scene = HanoiScene(
        is_move_valid=is_move_valid,
        is_game_over=is_game_over,
        move_generator=_generator,
        num_disks={NUM_DISKS},
        win_pole=('C' if EX_ID in ('ex4', 'ex5') else None),
    )
    scene.run()
    # ── Victoire ! Écran de félicitation selon l'exercice ──
    if EX_ID in ('ex4', 'ex5'):
        _show_celebration(EX_ID)
except NameError as e:
    _show_error("Fonction manquante", [
        str(e), "",
        "Assure-toi d'avoir écrit toutes les fonctions demandées !"
    ])
    sys.exit(1)
except Exception as e:
    import traceback
    lines = traceback.format_exc().strip().splitlines()
    _show_error("Erreur dans ton code", lines[-10:])
    sys.exit(1)
"""
    tmp = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as f:
            f.write(script)
            tmp = f.name
        result = subprocess.run([sys.executable, tmp], timeout=LAUNCH_TIMEOUT)
        game_ok = (result.returncode == 0)
        return True, "OK", game_ok
    except subprocess.TimeoutExpired:
        # Dépassement : souvent un play() sans yield qui boucle (ex. « while True »),
        # ce qui empêche même la fenêtre de s'ouvrir.
        return (False,
                "⏱ Le jeu a été interrompu (plus de 5 min). Vérifie que ta fonction "
                "utilise bien « yield » et qu'elle finit par s'arrêter.",
                False)
    except Exception:
        lines = traceback.format_exc().strip().splitlines()
        last  = next((l for l in reversed(lines) if l.strip()), "Erreur inconnue")
        return False, last, False
    finally:
        if tmp:
            try: os.unlink(tmp)
            except Exception: pass
