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
# 2. Installation de pygame via le proxy
# ─────────────────────────────────────────────────────────────────
banner "Installation des paquets"

echo -e "  ${D}→${N}  p pip install pygame ..."
p pip install pygame -q && ok "pygame installé" || { warn "pygame — échec" ; ERRORS=$((ERRORS+1)); }

# ─────────────────────────────────────────────────────────────────
# 3. Vérification des fichiers
# ─────────────────────────────────────────────────────────────────
banner "Vérification des fichiers du projet"

FILES=(
    "tp_hanoi.py"
    "engine/__init__.py"
    "engine/scene.py"
    "tests.py"
    "util.py"
    "tp/__init__.py"
    "tp/exercises.py"
    "tp/assets.py"
    "tp/celebration.py"
    "tp/logic.py"
    "tp/server.py"
    "tp/pages/__init__.py"
    "tp/pages/welcome.py"
    "tp/pages/docs.py"
    "tp/pages/tp_page.py"
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