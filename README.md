# TP Tours de Hanoï

## Lancement

```
.venv 3.11
pygame install
python tp_hanoi.py
```

Ouvre automatiquement le navigateur sur `http://localhost:5678/tp`.

## Structure du projet

```
hanoi/
├── tp_hanoi.py          # Point d'entrée — serveur HTTP + main()
├── engine/
│   ├── __init__.py      # Classes Pole, Disk, Camera, Stand
│   └── scene.py         # HanoiScene — fenêtre pygame du jeu
├── tests.py             # check_is_game_over, check_is_move_valid
├── util.py              # random_color()
└── tp/
    ├── __init__.py
    ├── exercises.py     # Liste des 5 exercices (données)
    ├── pages.py         # Pages HTML : WELCOME, DOCS, HTML (TP)
    ├── assets.py        # Image Zerg embarquée en base64
    ├── celebration.py   # Code pygame de félicitation (injecté)
    ├── logic.py         # run_test(), launch_pygame()
    └── server.py        # Serveur HTTP (Handler)
```

## Modifier les exercices

Éditer `tp/exercises.py` — chaque exercice est un dict avec :
- `id`, `num`, `title`
- `instructions` — liste de lignes HTML
- `starter` — code de départ affiché à l'élève
- `check_setup`, `check_call` — code de test automatique
- `unlock_after` — condition de déverrouillage
- `has_launch` — affiche le bouton "Lancer le jeu"

## Modifier les pages

Éditer `tp/pages.py` pour changer le contenu des onglets Accueil et Documentation.

## Modifier l'écran de félicitation

Éditer `tp/celebration.py` — le code pygame est injecté dans le sous-processus au moment du lancement.
