from typing import Dict, Callable, Tuple, Optional, Iterator

import pygame
from pygame import Color, Surface

from engine import Camera, Pole, Stand, Disk, IllegalMoveError

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

# Durée (en secondes) du déplacement animé d'un disque d'un poteau à l'autre.
ANIM_DURATION = 0.32


def _smoothstep(t: float) -> float:
    """Interpolation douce (accélère puis ralentit) — rend le mouvement naturel."""
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


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
        # Animation de déplacement en cours (None = aucun disque en mouvement)
        self._anim           = None
        # Cache des fonds dégradés (un par couleur d'état) pour éviter de les recalculer
        self._bg_cache       = {}
        # Cache des disques déjà composés (dégradé + reflet + contour), par taille/couleur
        self._disk_cache     = {}
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
        font     = pygame.font.SysFont(None, FONT_SIZE)
        font_msg = pygame.font.SysFont(None, FONT_SIZE + 8, bold=True)
        clock    = pygame.time.Clock()

        optimal_num_plays = 2 ** self._num_disk - 1
        game = self._reset_game()
        self._anim = None

        running = True
        while running:
            dt = clock.tick(60) / 1000.0   # temps écoulé depuis la frame précédente

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
                        self._anim = None

                # On ne joue un coup que si la partie est en cours ET qu'aucun
                # disque n'est déjà en train de se déplacer (pour ne pas couper l'animation).
                if (game['state'] == 'playing' and self._anim is None
                        and (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE
                             or event.type == pygame.MOUSEBUTTONDOWN and event.button == 1)):
                    self._start_next_move(game)

            # --- Avance l'animation en cours ; à la fin du déplacement, teste la victoire ---
            if self._anim is not None and self._advance_anim(dt):
                self._anim = None
                self._check_win(game)

            # --- Rendu ---
            self._draw_background(screen, game['background_color'])
            self._render_on(screen)

            w, h = screen.get_width(), screen.get_height()
            state = game['state']

            # Compteur de coups (coin supérieur gauche)
            self._draw_panel_text(
                screen, font,
                f"Coups : {game['num_plays']}   Optimal : {optimal_num_plays}",
                (50, 50, 50), topleft=(20, 20),
            )

            # Message central selon l'état
            if state == 'error':
                self._show_error(screen, font, game.get('error_msg', 'Erreur inconnue.'))
            elif state == 'win':
                self._draw_panel_text(
                    screen, font_msg, "Bravo ! Tu as gagné !   (appuie sur R pour rejouer)",
                    (20, 110, 20), center=(w // 2, 40), bg=(210, 255, 210, 220),
                )
            elif state == 'wrong move':
                self._draw_panel_text(
                    screen, font_msg, "Mouvement impossible !   Appuie sur R pour recommencer.",
                    (160, 30, 30), center=(w // 2, 40), bg=(255, 215, 215, 220),
                )

            # Aide en bas de l'écran
            self._draw_panel_text(
                screen, font,
                "Espace / Clic : jouer   |   Molette : zoom   |   R : recommencer   |   Échap : quitter",
                (90, 90, 90), center=(w // 2, h - 36),
            )

            pygame.display.flip()

        return game['state']  # 'win', 'wrong move', 'error' ou 'playing' (Échap)

    # -----------------------------------------------------------------
    # Animation des déplacements de disques
    # -----------------------------------------------------------------
    def _fail_move(self, game):
        """Bascule en état « mouvement impossible » (récupérable avec R)."""
        game['state']            = 'wrong move'
        game['background_color'] = Color(255, 179, 179)

    def _set_error(self, game, func_name, exc):
        """Affiche dans la fenêtre l'erreur levée par une fonction de l'élève,
        au lieu de laisser remonter un traceback interne au moteur."""
        game['state']            = 'error'
        game['background_color'] = Color(40, 0, 0)
        game['error_msg']        = (f"Ta fonction {func_name} a provoqué une erreur : "
                                    f"{type(exc).__name__} — {exc}")

    def _start_next_move(self, game):
        """Demande le coup suivant au générateur de l'élève et lance son animation."""
        try:
            src, dst = next(game['iterator'])
        except StopIteration:
            # Le générateur est épuisé avant la fin → état d'erreur
            self._fail_move(game)
            return
        except Exception as e:
            # play() a planté (ou n'a pas renvoyé un couple de poteaux).
            self._set_error(game, "play()", e)
            return

        # Poteau inexistant (ex. yield ('A', 'Z')) → mouvement impossible, pas un crash.
        if src not in self._poles or dst not in self._poles:
            self._fail_move(game)
            return

        try:
            valid = self._is_move_valid(self._poles, src, dst)
        except Exception as e:
            self._set_error(game, "is_move_valid()", e)
            return
        if not valid:
            self._fail_move(game)
            return

        # Garde-fou : même si l'is_move_valid() de l'élève accepte un coup illégal
        # (poteau vide, gros disque sur petit), le moteur le refuse. On rattrape
        # alors IllegalMoveError pour afficher un message clair au lieu d'un crash.
        disk = self._poles[src].upper_disk
        if disk is None:
            self._fail_move(game)
            return
        start = (disk.x_center, disk.y_bottom)
        try:
            self._poles[src].move_upper_disk(self._poles[dst])
        except IllegalMoveError:
            self._fail_move(game)
            return
        end = (disk.x_center, disk.y_bottom)
        game['num_plays'] += 1

        # Hauteur de survol : au-dessus de la plus haute pile possible
        lift_y = self._stand_height + (self._num_disk + 2) * self._disk_height

        disk.x_center, disk.y_bottom = start   # on replace le disque au départ pour l'animer
        self._anim = {'disk': disk, 'start': start, 'end': end, 'lift_y': lift_y, 't': 0.0}

    def _advance_anim(self, dt: float) -> bool:
        """Fait avancer l'animation d'un cran. Retourne True quand elle est terminée."""
        a = self._anim
        a['t'] += dt / ANIM_DURATION
        t = a['t']
        disk = a['disk']
        (sx, sy), (ex, ey), ly = a['start'], a['end'], a['lift_y']

        if t >= 1.0:
            disk.x_center, disk.y_bottom = ex, ey
            return True

        if t < 0.3:                       # 1) le disque monte
            f = _smoothstep(t / 0.3)
            disk.x_center = sx
            disk.y_bottom = sy + (ly - sy) * f
        elif t < 0.7:                     # 2) il glisse horizontalement
            f = _smoothstep((t - 0.3) / 0.4)
            disk.x_center = sx + (ex - sx) * f
            disk.y_bottom = ly
        else:                             # 3) il descend sur le poteau d'arrivée
            f = _smoothstep((t - 0.7) / 0.3)
            disk.x_center = ex
            disk.y_bottom = ly + (ey - ly) * f
        return False

    def _check_win(self, game):
        """Teste la victoire après un coup (les garde-fous anti-triche sont conservés)."""
        if game['state'] != 'playing':
            return
        # Vérification OBJECTIVE de la victoire, indépendante du is_game_over() de
        # l'élève : la tour complète doit réellement être reconstruite sur un poteau.
        #   • version stricte (ex. 4 et 5) : sur le poteau imposé (C) ;
        #   • version libre (ex. 3)        : sur B ou sur C.
        # Sans ça, un is_game_over() qui renvoie toujours True suffisait à « gagner »
        # après n'importe quels coups légaux.
        if self._win_pole is not None:
            target_poles = (self._win_pole,)
        else:
            target_poles = ('B', 'C')
        tower_complete = any(self._poles[p].num_disks == self._num_disk
                             for p in target_poles)
        # On conserve l'exigence du is_game_over() de l'élève (c'est l'objet des
        # exercices 1 et 4) : il doit reconnaître la fin de partie.
        try:
            over = self._is_game_over(self._poles)
        except Exception as e:
            self._set_error(game, "is_game_over()", e)
            return
        if over and tower_complete:
            game['state']            = 'win'
            game['background_color'] = Color(179, 255, 179)

    # -----------------------------------------------------------------
    # Rendu amélioré (disques en pastilles, poteaux/socle arrondis, ombres)
    # -----------------------------------------------------------------
    def _render_on(self, surface: Surface):
        self._draw_rounded_object(surface, self._stand, radius_ratio=0.35, shadow=True)
        # Ombres de contact posées sur le socle, sous chaque tour (profondeur)
        for pole in self._poles.values():
            self._draw_contact_shadow(surface, pole)
        for pole in self._poles.values():
            self._draw_rounded_object(surface, pole, radius_ratio=0.5, shadow=False)
        # Les disques sont dessinés après tous les poteaux : un disque en vol
        # (animation) passe ainsi visuellement au-dessus des poteaux.
        for pole in self._poles.values():
            for disk in pole._disks:
                self._draw_disk(surface, disk)

    def _draw_contact_shadow(self, surface, pole):
        """Ellipse sombre translucide à la base d'un poteau, sur le socle."""
        cam = self._camera
        footprint = max((d.width for d in pole._disks), default=pole.width * 2)
        cx = int((pole.x_center - cam.x) * cam.zoom) + surface.get_width() // 2
        cy = int(-(self._stand_height - cam.y) * cam.zoom) + surface.get_height() // 2
        ew = max(6, int(footprint * cam.zoom * 1.15))
        eh = max(4, int(self._disk_height * cam.zoom * 0.7))
        sh = pygame.Surface((ew, eh), pygame.SRCALPHA)
        pygame.draw.ellipse(sh, (0, 0, 0, 60), (0, 0, ew, eh))
        surface.blit(sh, (cx - ew // 2, cy - eh // 2))

    def _obj_rect(self, surface: Surface, obj):
        """Convertit un objet du monde en rectangle pixel (mêmes maths que la caméra)."""
        cam = self._camera
        px = int((obj.x_center - obj.width / 2 - cam.x) * cam.zoom) + surface.get_width() // 2
        py = int(-(obj.y_bottom + obj.height - cam.y) * cam.zoom) + surface.get_height() // 2
        return px, py, int(obj.width * cam.zoom), int(obj.height * cam.zoom)

    @staticmethod
    def _shade(color: Color, amount: int) -> Color:
        """Éclaircit (amount > 0) ou assombrit (amount < 0) une couleur."""
        return Color(
            max(0, min(255, color.r + amount)),
            max(0, min(255, color.g + amount)),
            max(0, min(255, color.b + amount)),
        )

    def _draw_rounded_object(self, surface, obj, radius_ratio, shadow):
        x, y, w, h = self._obj_rect(surface, obj)
        if w <= 0 or h <= 0:
            return
        radius = max(2, int(min(w, h) * radius_ratio))
        if shadow:
            sh = pygame.Surface((w + 12, h + 12), pygame.SRCALPHA)
            pygame.draw.rect(sh, (0, 0, 0, 60), (6, 8, w, h), border_radius=radius)
            surface.blit(sh, (x - 6, y - 4))
        pygame.draw.rect(surface, obj.color, (x, y, w, h), border_radius=radius)
        # Léger reflet sur le dessus
        pygame.draw.rect(surface, self._shade(obj.color, 28),
                         (x + 2, y + 2, w - 4, max(2, h // 4)), border_radius=radius)

    def _draw_disk(self, surface, disk):
        x, y, w, h = self._obj_rect(surface, disk)
        if w <= 0 or h <= 0:
            return
        radius = max(2, h // 2)   # forme de pastille / gélule
        # Ombre portée (translucide)
        sh = pygame.Surface((w + 12, h + 12), pygame.SRCALPHA)
        pygame.draw.rect(sh, (0, 0, 0, 70), (6, 8, w, h), border_radius=radius)
        surface.blit(sh, (x - 6, y - 4))
        # Corps du disque (dégradé + reflet + contour, mis en cache)
        surface.blit(self._disk_surface(w, h, disk.color), (x, y))

    def _disk_surface(self, w: int, h: int, color: Color) -> Surface:
        """Compose (et met en cache) un disque : dégradé vertical, reflet brillant, contour."""
        key = (w, h, color.r, color.g, color.b)
        cached = self._disk_cache.get(key)
        if cached is not None:
            return cached

        radius = max(2, h // 2)
        # Masque arrondi réutilisé pour découper dégradé et reflet à la forme de pastille
        mask = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(mask, (255, 255, 255, 255), (0, 0, w, h), border_radius=radius)

        # Dégradé vertical clair → foncé (effet cylindre)
        top, bot = self._shade(color, 50), self._shade(color, -40)
        body = pygame.Surface((w, h), pygame.SRCALPHA)
        for yy in range(h):
            f = yy / max(1, h - 1)
            body.fill(
                (int(top.r + (bot.r - top.r) * f),
                 int(top.g + (bot.g - top.g) * f),
                 int(top.b + (bot.b - top.b) * f), 255),
                (0, yy, w, 1),
            )
        body.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        # Reflet brillant : ellipse blanche translucide sur la moitié haute
        gloss = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.ellipse(gloss, (255, 255, 255, 75),
                            (int(w * 0.10), int(h * 0.08), int(w * 0.80), int(h * 0.50)))
        gloss.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        body.blit(gloss, (0, 0))

        # Contour plus foncé pour bien détacher les disques entre eux
        pygame.draw.rect(body, self._shade(color, -65), (0, 0, w, h),
                         width=max(1, h // 9), border_radius=radius)

        self._disk_cache[key] = body
        return body

    def _draw_background(self, screen: Surface, color: Color):
        """Remplit l'écran d'un léger dégradé vertical (plus doux qu'un aplat)."""
        key = (screen.get_width(), screen.get_height(), color.r, color.g, color.b)
        surf = self._bg_cache.get(key)
        if surf is None:
            w, h = screen.get_width(), screen.get_height()
            surf = pygame.Surface((w, h))
            top = self._shade(color, 22)
            for yy in range(h):
                f = yy / max(1, h - 1)
                surf.fill(
                    (int(top.r + (color.r - top.r) * f),
                     int(top.g + (color.g - top.g) * f),
                     int(top.b + (color.b - top.b) * f)),
                    (0, yy, w, 1),
                )
            self._bg_cache[key] = surf
        screen.blit(surf, (0, 0))

    def _draw_panel_text(self, screen, font, text, color,
                         center=None, topleft=None, pad=12, bg=(255, 255, 255, 170)):
        """Affiche du texte dans un petit panneau arrondi translucide."""
        txt = font.render(text, True, color)
        tw, th = txt.get_size()
        panel = pygame.Surface((tw + pad * 2, th + pad * 2), pygame.SRCALPHA)
        pygame.draw.rect(panel, bg, panel.get_rect(), border_radius=14)
        panel.blit(txt, (pad, pad))
        if center is not None:
            screen.blit(panel, panel.get_rect(center=center))
        else:
            screen.blit(panel, topleft)