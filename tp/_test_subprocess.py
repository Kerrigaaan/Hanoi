# Exécuteur isolé d'un test d'exercice.
# Lancé dans un SOUS-PROCESS par tp.logic.run_test, ce qui permet :
#   • d'imposer un timeout (une boucle infinie de l'élève ne gèle plus le serveur) ;
#   • de confiner le code de l'élève hors du process serveur.
#
# Usage :  python tp/_test_subprocess.py <payload.json>
# Le payload contient : base_dir, code, check_setup, check_call, expected_names.
# Le résultat est écrit sur stdout, préfixé par le marqueur __RESULT__ (JSON).
import os

# pygame imprime un bandeau de bienvenue sur stdout dès son import (déclenché par
# « from engine import ... »). Sans ça, ce bandeau se collerait devant le message
# du test (✅ comme ❌). On le masque AVANT tout import susceptible de charger pygame.
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "hide")

import sys
import io
import json
import re
import builtins
import traceback

RESULT_MARKER = "__RESULT__"


def main():
    with open(sys.argv[1], encoding="utf-8") as f:
        payload = json.load(f)

    # Le code de tests (from tests import ...) et le moteur (from engine import ...)
    # vivent à la racine du projet.
    sys.path.insert(0, payload["base_dir"])

    code        = payload["code"]
    check_setup = payload["check_setup"]
    check_call  = payload["check_call"]
    expected    = payload.get("expected_names", [])

    # On capture les print() (les fonctions check_* signalent le succès par un ✅).
    captured = io.StringIO()
    old_print = builtins.print
    builtins.print = lambda *a, **kw: captured.write(" ".join(str(x) for x in a) + "\n")
    try:
        ns = {}
        exec(check_setup, ns)
        exec(code, ns)
        exec(check_call, ns)
        out = captured.getvalue().strip()
        result = {"ok": "✅" in out, "message": out or "(aucun retour)"}
    # Python s'arrête à la PREMIÈRE erreur : l'élève la corrige, relance, et la
    # suivante apparaît. Messages clairs pour les erreurs d'écriture et de nommage.
    except IndentationError as e:
        result = {"ok": False, "message": (
            f"❌ Indentation ligne {e.lineno} : {e.msg}. "
            f"Vérifie tes espaces en début de ligne (4 espaces par niveau).")}
    except SyntaxError as e:
        result = {"ok": False, "message": (
            f"❌ Erreur d'écriture ligne {e.lineno} : {e.msg}. "
            f"Vérifie la ponctuation : deux-points « : », parenthèses, guillemets.")}
    except NameError as e:
        m = re.search(r"name '([^']+)' is not defined", str(e))
        nom = m.group(1) if m else None
        if nom in expected:
            result = {"ok": False, "message": (
                f"❌ Le nom « {nom} » n'est pas reconnu — as-tu bien nommé "
                f"ta fonction « {nom} » ? (vérifie l'orthographe exacte)")}
        else:
            result = {"ok": False, "message": (
                f"❌ Le nom « {nom} » n'est pas reconnu. Vérifie l'orthographe, "
                f"ou qu'il est bien défini / importé avant d'être utilisé.")}
    except Exception:
        lines = traceback.format_exc().strip().splitlines()
        last = next((l for l in reversed(lines) if l.strip()), "Erreur inconnue")
        result = {"ok": False, "message": f"❌ {last}"}
    finally:
        builtins.print = old_print

    sys.stdout.write(RESULT_MARKER + json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
