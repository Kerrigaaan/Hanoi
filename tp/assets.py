# Charge l'image Zerg depuis un vrai fichier PNG et l'expose en base64.
# (Avant, le base64 était un énorme littéral en dur — ~280 Ko de source.)
import base64
import os

_ASSET_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "assets", "zerg.png",
)

with open(_ASSET_PATH, "rb") as _f:
    _ZERG_B64 = base64.b64encode(_f.read()).decode("ascii")
