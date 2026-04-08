# Page d'accueil — onglet Accueil

WELCOME = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>Tours de Hanoï — Accueil</title>
<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
:root {
  --bg:     #0d1117;
  --panel:  #161c2a;
  --card:   #1c2333;
  --border: #2a3550;
  --text:   #ffffff;
  --muted:  #ffffff;
  --blue:   #58a6ff;
  --blue2:  #1f6feb;
  --green:  #3fb950;
  --yellow: #e6b84a;
  --yelbg:  #22200e;
}
html, body { min-height: 100%; background: var(--bg); color: var(--text);
  font-family: 'Segoe UI', system-ui, sans-serif; font-size: 16px; }

/* ── header ── */
header {
  background: var(--panel);
  border-bottom: 2px solid var(--border);
  padding: 0 40px;
  height: 64px;
  display: flex; align-items: center; gap: 14px;
}
header h1 { font-size: 20px; font-weight: 700; color: var(--blue); }
header span { font-size: 13px; color: var(--muted); }

/* ── hero ── */
.hero {
  text-align: center;
  padding: 60px 40px 40px;
}
.hero-icon { font-size: 72px; line-height: 1; margin-bottom: 20px; }
.hero h2   { font-size: 32px; font-weight: 800; color: var(--text); margin-bottom: 10px; }
.hero p    { font-size: 17px; color: #c8d0e0; max-width: 640px; margin: 0 auto; line-height: 1.8; }

/* ── contenu ── */
.content {
  max-width: 860px;
  margin: 0 auto;
  padding: 0 40px 80px;
  display: flex;
  flex-direction: column;
  gap: 28px;
}

/* ── section card ── */
.section {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 14px;
  overflow: hidden;
}
.section-head {
  padding: 16px 24px;
  background: var(--bg);
  border-bottom: 1px solid var(--border);
  display: flex; align-items: center; gap: 12px;
}
.section-icon { font-size: 20px; }
.section-head h3 { font-size: 16px; font-weight: 700; color: var(--text); }
.section-body {
  padding: 22px 24px;
  font-size: 16px;
  line-height: 2;
  color: #ffffff;
}
.section-body b {
  color: #ffffff;
  background: rgba(255,255,255,.1);
  padding: 1px 6px;
  border-radius: 4px;
}
.section-body code {
  background: rgba(88,166,255,.15);
  color: #ffffff;
  padding: 2px 9px;
  border-radius: 5px;
  font-family: 'Cascadia Code','Fira Code','Courier New', monospace;
  font-size: 14px;
  font-weight: 600;
  border: 1px solid rgba(88,166,255,.3);
}
.section-body ul {
  margin: 12px 0 0 20px;
  display: flex; flex-direction: column; gap: 8px;
}
.section-body ul li { list-style: none; padding-left: 8px; }
.section-body ul li::before { content: "→ "; color: var(--blue); font-weight: 700; }

/* ── règles visuelles ── */
.rules {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
  margin-top: 4px;
}
.rule {
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 16px 18px;
  display: flex; gap: 14px; align-items: flex-start;
}
.rule-num {
  width: 32px; height: 32px; border-radius: 50%;
  background: var(--blue2); color: #fff;
  font-size: 15px; font-weight: 800;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.rule-text { font-size: 15px; line-height: 1.7; color: #ffffff; }
.rule-text b { color: var(--text); }

/* ── étapes du TP ── */
.steps {
  display: flex; flex-direction: column; gap: 0;
  margin-top: 4px;
  border: 1px solid var(--border);
  border-radius: 10px;
  overflow: hidden;
}
.step {
  display: flex; align-items: center; gap: 16px;
  padding: 14px 18px;
  border-bottom: 1px solid var(--border);
  font-size: 15px; color: #ffffff;
}
.step:last-child { border-bottom: none; }
.step-badge {
  width: 28px; height: 28px; border-radius: 50%;
  background: var(--blue2); color: #fff;
  font-size: 13px; font-weight: 800;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.step b { color: var(--text); }
.step .lock { margin-left: auto; font-size: 13px; color: var(--border); }

/* ── imports ── */
.imports-block {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 18px 20px;
  margin-top: 4px;
  font-family: 'Cascadia Code','Fira Code','Courier New', monospace;
  font-size: 13px;
  line-height: 1.9;
  color: #8a9abb;
}
.imports-block .kw  { color: #ff7b72; }
.imports-block .mod { color: var(--blue); }
.imports-block .cmt { color: #444d60; }

/* ── bouton ── */
.cta-wrap {
  text-align: center;
  padding: 10px 0 0;
}
.cta-btn {
  display: inline-block;
  background: linear-gradient(135deg, var(--blue2), var(--blue));
  color: #fff;
  text-decoration: none;
  border-radius: 12px;
  padding: 16px 48px;
  font-size: 17px;
  font-weight: 800;
  letter-spacing: .3px;
  transition: filter .15s, transform .15s;
  box-shadow: 0 4px 24px rgba(31,111,235,.35);
}
.cta-btn:hover { filter: brightness(1.15); transform: translateY(-2px); }
.cta-sub { margin-top: 12px; font-size: 15px; color: #c8d0e0; }
</style>
</head>
<body>

<header>
  <h1><svg width="20" height="20" viewBox="0 0 28 28" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align:middle">
  <rect x="12" y="2" width="4" height="22" rx="2" fill="#58a6ff"/>
  <rect x="4" y="20" width="20" height="4" rx="2" fill="#58a6ff"/>
  <rect x="6" y="14" width="16" height="4" rx="1.5" fill="#7dbfff"/>
  <rect x="9" y="9" width="10" height="4" rx="1.5" fill="#9ecfff"/>
</svg> Tours de Hanoï</h1>
  <span>TP Python — Lycée</span>
</header>

<div class="hero">
  <div class="hero-icon"><svg width="80" height="80" viewBox="0 0 28 28" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect x="12" y="2" width="4" height="22" rx="2" fill="#58a6ff"/>
  <rect x="4" y="20" width="20" height="4" rx="2" fill="#58a6ff"/>
  <rect x="6" y="14" width="16" height="4" rx="1.5" fill="#7dbfff"/>
  <rect x="9" y="9" width="10" height="4" rx="1.5" fill="#9ecfff"/>
</svg></div>
  <h2>Bienvenue dans ce TP !</h2>
  <p>Tu vas coder pas à pas un mini jeu-vidéo des <b>Tours de Hanoï</b> en Python,
     et à la fin ton programme jouera <b>tout seul</b> à ta place !</p>
</div>

<div class="content">

  <!-- C'est quoi ? -->
  <div class="section">
    <div class="section-head">
      
      <h3>C'est quoi les Tours de Hanoï ?</h3>
    </div>
    <div class="section-body">
      <p>D'après <b>Wikipedia</b> :</p>
      <br>
      <p>Les tours de Hanoï sont un jeu de réflexion imaginé par le mathématicien
         français <b>Édouard Lucas</b> en 1883. Le but est de déplacer une pile de
         disques de diamètres différents d'une tour de <b>départ</b> vers une tour
         d'<b>arrivée</b>, en passant par une tour <b>intermédiaire</b>, en un minimum
         de coups.</p>
    </div>
  </div>

  <!-- Règles -->
  <div class="section">
    <div class="section-head">
      
      <h3>Les règles du jeu</h3>
    </div>
    <div class="section-body">
      <div class="rules">
        <div class="rule">
          <div class="rule-num">1</div>
          <div class="rule-text">On ne peut déplacer
            <b>qu'un seul disque</b> à la fois.</div>
        </div>
        <div class="rule">
          <div class="rule-num">2</div>
          <div class="rule-text">On ne peut poser un disque que sur un
            <b>disque plus grand</b> que lui, ou sur un
            <b>emplacement vide</b>.</div>
        </div>
      </div>
    </div>
  </div>

  <!-- Ce TP -->
  <div class="section">
    <div class="section-head">
      
      <h3>Ce que tu vas faire dans ce TP</h3>
    </div>
    <div class="section-body">
      <p>Le code du jeu est <b>déjà écrit</b> — la fenêtre de jeu, les graphismes,
         les animations. Il ne te reste qu'à compléter <b>5 fonctions</b>
         qui font tourner la logique du jeu.</p>
      <div class="steps">
        <div class="step">
          <div class="step-badge">1</div>
          <div><b>is_game_over()</b> — la partie est-elle terminée ?</div>
        </div>
        <div class="step">
          <div class="step-badge">2</div>
          <div><b>is_move_valid()</b> — ce mouvement respecte-t-il les règles ?</div>
        </div>
        <div class="step">
          <div class="step-badge">3</div>
          <div><b>play()</b> — un bot qui joue automatiquement (algorithme itératif)</div>
          <span class="lock">après ex. 2</span>
        </div>
        <div class="step">
          <div class="step-badge">4</div>
          <div><b>play() strict</b> — le bot dépose tout sur C uniquement</div>
          <span class="lock">après ex. 3</span>
        </div>
        <div class="step">
          <div class="step-badge">5</div>
          <div><b>play_rec()</b> — version récursive en 3 lignes !</div>
          <span class="lock">après ex. 4</span>
        </div>
      </div>
    </div>
  </div>

  <!-- Imports disponibles -->
  <div class="section">
    <div class="section-head">
      
      <h3>Ce qui est déjà disponible dans ton code</h3>
    </div>
    <div class="section-body">
      <p>Ces imports sont automatiquement disponibles dans chaque exercice,
         tu n'as <b>pas besoin</b> de les réécrire :</p>
      <br>
      <div class="imports-block">
        <span class="cmt"># Types Python pour les annotations</span><br>
        <span class="kw">from</span> typing <span class="kw">import</span>
        <span class="mod">Dict, Iterator, Tuple</span><br><br>
        <span class="cmt"># Les objets du jeu — poles contient A, B et C</span><br>
        <span class="cmt"># poles['A'].num_disks  → nombre de disques sur A</span><br>
        <span class="cmt"># poles['A'].upper_disk.width  → largeur du disque au sommet</span><br>
        <span class="kw">from</span> engine <span class="kw">import</span>
        <span class="mod">Pole, Disk</span>
      </div>
    </div>
  </div>

  <!-- Bouton -->
  <div class="cta-wrap">
    <a class="cta-btn" href="/tp">Commencer le TP →</a>
    <p class="cta-sub">Les exercices se débloquent dans l'ordre — commence par le 1 !</p>
  </div>

</div>
</body>
</html>
"""

