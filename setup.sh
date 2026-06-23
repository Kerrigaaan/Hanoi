#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────
#  TP Tours de Hanoï — Installation de l'environnement
#  Usage : bash setup.sh
# ─────────────────────────────────────────────────────────────────

G='\033[0;32m'; Y='\033[0;33m'; B='\033[0;34m'
C='\033[0;36m'; W='\033[1;37m'; D='\033[0;90m'; N='\033[0m'

ok()   { echo -e "  ${G}✔${N}  $*"; }
info() { echo -e "  ${C}ℹ${N}  $*"; }
warn() { echo -e "  ${Y}⚠${N}  $*"; }

banner() {
    local line="════════════════════════════════════════════════════════"
    echo -e "\n${B}${line}\n  $*\n${line}${N}"
}

echo -e "${W}  TP Tours de Hanoï — Installation${N}\n"
ERRORS=0
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ─────────────────────────────────────────────────────────────────
# 1. Création du venv
# ─────────────────────────────────────────────────────────────────
banner "Environnement virtuel"

if [[ -d "$SCRIPT_DIR/.venv" ]]; then
    info "Venv existant trouvé — réutilisation"
else
    echo -e "  ${D}→${N}  python3.11 -m venv .venv ..."
    python3.11 -m venv "$SCRIPT_DIR/.venv"
    echo -e "  Créé dans : $SCRIPT_DIR/.venv"
    ok "Venv créé (.venv/)"
fi

source "$SCRIPT_DIR/.venv/bin/activate"
ok "Venv activé  ($(python --version 2>&1))"

# ─────────────────────────────────────────────────────────────────
# 2. Installation de pygame (seule dépendance tierce)
# ─────────────────────────────────────────────────────────────────
banner "Installation des paquets"

echo -e "  ${D}→${N}  pip install pygame ..."
pip install pygame -q && ok "pygame installé" || { warn "pygame — échec" ; ERRORS=$((ERRORS+1)); }

# ─────────────────────────────────────────────────────────────────
# 3. Vérification des fichiers
# ─────────────────────────────────────────────────────────────────
banner "Vérification des fichiers du projet"

FILES=(
    # Point d'entrée et utilitaires
    "tp_hanoi.py"
    "util.py"
    # Moteur du jeu (fenêtre pygame)
    "engine/__init__.py"
    "engine/scene.py"
    # Logique serveur et exercices
    "tp/__init__.py"
    "tp/server.py"
    "tp/logic.py"
    "tp/exercises.py"
    "tp/progress.py"
    "tp/assets.py"
    "tp/celebration.py"
    "tp/_test_subprocess.py"
    # Page web (template HTML)
    "tp/pages/__init__.py"
    "tp/pages/tp_page.py"
    "tp/pages/templates/tp_page.html"
    # Ressources web servies via /static/
    "static/style.css"
    "static/style-home.css"
    "static/style-docs.css"
    "static/style-fun.css"
    "static/style-polish.css"
    "static/app.js"
    "static/hanoi.js"
    "static/challenges.js"
    "static/minigames.js"
    "static/trophies.js"
    # Image de l'écran de félicitations
    "assets/zerg.png"
    # Tests de non-régression
    "tests/__init__.py"
    "tests/test_regressions.py"
)

for f in "${FILES[@]}"; do
    if [[ -f "$SCRIPT_DIR/$f" ]]; then
        ok "$f"
    else
        warn "$f  ← MANQUANT"
        ERRORS=$((ERRORS+1))
    fi
done

# ─────────────────────────────────────────────────────────────────
# 4. Résumé
# ─────────────────────────────────────────────────────────────────
banner "Résumé"

if [[ "$ERRORS" -eq 0 ]]; then
    echo -e "${C}"
    cat << 'ART'

                                   ..
                                   ..:
                   .....::::.        ...
                        .::--::.     .:-:.     ..
                          ..==..     .-=-..     :.
                 ....     .--.      :-=-.       ::
           .:::..:-+:     .++:    .=*+:       ...-:
                  .::    .=#**+=:=++*+-:...  :-=+-.
                    .++=-+=-:.::.::::-=:-=****+=: .   .
            .:      =**--:.....   ...:.::-==+-       .:
         .:-++:   .==::...             .::::--.     .-:
        ::... ..=++=::..                 ..:-#*-:===*-.
      ..        =+-:..      ... ..        :.:+++:--::.
          .    .--:..     .. .......      .---=-.        .
        .-==:::++-:.     .- .:.. ...      ---:--..    ...
        -:. ...---:.     :-.-.     .     .-. :-=-:--:::.
       :.      .:-:      .---           .=-::--===*=:..
      .        .++.       :=-.         .=-...::-===::.
          :-:.:-=+=.     ...:::..  ..:==:....::----:.
          --.    :==:     ..  .::::---:.....::-==-:
         .:      .:--.      ....       ..::--==-:.
         ..     .-=--:.        ..::::::::---=+-.
          .   ::......:=:.         ..::---=-:.
              ::       ::::.             ..
               :.       :.......
                .       --:....::.
                       :-..... .-:..
              ....  ...:...:....
                ....:.......

ART
    echo -e "${N}"
    echo -e "${G}  Tout est prêt ! Lance le TP avec :${N}\n"
    echo -e "${W}      source .venv/bin/activate${N}"
    echo -e "${W}      python tp_hanoi.py${N}\n"
else
    echo ""
    warn "${ERRORS} problème(s) — relis les messages ci-dessus."
    echo ""
fi
