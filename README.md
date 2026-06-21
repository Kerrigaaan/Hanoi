# TP Tours de Hanoï

TP interactif : l'élève complète 5 fonctions Python et, à la fin, son programme
joue tout seul aux Tours de Hanoï dans une fenêtre pygame. L'interface (énoncés,
éditeur de code, documentation) est une page web servie en local.

## Lancement

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install pygame
python tp_hanoi.py
```

Ouvre automatiquement le navigateur sur `http://localhost:5678/tp`.

## Déroulé du TP

5 exercices qui se débloquent dans l'ordre :

1. `is_game_over()` — la partie est-elle terminée ?
2. `is_move_valid()` — ce mouvement respecte-t-il les règles ?
3. `play()` — un bot qui joue automatiquement (algorithme itératif)
4. `play()` strict — la tour doit arriver sur **C** uniquement
5. `play_rec()` — la version récursive

L'éditeur intègre une **coloration syntaxique** et des guides d'indentation.
Les erreurs de syntaxe / de nom sont expliquées une à la fois.

## L'onglet « Défis Fun »

Débloqué après la réussite de l'exercice 5. Il contient :

- un **Hanoï jouable** à la souris (volet latéral : glisser-déposer, animation,
  résolution automatique, 3 à 10 anneaux) ;
- **5 défis** Hanoï (contre-la-montre, coups comptés, départ aléatoire, 4 poteaux,
  marathon) avec médailles 🥇🥈🥉 ;
- **15 mini-jeux** sans rapport avec Hanoï (devine le nombre, morpion, pendu,
  Snake, 2048, Démineur…), chacun avec son **code Python expliqué** ;
- une **vitrine de trophées** (anneau de progression, rang, badges).

## Progression

La progression (exercices débloqués) est persistée **par élève** dans
`progress.json` (identifiant via cookie), donc conservée entre les redémarrages.

## Structure du projet

```text
hanoi/
├── tp_hanoi.py          # Point d'entrée — serveur HTTP + main()
├── engine/
│   ├── __init__.py      # Classes Pole, Disk, Camera, Stand
│   └── scene.py         # HanoiScene — fenêtre pygame du jeu (param win_pole)
├── tests/
│   ├── __init__.py      # check_is_game_over, check_is_move_valid (importé par les exos)
│   └── test_regressions.py  # Tests pytest de non-régression
├── util.py
├── assets/
│   └── zerg.png         # Image de l'écran de félicitation
├── static/              # Ressources servies via /static/
│   ├── style.css        # Base : header, cartes, éditeur, boutons, onglets
│   ├── style-home.css   # Page d'accueil
│   ├── style-docs.css   # Documentation Python
│   ├── style-fun.css    # Espace enseignant + vitrine des trophées
│   ├── style-polish.css # Responsive + animations
│   ├── app.js           # Onglets, exercices, test/lancement, coloration, admin
│   ├── hanoi.js         # Le Hanoï jouable du volet
│   ├── challenges.js    # Défis Hanoï de l'onglet « Défis Fun »
│   ├── minigames.js     # 15 mini-jeux bonus
│   └── trophies.js      # Vitrine des trophées
└── tp/
    ├── exercises.py     # Liste des 5 exercices (données)
    ├── logic.py         # run_test(), launch_pygame()
    ├── _test_subprocess.py  # Exécuteur isolé d'un test (sous-process + timeout)
    ├── server.py        # Serveur HTTP (Handler, fichiers statiques)
    ├── progress.py      # Persistance de la progression par élève
    ├── assets.py        # Charge assets/zerg.png et l'expose en base64
    ├── celebration.py   # Code pygame de félicitation (injecté)
    └── pages/
        ├── __init__.py  # Réexporte HTML
        ├── tp_page.py   # Charge le template HTML
        └── templates/
            └── tp_page.html  # HTML de la page (référence les fichiers static/)
```

## Tests

```bash
python -m pytest tests/ -q
```

## Modifier le TP

- **Exercices** : éditer `tp/exercises.py` (chaque exercice est un dict : `id`,
  `num`, `title`, `instructions`, `starter`, `check_setup`, `check_call`,
  `unlock_after`, `has_launch`).
- **Style / scripts** : éditer les fichiers de `static/`.
- **Pages Accueil / Documentation** : éditer `tp/pages/welcome.py` et `tp/pages/docs.py`.
- **Écran de félicitation** : éditer `tp/celebration.py`.
