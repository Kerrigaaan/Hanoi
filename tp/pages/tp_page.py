# Page exercices — onglet Exercices (template principal)

HTML = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>TP — Tours de Hanoï</title>
<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --bg:      #0d1117;
  --panel:   #161c2a;
  --card:    #1c2333;
  --border:  #2a3550;
  --border2: #3a4f72;
  --text:    #ffffff;
  --muted:   #c8d0e0;
  --hint:    #6a7a9a;
  --blue:    #58a6ff;
  --blue2:   #1f6feb;
  --green:   #3fb950;
  --red:     #f85149;
  --yellow:  #e6b84a;
  --yelbg:   #22200e;
  --lock-bg: #0a0e18;
}

html { height: 100%; }
body {
  min-height: 100%;
  background: var(--bg);
  color: var(--text);
  font-family: 'Segoe UI', system-ui, sans-serif;
  font-size: 16px;
}

/* ── header ── */
header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: var(--panel);
  border-bottom: 2px solid var(--border2);
  padding: 0 32px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
}
.hdr-left h1 { font-size: 20px; font-weight: 700; color: #ffffff; }
.hdr-left p  { font-size: 15px; color: #ccddee; margin-top: 3px; }
.hdr-right   { display: flex; align-items: center; gap: 18px; flex-shrink: 0; }

#statusMsg { font-size: 15px; max-width: 500px; color: #ffffff; }
#statusMsg.ok   { color: var(--green); }
#statusMsg.err  { color: var(--red);   }
#statusMsg.info { color: var(--blue);  }
#statusMsg.warn { color: var(--yellow);}

/* ── contenu ── */
main {
  padding: 36px 48px 60px;
  display: flex;
  flex-direction: column;
  gap: 28px;
  max-width: 1300px;
  margin: 0 auto;
}

/* ── card ── */
.card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 14px;
  overflow: hidden;
  transition: opacity .25s;
}

/* état verrouillé */
.card.locked {
  opacity: .45;
  pointer-events: none;  /* interdit tout clic / saisie */
}

.card-head {
  padding: 16px 22px;
  background: var(--bg);
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  gap: 14px;
}
.badge {
  width: 30px; height: 30px;
  border-radius: 50%;
  background: var(--blue2);
  color: #fff;
  font-size: 14px; font-weight: 800;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
  transition: background .25s;
}
.card.locked .badge { background: var(--hint); }
.card.passed .badge { background: var(--green); }

.card-title { font-size: 17px; font-weight: 700; color: #ffffff; }

/* cadenas affiché dans le header quand locked */
.lock-icon {
  margin-left: auto;
  font-size: 15px;
  color: var(--hint);
  display: none;
}
.card.locked .lock-icon { display: block; }

/* ── consigne ── */
.instr {
  margin: 16px 22px 0;
  padding: 14px 18px;
  background: var(--yelbg);
  border-left: 4px solid var(--yellow);
  border-radius: 0 10px 10px 0;
  font-size: 16px;
  line-height: 2.1;
  color: #ffffff;
  user-select: none;
  pointer-events: none;
}
.instr code {
  background: rgba(88,166,255,.15);
  color: #ffffff;
  padding: 2px 9px;
  border-radius: 5px;
  font-family: 'Cascadia Code','Fira Code','Courier New', monospace;
  font-size: 14px;
  font-weight: 600;
  border: 1px solid rgba(88,166,255,.3);
}
.instr b {
  color: #ffffff;
  font-weight: 800;
  text-decoration: underline;
  text-underline-offset: 3px;
}

/* ── éditeur ── */
.code-lbl {
  padding: 12px 22px 5px;
  font-size: 14px;
  color: #ccddee;
  text-transform: uppercase;
  letter-spacing: .08em;
}
.code-wrap {
  margin: 0 22px;
  border-radius: 10px;
  overflow: hidden;
  border: 1px solid var(--border2);
}
.code-wrap:focus-within { border-color: var(--blue); box-shadow: 0 0 0 3px rgba(88,166,255,.12); }
textarea {
  display: block; width: 100%;
  background: var(--bg); color: #ffffff;
  font-family: 'Cascadia Code','Fira Code','Courier New', monospace;
  font-size: 16px; line-height: 1.8;
  padding: 16px 18px;
  border: none; outline: none;
  resize: none;        /* auto-resize via JS — pas de poignée manuelle */
  min-height: 60px;
  overflow: hidden;    /* cache la scrollbar pendant le resize auto */
  /* Guides d'indentation : un trait vertical fin tous les 4 caractères.
     1ch = largeur d'un caractère en police monospace → 4ch = un niveau d'indentation.
     Le dégradé est répété ; le trait est posé au bord droit de chaque bloc de 4ch. */
  background-image: repeating-linear-gradient(
    to right,
    transparent 0,
    transparent calc(4ch - 1px),
    var(--indent-guide, rgba(255,255,255,.10)) calc(4ch - 1px),
    var(--indent-guide, rgba(255,255,255,.10)) 4ch
  );
  background-origin: content-box;            /* aligne les traits sur le début du texte */
  background-clip: content-box, border-box;  /* traits limités au texte ; fond plein conservé */
  background-attachment: local;              /* les traits suivent le texte au défilement */
}

/* ── actions ── */
.card-actions {
  padding: 14px 22px 18px;
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

/* bouton Tester */
.test-btn {
  background: var(--bg); color: var(--blue);
  border: 1px solid var(--blue2);
  border-radius: 7px; padding: 8px 20px;
  font-size: 13px; font-weight: 600;
  cursor: pointer; transition: .12s;
}
.test-btn:hover { background: var(--blue2); color: #fff; }

/* bouton Lancer */
.run-btn {
  background: linear-gradient(135deg, #145214, var(--green));
  color: #fff;
  border: none;
  border-radius: 7px; padding: 8px 22px;
  font-size: 13px; font-weight: 700;
  cursor: pointer; transition: filter .15s;
}
.run-btn:hover { filter: brightness(1.15); }
.run-btn:disabled { opacity: .4; cursor: not-allowed; filter: none; }

/* résultat du test */
.result { font-size: 15px; font-weight: 700; }
.result.ok  { color: #4ade80; }
.result.err { color: #ff7070; }
.result.run { color: #aabbcc; }

/* message de lancement */
.launch-result { font-size: 15px; font-weight: 700; }
.launch-result.ok  { color: #4ade80; }
.launch-result.err { color: #ff7070; }

/* message "termine d'abord…" visible sous une card locked */
.locked-msg {
  display: none;
  text-align: center;
  font-size: 13px;
  color: var(--hint);
  padding: 6px 0 2px;
  font-style: italic;
}
.card.locked + .locked-msg { display: block; font-size: 15px; color: #aabbcc; }


/* ── Onglets ──────────────────────────────────────────────── */
.tabs {
  display: flex;
  gap: 4px;
  background: var(--bg);
  border-bottom: 2px solid var(--border);
  padding: 0 32px;
  flex-shrink: 0;
}
.tab-btn {
  padding: 12px 28px;
  font-size: 15px;
  font-weight: 600;
  color: var(--muted);
  background: transparent;
  border: none;
  border-bottom: 3px solid transparent;
  margin-bottom: -2px;
  cursor: pointer;
  transition: color .15s, border-color .15s;
}
.tab-btn:hover { color: #ffffff; }
.tab-btn.active { color: var(--blue); border-bottom-color: var(--blue); }

/* ── Panneaux ──────────────────────────────────────────────── */
.tab-panel { display: none; }
.tab-panel.active { display: block; }

/* ── Styles page accueil ── */

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

/* ── Doc intégrée (reprise des styles DOCS) ─────────────────── */

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
:root {
  --bg:     #0d1117;
  --panel:  #161c2a;
  --card:   #1c2333;
  --border: #2a3550;
  --blue:   #58a6ff;
  --blue2:  #1f6feb;
  --green:  #3fb950;
  --yellow: #e6b84a;
  --yelbg:  #22200e;
  --purple: #c678dd;
  --orange: #e5a24b;
  --teal:   #56b6c2;
}
html, body {
  min-height: 100%;
  background: var(--bg);
  color: #ffffff;
  font-family: 'Segoe UI', system-ui, sans-serif;
  font-size: 16px;
}

/* ── header ── */
header {
  position: sticky; top: 0; z-index: 100;
  background: var(--panel);
  border-bottom: 2px solid var(--border);
  padding: 0 32px; height: 64px;
  display: flex; align-items: center; justify-content: space-between;
}
.hdr-left { display: flex; align-items: center; gap: 14px; }
.hdr-left h1 { font-size: 18px; font-weight: 700; color: var(--blue); }
.back-btn {
  background: var(--card); color: var(--blue);
  border: 1px solid var(--blue2); border-radius: 8px;
  padding: 8px 18px; font-size: 14px; font-weight: 600;
  text-decoration: none; transition: .12s;
}
.back-btn:hover { background: var(--blue2); color: #fff; }

/* ── layout ── */
.layout {
  display: flex;
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 32px 60px;
  gap: 32px;
}

/* ── sidebar navigation ── */
.sidebar {
  flex: 0 0 220px;
  position: sticky;
  top: 80px;
  align-self: flex-start;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.sidebar-title {
  font-size: 11px;
  font-weight: 700;
  color: #6a7a9a;
  text-transform: uppercase;
  letter-spacing: .08em;
  padding: 0 10px 10px;
}
.nav-link {
  display: block;
  padding: 9px 14px;
  border-radius: 8px;
  font-size: 14px;
  color: #c8d0e0;
  text-decoration: none;
  transition: .12s;
  border-left: 3px solid transparent;
}
.nav-link:hover { background: var(--card); color: #fff; }
.nav-link.active { background: var(--card); color: var(--blue); border-left-color: var(--blue); }

/* ── contenu ── */
.content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 28px;
  min-width: 0;
}

/* ── section doc ── */
.doc-section {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 14px;
  overflow: hidden;
  scroll-margin-top: 80px;
}
.doc-head {
  padding: 16px 24px;
  background: var(--bg);
  border-bottom: 1px solid var(--border);
  display: flex; align-items: center; gap: 12px;
}
.doc-icon { font-size: 20px; }
.doc-head h2 { font-size: 17px; font-weight: 700; color: #ffffff; }
.doc-body {
  padding: 22px 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* ── sous-sections ── */
.sub { display: flex; flex-direction: column; gap: 10px; }
.sub-title {
  font-size: 15px;
  font-weight: 700;
  color: var(--blue);
  border-bottom: 1px solid var(--border);
  padding-bottom: 6px;
}
.sub p, .sub li {
  font-size: 15px;
  line-height: 1.9;
  color: #c8d0e0;
}
.sub ul { padding-left: 20px; display: flex; flex-direction: column; gap: 5px; }
.sub ul li::marker { color: var(--blue); }

/* ── blocs de code ── */
.code-block {
  background: #070b12;
  border: 1px solid var(--border);
  border-radius: 10px;
  overflow: hidden;
}
.code-label {
  padding: 6px 16px;
  background: var(--panel);
  border-bottom: 1px solid var(--border);
  font-size: 11px;
  color: #6a7a9a;
  text-transform: uppercase;
  letter-spacing: .06em;
}
pre {
  padding: 16px 18px;
  font-family: 'Cascadia Code','Fira Code','Courier New', monospace;
  font-size: 14px;
  line-height: 1.85;
  overflow-x: auto;
  color: #abb2bf;
}
/* coloration syntaxique manuelle */
.kw  { color: #c678dd; }   /* keywords */
.fn  { color: #61afef; }   /* fonctions */
.st  { color: #98c379; }   /* strings */
.nb  { color: #e5c07b; }   /* nombres */
.cm  { color: #5c6370; font-style: italic; }   /* commentaires */
.op  { color: #56b6c2; }   /* opérateurs */
.var { color: #e06c75; }   /* variables / noms */

/* ── astuce / attention ── */
.tip {
  display: flex; gap: 12px; align-items: flex-start;
  background: #0e2010; border: 1px solid #1e5c28;
  border-radius: 10px; padding: 16px 18px;
  font-size: 15px; line-height: 1.9; color: #ffffff;
}
.warn {
  display: flex; gap: 12px; align-items: flex-start;
  background: #1c1205; border: 1px solid #7a5010;
  border-radius: 10px; padding: 14px 16px;
  font-size: 14px; line-height: 1.7; color: #f0c070;
}
.tip-icon, .warn-icon { font-size: 18px; flex-shrink: 0; margin-top: 1px; }

/* ── inline code ── */
ic { display: inline;
  background: rgba(88,166,255,.15);
  color: #ffffff; padding: 1px 7px; border-radius: 4px;
  font-family: 'Cascadia Code','Fira Code', monospace;
  font-size: 14px; font-weight: 600;
  border: 1px solid rgba(88,166,255,.25); }

</style>
</head>
<body>

<!-- header sans bouton docs -->
<header>
  <div class="hdr-left">
    <h1><svg width="20" height="20" viewBox="0 0 28 28" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align:middle">
  <rect x="12" y="2" width="4" height="22" rx="2" fill="#58a6ff"/>
  <rect x="4" y="20" width="20" height="4" rx="2" fill="#58a6ff"/>
  <rect x="6" y="14" width="16" height="4" rx="1.5" fill="#7dbfff"/>
  <rect x="9" y="9" width="10" height="4" rx="1.5" fill="#9ecfff"/>
</svg> TP — Tours de Hanoï</h1>
    <p>Fais les exercices <b>dans l\'ordre</b> — chaque exercice se débloque quand le précédent est réussi.</p>
  </div>
  <div class="hdr-right">
    <span id="statusMsg" class="info">Commence par l\'exercice 1 !</span>
  </div>
</header>

<!-- barre d'onglets -->
<div class="tabs">
  <button type="button" class="tab-btn active" id="tab-accueil"   onclick="switchTab('accueil')">Accueil</button>
  <button type="button" class="tab-btn" id="tab-exercises" onclick="switchTab('exercises')">Exercices</button>
  <button type="button" class="tab-btn" id="tab-docs"      onclick="switchTab('docs')">Documentation Python</button>
  <button type="button" class="tab-btn fun-tab hidden" id="tab-fun" onclick="switchTab('fun')">🎉 Défis Fun</button>
</div>

<!-- panneau accueil -->
<div id="panel-accueil" class="tab-panel active" style="overflow-y:auto;max-height:calc(100vh - 120px)">
  <div style="max-width:860px;margin:0 auto;padding:0 40px 60px">
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
    <button type="button" class="cta-btn" onclick="switchTab('exercises')">Commencer les exercices →</button>
    <p class="cta-sub">Les exercices se débloquent dans l'ordre — commence par le 1 !</p>
  </div>

</div>
  </div>
</div>

<!-- panneau exercices -->
<div id="panel-exercises" class="tab-panel" style="overflow-y:auto;max-height:calc(100vh - 120px);min-height:0">
  <main id="exList"></main>
</div></div>

<!-- panneau documentation -->
<div id="panel-docs" class="tab-panel">
<div class="layout">

  <!-- ── Sidebar ── -->
  <nav class="sidebar">
    <div class="sidebar-title">Sommaire</div>
    <a class="nav-link active" href="#booleens">Les booléens</a>
    <a class="nav-link" href="#conditions">Les conditions</a>
    <a class="nav-link" href="#fonctions">Les fonctions</a>
    <a class="nav-link" href="#retour">Retourner une valeur</a>
    <a class="nav-link" href="#boucles">Les boucles</a>
    <a class="nav-link" href="#yield">Le mot-clé yield</a>
    <a class="nav-link" href="#recursion">La récursion</a>
    <a class="nav-link" href="#objets">Accéder à un objet</a>
  </nav>

  <!-- ── Contenu ── -->
  <div class="content">

    <!-- BOOLÉENS -->
    <div class="doc-section" id="booleens">
      <div class="doc-head">
        
        <h2>Les booléens — Vrai ou Faux</h2>
      </div>
      <div class="doc-body">
        <div class="sub">
          <p>Un <b>booléen</b> est une valeur qui vaut soit <ic>True</ic> (vrai) soit <ic>False</ic> (faux). C'est le type de résultat que doivent retourner tes fonctions <ic>is_game_over()</ic> et <ic>is_move_valid()</ic>.</p>
        </div>
        <div class="sub">
          <div class="sub-title">Comparer des nombres</div>
          <div class="code-block">
            <div class="code-label">Exemples de comparaisons</div>
            <pre><span class="nb">5</span> <span class="op">==</span> <span class="nb">5</span>     <span class="cm"># True  — 5 est-il égal à 5 ?</span>
<span class="nb">3</span> <span class="op">==</span> <span class="nb">0</span>     <span class="cm"># False — 3 est-il égal à 0 ?</span>
<span class="nb">3</span> <span class="op">></span>  <span class="nb">1</span>     <span class="cm"># True  — 3 est-il plus grand que 1 ?</span>
<span class="nb">2</span> <span class="op">></span>  <span class="nb">5</span>     <span class="cm"># False — 2 est-il plus grand que 5 ?</span></pre>
          </div>
        </div>
        <div class="sub">
          <div class="sub-title">Combiner des conditions avec and / or</div>
          <div class="code-block">
            <div class="code-label">and = les deux doivent être vrais</div>
            <pre><span class="kw">True</span>  <span class="op">and</span> <span class="kw">True</span>   <span class="cm"># True</span>
<span class="kw">True</span>  <span class="op">and</span> <span class="kw">False</span>  <span class="cm"># False</span>
<span class="kw">False</span> <span class="op">and</span> <span class="kw">True</span>   <span class="cm"># False</span></pre>
          </div>
          <div class="code-block">
            <div class="code-label">or = au moins un doit être vrai</div>
            <pre><span class="kw">True</span>  <span class="op">or</span> <span class="kw">False</span>   <span class="cm"># True</span>
<span class="kw">False</span> <span class="op">or</span> <span class="kw">False</span>   <span class="cm"># False</span></pre>
          </div>
        </div>
        <div class="tip">
          <span class="tip-icon" style="font-size:16px;flex-shrink:0">i</span>
          <span>Tu peux directement <b>retourner le résultat d'une comparaison</b> sans écrire <ic>if</ic>. Par exemple : <ic>return x == 0</ic> retourne <ic>True</ic> si x vaut 0, <ic>False</ic> sinon.</span>
        </div>
      </div>
    </div>

    <!-- CONDITIONS -->
    <div class="doc-section" id="conditions">
      <div class="doc-head">
        
        <h2>Les conditions — if / elif / else</h2>
      </div>
      <div class="doc-body">
        <div class="sub">
          <p>Une condition permet d'exécuter du code <b>seulement si</b> quelque chose est vrai.</p>
          <div class="code-block">
            <div class="code-label">Structure d'un if</div>
            <pre><span class="kw">if</span> <span class="var">condition</span><span class="op">:</span>
    <span class="cm"># ce code s'exécute si condition est True</span>
    ...
<span class="kw">elif</span> <span class="var">autre_condition</span><span class="op">:</span>
    <span class="cm"># sinon, si cette autre condition est True</span>
    ...
<span class="kw">else</span><span class="op">:</span>
    <span class="cm"># sinon (aucune condition n'était vraie)</span>
    ...</pre>
          </div>
        </div>
        <div class="sub">
          <div class="sub-title">Exemple concret</div>
          <div class="code-block">
            <div class="code-label">Exemple</div>
            <pre><span class="var">score</span> <span class="op">=</span> <span class="nb">42</span>

<span class="kw">if</span> <span class="var">score</span> <span class="op">==</span> <span class="nb">0</span><span class="op">:</span>
    <span class="fn">print</span>(<span class="st">"Score nul"</span>)
<span class="kw">elif</span> <span class="var">score</span> <span class="op">></span> <span class="nb">100</span><span class="op">:</span>
    <span class="fn">print</span>(<span class="st">"Score énorme"</span>)
<span class="kw">else</span><span class="op">:</span>
    <span class="fn">print</span>(<span class="st">"Score normal"</span>)   <span class="cm"># affiché ici</span></pre>
          </div>
        </div>
        <div class="warn">
          <span class="warn-icon" style="font-size:16px;flex-shrink:0;color:#e6b84a;font-weight:800">!</span>
          <span>En Python, l'<b>indentation</b> (les espaces au début de chaque ligne) est obligatoire. Tout ce qui est à l'intérieur d'un <ic>if</ic> doit être décalé de 4 espaces.</span>
        </div>
      </div>
    </div>

    <!-- FONCTIONS -->
    <div class="doc-section" id="fonctions">
      <div class="doc-head">
        
        <h2>Les fonctions — def</h2>
      </div>
      <div class="doc-body">
        <div class="sub">
          <p>Une <b>fonction</b> est un bloc de code réutilisable qui effectue une tâche précise. On la définit avec le mot-clé <ic>def</ic>.</p>
          <div class="code-block">
            <div class="code-label">Structure d'une fonction</div>
            <pre><span class="kw">def</span> <span class="fn">nom_de_la_fonction</span>(<span class="var">parametre1</span>, <span class="var">parametre2</span>)<span class="op">:</span>
    <span class="cm"># code de la fonction</span>
    ...
    <span class="kw">return</span> <span class="var">resultat</span></pre>
          </div>
        </div>
        <div class="sub">
          <div class="sub-title">Exemple</div>
          <div class="code-block">
            <div class="code-label">Exemple</div>
            <pre><span class="kw">def</span> <span class="fn">est_positif</span>(<span class="var">nombre</span>)<span class="op">:</span>
    <span class="kw">if</span> <span class="var">nombre</span> <span class="op">></span> <span class="nb">0</span><span class="op">:</span>
        <span class="kw">return</span> <span class="kw">True</span>
    <span class="kw">else</span><span class="op">:</span>
        <span class="kw">return</span> <span class="kw">False</span>

<span class="fn">est_positif</span>(<span class="nb">5</span>)    <span class="cm"># donne True</span>
<span class="fn">est_positif</span>(<span class="op">-</span><span class="nb">3</span>)   <span class="cm"># donne False</span></pre>
          </div>
        </div>
      </div>
    </div>

    <!-- RETOURNER -->
    <div class="doc-section" id="retour">
      <div class="doc-head">
        
        <h2>Retourner une valeur — return</h2>
      </div>
      <div class="doc-body">
        <div class="sub">
          <p>Le mot-clé <ic>return</ic> permet de <b>renvoyer un résultat</b> depuis une fonction. Dès qu'un <ic>return</ic> est atteint, la fonction s'arrête immédiatement.</p>
          <div class="code-block">
            <div class="code-label">Plusieurs return possibles</div>
            <pre><span class="kw">def</span> <span class="fn">ma_fonction</span>(<span class="var">x</span>)<span class="op">:</span>
    <span class="kw">if</span> <span class="var">x</span> <span class="op">==</span> <span class="nb">0</span><span class="op">:</span>
        <span class="kw">return</span> <span class="kw">False</span>   <span class="cm"># s'arrête ici si x == 0</span>
    <span class="kw">return</span> <span class="kw">True</span>        <span class="cm"># sinon, arrive ici</span></pre>
          </div>
        </div>
        <div class="tip">
          <span class="tip-icon" style="font-size:16px;flex-shrink:0">i</span>
          <span>On peut avoir <b>plusieurs <ic>return</ic></b> dans une même fonction. Le premier <ic>return</ic> atteint lors de l'exécution arrête la fonction.</span>
        </div>
      </div>
    </div>

    <!-- BOUCLES -->
    <div class="doc-section" id="boucles">
      <div class="doc-head">
        
        <h2>Les boucles — while / for</h2>
      </div>
      <div class="doc-body">
        <div class="sub">
          <div class="sub-title">La boucle while — tant que</div>
          <p>Répète un bloc de code <b>tant qu'une condition est vraie</b>.</p>
          <div class="code-block">
            <div class="code-label">Structure while</div>
            <pre><span class="kw">while</span> <span class="var">condition</span><span class="op">:</span>
    <span class="cm"># répété tant que condition est True</span>
    ...</pre>
          </div>
          <div class="code-block">
            <div class="code-label">Exemple — compter jusqu'à 3</div>
            <pre><span class="var">i</span> <span class="op">=</span> <span class="nb">0</span>
<span class="kw">while</span> <span class="var">i</span> <span class="op"><</span> <span class="nb">3</span><span class="op">:</span>
    <span class="fn">print</span>(<span class="var">i</span>)   <span class="cm"># affiche 0, puis 1, puis 2</span>
    <span class="var">i</span> <span class="op">=</span> <span class="var">i</span> <span class="op">+</span> <span class="nb">1</span></pre>
          </div>
        </div>
        <div class="sub">
          <div class="sub-title">La boucle for — pour chaque</div>
          <p>Parcourt une liste d'éléments un par un.</p>
          <div class="code-block">
            <div class="code-label">Exemple — parcourir une liste</div>
            <pre><span class="var">paires</span> <span class="op">=</span> [(<span class="st">'A'</span>, <span class="st">'B'</span>), (<span class="st">'A'</span>, <span class="st">'C'</span>), (<span class="st">'B'</span>, <span class="st">'C'</span>)]

<span class="kw">for</span> <span class="var">p1</span>, <span class="var">p2</span> <span class="kw">in</span> <span class="var">paires</span><span class="op">:</span>
    <span class="fn">print</span>(<span class="var">p1</span>, <span class="st">"→"</span>, <span class="var">p2</span>)
<span class="cm"># affiche : A → B, puis A → C, puis B → C</span></pre>
          </div>
        </div>
        <div class="warn">
          <span class="warn-icon" style="font-size:16px;flex-shrink:0;color:#e6b84a;font-weight:800">!</span>
          <span>Une boucle <ic>while True:</ic> tourne <b>indéfiniment</b>. Il faut toujours prévoir une façon d'en sortir, avec <ic>break</ic> ou en utilisant <ic>yield</ic> (voir plus bas).</span>
        </div>
      </div>
    </div>

    <!-- YIELD -->
    <div class="doc-section" id="yield">
      <div class="doc-head">
        
        <h2>Le mot-clé yield — générateur</h2>
      </div>
      <div class="doc-body">
        <div class="sub">
          <p><ic>yield</ic> permet à une fonction de <b>produire des valeurs une par une</b>, à la demande, sans tout calculer d'un coup. Une fonction qui contient <ic>yield</ic> s'appelle un <b>générateur</b>.</p>
        </div>
        <div class="sub">
          <div class="sub-title">Différence avec return</div>
          <ul>
            <li>Avec <ic>return</ic> : la fonction s'arrête et renvoie une valeur.</li>
            <li>Avec <ic>yield</ic> : la fonction <b>se met en pause</b> et renvoie une valeur, puis <b>reprend</b> là où elle s'est arrêtée au prochain appel.</li>
          </ul>
        </div>
        <div class="sub">
          <div class="sub-title">Exemple simple</div>
          <div class="code-block">
            <div class="code-label">Un générateur qui donne 3 valeurs</div>
            <pre><span class="kw">def</span> <span class="fn">compteur</span>()<span class="op">:</span>
    <span class="kw">yield</span> <span class="nb">1</span>   <span class="cm"># pause ici, donne 1</span>
    <span class="kw">yield</span> <span class="nb">2</span>   <span class="cm"># pause ici, donne 2</span>
    <span class="kw">yield</span> <span class="nb">3</span>   <span class="cm"># pause ici, donne 3</span></pre>
          </div>
        </div>
        <div class="sub">
          <div class="sub-title">yield dans une boucle</div>
          <div class="code-block">
            <div class="code-label">Générateur infini</div>
            <pre><span class="kw">def</span> <span class="fn">ma_fonction</span>()<span class="op">:</span>
    <span class="kw">while</span> <span class="kw">True</span><span class="op">:</span>
        <span class="kw">yield</span> (<span class="st">'A'</span>, <span class="st">'B'</span>)   <span class="cm"># donne A→B, attend, reprend...</span>
        <span class="kw">yield</span> (<span class="st">'A'</span>, <span class="st">'C'</span>)   <span class="cm"># donne A→C, attend, reprend...</span></pre>
          </div>
        </div>
        <div class="sub">
          <div class="sub-title">yield from — déléguer à une autre fonction</div>
          <p><ic>yield from</ic> permet de <b>déléguer</b> tous les <ic>yield</ic> d'une autre fonction génératrice.</p>
          <div class="code-block">
            <div class="code-label">Exemple yield from</div>
            <pre><span class="kw">def</span> <span class="fn">sous_fonction</span>()<span class="op">:</span>
    <span class="kw">yield</span> <span class="nb">1</span>
    <span class="kw">yield</span> <span class="nb">2</span>

<span class="kw">def</span> <span class="fn">ma_fonction</span>()<span class="op">:</span>
    <span class="kw">yield from</span> <span class="fn">sous_fonction</span>()  <span class="cm"># donne 1, puis 2</span>
    <span class="kw">yield</span> <span class="nb">3</span>                      <span class="cm"># puis donne 3</span></pre>
          </div>
        </div>
        <div class="tip">
          <span class="tip-icon" style="font-size:16px;flex-shrink:0">i</span>
          <span>Dans le TP, le jeu appelle ta fonction <ic>play()</ic> et récupère les coups un par un avec <ic>yield</ic>. Tu n'as pas à gérer toi-même quand la partie s'arrête — le jeu s'en charge.</span>
        </div>
      </div>
    </div>

    <!-- RÉCURSION -->
    <div class="doc-section" id="recursion">
      <div class="doc-head">
        
        <h2>La récursion — fonction qui s'appelle elle-même</h2>
      </div>
      <div class="doc-body">
        <div class="sub">
          <p>Une fonction <b>récursive</b> est une fonction qui s'appelle elle-même pour résoudre un problème plus petit.</p>
        </div>
        <div class="sub">
          <div class="sub-title">Les deux règles obligatoires</div>
          <ul>
            <li>Un <b>cas de base</b> : une condition qui arrête la récursion.</li>
            <li>Un <b>appel récursif</b> : la fonction se rappelle avec un problème plus petit.</li>
          </ul>
        </div>
        <div class="sub">
          <div class="sub-title">Exemple — compter à rebours</div>
          <div class="code-block">
            <div class="code-label">Exemple récursif</div>
            <pre><span class="kw">def</span> <span class="fn">compte_a_rebours</span>(<span class="var">n</span>)<span class="op">:</span>
    <span class="kw">if</span> <span class="var">n</span> <span class="op">==</span> <span class="nb">0</span><span class="op">:</span>          <span class="cm"># cas de base — STOP</span>
        <span class="kw">return</span>
    <span class="fn">print</span>(<span class="var">n</span>)            <span class="cm"># affiche n</span>
    <span class="fn">compte_a_rebours</span>(<span class="var">n</span> <span class="op">-</span> <span class="nb">1</span>)  <span class="cm"># appel récursif</span>

<span class="fn">compte_a_rebours</span>(<span class="nb">3</span>)
<span class="cm"># affiche : 3, puis 2, puis 1</span></pre>
          </div>
        </div>
        <div class="warn">
          <span class="warn-icon" style="font-size:16px;flex-shrink:0;color:#e6b84a;font-weight:800">!</span>
          <span>Sans cas de base, la récursion ne s'arrête jamais et provoque une erreur. Vérifie toujours que ton <ic>if n == 0</ic> (ou équivalent) est présent !</span>
        </div>
      </div>
    </div>

    <!-- OBJETS -->
    <div class="doc-section" id="objets">
      <div class="doc-head">
        
        <h2>Accéder aux objets du jeu</h2>
      </div>
      <div class="doc-body">
        <div class="sub">
          <p>Dans ce TP, <ic>poles</ic> est un dictionnaire qui contient les trois poteaux <ic>'A'</ic>, <ic>'B'</ic> et <ic>'C'</ic>. Chaque poteau est un <b>objet</b> qui possède des propriétés accessibles avec un point <ic>.</ic></p>
        </div>
        <div class="sub">
          <div class="sub-title">Propriétés disponibles</div>
          <div class="code-block">
            <div class="code-label">Ce que tu peux utiliser</div>
            <pre><span class="cm"># Nombre de disques sur le poteau A</span>
<span class="var">poles</span>[<span class="st">'A'</span>].<span class="var">num_disks</span>

<span class="cm"># Vaut 0 si le poteau A est vide</span>
<span class="var">poles</span>[<span class="st">'A'</span>].<span class="var">num_disks</span> <span class="op">==</span> <span class="nb">0</span>

<span class="cm"># Largeur du disque au sommet du poteau A</span>
<span class="cm"># (attention : erreur si le poteau est vide !)</span>
<span class="var">poles</span>[<span class="st">'A'</span>].<span class="var">upper_disk</span>.<span class="var">width</span>

<span class="cm"># Pour accéder à un poteau dont le nom est dans une variable :</span>
<span class="var">source</span> <span class="op">=</span> <span class="st">'B'</span>
<span class="var">poles</span>[<span class="var">source</span>].<span class="var">num_disks</span>   <span class="cm"># identique à poles['B'].num_disks</span></pre>
          </div>
        </div>
        <div class="warn">
          <span class="warn-icon" style="font-size:16px;flex-shrink:0;color:#e6b84a;font-weight:800">!</span>
          <span>Avant d'accéder à <ic>upper_disk.width</ic>, assure-toi que le poteau n'est <b>pas vide</b> — sinon Python lève une erreur. Utilise d'abord <ic>num_disks == 0</ic> pour vérifier.</span>
        </div>
      </div>
    </div>

  </div><!-- /content -->
</div><!-- /layout -->
</div>

<script>
function switchTab(name) {
  document.querySelectorAll('.tab-btn').forEach(b => {
    b.classList.toggle('active', b.id === 'tab-' + name);
  });
  document.querySelectorAll('.tab-panel').forEach(p => {
    p.classList.toggle('active', p.id === 'panel-' + name);
  });
  try { localStorage.setItem('hanoi_tab', name); } catch(e) {}
  // Relance l'auto-resize quand on arrive sur l'onglet exercices
  if (name === 'exercises') {
    document.querySelectorAll('#panel-exercises textarea').forEach(autoResize);
  }
}

document.addEventListener('click', function(e) {
  const btn = e.target.closest('[data-tab]');
  if (btn) { e.preventDefault(); switchTab(btn.dataset.tab); }
});

(function() {
  const saved = localStorage.getItem('hanoi_tab');
  if (saved && saved !== 'accueil') switchTab(saved);
}());


// Restaure onglet au chargement
(function() {
  var saved = localStorage.getItem('hanoi_tab');
  if (saved && saved !== 'accueil') switchTab(saved);
}());

const EXS = %EXERCISES_JSON%;

// ── état global ──────────────────────────────────────────────
// passed[id]  = true quand le test de cet exo est vert
// ex3_run     = true quand le Lancer de ex3 a réussi au moins une fois
//               → géré côté serveur Python, rechargé au démarrage
const passed  = {};
EXS.forEach(ex => passed[ex.id] = false);
let ex3_run = false;  // sera mis à jour par /api/state au chargement
let ex4_run = false;

// ── construction des cartes ──────────────────────────────────
const list = document.getElementById('exList');

EXS.forEach((ex, idx) => {
  // La card elle-même
  const card = document.createElement('div');
  card.className = 'card' + (ex.unlock_after ? ' locked' : '');
  card.id = 'card-' + ex.id;

  const hasTest   = !!ex.check_call;
  const hasLaunch = ex.has_launch;

  card.innerHTML = `
    <div class="card-head">
      <div class="badge" id="badge-${ex.id}">${ex.num}</div>
      <div class="card-title">${ex.title}</div>
      <span class="lock-icon">verrouillé</span>
    </div>
    <div class="instr">
      ${ex.instructions.map(l => l==='' ? '<br>' : '<div>'+l+'</div>').join('')}
    </div>
    <div class="code-lbl">${ex.code_label || 'Ton code Python'}</div>
    <div class="code-wrap">
      <textarea id="c${ex.id}" spellcheck="false"
        onkeydown="handleTab(event)">${ex.starter}</textarea>
    </div>
    <div class="card-actions">
      ${hasTest
        ? `<button class="test-btn" id="tbtn-${ex.id}"
               onclick="runTest('${ex.id}')">▶ Tester</button>
           <span class="result" id="r${ex.id}"></span>`
        : ''}
      ${hasLaunch
        ? `<button class="run-btn" id="lbtn-${ex.id}"
               onclick="launchEx('${ex.id}')"
               ${ex.unlock_after ? 'disabled' : ''}>
             Lancer le jeu
           </button>
           <span class="launch-result" id="lr${ex.id}"></span>`
        : ''}
    </div>`;

  list.appendChild(card);

  // Message "débloque d'abord l'exo précédent"
  if (ex.unlock_after) {
    const msg = document.createElement('p');
    msg.className = 'locked-msg';
    const prev = EXS[idx - 1];
    msg.textContent = `Termine l'exercice ${prev ? prev.num : '?'} d'abord !`;
    list.appendChild(msg);
  }
});

// ── auto-resize textarea ────────────────────────────────────
function autoResize(ta) {
  ta.style.height = 'auto';
  ta.style.height = ta.scrollHeight + 'px';
}
// ── sauvegarde/restauration du code via localStorage ─────────
function saveCode(exId, value) {
  try { localStorage.setItem('hanoi_code_' + exId, value); } catch(e) {}
}
function loadCode(exId, fallback) {
  try {
    const saved = localStorage.getItem('hanoi_code_' + exId);
    return (saved !== null && saved !== '') ? saved : fallback;
  } catch(e) { return fallback; }
}

// applique l'auto-resize + restaure le code sauvegardé au chargement
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('textarea').forEach(ta => {
    const exId = ta.id.replace(/^c/, '');
    ta.value = loadCode(exId, ta.value);  // restaure si sauvegardé
    autoResize(ta);
    ta.addEventListener('input', () => {
      autoResize(ta);
      saveCode(exId, ta.value);           // sauvegarde à chaque frappe
    });
  });

  // Charge l'état depuis le serveur : ex4 déverrouillé seulement si le serveur le dit
  fetch('/api/state')
    .then(r => r.json())
    .then(state => {
      if (state.ex3_unlocked) {
        ex3_run = true;
        triggerUnlockByKey('ex3_run');
      }
      if (state.ex4_unlocked) {
        ex4_run = true;
        triggerUnlockByKey('ex4_run');
      }
    });
});

// ── Tab = 4 espaces ──────────────────────────────────────────
function handleTab(e) {
  if (e.key !== 'Tab') return;
  e.preventDefault();
  const t = e.target, s = t.selectionStart;
  t.value = t.value.slice(0, s) + '    ' + t.value.slice(t.selectionEnd);
  t.selectionStart = t.selectionEnd = s + 4;
  autoResize(t);
}

// ── collecte le code de tous les exos ───────────────────────
function codes() {
  const o = {};
  EXS.forEach(ex => o[ex.id] = document.getElementById('c'+ex.id).value);
  return o;
}

// ── déverrouillage d'un exercice ────────────────────────────
function unlock(exId) {
  const card = document.getElementById('card-' + exId);
  if (!card) return;
  card.classList.remove('locked');
  // active aussi le bouton Lancer si présent
  const lb = document.getElementById('lbtn-' + exId);
  if (lb) lb.disabled = false;
  // scroll doux vers la card débloquée
  setTimeout(() => card.scrollIntoView({ behavior: 'smooth', block: 'start' }), 100);
}

// ── teste un exercice ────────────────────────────────────────
async function runTest(id) {
  const r = document.getElementById('r' + id);
  r.className = 'result run';
  r.textContent = '⏳ en cours…';

  let d;
  try {
    const res = await fetch('/api/test', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ex_id: id, codes: codes() })
    });
    d = await res.json();
  } catch {
    r.className = 'result err';
    r.textContent = '❌ Serveur inaccessible.';
    return;
  }

  r.className = 'result ' + (d.ok ? 'ok' : 'err');
  r.textContent = d.message;

  if (d.ok && !passed[id]) {
    passed[id] = true;
    // marque la badge en vert
    const badge = document.getElementById('badge-' + id);
    if (badge) { badge.innerHTML = '<svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M2 7l3.5 3.5L12 3" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'; badge.style.background = 'var(--green)'; }
    // débloque l'exercice suivant
    triggerUnlock(id);
  }
}

// Détermine quel exo débloquer après un succès
function triggerUnlock(doneId) {
  EXS.forEach(ex => {
    if (ex.unlock_after === doneId) unlock(ex.id);
  });
}

// ── lancer pygame depuis une card ────────────────────────────
async function launchEx(id) {
  const btn = document.getElementById('lbtn-' + id);
  const msg = document.getElementById('lr' + id);
  btn.disabled = true;
  msg.className = 'launch-result';
  msg.textContent = '⏳ Lancement…';

  let d;
  try {
    const res = await fetch('/api/launch', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ codes: codes(), ex_id: id })
    });
    d = await res.json();
  } catch {
    msg.className = 'launch-result err';
    msg.textContent = '❌ Serveur inaccessible.';
    btn.disabled = false;
    return;
  }

  if (d.ok && d.game_success) {
    // Jeu terminé normalement (exit 0) → valide
    msg.className = 'launch-result ok';
    msg.textContent = '✅ Bravo, le jeu a fonctionné !';
    btn.disabled = false;
    // Débloque l'exercice suivant selon lequel vient d'être validé
    if (id === 'ex3' && !ex3_run) {
      ex3_run = true;
      triggerUnlockByKey('ex3_run');
      setStatus('ok', '✅ Exercice 3 validé ! Tu peux passer au 4.');
    } else if (id === 'ex4' && !ex4_run) {
      ex4_run = true;
      triggerUnlockByKey('ex4_run');
      setStatus('ok', '✅ Exercice 4 validé ! Tu peux passer au 5.');
    } else if (id === 'ex5') {
      revealFunTab();
      setStatus('ok', '🎉 Exercice 5 réussi ! L\\'onglet « Défis Fun » est débloqué !');
    } else {
      setStatus('ok', '✅ Jeu lancé avec succès !');
    }
  } else if (d.ok && !d.game_success) {
    // Le serveur a répondu mais le jeu a planté (exit 1)
    msg.className = 'launch-result err';
    msg.textContent = '❌ Le jeu a planté — corrige ton code et relance !';
    btn.disabled = false;
    setStatus('err', '❌ Corrige ton code puis relance.');
  } else {
    msg.className = 'launch-result err';
    msg.textContent = '❌ ' + d.message;
    btn.disabled = false;
    setStatus('err', '❌ Erreur — corrige ton code puis relance.');
  }
}

function triggerUnlockByKey(key) {
  EXS.forEach(ex => {
    if (ex.unlock_after === key) unlock(ex.id);
  });
}

// ── statut en haut ────────────────────────────────────────────
function setStatus(type, txt) {
  const el = document.getElementById('statusMsg');
  el.className = type;
  el.textContent = txt;
}


// ── docs nav observer ──────────────────────────────────────────

// Active le lien de navigation correspondant à la section visible
const links = document.querySelectorAll('.nav-link');
const sections = document.querySelectorAll('.doc-section');

const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      links.forEach(l => l.classList.remove('active'));
      const active = document.querySelector('.nav-link[href="#' + entry.target.id + '"]');
      if (active) active.classList.add('active');
    }
  });
}, { threshold: 0.3 });

sections.forEach(s => observer.observe(s));

// ───────── Mini-Hanoï jouable (volet de droite) — version animée ─────────
let hanoiState = null, hanoiSel = null, hanoiMoves = 0;
let hanoiBusy = false, hanoiSolving = false, hanoiStop = false, hanoiAuto = false;
let hanoiHistory = [], hanoiT0 = 0, hanoiTimer = null;
let hanoiPending = null, hanoiSuppressClick = false;
const HANOI_COLORS = ['#e04646','#e68c32','#d2c332','#50b450','#3c82d2','#8c50c8','#c850a0'];

function hanoiN() { return parseInt(document.getElementById('hanoiCount').value, 10); }
function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

function toggleHanoi() {
  const d = document.getElementById('hanoiDrawer');
  d.classList.toggle('open');
  if (d.classList.contains('open') && !hanoiState) hanoiReset();
}

function hanoiReset() {
  hanoiStop = true; hanoiSolving = false; hanoiAuto = false; hanoiBusy = false;
  setSolveLabel(false);
  const n = hanoiN();
  hanoiState = [[], [], []];
  for (let s = n; s >= 1; s--) hanoiState[0].push(s);   // bas = grand … sommet = petit
  hanoiSel = null; hanoiMoves = 0; hanoiHistory = [];
  stopTimer(); hanoiT0 = 0; updateTime();
  const msg = document.getElementById('hanoiMsg');
  msg.className = 'hanoi-msg'; msg.textContent = '';
  loadBest();
  hanoiRender();
}

function hanoiRender() {
  const n = hanoiN();
  const board = document.getElementById('hanoiBoard');
  board.innerHTML = '';
  const moving = hanoiSel !== null ? hanoiState[hanoiSel][hanoiState[hanoiSel].length - 1] : null;
  ['A', 'B', 'C'].forEach((name, i) => {
    const pole = document.createElement('div');
    let cls = 'hanoi-pole';
    if (hanoiSel === i) cls += ' selected';
    else if (hanoiSel !== null) {
      const top = hanoiState[i][hanoiState[i].length - 1];
      if (hanoiState[i].length === 0 || top > moving) cls += ' valid';
    }
    pole.className = cls;
    pole.onclick = () => hanoiClick(i);
    const diskH = Math.max(13, Math.min(22, Math.floor(250 / n)));   // s'adapte jusqu'à 10 anneaux
    hanoiState[i].forEach((size, idx) => {
      const disk = document.createElement('div');
      const isTop = idx === hanoiState[i].length - 1;
      disk.className = 'hanoi-disk' + (hanoiSel === i && isTop ? ' lifted' : '');
      disk.dataset.size = size;
      disk.style.width = (30 + (size - 1) / (n - 1 || 1) * 60) + '%';
      disk.style.height = diskH + 'px';
      disk.style.backgroundColor = HANOI_COLORS[(size - 1) % HANOI_COLORS.length];
      if (isTop) {   // seul l'anneau du sommet est saisissable à la souris
        disk.style.cursor = 'grab';
        disk.addEventListener('pointerdown', ev => hanoiDiskDown(ev, i, size));
      }
      pole.appendChild(disk);
    });
    const lab = document.createElement('div');
    lab.className = 'hanoi-label'; lab.textContent = name;
    pole.appendChild(lab);
    board.appendChild(pole);
  });
  document.getElementById('hanoiMoves').textContent = 'Coups : ' + hanoiMoves + ' / ' + (Math.pow(2, n) - 1);
}

function diskEl(size) {
  return document.querySelector('#hanoiBoard .hanoi-disk[data-size="' + size + '"]');
}

// Déplace l'anneau du sommet de `from` vers `to`, avec une animation en arc (prendre → glisser → poser).
function doMove(from, to, countIt) {
  const size = hanoiState[from][hanoiState[from].length - 1];
  const O = diskEl(size).getBoundingClientRect();
  hanoiState[to].push(hanoiState[from].pop());
  if (countIt) { hanoiMoves++; hanoiHistory.push([from, to]); startTimer(); }
  hanoiSel = null;
  hanoiRender();
  const newEl = diskEl(size);
  const N = newEl.getBoundingClientRect();
  const top = document.getElementById('hanoiBoard').getBoundingClientRect().top - 6;
  const dx = O.left - N.left, dy = O.top - N.top;
  hanoiBusy = true;
  return new Promise(resolve => {
    let anim = null;
    try {
      anim = newEl.animate([
        { transform: 'translate(' + dx + 'px,' + dy + 'px)' },
        { transform: 'translate(' + dx + 'px,' + (top - N.top) + 'px)', offset: 0.25 },
        { transform: 'translate(0px,' + (top - N.top) + 'px)', offset: 0.62 },
        { transform: 'translate(0px,0px)' }
      ], { duration: 340, easing: 'cubic-bezier(.45,.05,.3,1)' });
    } catch (e) { anim = null; }
    const done = () => { hanoiBusy = false; resolve(); };
    if (anim && anim.finished) anim.finished.then(done).catch(done);
    else if (anim) anim.onfinish = done;
    else done();
  });
}

async function hanoiClick(i) {
  if (hanoiSuppressClick) { hanoiSuppressClick = false; return; }  // clic émis juste après un glisser
  if (hanoiBusy || hanoiSolving) return;
  const msg = document.getElementById('hanoiMsg');
  msg.className = 'hanoi-msg';
  if (hanoiSel === null) {
    if (hanoiState[i].length === 0) {
      msg.className = 'hanoi-msg bad'; msg.textContent = 'Ce poteau est vide.';
      return;
    }
    hanoiSel = i; hanoiRender(); return;
  }
  if (i === hanoiSel) { hanoiSel = null; hanoiRender(); return; }  // re-clic = repose
  const src = hanoiState[hanoiSel], dst = hanoiState[i];
  const moving = src[src.length - 1];
  if (dst.length && dst[dst.length - 1] < moving) {
    msg.className = 'hanoi-msg bad';
    msg.textContent = 'Interdit : un grand anneau ne va pas sur un plus petit.';
    hanoiSel = null; hanoiRender(); return;
  }
  await doMove(hanoiSel, i, true);
  checkWin(false);
}

// ── Glisser-déposer : maintenir un anneau et le lâcher sur un poteau ──
function hanoiDiskDown(ev, from, size) {
  if (hanoiBusy || hanoiSolving) return;
  if (hanoiState[from][hanoiState[from].length - 1] !== size) return;   // seulement le sommet
  hanoiPending = { from: from, size: size, x0: ev.clientX, y0: ev.clientY, started: false, clone: null, offX: 0, offY: 0 };
  window.addEventListener('pointermove', hanoiDragMove);
  window.addEventListener('pointerup', hanoiDragEnd);
}

function hanoiDragMove(ev) {
  const p = hanoiPending;
  if (!p) return;
  if (!p.started) {
    if (Math.abs(ev.clientX - p.x0) + Math.abs(ev.clientY - p.y0) < 6) return;  // seuil clic vs glisser
    p.started = true;
    hanoiSel = p.from; hanoiRender();          // surligne les poteaux valides
    const real = diskEl(p.size);
    const r = real.getBoundingClientRect();
    real.style.visibility = 'hidden';          // on cache l'original, le clone suit la souris
    const clone = document.createElement('div');
    clone.className = 'hanoi-disk';
    clone.style.position = 'fixed'; clone.style.margin = '0';
    clone.style.width = r.width + 'px'; clone.style.height = r.height + 'px';
    clone.style.backgroundColor = HANOI_COLORS[(p.size - 1) % HANOI_COLORS.length];
    clone.style.zIndex = '3000'; clone.style.pointerEvents = 'none';
    clone.style.outline = '2px solid #fff'; clone.style.cursor = 'grabbing';
    document.body.appendChild(clone);
    p.clone = clone; p.offX = ev.clientX - r.left; p.offY = ev.clientY - r.top;
  }
  p.clone.style.left = (ev.clientX - p.offX) + 'px';
  p.clone.style.top = (ev.clientY - p.offY) + 'px';
}

function hanoiDragEnd(ev) {
  window.removeEventListener('pointermove', hanoiDragMove);
  window.removeEventListener('pointerup', hanoiDragEnd);
  const p = hanoiPending; hanoiPending = null;
  if (!p) return;
  if (!p.started) return;                       // simple clic → géré par hanoiClick
  if (p.clone && p.clone.parentNode) p.clone.parentNode.removeChild(p.clone);
  hanoiSuppressClick = true;                    // neutralise le clic qui suit le relâché
  const target = hanoiPoleAt(ev.clientX, ev.clientY);
  const from = p.from, size = p.size;
  hanoiSel = null;
  const msg = document.getElementById('hanoiMsg'); msg.className = 'hanoi-msg';
  if (target === null || target === from) { hanoiRender(); return; }   // lâché dans le vide → annule
  const dst = hanoiState[target];
  if (dst.length && dst[dst.length - 1] < size) {
    msg.className = 'hanoi-msg bad';
    msg.textContent = 'Interdit : un grand anneau ne va pas sur un plus petit.';
    hanoiRender(); return;
  }
  hanoiState[target].push(hanoiState[from].pop());
  hanoiMoves++; hanoiHistory.push([from, target]); startTimer();
  hanoiRender();
  checkWin(false);
}

function hanoiPoleAt(x, y) {
  const poles = document.querySelectorAll('#hanoiBoard .hanoi-pole');
  for (let i = 0; i < poles.length; i++) {
    const r = poles[i].getBoundingClientRect();
    if (x >= r.left && x <= r.right && y >= r.top - 50 && y <= r.bottom + 50) return i;
  }
  return null;
}

function checkWin(auto) {
  const n = hanoiN();
  if (hanoiState[1].length === n || hanoiState[2].length === n) {
    stopTimer();
    const opt = Math.pow(2, n) - 1;
    const msg = document.getElementById('hanoiMsg');
    msg.className = 'hanoi-msg win';
    if (auto) {
      msg.textContent = 'Résolu automatiquement en ' + opt + ' coups ✨';
    } else {
      msg.textContent = '🎉 Gagné en ' + hanoiMoves + ' coups !' +
        (hanoiMoves === opt ? ' Parfait !' : ' (optimal : ' + opt + ')');
      saveBest(hanoiMoves);
    }
    hanoiConfetti();
    return true;
  }
  return false;
}

// ── Annuler le dernier coup ──
async function hanoiUndo() {
  if (hanoiBusy || hanoiSolving || !hanoiHistory.length) return;
  const mv = hanoiHistory.pop();
  hanoiSel = null;
  await doMove(mv[1], mv[0], false);
  hanoiMoves = Math.max(0, hanoiMoves - 1);
  hanoiRender();
  const msg = document.getElementById('hanoiMsg');
  msg.className = 'hanoi-msg'; msg.textContent = '';
}

// ── Résolution automatique animée (algorithme récursif optimal) ──
function setSolveLabel(on) {
  const b = document.getElementById('hanoiSolveBtn');
  if (b) b.textContent = on ? '■ Stop' : '✨ Résoudre';
}
async function hanoiSolveToggle() {
  if (hanoiSolving) { hanoiStop = true; return; }
  hanoiReset();
  hanoiSolving = true; hanoiAuto = true; hanoiStop = false; setSolveLabel(true);
  const n = hanoiN();
  const moves = [];
  (function rec(k, from, to, via) {
    if (k === 0) return;
    rec(k - 1, from, via, to);
    moves.push([from, to]);
    rec(k - 1, via, to, from);
  })(n, 0, 2, 1);
  for (const mv of moves) {
    if (hanoiStop) break;
    await doMove(mv[0], mv[1], false);
    await sleep(110);
  }
  const stopped = hanoiStop;
  hanoiSolving = false; hanoiStop = false; setSolveLabel(false);
  if (!stopped) checkWin(true);
}

// ── Chronomètre ──
function startTimer() { if (!hanoiTimer && !hanoiAuto) { hanoiT0 = Date.now(); hanoiTimer = setInterval(updateTime, 200); } }
function stopTimer() { if (hanoiTimer) { clearInterval(hanoiTimer); hanoiTimer = null; } }
function updateTime() {
  const s = hanoiT0 ? (Date.now() - hanoiT0) / 1000 : 0;
  const el = document.getElementById('hanoiTime');
  if (el) el.textContent = '⏱ ' + s.toFixed(1) + 's';
}

// ── Record (localStorage, par nombre d'anneaux) ──
function bestKey() { return 'hanoi_best_' + hanoiN(); }
function loadBest() {
  let b = null;
  try { b = localStorage.getItem(bestKey()); } catch (e) {}
  const el = document.getElementById('hanoiBest');
  if (el) el.textContent = b ? ('🏆 ' + b) : '🏆 —';
}
function saveBest(m) {
  try {
    const k = bestKey(), prev = parseInt(localStorage.getItem(k) || '0', 10);
    if (!prev || m < prev) localStorage.setItem(k, m);
  } catch (e) {}
  loadBest();
}

// ── Confettis de victoire (réutilisable : volet ou panneau) ──
function hanoiConfetti() {
  popConfetti(document.getElementById('hanoiConfetti'), document.getElementById('hanoiDrawer'));
}
function popConfetti(cv, host) {
  if (!cv || !host) return;
  cv.width = host.clientWidth; cv.height = host.clientHeight;
  const ctx = cv.getContext('2d');
  const parts = [];
  for (let i = 0; i < 150; i++) {
    parts.push({
      x: Math.random() * cv.width, y: -20 - Math.random() * cv.height * 0.4,
      r: 4 + Math.random() * 5, c: HANOI_COLORS[i % HANOI_COLORS.length],
      vy: 2 + Math.random() * 3.5, vx: -1.5 + Math.random() * 3, a: 1,
      rot: Math.random() * 6.28, vr: -0.2 + Math.random() * 0.4
    });
  }
  const t0 = Date.now();
  (function frame() {
    const el = Date.now() - t0;
    ctx.clearRect(0, 0, cv.width, cv.height);
    parts.forEach(p => {
      p.x += p.vx; p.y += p.vy; p.vy += 0.04; p.rot += p.vr;
      if (el > 1600) p.a = Math.max(0, p.a - 0.03);
      ctx.save(); ctx.globalAlpha = p.a; ctx.translate(p.x, p.y); ctx.rotate(p.rot);
      ctx.fillStyle = p.c; ctx.fillRect(-p.r, -p.r * 0.6, p.r * 2, p.r * 1.2); ctx.restore();
    });
    if (el < 2600) requestAnimationFrame(frame);
    else ctx.clearRect(0, 0, cv.width, cv.height);
  })();
}

// ── Raccourcis clavier quand le volet est ouvert ──
document.addEventListener('keydown', e => {
  const d = document.getElementById('hanoiDrawer');
  if (!d || !d.classList.contains('open')) return;
  const tag = e.target && e.target.tagName;
  if (tag === 'TEXTAREA' || tag === 'INPUT' || tag === 'SELECT') return;
  const k = e.key.toLowerCase();
  if (k === 'a' || k === '1') hanoiClick(0);
  else if (k === 'b' || k === '2') hanoiClick(1);
  else if (k === 'c' || k === '3') hanoiClick(2);
  else if (k === 'r') hanoiReset();
  else if (k === 'u') hanoiUndo();
});

</script>
</body>
</html>
"""

