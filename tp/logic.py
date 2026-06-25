# Logique Python : tests, assemblage du code élève, lancement pygame
import os, sys, io, builtins, traceback, tempfile, subprocess, ast, textwrap, json, keyword, difflib

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


# ── Vérification de syntaxe « à la volée » pour l'éditeur ────────────────────
def _fr_syntax_cause(msg: str) -> str:
    """Traduit en français clair (pour des enfants) le message d'erreur Python."""
    import re as _re
    raw = msg or ""
    low = raw.lower()

    # « '(' was never closed », « '[' was never closed », etc.
    m = _re.search(r"'(.)' was never closed", raw)
    if m:
        noms = {'(': "une parenthèse « ( »", '[': "un crochet « [ »",
                '{': "une accolade « { »"}
        return f"{noms.get(m.group(1), 'un symbole')} n'a jamais été fermé(e)"

    table = [
        ("expected ':'",                 "il manque un deux-points « : » en fin de ligne"),
        ("expected an indented block",   "il manque un bloc indenté : après « : », la ligne suivante doit commencer par 4 espaces"),
        ("unexpected indent",            "indentation inattendue : trop d'espaces au début de la ligne"),
        ("unindent does not match",      "l'indentation ne correspond à aucun niveau précédent"),
        ("inconsistent use of tabs",     "mélange de tabulations et d'espaces : utilise seulement des espaces"),
        ("unterminated string",          "une chaîne de caractères n'est pas fermée : il manque un guillemet"),
        ("eol while scanning string",    "une chaîne de caractères n'est pas fermée : il manque un guillemet"),
        ("unexpected eof",               "le code s'arrête trop tôt : un bloc ou une parenthèse n'est pas terminé"),
        ("eof in multi-line",            "une parenthèse ou une chaîne n'est jamais fermée"),
        ("missing parentheses in call to 'print'", "il manque des parenthèses : écris print(...)"),
        ("invalid character",            "un caractère invalide s'est glissé dans le code (copier-coller ?)"),
        ("cannot assign to",             "on ne peut pas affecter ici (« = » au lieu de « == » ?)"),
        ("invalid syntax",               "syntaxe invalide : vérifie la ponctuation (« : », parenthèses, guillemets, virgules)"),
    ]
    for key, fr in table:
        if key in low:
            return fr
    return "syntaxe invalide : vérifie la ponctuation (« : », parenthèses, guillemets, virgules)"


# Fonctions du TP qu'un exercice peut appeler alors qu'elles sont écrites dans un
# AUTRE exercice (fusionnées seulement au lancement). On ne doit donc pas les
# signaler comme « inconnues » dans l'éditeur.
_TP_NAMES = {"is_move_valid", "is_game_over", "play", "play_rec"}


def _collect_defined_names(tree: ast.AST) -> set:
    """Tous les noms « définis » par le code : params, variables affectées,
    fonctions, classes, imports, cibles de boucles/compréhensions, etc."""
    defined = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            defined.add(node.name)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
            a = node.args
            for arg in (*a.posonlyargs, *a.args, *a.kwonlyargs):
                defined.add(arg.arg)
            if a.vararg: defined.add(a.vararg.arg)
            if a.kwarg:  defined.add(a.kwarg.arg)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            for n in node.names:
                defined.add((n.asname or n.name).split(".")[0])
        elif isinstance(node, (ast.Global, ast.Nonlocal)):
            defined.update(node.names)
        elif isinstance(node, ast.ExceptHandler) and node.name:
            defined.add(node.name)
        elif isinstance(node, ast.Name) and isinstance(node.ctx, (ast.Store, ast.Del)):
            # affectations, cibles de for/with/compréhensions, walrus…
            defined.add(node.id)
    return defined


def _check_unknown_names(tree: ast.AST):
    """Repère un nom utilisé mais jamais défini (faute de frappe sur un mot-clé
    ou un nom), façon VSCode. Retourne {"line","col","msg"} ou None."""
    # En présence d'un import étoilé (from x import *), on ne peut pas connaître
    # les noms importés : on s'abstient pour ne pas signaler à tort.
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and any(n.name == "*" for n in node.names):
            return None

    defined  = _collect_defined_names(tree)
    builtin  = set(dir(builtins))
    allowed  = builtin | set(keyword.kwlist) | _TP_NAMES | defined | {"__name__", "__doc__"}
    vocab    = builtin | set(keyword.kwlist) | _TP_NAMES | defined

    # On signale le PREMIER nom inconnu dans l'ordre du code.
    unknown = [n for n in ast.walk(tree)
               if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)
               and n.id not in allowed]
    if not unknown:
        return None
    n = min(unknown, key=lambda x: (x.lineno, x.col_offset))
    line, col = n.lineno, n.col_offset + 1
    sugg = difflib.get_close_matches(n.id, vocab, n=1, cutoff=0.8)
    if sugg:
        msg = (f"Ligne {line} — « {n.id} » n'est pas reconnu. "
               f"Voulais-tu dire « {sugg[0]} » ?")
    else:
        msg = f"Ligne {line} — « {n.id} » n'est pas reconnu (nom ou mot-clé mal écrit ?)."
    return {"line": line, "col": col, "msg": msg}


def check_syntax(code: str) -> dict:
    """
    Vérifie le code de l'éditeur SANS l'exécuter et renvoie une erreur claire :
      1. erreur de syntaxe / d'indentation (via le parseur Python) ;
      2. sinon, nom ou mot-clé inconnu (faute de frappe, façon VSCode).
    Retourne {"ok": bool, "error": {"line", "col", "msg"} | None}.
    """
    try:
        tree = ast.parse(code or "", "<editeur>", "exec")
    except SyntaxError as e:          # IndentationError / TabError en héritent
        line  = e.lineno or 1
        col   = e.offset or 1
        cause = _fr_syntax_cause(e.msg)
        prefix = "indentation" if isinstance(e, IndentationError) else "erreur d'écriture"
        return {"ok": False,
                "error": {"line": line, "col": col,
                          "msg": f"Ligne {line} — {prefix} : {cause}."}}
    except Exception:
        # Tout autre souci au parsing : on ne dérange pas l'élève.
        return {"ok": True, "error": None}

    err = _check_unknown_names(tree)
    return {"ok": err is None, "error": err}


import ast, textwrap

def _extract_functions(code: str) -> dict:
    """
    Parse le code et retourne un dict {nom_fonction: source_complète} pour les
    fonctions définies AU NIVEAU MODULE uniquement.

    On parcourt `tree.body` (et non `ast.walk`) afin d'ignorer les fonctions
    imbriquées et les méthodes de classe : les ré-émettre au niveau module
    produirait du code mal indenté (IndentationError au lancement).
    Les fonctions dont le corps est uniquement 'pass' (stubs non remplis) sont
    également ignorées.
    """
    funcs = {}
    dedented = textwrap.dedent(code)
    try:
        tree = ast.parse(dedented)
    except SyntaxError:
        return funcs
    lines = dedented.splitlines()
    for node in tree.body:
        if not isinstance(node, ast.FunctionDef):
            continue
        if all(isinstance(n, ast.Pass) for n in node.body):
            continue  # stub → ignoré
        funcs[node.name] = "\n".join(lines[node.lineno - 1:node.end_lineno])
    return funcs


def _is_recursive(code: str, func_name: str) -> bool:
    """
    True si la fonction `func_name` s'appelle elle-même quelque part dans son corps.
    Sert à imposer une vraie solution récursive (ex. 5) : une suite de `yield`
    « à la main » (itérative) ne contient aucun appel à play_rec → refusée.
    """
    try:
        tree = ast.parse(textwrap.dedent(code))
    except SyntaxError:
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == func_name:
            for sub in ast.walk(node):
                if (isinstance(sub, ast.Call)
                        and isinstance(sub.func, ast.Name)
                        and sub.func.id == func_name):
                    return True
    return False


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


def _extract_assignments(code: str) -> list:
    """
    Retourne les lignes source des affectations de niveau module (constantes,
    tables…). Sans ça, un élève qui factorise par ex. `SEQUENCE = [...]` et s'en
    sert dans play() déclencherait un NameError au lancement (la variable serait
    perdue, seules les fonctions et les imports étant conservés).
    """
    assigns = []
    dedented = textwrap.dedent(code)
    try:
        tree = ast.parse(dedented)
    except SyntaxError:
        return assigns
    lines = dedented.splitlines()
    for node in tree.body:   # uniquement le niveau module
        if isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
            assigns.append("\n".join(lines[node.lineno - 1:node.end_lineno]))
    return assigns



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

    # L'exercice 5 doit être résolu de façon RÉCURSIVE : play_rec() doit s'appeler
    # elle-même. Une solution qui se contente d'enchaîner des yield (itérative, ou
    # codée en dur) n'utilise pas la récursion et n'est donc pas acceptée ici.
    if ex_id == "ex5" and not _is_recursive(codes_by_id.get("ex5", ""), "play_rec"):
        return (False,
                "L'exercice 5 doit être résolu de façon récursive : ta fonction "
                "play_rec() doit s'appeler elle-même avec « yield from play_rec(...) ». "
                "Une solution itérative (enchaîner des yield à la main) n'est pas "
                "acceptée pour cet exercice.",
                False)

    all_ids = [ex["id"] for ex in EXERCISES]
    # On ne fusionne que les exercices JUSQU'À celui qu'on lance (inclus).
    # Sinon, lancer l'exo 3 utiliserait le is_game_over strict de l'exo 4, qui ne
    # reconnaît la victoire que sur C — alors que l'algo de l'exo 3 finit sur B.
    if ex_id in all_ids:
        all_ids = all_ids[:all_ids.index(ex_id) + 1]
    merged  = {}   # nom_fonction → source
    imports = []   # imports de l'élève (dédupliqués), à conserver
    assigns = []   # constantes/variables de niveau module de l'élève, à conserver

    for eid in all_ids:
        code = codes_by_id.get(eid, "").strip()
        if not code:
            continue
        for imp in _extract_imports(code):
            if imp not in imports:
                imports.append(imp)
        for asg in _extract_assignments(code):
            if asg not in assigns:
                assigns.append(asg)
        for fname, fsrc in _extract_functions(code).items():
            merged[fname] = fsrc   # écrase seulement si non-stub

    stu_code = "\n\n".join(imports + assigns + list(merged.values()))

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
