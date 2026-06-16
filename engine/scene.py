from typing import Dict, Callable, Tuple, Optional, Iterator

import pygame
from pygame import Color, Surface

from engine import Camera, Pole, Stand, Disk

MIN_DISK_WIDTH: float = 2.
MAX_DISK_WIDTH: float = 5.
MIN_DISK_HEIGHT: float = 1.
MIN_POLE_WIDTH: float = 1.
MIN_STAND_HEIGHT: float = 1.
MIN_DISK_COUNT: int = 2

# Palette de couleurs vives et distinctes pour les disques (remplace random_color)
DISK_COLORS = [
    Color(220,  70,  70),   # rouge
    Color(230, 140,  50),   # orange
    Color(210, 195,  50),   # jaune
    Color( 80, 180,  80),   # vert
    Color( 60, 130, 210),   # bleu
    Color(140,  80, 200),   # violet
    Color(200,  80, 160),   # rose
]

IsMoveValid = Callable[[Dict[str, Pole], str, str], bool]
IsGameOver  = Callable[[Dict[str, Pole]], bool]
MoveGenerator = Callable[[int, Dict[str, Pole]], Iterator[Tuple[str, str]]]

FONT_SIZE = 32


class HanoiScene:
    _is_move_valid:   IsMoveValid
    _is_game_over:    IsGameOver
    _move_generator:  MoveGenerator
    _disk_height:     float
    _pole_width:      float
    _stand_height:    float
    _num_disk:        int
    _camera:          Camera
    _poles:           Dict[str, 'Pole']
    _stand:           'Stand'

    def __init__(self, is_move_valid: IsMoveValid,
                 is_game_over: IsGameOver,
                 move_generator: MoveGenerator,
                 disk_height: float = MIN_DISK_HEIGHT, pole_width: float = MIN_POLE_WIDTH,
                 stand_height: float = MIN_STAND_HEIGHT, num_disks: int = MIN_DISK_COUNT,
                 win_pole: Optional[str] = None):
        self._is_move_valid  = is_move_valid
        self._is_game_over   = is_game_over
        self._move_generator = move_generator
        # Si défini (ex. 'C'), la victoire n'est acceptée que si tous les disques
        # sont sur ce poteau — peu importe ce que retourne is_game_over de l'élève.
        self._win_pole       = win_pole
        self._disk_height    = disk_height
        self._pole_width     = pole_width
        self._stand_height   = stand_height
        self._num_disk       = num_disks
        self._camera         = Camera(x=0., y=0., zoom=20.)
        self._create_objects(num_disks)   # typo corrigée : _create_objetcs → _create_objects
        self._set_camera_y()

    def _set_camera_y(self):
        y_center = (self._stand.height + next(iter(self._poles.values())).height) / 2
        self._camera.y = y_center

    def _create_objects(self, disk_count: int):
        assert disk_count >= MIN_DISK_COUNT
        stand_color = Color(235, 211, 115)
        self._stand = Stand(
            x_center=0,
            y_bottom=0,
            width=4 * MAX_DISK_WIDTH,
            height=self._stand_height,
            color=stand_color,
        )
        pole_names = ['A', 'B', 'C']
        self._poles = dict()
        for i in [-1, 0, 1]:
            self._poles[pole_names[i + 1]] = Pole(
                x_center=i * MAX_DISK_WIDTH,
                y_bottom=self._stand_height,
                width=self._pole_width,
                height=(disk_count + 1) * self._disk_height,
                color=stand_color,
            )
        left_pole = self._poles[pole_names[0]]
        for i in range(disk_count):
            left_pole.add_disk(
                Disk(
                    x_center=0,
                    y_bottom=0,
                    width=MAX_DISK_WIDTH - (MAX_DISK_WIDTH - MIN_DISK_WIDTH) * (i / disk_count),
                    height=self._disk_height,
                    color=DISK_COLORS[i % len(DISK_COLORS)],  # couleur distincte par disque
                )
            )

    # -----------------------------------------------------------------
    # Affiche un message d'erreur clair dans la fenêtre pygame
    # -----------------------------------------------------------------
    def _show_error(self, screen: Surface, font, message: str):
        w, h = screen.get_width(), screen.get_height()
        screen.fill(Color(40, 0, 0))
        title = font.render("⚠  Erreur dans ton code", True, Color(255, 100, 100))
        screen.blit(title, (w // 2 - title.get_width() // 2, h // 2 - 60))
        # Coupe le message en lignes de 70 chars max
        words, lines, current = message.split(), [], ""
        for word in words:
            if len(current) + len(word) + 1 <= 70:
                current += (" " if current else "") + word
            else:
                lines.append(current); current = word
        if current:
            lines.append(current)
        for i, line in enumerate(lines[:4]):
            surf = font.render(line, True, Color(230, 180, 80))
            screen.blit(surf, (w // 2 - surf.get_width() // 2, h // 2 + i * 40))
        hint = font.render("Corrige ton code et clique à nouveau sur Lancer.", True, Color(140, 140, 140))
        screen.blit(hint, (w // 2 - hint.get_width() // 2, h - 60))

    # -----------------------------------------------------------------
    # Méthode interne : réinitialise la partie sans recréer la scène
    # -----------------------------------------------------------------
    def _reset_game(self):
        self._create_objects(self._num_disk)
        self._set_camera_y()

        raw = self._move_generator(self._num_disk, self._poles)

        # Si play() contient juste "pass", raw vaut None → on renvoie un état d'erreur
        if raw is None:
            return {
                'iterator':         iter([]),
                'background_color': Color(40, 0, 0),
                'state':            'error',
                'error_msg':        "Ta fonction play() ne génère aucun mouvement. "
                                    "As-tu bien utilisé 'yield' ?",
                'num_plays':        0,
            }

        try:
            iterator = iter(raw)
        except TypeError:
            return {
                'iterator':         iter([]),
                'background_color': Color(40, 0, 0),
                'state':            'error',
                'error_msg':        "Ta fonction play() doit utiliser 'yield' pour donner des coups.",
                'num_plays':        0,
            }

        return {
            'iterator':         iterator,
            'background_color': Color(230, 249, 255),
            'state':            'playing',
            'num_plays':        0,
        }

    def run(self):
        import sys as _sys
        pygame.init()
        try:
            final_state = self._do_run()
        finally:
            pygame.quit()
        # Seule une vraie victoire (état 'win') vaut exit 0.
        # Tout le reste — mauvais mouvement, erreur, Échap sans gagner — vaut exit 1.
        # Le serveur web utilise ce code pour savoir si le code de l'élève est correct.
        if final_state != 'win':
            _sys.exit(1)

    def _do_run(self):
        pygame.display.set_caption("Tours de Hanoï")           # titre de fenêtre
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        font   = pygame.font.SysFont(None, FONT_SIZE)

        optimal_num_plays = 2 ** self._num_disk - 1
        game = self._reset_game()

        running = True
        while running:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False

                # ZOOM — borné à 1 minimum pour éviter affichage nul/inversé
                if event.type == pygame.MOUSEWHEEL:
                    self._camera.zoom = max(1, self._camera.zoom + event.y)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_r:           # R = recommencer à tout moment
                        game = self._reset_game()

                # --- Actions selon l'état courant ---
                match game['state']:
                    case 'error':
                        pass  # rendu géré ci-dessous
                    case 'playing':
                        if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE
                                or event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                            try:
                                src, dst = next(game['iterator'])
                                if self._is_move_valid(self._poles, src, dst):
                                    self._poles[src].move_upper_disk(self._poles[dst])
                                    game['num_plays'] += 1
                                else:
                                    # Mouvement invalide → état d'erreur (récupérable avec R)
                                    game['state']            = 'wrong move'
                                    game['background_color'] = Color(255, 179, 179)
                            except StopIteration:
                                # Le générateur est épuisé avant la fin → état d'erreur
                                game['state']            = 'wrong move'
                                game['background_color'] = Color(255, 179, 179)

                        # Victoire valide SEULEMENT si le nombre minimal de coups
                        # a été joué — empêche un is_game_over() qui retourne True en
                        # permanence de tricher
                        min_moves = 2 ** self._num_disk - 1
                        # En version stricte (ex. 4 et 5), la tour doit être sur le
                        # poteau imposé (C). On n'accepte donc pas une victoire sur B,
                        # même si is_game_over() de l'élève la considère comme finie.
                        on_win_pole = (self._win_pole is None
                                       or self._poles[self._win_pole].num_disks == self._num_disk)
                        if (self._is_game_over(self._poles)
                                and game['num_plays'] >= min_moves
                                and on_win_pole):
                            game['state']            = 'win'
                            game['background_color'] = Color(179, 255, 179)

            # --- Rendu ---
            screen.fill(game['background_color'])
            self._render_on(screen)

            w, h = screen.get_width(), screen.get_height()
            state = game['state']

            # Compteur de coups (coin supérieur gauche)
            count_surf = font.render(
                f"Coups : {game['num_plays']}   Optimal : {optimal_num_plays}",
                True, (50, 50, 50)
            )
            screen.blit(count_surf, (20, 20))

            # Message central selon l'état
            if state == 'error':
                self._show_error(screen, font, game.get('error_msg', 'Erreur inconnue.'))
            elif state == 'win':
                msg = font.render(
                    "Bravo ! Tu as gagné !   (appuie sur R pour rejouer)",
                    True, (20, 110, 20)
                )
                screen.blit(msg, (w // 2 - msg.get_width() // 2, 20))
            elif state == 'wrong move':
                msg = font.render(
                    "Mouvement impossible !   Appuie sur R pour recommencer.",
                    True, (160, 30, 30)
                )
                screen.blit(msg, (w // 2 - msg.get_width() // 2, 20))

            # Aide en bas de l'écran
            hint = font.render(
                "Espace / Clic : jouer   |   Molette : zoom   |   R : recommencer   |   Échap : quitter",
                True, (110, 110, 110)
            )
            screen.blit(hint, (w // 2 - hint.get_width() // 2, h - 40))

            pygame.display.flip()

        return game['state']  # 'win', 'wrong move', 'error' ou 'playing' (Échap)

    def _render_on(self, surface: Surface):
        self._camera.render(surface, self._stand)
        for pole in self._poles.values():
            self._camera.render(surface, pole)
            for disk in pole._disks:
                self._camera.render(surface, disk)