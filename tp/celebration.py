# Code pygame de célébration injecté dans le sous-processus

# ── Code de célébration injecté dans le script pygame ────────────────────────
# Affiche un écran de félicitations spectaculaire après une victoire (ex4 / ex5) :
# ciel étoilé, vrais feux d'artifice (lueur additive), confettis, emblème lumineux
# et titre animé. Tout est self-contained : ne dépend que de pygame et de _ZERG_B64.
_CELEBRATION_CODE = '''
import math as _math
import random as _random


# ── Lueur radiale réutilisable (mise en cache) ───────────────────────────────
# La lueur est dessinée en dégradé RVB (et non en alpha) pour pouvoir être
# additionnée à l'écran avec BLEND_RGB_ADD → rendu lumineux des feux d'artifice.
_GLOW_CACHE = {}

def _glow(radius, color):
    radius = max(2, int(radius))
    key = (radius, color)
    surf = _GLOW_CACHE.get(key)
    if surf is None:
        surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        cx = cy = radius
        for r in range(radius, 0, -1):
            f = (1 - r / radius) ** 2
            col = (int(color[0] * f), int(color[1] * f), int(color[2] * f))
            pygame.draw.circle(surf, col, (cx, cy), r)
        _GLOW_CACHE[key] = surf
    return surf


def _blit_glow(surf, x, y, radius, color):
    g = _glow(radius, color)
    surf.blit(g, (int(x - g.get_width() / 2), int(y - g.get_height() / 2)),
              special_flags=pygame.BLEND_RGB_ADD)


def _palette_color(palette, t, speed=0.02):
    """Couleur qui glisse continûment d'une teinte de la palette à la suivante."""
    pos = (t * speed) % len(palette)
    i = int(pos)
    f = pos - i
    c1 = palette[i]
    c2 = palette[(i + 1) % len(palette)]
    return tuple(int(c1[k] + (c2[k] - c1[k]) * f) for k in range(3))


def _ease_back(p):
    """Interpolation avec léger dépassement (effet « pop » élastique)."""
    c1 = 1.70158
    c3 = c1 + 1
    return 1 + c3 * (p - 1) ** 3 + c1 * (p - 1) ** 2


def _star_points(cx, cy, outer, inner, rot):
    pts = []
    for i in range(10):
        r = outer if i % 2 == 0 else inner
        a = _math.radians(rot + i * 36 - 90)
        pts.append((cx + r * _math.cos(a), cy + r * _math.sin(a)))
    return pts


def _show_celebration(ex_id):
    pygame.init()
    info = pygame.display.Info()
    W, H = info.current_w, info.current_h
    screen = pygame.display.set_mode((W, H), pygame.FULLSCREEN)
    pygame.display.set_caption("Felicitations")
    clock = pygame.time.Clock()

    # ── Thème selon l'exercice ───────────────────────────────────────────────
    if ex_id == "ex4":
        sky_top   = (8, 6, 30)
        sky_bot   = (40, 20, 70)
        title_txt = "EXERCICE 4 TERMINE !"
        sub_txt   = "Tu as maitrise l algo strict !"
        palette   = [(255,220,60),(255,150,40),(255,90,90),(120,255,160),(80,200,255),(255,120,200)]
        accent    = (255, 210, 80)
    else:
        sky_top   = (10, 2, 26)
        sky_bot   = (50, 10, 70)
        title_txt = "EXERCICE 5 TERMINE !"
        sub_txt   = "La recursion n a plus de secrets pour toi !"
        palette   = [(190,70,255),(255,90,210),(140,40,230),(225,130,255),(110,30,200),(255,160,255)]
        accent    = (200, 110, 255)

    # ── Fond dégradé (ciel) pré-rendu une seule fois ─────────────────────────
    bg = pygame.Surface((W, H))
    for yy in range(H):
        f = yy / max(1, H - 1)
        bg.fill(
            (int(sky_top[0] + (sky_bot[0] - sky_top[0]) * f),
             int(sky_top[1] + (sky_bot[1] - sky_top[1]) * f),
             int(sky_top[2] + (sky_bot[2] - sky_top[2]) * f)),
            (0, yy, W, 1),
        )

    # ── Étoiles scintillantes ────────────────────────────────────────────────
    stars = [
        (_random.randint(0, W), _random.randint(0, H),
         _random.randint(1, 3), _random.uniform(0.02, 0.06), _random.uniform(0, 6.28))
        for _ in range(160)
    ]

    # ── Image Zerg (ex5) ─────────────────────────────────────────────────────
    zerg_img = None
    zw = zh = 320
    try:
        import io as _io, base64 as _b64
        raw = _b64.b64decode(_ZERG_B64)
        zerg_img = pygame.image.load(_io.BytesIO(raw), "zerg.png").convert_alpha()
        iw, ih = zerg_img.get_size()
        scale = min(320 / iw, 320 / ih)
        zw, zh = int(iw * scale), int(ih * scale)
        zerg_img = pygame.transform.smoothscale(zerg_img, (zw, zh))
    except Exception:
        zerg_img = None

    # ── Feux d'artifice ──────────────────────────────────────────────────────
    class Spark:
        __slots__ = ("x", "y", "vx", "vy", "color", "life", "age", "trail")
        def __init__(self, x, y, vx, vy, color, life):
            self.x = x; self.y = y; self.vx = vx; self.vy = vy
            self.color = color; self.life = life; self.age = 0
            self.trail = []
        def update(self):
            self.vy += 0.07
            self.vx *= 0.985; self.vy *= 0.985
            self.x += self.vx; self.y += self.vy; self.age += 1
            self.trail.append((self.x, self.y))
            if len(self.trail) > 5:
                self.trail.pop(0)
        @property
        def dead(self):
            return self.age >= self.life
        def draw(self, surf):
            f = max(0.0, 1 - self.age / self.life)
            for j, (tx, ty) in enumerate(self.trail):
                _blit_glow(surf, tx, ty, 2 + 3 * f * (j / 5), self.color)
            _blit_glow(surf, self.x, self.y, 4 + 6 * f, self.color)

    class Rocket:
        def __init__(self):
            self.x = _random.randint(W // 6, 5 * W // 6)
            self.y = H + 10
            self.vy = -_random.uniform(11, 15)
            self.vx = _random.uniform(-2.2, 2.2)
            self.peak = _random.randint(H // 8, H // 2)
            self.color = _random.choice(palette)
            self.exploded = False
            self.sparks = []
        def explode(self):
            self.exploded = True
            shape = _random.random()
            n = _random.randint(55, 90)
            for i in range(n):
                ang = 2 * _math.pi * i / n + _random.uniform(-0.06, 0.06)
                if shape < 0.4:                 # anneau net
                    spd = _random.uniform(5.0, 6.5)
                elif shape < 0.7:               # sphère pleine
                    spd = _random.uniform(1.5, 6.5)
                else:                           # double couleur
                    spd = _random.uniform(2.0, 6.0)
                col = self.color if shape < 0.7 or i % 2 == 0 else _random.choice(palette)
                self.sparks.append(Spark(
                    self.x, self.y,
                    _math.cos(ang) * spd, _math.sin(ang) * spd,
                    col, _random.randint(45, 75),
                ))
        def update(self):
            if not self.exploded:
                self.x += self.vx
                self.y += self.vy
                self.vy += 0.18
                if self.vy >= -1.5 or self.y <= self.peak:
                    self.explode()
            else:
                for s in self.sparks:
                    s.update()
                self.sparks = [s for s in self.sparks if not s.dead]
        @property
        def done(self):
            return self.exploded and not self.sparks
        def draw(self, surf):
            if not self.exploded:
                _blit_glow(surf, self.x, self.y, 9, self.color)
                _blit_glow(surf, self.x, self.y + 10, 5, (180, 180, 120))
            else:
                for s in self.sparks:
                    s.draw(surf)

    rockets = [Rocket() for _ in range(3)]
    spawn_timer = 0

    # ── Confettis ────────────────────────────────────────────────────────────
    class Confetti:
        def __init__(self, start_top=False):
            self.reset(start_top)
        def reset(self, start_top=False):
            self.x = _random.randint(0, W)
            self.y = _random.randint(-40, 0) if start_top else _random.randint(-H, 0)
            self.size = _random.randint(7, 14)
            self.color = _random.choice(palette)
            self.vy = _random.uniform(1.6, 3.6)
            self.angle = _random.uniform(0, 360)
            self.spin = _random.uniform(-7, 7)
            self.sway = _random.uniform(0.6, 1.8)
            self.phase = _random.uniform(0, 6.28)
        def update(self, t):
            self.y += self.vy
            self.x += _math.sin(t * 0.05 + self.phase) * self.sway
            self.angle += self.spin
            if self.y > H + 20:
                self.reset(start_top=True)
        def draw(self, surf):
            piece = pygame.Surface((self.size, max(2, int(self.size * 0.6))), pygame.SRCALPHA)
            piece.fill((*self.color, 235))
            rot = pygame.transform.rotate(piece, self.angle)
            surf.blit(rot, (self.x, self.y))

    confettis = [Confetti() for _ in range(110)]

    # ── Sparks en orbite autour de l'emblème ─────────────────────────────────
    orbiters = [
        {"a": _random.uniform(0, 6.28), "spd": _random.uniform(0.01, 0.03),
         "r": _random.uniform(0.55, 0.95), "col": _random.choice(palette),
         "sz": _random.uniform(3, 6)}
        for _ in range(14)
    ]

    # ── Polices ──────────────────────────────────────────────────────────────
    title_size = min(int(H / 7), 120)
    font_title = pygame.font.SysFont(None, title_size, bold=True)
    font_sub   = pygame.font.SysFont(None, max(28, title_size // 2))
    font_hint  = pygame.font.SysFont(None, 34)

    emblem_cx, emblem_cy = W // 2, int(H * 0.6)
    emblem_r = int(min(W, H) * 0.13)

    t = 0
    running = True
    while running:
        clock.tick(60)
        t += 1
        for ev in pygame.event.get():
            # Petite grâce de 25 frames pour éviter de quitter sur le clic résiduel
            if ev.type == pygame.QUIT:
                running = False
            elif ev.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN) and t > 25:
                running = False

        # — Fond + étoiles —
        screen.blit(bg, (0, 0))
        for (sx, sy, sr, ssp, sph) in stars:
            tw = 0.5 + 0.5 * _math.sin(t * ssp + sph)
            c = int(120 + 135 * tw)
            _blit_glow(screen, sx, sy, sr + 1, (c, c, min(255, c + 20)))

        # — Confettis (derrière l'emblème) —
        for c in confettis:
            c.update(t); c.draw(screen)

        # — Emblème lumineux —
        pulse = 1.0 + 0.06 * _math.sin(t * 0.06)
        # halo
        halo_r = int(emblem_r * 2.1 * pulse)
        _blit_glow(screen, emblem_cx, emblem_cy, halo_r, tuple(int(x * 0.5) for x in accent))
        # sparks en orbite
        for o in orbiters:
            o["a"] += o["spd"]
            ox = emblem_cx + _math.cos(o["a"]) * emblem_r * 1.6 * o["r"]
            oy = emblem_cy + _math.sin(o["a"]) * emblem_r * 1.0 * o["r"]
            _blit_glow(screen, ox, oy, o["sz"] * (1.2 + 0.4 * _math.sin(t * 0.1 + o["a"])), o["col"])

        if ex_id == "ex5" and zerg_img is not None:
            sc2 = pulse
            nw, nh = int(zw * sc2), int(zh * sc2)
            scaled = pygame.transform.smoothscale(zerg_img, (nw, nh))
            rotated = pygame.transform.rotate(scaled, 6 * _math.sin(t * 0.03))
            screen.blit(rotated, rotated.get_rect(center=(emblem_cx, emblem_cy)))
        else:
            # Étoile dorée (ex4, ou repli si l'image manque)
            rot = t * 0.6
            er = emblem_r * pulse
            outer = _star_points(emblem_cx, emblem_cy, er, er * 0.45, rot)
            pygame.draw.polygon(screen, (255, 235, 140), outer)
            pygame.draw.polygon(screen, (255, 180, 40), outer, 4)
            inner = _star_points(emblem_cx, emblem_cy, er * 0.55, er * 0.24, rot)
            pygame.draw.polygon(screen, (255, 250, 220), inner)
            _blit_glow(screen, emblem_cx, emblem_cy, int(er * 0.7), (255, 200, 80))

        # — Feux d'artifice (devant) —
        spawn_timer -= 1
        if spawn_timer <= 0:
            rockets.append(Rocket())
            spawn_timer = _random.randint(18, 36)
        for r in rockets:
            r.update(); r.draw(screen)
        rockets = [r for r in rockets if not r.done]
        if len(rockets) > 14:
            rockets = rockets[-14:]

        # — Titre animé (pop-in, oscillation, shimmer, halo) —
        intro = min(1.0, t / 36)
        scale = _ease_back(intro)
        bob = _math.sin(t * 0.05) * 8
        tcol = _palette_color(palette, t, speed=0.05)
        base = font_title.render(title_txt, True, tcol)
        if scale > 0.01:
            fit = min(1.0, (W * 0.92) / base.get_width())   # ne déborde jamais de l'écran
            tw2 = max(1, int(base.get_width() * scale * fit))
            th2 = max(1, int(base.get_height() * scale * fit))
            ts = pygame.transform.smoothscale(base, (tw2, th2))
            cx, cy = W // 2, int(H * 0.16 + bob)
            # halo derrière le titre
            _blit_glow(screen, cx, cy, int(th2 * 1.4), tuple(int(x * 0.6) for x in accent))
            # contour sombre pour la lisibilité
            outline = font_title.render(title_txt, True, (0, 0, 0))
            outline = pygame.transform.smoothscale(outline, (tw2, th2))
            for dx, dy in ((-3, 0), (3, 0), (0, -3), (0, 3)):
                screen.blit(outline, outline.get_rect(center=(cx + dx, cy + dy)))
            screen.blit(ts, ts.get_rect(center=(cx, cy)))

        # — Sous-titre (apparaît après le titre) —
        if t > 30:
            a = min(255, (t - 30) * 8)
            ss = font_sub.render(sub_txt, True, (235, 235, 255))
            ss.set_alpha(a)
            screen.blit(ss, ss.get_rect(center=(W // 2, int(H * 0.16) + title_size)))

        # — Flash d'ouverture —
        if t < 12:
            flash = pygame.Surface((W, H))
            flash.fill((255, 255, 255))
            flash.set_alpha(int(255 * (1 - t / 12)))
            screen.blit(flash, (0, 0))

        # — Aide en bas —
        hint = font_hint.render("Appuie sur une touche pour continuer", True, (170, 170, 200))
        screen.blit(hint, hint.get_rect(center=(W // 2, H - 50)))

        pygame.display.flip()
'''
