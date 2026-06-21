# Page principale du TP.
# Le HTML vit dans templates/tp_page.html (édition/coloration HTML dans l'éditeur).
# Le serveur y remplace %EXERCISES_JSON% par la liste des exercices à la volée.
import os

_TEMPLATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "tp_page.html")

with open(_TEMPLATE, encoding="utf-8") as _f:
    HTML = _f.read()
