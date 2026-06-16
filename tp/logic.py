# Logique Python : tests, assemblage du code élève, lancement pygame
import os, sys, io, builtins, traceback, tempfile, subprocess, ast, textwrap

from tp.exercises   import EXERCISES
from tp.assets      import _ZERG_B64
from tp.celebration import _CELEBRATION_CODE

# Racine du projet et nombre de disques du jeu
BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NUM_DISKS = 3

def run_test(ex_id, codes_by_id):
    ex = next((e for e in EXERCISES if e["id"] == ex_id), None)
    if not ex:               return False, "Exercice introuvable."
    if not ex["check_call"]: return True,  "Testé au lancement du jeu."

    needed = list(ex.get("needs", [])) + [ex_id]
    code   = "\n\n".join(codes_by_id.get(i, "").strip() for i in needed if i in codes_by_id)

    captured = io.StringIO()
    old_p    = builtins.print
    builtins.print = lambda *a, **kw: captured.write(" ".join(str(x) for x in a) + "\n")
    try:
        ns = {}
        exec(ex["check_setup"], ns)
        exec(code, ns)
        exec(ex["check_call"], ns)
        out = captured.getvalue().strip()
        return "✅" in out, out or "(aucun retour)"
    # Python s'arrête à la PREMIÈRE erreur : l'élève la corrige, relance, et la
    # suivante apparaît. On rend ces messages clairs pour les erreurs d'écriture
    # (syntaxe/indentation) et de nomenclature (noms mal orthographiés).
    except IndentationError as e:
        return False, (f"❌ Indentation ligne {e.lineno} : {e.msg}. "
                       f"Vérifie tes espaces en début de ligne (4 espaces par niveau).")
    except SyntaxError as e:
        return False, (f"❌ Erreur d'écriture ligne {e.lineno} : {e.msg}. "
                       f"Vérifie la ponctuation : deux-points « : », parenthèses, guillemets.")
    except NameError as e:
        import re as _re
        m   = _re.search(r"name '([^']+)' is not defined", str(e))
        nom = m.group(1) if m else None
        expected = _starter_function_names(ex["starter"])
        if nom in expected:
            return False, (f"❌ Le nom « {nom} » n'est pas reconnu — as-tu bien nommé "
                           f"ta fonction « {nom} » ? (vérifie l'orthographe exacte)")
        return False, (f"❌ Le nom « {nom} » n'est pas reconnu. Vérifie l'orthographe, "
                       f"ou qu'il est bien défini / importé avant d'être utilisé.")
    except Exception:
        lines = traceback.format_exc().strip().splitlines()
        last  = next((l for l in reversed(lines) if l.strip()), "Erreur inconnue")
        return False, f"❌ {last}"
    finally:
        builtins.print = old_p


import ast, textwrap

def _extract_functions(code: str) -> dict:
    """
    Parse le code et retourne un dict {nom_fonction: source_complète}.
    Ignore les fonctions dont le corps est uniquement 'pass'.
    """
    funcs = {}
    try:
        tree = ast.parse(textwrap.dedent(code))
    except SyntaxError:
        return funcs
    lines = code.splitlines()
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef):
            continue
        # Corps = uniquement Pass ?
        body = [n for n in node.body if not isinstance(n, ast.Expr)]
        only_pass = all(isinstance(n, ast.Pass) for n in node.body)
        if only_pass:
            continue  # stub → ignoré
        # Extrait les lignes source de la fonction
        start = node.lineno - 1
        end   = node.end_lineno
        funcs[node.name] = "\n".join(lines[start:end])
    return funcs


def _starter_function_names(code: str) -> list:
    """Noms de toutes les fonctions déclarées dans un starter (stubs inclus)."""
    try:
        tree = ast.parse(textwrap.dedent(code))
    except SyntaxError:
        return []
    return [n.name for n in tree.body if isinstance(n, ast.FunctionDef)]


def _extract_imports(code: str) -> list:
    """
    Retourne les lignes source des imports de niveau module.
    Sans ça, un 'from itertools import cycle' écrit par l'élève serait
    perdu au lancement du jeu → NameError: name 'cycle' is not defined.
    """
    imports = []
    dedented = textwrap.dedent(code)
    try:
        tree = ast.parse(dedented)
    except SyntaxError:
        return imports
    lines = dedented.splitlines()
    for node in tree.body:   # uniquement le niveau module
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            imports.append("\n".join(lines[node.lineno - 1:node.end_lineno]))
    return imports



# ── Image Zerg embarquée en base64 ──────────────────────────────────────────
# _ZERG_B64 est importé depuis tp.assets (image chargée depuis assets/zerg.png)

# ── Code de célébration injecté dans le script pygame ────────────────────────
_CELEBRATION_CODE = '''
import math as _math, random as _random

def _draw_zerg_logo(surface, cx, cy, size, alpha=255):
    """Logo Zerg : spirale organique violette avec griffes, inspiree du logo StarCraft 2."""
    import math as _m
    S = size * 3
    s = pygame.Surface((S, S), pygame.SRCALPHA)
    ox, oy = S // 2, S // 2  # centre dans la surface

    # Couleurs
    purp   = (140, 30, 200, alpha)
    purp2  = (180, 60, 230, alpha)
    light  = (220,110, 255, alpha)
    dark   = ( 60,  0,  90, alpha)
    red    = (160, 20,  40, alpha)
    red2   = (200, 40,  60, alpha)
    drip   = (180, 30,  60, alpha)

    def pt(angle_deg, r, dx=0, dy=0):
        a = _m.radians(angle_deg)
        return (int(ox + dx + r * _m.cos(a)), int(oy + dy + r * _m.sin(a)))

    def poly(pts, col, w=0):
        if len(pts) >= 3:
            pygame.draw.polygon(s, col, pts, w)

    def circ(x, y, r, col):
        pygame.draw.circle(s, col, (x, y), r)

    r = size  # rayon de base

    # ── Corps central : anneau spiral ────────────────────────────────────
    # Gros anneau sombre (fond)
    circ(ox, oy, int(r * 0.95), dark)
    # Anneau principal violet
    pygame.draw.circle(s, purp, (ox, oy), int(r * 0.85), int(r * 0.28))
    # Anneau intérieur lumineux
    pygame.draw.circle(s, purp2, (ox, oy), int(r * 0.58), int(r * 0.14))

    # ── Spirale centrale ──────────────────────────────────────────────────
    # Oeil : cercle sombre au centre
    circ(ox - int(r*0.08), oy - int(r*0.05), int(r*0.28), (20, 0, 35, alpha))
    circ(ox - int(r*0.08), oy - int(r*0.05), int(r*0.18), (100, 10, 160, alpha))
    circ(ox - int(r*0.08), oy - int(r*0.05), int(r*0.09), light)

    # Queue de spirale (arc épais qui s'enroule vers le bas-droite)
    for i in range(18):
        ang  = 20 + i * 9
        rad  = int(r * (0.72 - i * 0.022))
        thick = max(2, int(r * (0.22 - i * 0.008)))
        col_t = (
            int(140 + i*3),
            int(30  + i*2),
            int(190 + i*2),
            max(60, alpha - i * 8)
        )
        if rad > 4:
            pygame.draw.circle(s, col_t, pt(ang, rad), thick)

    # ── Griffes / tentacules ──────────────────────────────────────────────
    # Griffe haut-gauche (grande, incurvée)
    griffe_1 = [
        pt(-60, int(r*0.85)),
        pt(-85, int(r*1.35)),
        pt(-100,int(r*1.55)),
        pt(-90, int(r*1.65)),
        pt(-70, int(r*1.45)),
        pt(-50, int(r*1.1)),
    ]
    poly(griffe_1, red)
    poly(griffe_1, red2, 2)

    # Griffe haut-droite
    griffe_2 = [
        pt( 30, int(r*0.82)),
        pt( 55, int(r*1.3)),
        pt( 65, int(r*1.55)),
        pt( 75, int(r*1.5)),
        pt( 65, int(r*1.3)),
        pt( 45, int(r*0.95)),
    ]
    poly(griffe_2, purp)
    poly(griffe_2, light, 2)

    # Griffe droite (horizontale)
    griffe_3 = [
        pt(  5, int(r*0.88)),
        pt( 15, int(r*1.5)),
        pt( 20, int(r*1.7)),
        pt( 30, int(r*1.65)),
        pt( 25, int(r*1.45)),
        pt( 15, int(r*1.1)),
    ]
    poly(griffe_3, purp2)
    poly(griffe_3, light, 2)

    # Griffe bas-gauche (tentacule tombant)
    griffe_4 = [
        pt(200, int(r*0.8)),
        pt(215, int(r*1.25)),
        pt(210, int(r*1.55)),
        pt(220, int(r*1.6)),
        pt(230, int(r*1.4)),
        pt(225, int(r*1.0)),
    ]
    poly(griffe_4, red)
    poly(griffe_4, red2, 2)

    # Griffe gauche courte
    griffe_5 = [
        pt(155, int(r*0.78)),
        pt(145, int(r*1.2)),
        pt(138, int(r*1.42)),
        pt(148, int(r*1.48)),
        pt(158, int(r*1.25)),
        pt(165, int(r*0.92)),
    ]
    poly(griffe_5, purp)
    poly(griffe_5, purp2, 2)

    # ── Excroissances du bord supérieur ──────────────────────────────────
    # 3 pointes organiques sur le dessus de l anneau
    for ang, rl, rend in [(-40, r*0.85, r*1.3), (-20, r*0.82, r*1.45), (5, r*0.80, r*1.28)]:
        tip = [
            pt(ang - 7, int(rl)),
            pt(ang,     int(rend)),
            pt(ang + 7, int(rl)),
        ]
        poly(tip, purp2)
        poly(tip, light, 2)

    # ── Gouttes de sang/liquide en bas ────────────────────────────────────
    for i, (bx, by, br) in enumerate([
        (ox - int(r*0.25), oy + int(r*0.90), int(r*0.055)),
        (ox + int(r*0.05), oy + int(r*0.92), int(r*0.04)),
        (ox + int(r*0.30), oy + int(r*0.85), int(r*0.06)),
    ]):
        pygame.draw.rect(s, drip, (bx - int(br*0.7), by, int(br*1.4), int(r*0.15)))
        pygame.draw.circle(s, drip, (bx, by + int(r*0.17)), br)

    # ── Reflet lumineux sur l anneau ──────────────────────────────────────
    pygame.draw.circle(s, (*light[:3], min(alpha, 100)),
                       (ox - int(r*0.32), oy - int(r*0.38)), int(r*0.18))

    surface.blit(s, (cx - S//2, cy - S//2))

def _show_celebration(ex_id):
    pygame.init()
    info = pygame.display.Info()
    W, H = info.current_w, info.current_h
    screen = pygame.display.set_mode((W, H), pygame.FULLSCREEN)
    pygame.display.set_caption("Felicitations")
    clock = pygame.time.Clock()

    # Chargement de l'image Zerg depuis la base64 embarquée
    _zerg_img = None
    _zerg_base_w = _zerg_base_h = 300
    try:
        import io as _io, base64 as _b64
        _raw = _b64.b64decode(_ZERG_B64)
        _buf = _io.BytesIO(_raw)
        _zerg_img = pygame.image.load(_buf, "zerg.png").convert_alpha()
        # Redimensionne à 300px max en gardant les proportions
        _zw, _zh = _zerg_img.get_size()
        _scale = min(300/_zw, 300/_zh)
        _zerg_base_w = int(_zw*_scale); _zerg_base_h = int(_zh*_scale)
        _zerg_img = pygame.transform.smoothscale(_zerg_img, (_zerg_base_w, _zerg_base_h))
    except Exception:
        pass
    font_big   = pygame.font.SysFont(None, 96)
    font_med   = pygame.font.SysFont(None, 52)
    font_small = pygame.font.SysFont(None, 36)
    if ex_id == "ex4":
        bg_col    = (5, 5, 20)
        title_txt = "EXERCICE 4 TERMINE !"
        sub_txt   = "Tu as maitrise l algo strict !"
        fw_cols   = [(255,220,50),(50,200,255),(255,100,100),(100,255,150),(255,150,50)]
    else:
        bg_col    = (10, 0, 20)
        title_txt = "EXERCICE 5 TERMINE !"
        sub_txt   = "La recursion n a plus de secrets pour toi !"
        fw_cols   = [(180,40,255),(255,80,200),(120,0,200),(220,100,255),(80,0,180)]

    class Particle:
        def __init__(self):
            self.x=_random.randint(0,W); self.y=_random.randint(-H,0)
            self.vx=_random.uniform(-1.5,1.5); self.vy=_random.uniform(1.5,4.5)
            self.size=_random.randint(3,9); self.color=_random.choice(fw_cols)
            self.life=_random.randint(80,200); self.age=0
        def update(self):
            self.x+=self.vx; self.y+=self.vy; self.age+=1
            if self.age>self.life or self.y>H+20:
                self.__init__()
        def draw(self,surf):
            a=max(0,255-int(255*self.age/self.life))
            s=pygame.Surface((self.size*2,self.size*2),pygame.SRCALPHA)
            pygame.draw.circle(s,(*self.color,a),(self.size,self.size),self.size)
            surf.blit(s,(int(self.x)-self.size,int(self.y)-self.size))

    class Firework:
        def __init__(self):
            self.x=_random.randint(W//6,5*W//6); self.y=_random.randint(H//8,H//2)
            self.r=0; self.max_r=_random.randint(60,160); self.spd=_random.uniform(2.5,5)
            self.color=_random.choice(fw_cols); self.done=False; self.timer=_random.randint(0,80)
        def update(self):
            if self.timer>0: self.timer-=1; return
            self.r+=self.spd
            if self.r>=self.max_r: self.done=True
        def draw(self,surf):
            if self.timer>0: return
            a=int(255*(1-self.r/self.max_r))
            for i in range(12):
                angle=2*_math.pi*i/12
                ex=int(self.x+self.r*_math.cos(angle)); ey=int(self.y+self.r*_math.sin(angle))
                ss=pygame.Surface((8,8),pygame.SRCALPHA)
                pygame.draw.circle(ss,(*self.color,max(0,a)),(4,4),4)
                surf.blit(ss,(ex-4,ey-4))
                if self.r>10:
                    pygame.draw.line(surf,(*self.color,max(0,a//2)),(int(self.x),int(self.y)),(ex,ey),1)

    parts=[Particle() for _ in range(120)]
    fws=[Firework() for _ in range(8)]
    t=0
    running=True
    while running:
        clock.tick(60); t+=1
        for ev in pygame.event.get():
            if ev.type in (pygame.QUIT,pygame.KEYDOWN,pygame.MOUSEBUTTONDOWN):
                running=False
        screen.fill(bg_col)
        for fw in fws:
            fw.update(); fw.draw(screen)
            if fw.done: fw.__init__()
        for p in parts:
            p.update(); p.draw(screen)
        if ex_id=="ex5" and _zerg_img is not None:
            # Pulse : légère oscillation de taille
            sc2=1.0+0.06*_math.sin(t*.04)
            nw=int(_zerg_base_w*sc2); nh=int(_zerg_base_h*sc2)
            scaled=pygame.transform.smoothscale(_zerg_img,(nw,nh))
            # Légère rotation oscillante
            angle=8*_math.sin(t*.03)
            rotated=pygame.transform.rotate(scaled,angle)
            rr=rotated.get_rect(center=(W//2, H//2+80))
            screen.blit(rotated, rr)
        sf=1.0+0.04*_math.sin(t*.07)
        df=pygame.font.SysFont(None,int(96*sf))
        tc=fw_cols[t//15%len(fw_cols)]
        ts=df.render(title_txt,True,tc)
        screen.blit(ts,(W//2-ts.get_width()//2,H//4))
        ss2=font_med.render(sub_txt,True,(220,220,255))
        screen.blit(ss2,(W//2-ss2.get_width()//2,H//4+110))
        hs=font_small.render("Appuie sur une touche pour continuer",True,(120,120,160))
        screen.blit(hs,(W//2-hs.get_width()//2,H-60))
        pygame.display.flip()
'''

def launch_pygame(codes_by_id, ex_id=''):
    """
    Assemble le code élève fonction par fonction :
    - parcourt les exercices dans l'ordre
    - pour chaque fonction trouvée, la version la plus récente NON-STUB gagne
    (ex4 peut écraser ex3 si sa version est réellement implémentée)
    """
    # Les fonctions propres à l'exercice lancé (celles de son starter) doivent être
    # réellement écrites par l'élève. Sinon, le jeu retomberait en silence sur les
    # versions des exercices précédents (ex. l'ancien play()), ce qui est déroutant.
    current = next((e for e in EXERCISES if e["id"] == ex_id), None)
    if current:
        # Noms des fonctions attendues = celles déclarées dans le starter (même en stub).
        required = _starter_function_names(current["starter"])
        # _extract_functions ignore les stubs (corps 'pass') : une fonction laissée
        # vide n'y figure pas → on la repère comme manquante.
        own = _extract_functions(codes_by_id.get(ex_id, ""))
        missing = [name for name in required if name not in own]
        if missing:
            noms = ", ".join(f"{n}()" for n in missing)
            return (False,
                    f"Tu n'as pas encore écrit {noms} dans l'exercice {current['num']}. "
                    f"Complète ton code avant de lancer le jeu.",
                    False)

    all_ids = [ex["id"] for ex in EXERCISES]
    # On ne fusionne que les exercices JUSQU'À celui qu'on lance (inclus).
    # Sinon, lancer l'exo 3 utiliserait le is_game_over strict de l'exo 4, qui ne
    # reconnaît la victoire que sur C — alors que l'algo de l'exo 3 finit sur B.
    if ex_id in all_ids:
        all_ids = all_ids[:all_ids.index(ex_id) + 1]
    merged  = {}   # nom_fonction → source
    imports = []   # imports de l'élève (dédupliqués), à conserver

    for eid in all_ids:
        code = codes_by_id.get(eid, "").strip()
        if not code:
            continue
        for imp in _extract_imports(code):
            if imp not in imports:
                imports.append(imp)
        for fname, fsrc in _extract_functions(code).items():
            merged[fname] = fsrc   # écrase seulement si non-stub

    stu_code = "\n\n".join(imports + list(merged.values()))

    script = f"""
import sys
sys.path.insert(0, {repr(BASE_DIR)})
import pygame

# Image Zerg embarquée
_ZERG_B64 = "{_ZERG_B64}"

from engine.scene import HanoiScene
from typing import Dict, Iterator, Tuple

# ── code de l'élève ──────────────────────────
{stu_code}
# ─────────────────────────────────────────────

{_CELEBRATION_CODE}

def _show_error(title, lines):
    import pygame
    pygame.init()
    W, H = 740, 300
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption(title)
    font  = pygame.font.SysFont(None, 27)
    small = pygame.font.SysFont(None, 22)
    screen.fill((28, 6, 6))
    pygame.draw.rect(screen, (120, 20, 20), (0, 0, W, 46))
    screen.blit(font.render(title, True, (255, 120, 120)), (16, 12))
    for i, line in enumerate(lines[:8]):
        screen.blit(small.render(str(line)[:92], True, (210, 170, 100)), (16, 58 + i * 26))
    screen.blit(small.render("Appuie sur une touche ou ferme la fenêtre.", True, (110,110,110)), (16, 262))
    pygame.display.flip()
    running = True
    while running:
        for ev in pygame.event.get():
            if ev.type in (pygame.QUIT, pygame.KEYDOWN):
                running = False
    pygame.quit()

EX_ID = "{ex_id}"

try:
    # L'exo 5 demande la fonction récursive play_rec() ; les autres utilisent play().
    # Si play_rec n'est pas encore écrite, la référence lève NameError ci-dessous
    # → écran "Fonction manquante" (au lieu de gagner en silence avec l'ancien play).
    _generator = play_rec if EX_ID == 'ex5' else play
    scene = HanoiScene(
        is_move_valid=is_move_valid,
        is_game_over=is_game_over,
        move_generator=_generator,
        num_disks={NUM_DISKS},
        win_pole=('C' if EX_ID in ('ex4', 'ex5') else None),
    )
    scene.run()
    # ── Victoire ! Écran de félicitation selon l'exercice ──
    if EX_ID in ('ex4', 'ex5'):
        _show_celebration(EX_ID)
except NameError as e:
    _show_error("Fonction manquante", [
        str(e), "",
        "Assure-toi d'avoir écrit toutes les fonctions demandées !"
    ])
    sys.exit(1)
except Exception as e:
    import traceback
    lines = traceback.format_exc().strip().splitlines()
    _show_error("Erreur dans ton code", lines[-10:])
    sys.exit(1)
"""
    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as f:
            f.write(script)
            tmp = f.name
        result = subprocess.run([sys.executable, tmp])
        try:
            os.unlink(tmp)
        except Exception:
            pass
        game_ok = (result.returncode == 0)
        return True, "OK", game_ok
    except Exception:
        lines = traceback.format_exc().strip().splitlines()
        last  = next((l for l in reversed(lines) if l.strip()), "Erreur inconnue")
        return False, last, False
