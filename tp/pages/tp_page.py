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

// ═══════════ Onglet « Défis Fun » (débloqué après l'exercice 5) ═══════════
// Icônes SVG des défis (pas d'emoji)
const FUN_ICONS = {
  speed: '<svg viewBox="0 0 24 24" fill="none" stroke="#e68c32" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="13" r="8"/><path d="M12 13l3-2"/><path d="M9 2h6"/><path d="M12 2v3"/><path d="M18.6 6.4l1.6-1.6"/></svg>',
  counted: '<svg viewBox="0 0 24 24" fill="none" stroke="#e04646" stroke-width="2"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.5" fill="#e04646"/></svg>',
  chaos: '<svg viewBox="0 0 24 24" fill="none" stroke="#50b450" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 3 21 3 21 8"/><line x1="4" y1="20" x2="21" y2="3"/><polyline points="21 16 21 21 16 21"/><line x1="15" y1="15" x2="21" y2="21"/><line x1="4" y1="4" x2="9" y2="9"/></svg>',
  fourpoles: '<svg viewBox="0 0 24 24" fill="none" stroke="#58a6ff" stroke-width="2" stroke-linecap="round"><path d="M2 21h20"/><path d="M5 21V7M10 21V4M15 21V9M20 21V6"/></svg>',
  marathon: '<svg viewBox="0 0 24 24" fill="none"><path d="M3 22h18" stroke="#8c50c8" stroke-width="2" stroke-linecap="round"/><rect x="5" y="18" width="14" height="2.6" rx="1" fill="#8c50c8"/><rect x="6.6" y="14.4" width="10.8" height="2.6" rx="1" fill="#8c50c8" opacity=".82"/><rect x="8" y="10.8" width="8" height="2.6" rx="1" fill="#8c50c8" opacity=".66"/><rect x="9.2" y="7.2" width="5.6" height="2.6" rx="1" fill="#8c50c8" opacity=".5"/><rect x="10.2" y="3.6" width="3.6" height="2.6" rx="1" fill="#8c50c8" opacity=".36"/></svg>'
};
const FUN_CHALLENGES = [
  { id:'speed',     icon:FUN_ICONS.speed, title:'Contre-la-montre', disks:5,  poles:3, goal:2, medalBy:'time',  gold:20, silver:45,
    desc:'5 anneaux, 3 poteaux. Reconstruis la tour sur C le plus vite possible !' },
  { id:'counted',   icon:FUN_ICONS.counted, title:'Coups comptés',    disks:6,  poles:3, goal:2, medalBy:'moves', par:63,
    desc:'6 anneaux. La médaille d’or exige la perfection : 63 coups, pas un de plus.' },
  { id:'chaos',     icon:FUN_ICONS.chaos, title:'Départ chaotique',  disks:5,  poles:3, goal:2, scramble:true, medalBy:'moves', par:31,
    desc:'5 anneaux éparpillés au hasard. Rassemble toute la tour sur C !' },
  { id:'fourpoles', icon:FUN_ICONS.fourpoles, title:'Quatre poteaux',    disks:6,  poles:4, goal:3, medalBy:'moves', par:17,
    desc:'Un poteau bonus (D) ! Avec 4 poteaux on fait bien moins de coups. Objectif : tout sur D.' },
  { id:'marathon',  icon:FUN_ICONS.marathon, title:'Le marathon',       disks:10, poles:3, goal:2, medalBy:'moves', par:1023,
    desc:'10 anneaux, 3 poteaux, 1023 coups au minimum. Bon courage, champion !' }
];
const MEDAL_EMOJI = { gold:'🥇', silver:'🥈', bronze:'🥉' };
const FUN_WIN = ['Incroyable !', 'Tu es une légende du Hanoï !', 'Magistral !',
  'Les moines du temple t’applaudissent 👏', 'Maître des tours, respect !', 'GG, c’était stylé !'];

let funCfg = null, funPoles = null, funSel = null, funMoves = 0, funHistory = [];
let funT0 = 0, funTimer = null, funBusy = false;
let funPending = null, funSuppressClick = false;

function revealFunTab() {
  const t = document.getElementById('tab-fun');
  if (t) t.classList.remove('hidden');
  try { localStorage.setItem('hanoi_fun_unlocked', '1'); } catch (e) {}
}

function funGetMedal(id) { try { return localStorage.getItem('hanoi_fun_' + id); } catch (e) { return null; } }
function funSaveMedal(id, m) {
  const rank = { bronze:1, silver:2, gold:3 };
  try {
    const cur = localStorage.getItem('hanoi_fun_' + id);
    if (!cur || rank[m] > rank[cur]) localStorage.setItem('hanoi_fun_' + id, m);
  } catch (e) {}
}
function funMedal(cfg, moves, secs) {
  if (cfg.medalBy === 'time') return secs <= cfg.gold ? 'gold' : (secs <= cfg.silver ? 'silver' : 'bronze');
  return moves <= cfg.par ? 'gold' : (moves <= Math.ceil(cfg.par * 1.3) ? 'silver' : 'bronze');
}

function funRenderCards() {
  const wrap = document.getElementById('funCards');
  if (!wrap) return;
  wrap.innerHTML = '';
  FUN_CHALLENGES.forEach(cfg => {
    const card = document.createElement('div');
    card.className = 'fun-card';
    card.onclick = () => funStart(cfg.id);
    const m = funGetMedal(cfg.id);
    card.innerHTML =
      '<div class="mg-icon">' + cfg.icon + '</div>' +
      '<h3>' + cfg.title + '</h3>' +
      '<p>' + cfg.desc + '</p>' +
      '<div class="medal">' + (m ? ('Meilleure médaille : ' + MEDAL_EMOJI[m]) : 'Pas encore tenté') + '</div>';
    wrap.appendChild(card);
  });
}

function funStart(id) {
  funCfg = FUN_CHALLENGES.find(c => c.id === id);
  if (!funCfg) return;
  do {
    funPoles = Array.from({ length: funCfg.poles }, () => []);
    if (funCfg.scramble) {
      for (let s = funCfg.disks; s >= 1; s--) funPoles[Math.floor(Math.random() * funCfg.poles)].push(s);
    } else {
      for (let s = funCfg.disks; s >= 1; s--) funPoles[0].push(s);
    }
  } while (funPoles[funCfg.goal].length === funCfg.disks);   // pas déjà gagné
  funSel = null; funMoves = 0; funHistory = []; funBusy = false;
  funStopTimer(); funT0 = 0; funUpdateTime();
  document.getElementById('funTitle').innerHTML = '<span class="mg-title-icon">' + funCfg.icon + '</span>' + funCfg.title;
  document.getElementById('funGoal').textContent = 'Objectif : tout sur ' + ['A','B','C','D'][funCfg.goal];
  document.getElementById('funMsg').className = 'hanoi-msg';
  document.getElementById('funMsg').textContent = '';
  document.getElementById('funPlay').style.display = 'block';
  funRender();
  document.getElementById('funPlay').scrollIntoView({ behavior:'smooth', block:'start' });
}

function funRender() {
  const cfg = funCfg, board = document.getElementById('funBoard');
  board.innerHTML = '';
  const names = ['A','B','C','D'];
  const moving = funSel !== null ? funPoles[funSel][funPoles[funSel].length - 1] : null;
  const diskH = Math.max(12, Math.min(22, Math.floor(250 / cfg.disks)));
  for (let i = 0; i < cfg.poles; i++) {
    const pole = document.createElement('div');
    let cls = 'hanoi-pole';
    if (funSel === i) cls += ' selected';
    else if (funSel !== null) {
      const t = funPoles[i][funPoles[i].length - 1];
      if (funPoles[i].length === 0 || t > moving) cls += ' valid';
    }
    pole.className = cls;
    pole.onclick = () => funClick(i);
    funPoles[i].forEach((size, idx) => {
      const d = document.createElement('div');
      const isTop = idx === funPoles[i].length - 1;
      d.className = 'hanoi-disk' + (funSel === i && isTop ? ' lifted' : '');
      d.dataset.size = size;
      d.style.width = (30 + (size - 1) / (cfg.disks - 1 || 1) * 60) + '%';
      d.style.height = diskH + 'px';
      d.style.backgroundColor = HANOI_COLORS[(size - 1) % HANOI_COLORS.length];
      if (isTop) {                               // anneau du sommet : saisissable
        d.style.cursor = 'grab';
        d.addEventListener('pointerdown', ev => funDiskDown(ev, i, size));
      }
      pole.appendChild(d);
    });
    const lab = document.createElement('div');
    lab.className = 'hanoi-label';
    lab.textContent = names[i] + (i === cfg.goal ? ' 🎯' : '');
    pole.appendChild(lab);
    board.appendChild(pole);
  }
  document.getElementById('funMoves').textContent = 'Coups : ' + funMoves;
}

function funDiskEl(size) { return document.querySelector('#funBoard .hanoi-disk[data-size="' + size + '"]'); }

// Déplacement animé en arc (identique au volet latéral)
function funDoMove(from, to, countIt) {
  const size = funPoles[from][funPoles[from].length - 1];
  const O = funDiskEl(size).getBoundingClientRect();
  funPoles[to].push(funPoles[from].pop());
  if (countIt) { funMoves++; funHistory.push([from, to]); funStartTimer(); }
  funSel = null; funRender();
  const newEl = funDiskEl(size);
  const N = newEl.getBoundingClientRect();
  const top = document.getElementById('funBoard').getBoundingClientRect().top - 6;
  const dx = O.left - N.left, dy = O.top - N.top;
  funBusy = true;
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
    const done = () => { funBusy = false; resolve(); };
    if (anim && anim.finished) anim.finished.then(done).catch(done);
    else if (anim) anim.onfinish = done;
    else done();
  });
}

async function funClick(i) {
  if (funSuppressClick) { funSuppressClick = false; return; }
  if (funBusy) return;
  const msg = document.getElementById('funMsg'); msg.className = 'hanoi-msg';
  if (funSel === null) {
    if (funPoles[i].length === 0) { msg.className = 'hanoi-msg bad'; msg.textContent = 'Ce poteau est vide.'; return; }
    funSel = i; funRender(); return;
  }
  if (i === funSel) { funSel = null; funRender(); return; }
  const src = funPoles[funSel], dst = funPoles[i], mv = src[src.length - 1];
  if (dst.length && dst[dst.length - 1] < mv) {
    msg.className = 'hanoi-msg bad';
    msg.textContent = 'Interdit : un grand anneau ne va pas sur un plus petit.';
    funSel = null; funRender(); return;
  }
  await funDoMove(funSel, i, true);
  funCheckWin();
}

async function funUndo() {
  if (funBusy || !funHistory.length) return;
  const mv = funHistory.pop();
  funSel = null;
  await funDoMove(mv[1], mv[0], false);
  funMoves = Math.max(0, funMoves - 1);
  funRender();
  document.getElementById('funMsg').className = 'hanoi-msg';
  document.getElementById('funMsg').textContent = '';
}

// ── Glisser-déposer sur le plateau des défis ──
function funDiskDown(ev, from, size) {
  if (funBusy) return;
  if (funPoles[from][funPoles[from].length - 1] !== size) return;
  funPending = { from: from, size: size, x0: ev.clientX, y0: ev.clientY, started: false, clone: null, offX: 0, offY: 0 };
  window.addEventListener('pointermove', funDragMove);
  window.addEventListener('pointerup', funDragEnd);
}
function funDragMove(ev) {
  const p = funPending; if (!p) return;
  if (!p.started) {
    if (Math.abs(ev.clientX - p.x0) + Math.abs(ev.clientY - p.y0) < 6) return;
    p.started = true; funSel = p.from; funRender();
    const real = funDiskEl(p.size); const r = real.getBoundingClientRect();
    real.style.visibility = 'hidden';
    const clone = document.createElement('div');
    clone.className = 'hanoi-disk';
    clone.style.position = 'fixed'; clone.style.margin = '0';
    clone.style.width = r.width + 'px'; clone.style.height = r.height + 'px';
    clone.style.backgroundColor = HANOI_COLORS[(p.size - 1) % HANOI_COLORS.length];
    clone.style.zIndex = '3000'; clone.style.pointerEvents = 'none'; clone.style.outline = '2px solid #fff';
    document.body.appendChild(clone);
    p.clone = clone; p.offX = ev.clientX - r.left; p.offY = ev.clientY - r.top;
  }
  p.clone.style.left = (ev.clientX - p.offX) + 'px';
  p.clone.style.top = (ev.clientY - p.offY) + 'px';
}
function funDragEnd(ev) {
  window.removeEventListener('pointermove', funDragMove);
  window.removeEventListener('pointerup', funDragEnd);
  const p = funPending; funPending = null;
  if (!p || !p.started) return;
  if (p.clone && p.clone.parentNode) p.clone.parentNode.removeChild(p.clone);
  funSuppressClick = true;
  const target = funPoleAt(ev.clientX, ev.clientY);
  const from = p.from, size = p.size; funSel = null;
  const msg = document.getElementById('funMsg'); msg.className = 'hanoi-msg';
  if (target === null || target === from) { funRender(); return; }
  const dst = funPoles[target];
  if (dst.length && dst[dst.length - 1] < size) {
    msg.className = 'hanoi-msg bad';
    msg.textContent = 'Interdit : un grand anneau ne va pas sur un plus petit.';
    funRender(); return;
  }
  funPoles[target].push(funPoles[from].pop());
  funMoves++; funHistory.push([from, target]); funStartTimer();
  funRender(); funCheckWin();
}
function funPoleAt(x, y) {
  const poles = document.querySelectorAll('#funBoard .hanoi-pole');
  for (let i = 0; i < poles.length; i++) {
    const r = poles[i].getBoundingClientRect();
    if (x >= r.left && x <= r.right && y >= r.top - 50 && y <= r.bottom + 50) return i;
  }
  return null;
}
function funRestart() { if (funCfg) funStart(funCfg.id); }
function funClose() { funStopTimer(); document.getElementById('funPlay').style.display = 'none'; document.getElementById('funCards').scrollIntoView({ behavior:'smooth' }); }

function funCheckWin() {
  const cfg = funCfg;
  if (funPoles[cfg.goal].length === cfg.disks) {
    funStopTimer();
    const secs = funT0 ? (Date.now() - funT0) / 1000 : 0;
    const medal = funMedal(cfg, funMoves, secs);
    funSaveMedal(cfg.id, medal);
    const msg = document.getElementById('funMsg'); msg.className = 'hanoi-msg win';
    msg.textContent = MEDAL_EMOJI[medal] + ' ' + FUN_WIN[Math.floor(Math.random() * FUN_WIN.length)] +
      '  (' + funMoves + ' coups, ' + secs.toFixed(1) + 's)';
    popConfetti(document.getElementById('funConfetti'), document.querySelector('#panel-fun .fun-wrap'));
    funRenderCards();
  }
}

function funStartTimer() { if (!funTimer) { funT0 = Date.now(); funTimer = setInterval(funUpdateTime, 200); } }
function funStopTimer() { if (funTimer) { clearInterval(funTimer); funTimer = null; } }
function funUpdateTime() {
  const s = funT0 ? (Date.now() - funT0) / 1000 : 0;
  const el = document.getElementById('funTime'); if (el) el.textContent = '⏱ ' + s.toFixed(1) + 's';
}

// ═══════════ Mini-jeux bonus (sans rapport avec Hanoï) + code Python ═══════════
// Icônes SVG inline (pas d'emoji, pas de dépendance réseau)
const MG_ICONS = {
  guess: '<svg viewBox="0 0 24 24" fill="none"><circle cx="10" cy="10" r="6.5" stroke="#58a6ff" stroke-width="2"/><line x1="15" y1="15" x2="20.5" y2="20.5" stroke="#58a6ff" stroke-width="2" stroke-linecap="round"/><text x="10" y="13.5" font-size="9" fill="#58a6ff" text-anchor="middle" font-weight="700" font-family="sans-serif">?</text></svg>',
  rps: '<svg viewBox="0 0 24 24" fill="none" stroke="#e68c32" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><line x1="20" y1="4" x2="8.12" y2="15.88"/><line x1="14.47" y1="14.48" x2="20" y2="20"/><line x1="8.12" y1="8.12" x2="12" y2="12"/></svg>',
  ttt: '<svg viewBox="0 0 24 24" fill="none" stroke-width="2"><path d="M9 3v18M15 3v18M3 9h18M3 15h18" stroke="#475363" stroke-width="1.6"/><path d="M4.6 4.6l2.8 2.8M7.4 4.6l-2.8 2.8" stroke="#e04646" stroke-linecap="round"/><circle cx="18.4" cy="6" r="2" stroke="#58a6ff"/><circle cx="6" cy="18.4" r="2" stroke="#58a6ff"/><path d="M16.6 16.6l3 3M19.6 16.6l-3 3" stroke="#e04646" stroke-linecap="round"/></svg>',
  hangman: '<svg viewBox="0 0 24 24" fill="none" stroke="#d2c332" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 21h8M5 21V3h11M16 3v3"/><circle cx="16" cy="8" r="2"/><path d="M16 10v5M16 12l-2.5 2M16 12l2.5 2M16 15l-2.5 3M16 15l2.5 3"/></svg>',
  fizzbuzz: '<svg viewBox="0 0 24 24" fill="#f2cc4b" stroke="#f2cc4b" stroke-width="1.5" stroke-linejoin="round"><polygon points="13 2 4 14 11 14 10 22 20 9 13 9 13 2"/></svg>',
  times: '<svg viewBox="0 0 24 24" fill="none" stroke="#50b450" stroke-width="2" stroke-linecap="round"><rect x="3" y="3" width="18" height="18" rx="4"/><path d="M9 9l6 6M15 9l-6 6"/></svg>',
  simon: '<svg viewBox="0 0 24 24"><path d="M12 12 L12 2 A10 10 0 0 1 22 12 Z" fill="#e04646"/><path d="M12 12 L22 12 A10 10 0 0 1 12 22 Z" fill="#50b450"/><path d="M12 12 L12 22 A10 10 0 0 1 2 12 Z" fill="#3c82d2"/><path d="M12 12 L2 12 A10 10 0 0 1 12 2 Z" fill="#d2c332"/><circle cx="12" cy="12" r="3.4" fill="#0d1117"/></svg>',
  reflex: '<svg viewBox="0 0 24 24" fill="none" stroke="#58a6ff" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="13" r="8"/><path d="M12 13l3-3"/><path d="M9 2h6"/><path d="M12 2v3"/></svg>',
  memory: '<svg viewBox="0 0 24 24" fill="none" stroke="#8c50c8" stroke-width="2"><rect x="3" y="6" width="9" height="14" rx="2"/><rect x="12.5" y="4" width="9" height="14" rx="2" fill="#8c50c8" fill-opacity="0.18"/></svg>',
  quiz: '<svg viewBox="0 0 24 24" fill="none" stroke="#50b450" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.5 8.5 0 0 1-12.5 7.5L3 21l2-5.5A8.5 8.5 0 1 1 21 11.5z"/><path d="M9.5 9.2a2.5 2.5 0 0 1 4.6 1.3c0 1.6-2.1 2-2.1 3"/><circle cx="12" cy="16.6" r="0.7" fill="#50b450" stroke="none"/></svg>',
  mastermind: '<svg viewBox="0 0 24 24"><circle cx="6" cy="8" r="2.7" fill="#e04646"/><circle cx="13" cy="8" r="2.7" fill="#50b450"/><circle cx="20" cy="8" r="2.7" fill="#3c82d2"/><circle cx="6" cy="16" r="2.7" fill="#d2c332"/><circle cx="13" cy="16" r="2.7" fill="#8c50c8"/><circle cx="20" cy="16" r="2.7" fill="#e68c32"/></svg>',
  anagram: '<svg viewBox="0 0 24 24" fill="none"><rect x="2.5" y="8.5" width="8" height="8" rx="1.5" stroke="#e68c32" stroke-width="2"/><rect x="13" y="6" width="8" height="8" rx="1.5" stroke="#e68c32" stroke-width="2" transform="rotate(11 17 10)"/><text x="6.5" y="14.5" font-size="6" fill="#e68c32" text-anchor="middle" font-family="sans-serif" font-weight="700">A</text><text x="17" y="12" font-size="6" fill="#e68c32" text-anchor="middle" font-family="sans-serif" font-weight="700" transform="rotate(11 17 10)">Z</text></svg>'
};
const MINI_GAMES = [
  { id:'guess', icon:MG_ICONS.guess, title:'Devine le nombre', init: mgGuess,
    desc:'L’ordinateur choisit un nombre entre 1 et 100. À toi de le trouver avec des indices plus grand / plus petit !',
    code:
`import random

secret = random.randint(1, 100)
essais = 0

while True:
    proposition = int(input("Ton nombre (1-100) : "))
    essais += 1
    if proposition < secret:
        print("C'est plus grand !")
    elif proposition > secret:
        print("C'est plus petit !")
    else:
        print(f"Bravo ! Trouvé en {essais} essais.")
        break` },
  { id:'rps', icon:MG_ICONS.rps, title:'Pierre-Feuille-Ciseaux', init: mgRPS,
    desc:'Affronte l’ordinateur. Le premier à comprendre random.choice gagne… ou pas !',
    code:
`import random

coups = ["pierre", "feuille", "ciseaux"]
bat = {"pierre": "ciseaux", "feuille": "pierre", "ciseaux": "feuille"}

moi = input("Ton coup (pierre/feuille/ciseaux) : ")
ordi = random.choice(coups)
print("L'ordi a joué :", ordi)

if moi == ordi:
    print("Égalité !")
elif bat[moi] == ordi:
    print("Gagné !")
else:
    print("Perdu...")` },
  { id:'ttt', icon:MG_ICONS.ttt, title:'Morpion', init: mgTTT,
    desc:'Le bon vieux tic-tac-toe contre une IA simple. Aligne 3 symboles !',
    code:
`plateau = [" "] * 9   # 9 cases vides

def gagne(p, joueur):
    lignes = [(0,1,2),(3,4,5),(6,7,8),   # horizontales
              (0,3,6),(1,4,7),(2,5,8),   # verticales
              (0,4,8),(2,4,6)]           # diagonales
    return any(all(p[i] == joueur for i in ligne) for ligne in lignes)

case = int(input("Numéro de case (0-8) : "))
plateau[case] = "X"

if gagne(plateau, "X"):
    print("Gagné !")` },
  { id:'hangman', icon:MG_ICONS.hangman, title:'Le Pendu', init: mgHangman,
    desc:'Devine le mot caché lettre par lettre… avant d’épuiser tes 6 vies !',
    code:
`import random

mots = ["PYTHON", "ORDINATEUR", "VARIABLE", "BOUCLE", "FONCTION"]
mot = random.choice(mots)
trouvees = set()
vies = 6

while vies > 0:
    affichage = "".join(c if c in trouvees else "_" for c in mot)
    print(affichage, " Vies :", vies)
    if all(c in trouvees for c in mot):
        print("Gagné !")
        break
    lettre = input("Une lettre : ").upper()
    trouvees.add(lettre)
    if lettre not in mot:
        vies -= 1
        print("Raté !")

if vies == 0:
    print("Perdu ! Le mot était", mot)` },
  { id:'fizzbuzz', icon:MG_ICONS.fizzbuzz, title:'FizzBuzz éclair', init: mgFizzBuzz,
    desc:'Pour le nombre affiché, clique vite : Fizz (÷3), Buzz (÷5), FizzBuzz (÷15) ou Nombre. Fais la plus longue série !',
    code:
`for n in range(1, 31):
    if n % 15 == 0:
        print("FizzBuzz")
    elif n % 3 == 0:
        print("Fizz")
    elif n % 5 == 0:
        print("Buzz")
    else:
        print(n)` },
  { id:'times', icon:MG_ICONS.times, title:'Quiz des tables', init: mgTimes,
    desc:'Réponds aux multiplications le plus vite possible. Une erreur remet ta série à zéro !',
    code:
`import random

score = 0
while True:
    a = random.randint(2, 9)
    b = random.randint(2, 9)
    reponse = int(input(f"{a} x {b} = "))
    if reponse == a * b:
        score += 1
        print("Bravo !", score, "d'affilee")
    else:
        print("Rate ! La reponse etait", a * b)
        score = 0` },
  { id:'simon', icon:MG_ICONS.simon, title:'Simon (mémoire)', init: mgSimon,
    desc:'Mémorise puis reproduis la séquence de couleurs, qui s’allonge à chaque tour.',
    code:
`import random

sequence = []
niveau = 0

while True:
    sequence.append(random.choice(["rouge", "vert", "bleu", "jaune"]))
    niveau += 1
    print("Mémorise :", sequence)
    for couleur in sequence:
        proposition = input("Couleur suivante : ")
        if proposition != couleur:
            print("Raté ! Niveau atteint :", niveau - 1)
            exit()
    print("Bravo, niveau", niveau, "réussi !")` },
  { id:'reflex', icon:MG_ICONS.reflex, title:'Test de réflexe', init: mgReflex,
    desc:'Clique dès que la zone passe au vert. Ton temps de réaction s’affiche en millisecondes !',
    code:
`import time, random

print("Quand tu vois GO, appuie sur Entrée le plus vite possible !")
time.sleep(random.uniform(1, 4))
print("GO !")
debut = time.time()
input()
temps = (time.time() - debut) * 1000
print(f"Ton temps : {temps:.0f} ms")` },
  { id:'memory', icon:MG_ICONS.memory, title:'Memory (paires)', init: mgMemory,
    desc:'Retourne les cartes deux par deux et retrouve les 6 paires en un minimum de coups.',
    code:
`import random

cartes = ["A", "A", "B", "B", "C", "C", "D", "D"]
random.shuffle(cartes)
trouvees = []

while len(trouvees) < len(cartes):
    i = int(input("Première carte : "))
    j = int(input("Deuxième carte : "))
    if i != j and cartes[i] == cartes[j]:
        print("Paire trouvée !")
        trouvees += [i, j]
    else:
        print("Raté, essaie encore.")` },
  { id:'quiz', icon:MG_ICONS.quiz, title:'Quiz Python', init: mgQuiz,
    desc:'6 questions sur les notions du TP (booléens, boucles, fonctions…). Teste tes connaissances !',
    code:
`questions = [
    ("Que vaut 7 % 2 ?", ["1", "3", "0"], 0),
    ("Quel mot-clé définit une fonction ?", ["func", "def", "lambda"], 1),
    ("Que renvoie len('abc') ?", ["2", "3", "4"], 1),
]
score = 0
for question, options, bonne in questions:
    print(question)
    for i, opt in enumerate(options):
        print(i, "-", opt)
    rep = int(input("Ton choix : "))
    if rep == bonne:
        print("Correct !")
        score += 1
    else:
        print("Non, la bonne réponse était :", options[bonne])
print("Score :", score, "/", len(questions))` },
  { id:'mastermind', icon:MG_ICONS.mastermind, title:'Mastermind', init: mgMastermind,
    desc:'Devine le code de 4 couleurs. Indices : combien sont bien placées, combien sont juste présentes.',
    code:
`import random

couleurs = ["R", "V", "B", "J", "M", "O"]
secret = [random.choice(couleurs) for _ in range(4)]

for essai in range(10):
    proposition = list(input("Ton code (4 lettres, ex RVBJ) : "))
    bien = sum(1 for i in range(4) if proposition[i] == secret[i])
    presents = sum(min(proposition.count(c), secret.count(c)) for c in set(couleurs))
    mal = presents - bien
    print("Bien placés :", bien, " Mal placés :", mal)
    if bien == 4:
        print("Gagné !")
        break` },
  { id:'anagram', icon:MG_ICONS.anagram, title:'Anagramme', init: mgAnagram,
    desc:'Les lettres d’un mot sont mélangées : remets-les dans le bon ordre.',
    code:
`import random

mots = ["ORDINATEUR", "PYTHON", "VARIABLE", "FONCTION"]
mot = random.choice(mots)

lettres = list(mot)
random.shuffle(lettres)
print("Mot mélangé :", "".join(lettres))

reponse = input("Ta réponse : ").upper()
if reponse == mot:
    print("Bravo !")
else:
    print("Non, c'était", mot)` }
];

let miniCur = null;

function miniRenderCards() {
  const wrap = document.getElementById('miniCards');
  if (!wrap) return;
  wrap.innerHTML = '';
  MINI_GAMES.forEach(g => {
    const card = document.createElement('div');
    card.className = 'fun-card';
    card.onclick = () => miniStart(g.id);
    card.innerHTML = '<div class="mg-icon">' + g.icon + '</div><h3>' + g.title +
      '</h3><p>' + g.desc + '</p><div class="medal">▶ Jouer</div>';
    wrap.appendChild(card);
  });
}

function miniStart(id) {
  miniCur = MINI_GAMES.find(g => g.id === id);
  if (!miniCur) return;
  document.getElementById('miniTitle').innerHTML = '<span class="mg-title-icon">' + miniCur.icon + '</span>' + miniCur.title;
  const code = document.getElementById('miniCode');
  code.style.display = 'none'; code.textContent = miniCur.code;
  document.getElementById('miniCodeBtn').textContent = '📖 Voir le code Python';
  document.getElementById('miniPlay').style.display = 'block';
  miniCur.init(document.getElementById('miniArea'));
  document.getElementById('miniPlay').scrollIntoView({ behavior:'smooth', block:'start' });
}

function miniClose() {
  document.getElementById('miniPlay').style.display = 'none';
  document.getElementById('miniCards').scrollIntoView({ behavior:'smooth' });
}

function miniToggleCode() {
  const c = document.getElementById('miniCode'), b = document.getElementById('miniCodeBtn');
  const show = c.style.display === 'none';
  c.style.display = show ? 'block' : 'none';
  b.textContent = show ? '🙈 Masquer le code' : '📖 Voir le code Python';
}

// ── Jeu : Devine le nombre ──
function mgGuess(area) {
  const secret = Math.floor(Math.random() * 100) + 1;
  let tries = 0;
  area.innerHTML =
    '<div class="mg-row"><input id="mgGuessInput" type="number" min="1" max="100" placeholder="1 - 100">' +
    '<button class="hanoi-btn" id="mgGuessBtn">Deviner</button></div>' +
    '<div id="mgGuessMsg" class="mg-msg">Je pense à un nombre entre 1 et 100…</div>';
  const input = area.querySelector('#mgGuessInput');
  const msg = area.querySelector('#mgGuessMsg');
  function go() {
    const v = parseInt(input.value, 10);
    if (!v) { msg.textContent = 'Entre un nombre valide.'; return; }
    tries++;
    if (v < secret) msg.textContent = '🔼 C’est plus grand ! (essai ' + tries + ')';
    else if (v > secret) msg.textContent = '🔽 C’est plus petit ! (essai ' + tries + ')';
    else {
      msg.textContent = '🎉 Bravo ! Trouvé en ' + tries + ' essais.';
      popConfetti(document.getElementById('funConfetti'), document.querySelector('#panel-fun .fun-wrap'));
    }
    input.value = ''; input.focus();
  }
  area.querySelector('#mgGuessBtn').addEventListener('click', go);
  input.addEventListener('keydown', e => { if (e.key === 'Enter') go(); });
  input.focus();
}

// ── Jeu : Pierre-Feuille-Ciseaux ──
function mgRPS(area) {
  let win = 0, lose = 0;
  const choices = [['pierre', '🪨'], ['feuille', '📄'], ['ciseaux', '✂️']];
  area.innerHTML =
    '<div class="mg-row">' +
    choices.map((c, i) => '<button class="hanoi-btn" data-i="' + i + '">' + c[1] + ' ' + c[0] + '</button>').join('') +
    '</div><div id="mgRpsMsg" class="mg-msg">Choisis ton coup !</div>' +
    '<div id="mgRpsScore" class="mg-msg">Score — Toi 0 / Ordi 0</div>';
  const msg = area.querySelector('#mgRpsMsg'), sc = area.querySelector('#mgRpsScore');
  area.querySelectorAll('[data-i]').forEach(b => b.addEventListener('click', () => {
    const me = parseInt(b.dataset.i, 10), ai = Math.floor(Math.random() * 3);
    let r;
    if (me === ai) r = 'Égalité !';
    else if ((me === 0 && ai === 2) || (me === 1 && ai === 0) || (me === 2 && ai === 1)) { r = 'Gagné ! 🎉'; win++; }
    else { r = 'Perdu… 😅'; lose++; }
    msg.textContent = 'Toi ' + choices[me][1] + '  vs  ' + choices[ai][1] + ' Ordi  →  ' + r;
    sc.textContent = 'Score — Toi ' + win + ' / Ordi ' + lose;
  }));
}

// ── Jeu : Morpion (vs IA aléatoire) ──
function mgTTT(area) {
  let board = Array(9).fill(''), over = false;
  area.innerHTML =
    '<div id="mgTTT" class="mg-ttt"></div>' +
    '<div id="mgTTTmsg" class="mg-msg">À toi (❌). Clique une case.</div>' +
    '<button class="hanoi-btn" id="mgTTTreset" style="margin-top:10px">↺ Rejouer</button>';
  const grid = area.querySelector('#mgTTT'), msg = area.querySelector('#mgTTTmsg');
  const L = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]];
  const wins = (b, p) => L.some(l => l.every(i => b[i] === p));
  function draw() {
    grid.innerHTML = '';
    board.forEach((v, i) => {
      const c = document.createElement('div');
      c.className = 'mg-cell'; c.textContent = v;
      c.addEventListener('click', () => play(i));
      grid.appendChild(c);
    });
  }
  function play(i) {
    if (over || board[i]) return;
    board[i] = '❌';
    if (wins(board, '❌')) { msg.textContent = '🎉 Tu as gagné !'; over = true; draw(); return; }
    if (board.every(x => x)) { msg.textContent = 'Match nul !'; over = true; draw(); return; }
    const free = board.map((v, j) => v ? -1 : j).filter(j => j >= 0);
    board[free[Math.floor(Math.random() * free.length)]] = '⭕';
    if (wins(board, '⭕')) { msg.textContent = 'L’ordi gagne… 😅'; over = true; }
    else if (board.every(x => x)) msg.textContent = 'Match nul !';
    draw();
  }
  area.querySelector('#mgTTTreset').addEventListener('click', () => {
    board = Array(9).fill(''); over = false;
    msg.textContent = 'À toi (❌). Clique une case.'; draw();
  });
  draw();
}

// ── Jeu : Le Pendu ──
function mgHangman(area) {
  const words = ['PYTHON','ORDINATEUR','VARIABLE','BOUCLE','FONCTION','ALGORITHME','CLAVIER','ECRAN'];
  const word = words[Math.floor(Math.random() * words.length)];
  let guessed = [], lives = 6;
  function render() {
    const masked = word.split('').map(c => guessed.includes(c) ? c : '_').join(' ');
    const won = word.split('').every(c => guessed.includes(c));
    const lost = lives <= 0;
    area.innerHTML =
      '<div class="mg-msg" style="font-size:26px;letter-spacing:5px">' + masked + '</div>' +
      '<div class="mg-msg">❤️ Vies : ' + lives + '</div>' +
      '<div id="mgHbtns" class="mg-row" style="max-width:430px"></div>' +
      '<div id="mgHmsg" class="mg-msg"></div>';
    const btns = area.querySelector('#mgHbtns');
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('').forEach(letter => {
      const b = document.createElement('button');
      b.className = 'hanoi-btn'; b.textContent = letter;
      b.style.padding = '4px 8px'; b.style.minWidth = '30px';
      if (guessed.includes(letter) || won || lost) b.disabled = true;
      b.addEventListener('click', () => {
        guessed.push(letter);
        if (!word.includes(letter)) lives--;
        render();
      });
      btns.appendChild(b);
    });
    const m = area.querySelector('#mgHmsg');
    if (won) {
      m.textContent = '🎉 Gagné ! Le mot était ' + word;
      popConfetti(document.getElementById('funConfetti'), document.querySelector('#panel-fun .fun-wrap'));
    } else if (lost) {
      m.textContent = '💀 Perdu ! Le mot était ' + word;
    }
  }
  render();
}

// ── Jeu : FizzBuzz éclair ──
function mgFizzBuzz(area) {
  let score = 0, n = 1;
  const correct = x => x % 15 === 0 ? 'FizzBuzz' : (x % 3 === 0 ? 'Fizz' : (x % 5 === 0 ? 'Buzz' : 'Nombre'));
  area.innerHTML =
    '<div id="fbNum" class="mg-msg" style="font-size:42px">?</div>' +
    '<div class="mg-row">' +
    ['Nombre','Fizz','Buzz','FizzBuzz'].map(o => '<button class="hanoi-btn" data-o="' + o + '">' + o + '</button>').join('') +
    '</div><div id="fbMsg" class="mg-msg">Fizz si ÷3, Buzz si ÷5, FizzBuzz si ÷15, sinon Nombre.</div>' +
    '<div id="fbScore" class="mg-msg">Série : 0</div>';
  const msg = area.querySelector('#fbMsg'), sc = area.querySelector('#fbScore');
  const num = area.querySelector('#fbNum');
  function next() { n = Math.floor(Math.random() * 30) + 1; num.textContent = n; }
  area.querySelectorAll('[data-o]').forEach(b => b.addEventListener('click', () => {
    if (b.dataset.o === correct(n)) { score++; msg.textContent = '✅ Correct !'; }
    else { msg.textContent = '❌ Raté ! ' + n + ' → ' + correct(n); score = 0; }
    sc.textContent = 'Série : ' + score;
    next();
  }));
  next();
}

// ── Jeu : Quiz des tables de multiplication ──
function mgTimes(area) {
  let score = 0, a = 2, b = 2;
  area.innerHTML =
    '<div id="tqQ" class="mg-msg" style="font-size:30px"></div>' +
    '<div class="mg-row"><input id="tqIn" type="number" placeholder="?"><button class="hanoi-btn" id="tqBtn">Valider</button></div>' +
    '<div id="tqMsg" class="mg-msg"></div><div id="tqScore" class="mg-msg">Bonnes réponses d’affilée : 0</div>';
  const inp = area.querySelector('#tqIn'), msg = area.querySelector('#tqMsg'), sc = area.querySelector('#tqScore');
  const q = area.querySelector('#tqQ');
  function nextQ() { a = Math.floor(Math.random() * 8) + 2; b = Math.floor(Math.random() * 8) + 2; q.textContent = a + ' × ' + b + ' = ?'; }
  function go() {
    const v = parseInt(inp.value, 10);
    if (v === a * b) { score++; msg.textContent = '✅ Bravo !'; }
    else { msg.textContent = '❌ Non, ' + a + ' × ' + b + ' = ' + (a * b); score = 0; }
    sc.textContent = 'Bonnes réponses d’affilée : ' + score;
    inp.value = ''; inp.focus(); nextQ();
  }
  area.querySelector('#tqBtn').addEventListener('click', go);
  inp.addEventListener('keydown', e => { if (e.key === 'Enter') go(); });
  nextQ(); inp.focus();
}

const FUN_HOST = () => document.querySelector('#panel-fun .fun-wrap');
function funBoom() { popConfetti(document.getElementById('funConfetti'), FUN_HOST()); }

// ── Jeu : Simon (mémoire de séquence) ──
function mgSimon(area) {
  const colors = ['#e04646', '#50b450', '#3c82d2', '#d2c332'];
  let seq = [], pos = 0, accepting = false, level = 0;
  area.innerHTML =
    '<div id="simonPads" style="display:grid;grid-template-columns:repeat(2,82px);gap:8px;width:172px"></div>' +
    '<div id="simonMsg" class="mg-msg">Niveau 0 — clique sur Démarrer.</div>' +
    '<button class="hanoi-btn" id="simonStart" style="margin-top:8px">▶ Démarrer</button>';
  const padsEl = area.querySelector('#simonPads'), msg = area.querySelector('#simonMsg'), pads = [];
  colors.forEach((c, i) => {
    const p = document.createElement('div');
    p.style.cssText = 'height:82px;border-radius:10px;cursor:pointer;transition:opacity .12s;opacity:.45;background:' + c;
    p.addEventListener('click', () => playerClick(i));
    padsEl.appendChild(p); pads.push(p);
  });
  function flash(i) { return new Promise(r => { pads[i].style.opacity = '1'; setTimeout(() => { pads[i].style.opacity = '.45'; setTimeout(r, 150); }, 340); }); }
  async function playSeq() { accepting = false; msg.textContent = 'Regarde bien…'; for (const i of seq) await flash(i); accepting = true; pos = 0; msg.textContent = 'À toi ! (niveau ' + level + ')'; }
  function addStep() { seq.push(Math.floor(Math.random() * 4)); level++; }
  async function playerClick(i) {
    if (!accepting) return;
    await flash(i);
    if (i !== seq[pos]) { accepting = false; msg.textContent = '💥 Raté ! Niveau atteint : ' + (level - 1) + '.'; return; }
    pos++;
    if (pos === seq.length) { accepting = false; addStep(); setTimeout(playSeq, 550); }
  }
  area.querySelector('#simonStart').addEventListener('click', () => { seq = []; level = 0; addStep(); playSeq(); });
}

// ── Jeu : Test de réflexe ──
function mgReflex(area) {
  area.innerHTML =
    '<div id="rxBox" style="height:140px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:18px;cursor:pointer;color:#fff;background:#b04040">Clique pour commencer</div>' +
    '<div id="rxMsg" class="mg-msg"></div>';
  const box = area.querySelector('#rxBox'), msg = area.querySelector('#rxMsg');
  let state = 'idle', t0 = 0, timer = null;
  box.addEventListener('click', () => {
    if (state === 'idle' || state === 'done') {
      state = 'waiting'; box.style.background = '#b04040'; box.textContent = 'Attends le VERT…'; msg.textContent = '';
      timer = setTimeout(() => { state = 'go'; t0 = performance.now(); box.style.background = '#2ea043'; box.textContent = 'CLIQUE !'; }, 900 + Math.random() * 2600);
    } else if (state === 'waiting') {
      clearTimeout(timer); state = 'done'; box.style.background = '#b04040'; box.textContent = 'Trop tôt ! Reclique pour réessayer';
    } else if (state === 'go') {
      const ms = Math.round(performance.now() - t0); state = 'done'; box.style.background = '#1f6feb'; box.textContent = ms + ' ms';
      msg.textContent = ms < 250 ? '⚡ Réflexes de félin !' : (ms < 400 ? 'Pas mal !' : 'On se réveille 😴');
    }
  });
}

// ── Jeu : Memory (paires) ──
function mgMemory(area) {
  const syms = ['A', 'B', 'C', 'D', 'E', 'F'];
  let deck = syms.concat(syms).sort(() => Math.random() - 0.5);
  let flipped = [], matched = [], moves = 0, lock = false;
  area.innerHTML = '<div id="memGrid" style="display:grid;grid-template-columns:repeat(4,64px);gap:8px"></div><div id="memMsg" class="mg-msg">Trouve les 6 paires !</div>';
  const grid = area.querySelector('#memGrid'), msg = area.querySelector('#memMsg');
  function draw() {
    grid.innerHTML = '';
    deck.forEach((v, i) => {
      const shown = flipped.includes(i) || matched.includes(i);
      const c = document.createElement('div');
      c.style.cssText = 'height:64px;display:flex;align-items:center;justify-content:center;font-size:24px;font-weight:700;border-radius:8px;cursor:pointer;color:#fff;border:1px solid #30363d;background:' + (shown ? '#1f6feb' : '#161c2a');
      c.textContent = shown ? v : '';
      c.addEventListener('click', () => flip(i));
      grid.appendChild(c);
    });
  }
  function flip(i) {
    if (lock || flipped.includes(i) || matched.includes(i)) return;
    flipped.push(i); draw();
    if (flipped.length === 2) {
      moves++;
      if (deck[flipped[0]] === deck[flipped[1]]) {
        matched = matched.concat(flipped); flipped = []; draw();
        if (matched.length === deck.length) { msg.textContent = '🎉 Gagné en ' + moves + ' coups !'; funBoom(); }
      } else { lock = true; setTimeout(() => { flipped = []; lock = false; draw(); }, 700); }
    }
  }
  draw();
}

// ── Jeu : Quiz Python ──
function mgQuiz(area) {
  const Q = [
    { q:'Que vaut 7 % 2 ?', o:['1', '3', '0', '3.5'], a:0 },
    { q:'Quel mot-clé répète tant qu’une condition est vraie ?', o:['for', 'while', 'if', 'def'], a:1 },
    { q:'Quel mot-clé définit une fonction ?', o:['func', 'def', 'function', 'lambda'], a:1 },
    { q:'Que renvoie len("abc") ?', o:['2', '3', '4', '"abc"'], a:1 },
    { q:'Quel type renvoie 5 == 5 ?', o:['int', 'str', 'bool', 'list'], a:2 },
    { q:'Comment accéder au 1er élément d’une liste L ?', o:['L(0)', 'L[1]', 'L[0]', 'L.first'], a:2 }
  ];
  let idx = 0, score = 0;
  function render() {
    if (idx >= Q.length) {
      area.innerHTML = '<div class="mg-msg" style="font-size:20px">Score final : ' + score + ' / ' + Q.length + '</div><button class="hanoi-btn" id="quizAgain" style="margin-top:10px">↺ Recommencer</button>';
      area.querySelector('#quizAgain').addEventListener('click', () => { idx = 0; score = 0; render(); });
      if (score === Q.length) funBoom();
      return;
    }
    const cur = Q[idx];
    area.innerHTML = '<div class="mg-msg" style="font-size:17px">Q' + (idx + 1) + '. ' + cur.q + '</div>' +
      '<div id="quizOpts" class="mg-row" style="flex-direction:column;align-items:stretch;max-width:360px"></div><div id="quizMsg" class="mg-msg"></div>';
    const opts = area.querySelector('#quizOpts'), msg = area.querySelector('#quizMsg');
    cur.o.forEach((o, i) => {
      const b = document.createElement('button');
      b.className = 'hanoi-btn'; b.style.textAlign = 'left'; b.textContent = o;
      b.addEventListener('click', () => {
        if (i === cur.a) { score++; msg.textContent = '✅ Correct !'; }
        else { msg.textContent = '❌ Non. Bonne réponse : ' + cur.o[cur.a]; }
        opts.querySelectorAll('button').forEach(x => x.disabled = true);
        setTimeout(() => { idx++; render(); }, 950);
      });
      opts.appendChild(b);
    });
  }
  render();
}

// ── Jeu : Mastermind ──
function mgMastermind(area) {
  const palette = ['#e04646', '#50b450', '#3c82d2', '#d2c332', '#8c50c8', '#e68c32'];
  const N = 4;
  let secret = Array.from({ length: N }, () => Math.floor(Math.random() * palette.length));
  let guess = [], rows = 0, over = false;
  area.innerHTML =
    '<div id="mmPal" class="mg-row"></div><div id="mmCur" class="mg-row" style="gap:6px"></div>' +
    '<div class="mg-row"><button class="hanoi-btn" id="mmClear">Effacer</button><button class="hanoi-btn" id="mmOk">Valider</button></div>' +
    '<div id="mmHist"></div><div id="mmMsg" class="mg-msg">Trouve le code de 4 couleurs (10 essais).</div>';
  const pal = area.querySelector('#mmPal'), cur = area.querySelector('#mmCur'), hist = area.querySelector('#mmHist'), msg = area.querySelector('#mmMsg');
  function dot(color, s) { const d = document.createElement('span'); d.style.cssText = 'display:inline-block;width:' + s + 'px;height:' + s + 'px;border-radius:50%;border:1px solid #0008;background:' + color; return d; }
  palette.forEach((c, i) => {
    const b = document.createElement('button'); b.className = 'hanoi-btn';
    b.style.cssText = 'padding:0;width:30px;height:30px;border-radius:50%;background:' + c;
    b.addEventListener('click', () => { if (over || guess.length >= N) return; guess.push(i); drawCur(); });
    pal.appendChild(b);
  });
  function drawCur() { cur.innerHTML = ''; for (let k = 0; k < N; k++) cur.appendChild(dot(guess[k] !== undefined ? palette[guess[k]] : '#161c2a', 26)); }
  function feedback(g) {
    let black = 0, white = 0; const s = secret.slice(), gg = g.slice();
    for (let k = 0; k < N; k++) if (gg[k] === s[k]) { black++; s[k] = -1; gg[k] = -2; }
    for (let k = 0; k < N; k++) { if (gg[k] < 0) continue; const idx = s.indexOf(gg[k]); if (idx >= 0) { white++; s[idx] = -1; } }
    return [black, white];
  }
  area.querySelector('#mmClear').addEventListener('click', () => { if (!over) { guess = []; drawCur(); } });
  area.querySelector('#mmOk').addEventListener('click', () => {
    if (over || guess.length < N) return;
    const fb = feedback(guess); rows++;
    const row = document.createElement('div'); row.className = 'mg-row'; row.style.gap = '6px';
    guess.forEach(gi => row.appendChild(dot(palette[gi], 22)));
    const t = document.createElement('span'); t.className = 'mg-msg'; t.style.marginLeft = '10px';
    t.textContent = '● bien placés : ' + fb[0] + '   ○ mal placés : ' + fb[1]; row.appendChild(t);
    hist.appendChild(row);
    if (fb[0] === N) { over = true; msg.textContent = '🎉 Code trouvé en ' + rows + ' essais !'; funBoom(); }
    else if (rows >= 10) {
      over = true; msg.textContent = '💀 Perdu ! Le code était :';
      const r = document.createElement('div'); r.className = 'mg-row'; r.style.gap = '6px';
      secret.forEach(si => r.appendChild(dot(palette[si], 22))); hist.appendChild(r);
    }
    guess = []; drawCur();
  });
  drawCur();
}

// ── Jeu : Anagramme ──
function mgAnagram(area) {
  const words = ['ORDINATEUR', 'PYTHON', 'VARIABLE', 'FONCTION', 'ALGORITHME', 'PROGRAMME', 'CLAVIER', 'BOUCLE'];
  const word = words[Math.floor(Math.random() * words.length)];
  let scrambled;
  do { scrambled = word.split('').sort(() => Math.random() - 0.5).join(''); } while (scrambled === word);
  area.innerHTML =
    '<div class="mg-msg" style="font-size:26px;letter-spacing:6px">' + scrambled.split('').join(' ') + '</div>' +
    '<div class="mg-row"><input id="anIn" type="text" style="width:220px;text-transform:uppercase"><button class="hanoi-btn" id="anOk">Vérifier</button></div>' +
    '<div id="anMsg" class="mg-msg">Remets les lettres dans le bon ordre !</div>' +
    '<button class="hanoi-btn" id="anNew" style="margin-top:6px">↻ Autre mot</button>';
  const inp = area.querySelector('#anIn'), msg = area.querySelector('#anMsg');
  function check() {
    if (inp.value.trim().toUpperCase() === word) { msg.textContent = '🎉 Bravo, c’était ' + word + ' !'; funBoom(); }
    else { msg.textContent = '❌ Pas encore… essaie encore.'; }
  }
  area.querySelector('#anOk').addEventListener('click', check);
  inp.addEventListener('keydown', e => { if (e.key === 'Enter') check(); });
  area.querySelector('#anNew').addEventListener('click', () => mgAnagram(area));
  inp.focus();
}

// Init : cartes + révèle l'onglet s'il a déjà été débloqué.
// On attend le DOM : le panneau #panel-fun est inséré plus bas que ce script.
document.addEventListener('DOMContentLoaded', () => {
  funRenderCards();
  miniRenderCards();
  try { if (localStorage.getItem('hanoi_fun_unlocked') === '1') revealFunTab(); } catch (e) {}
});

</script>

<!-- ───────── Onglet « Défis Fun » ───────── -->
<style>
.tab-btn.hidden { display: none; }
.tab-btn.fun-tab { color: #d2c332; }
.tab-btn.fun-tab.active { color: #ffd33d; border-bottom-color: #ffd33d; }
.fun-wrap { position: relative; max-width: 920px; margin: 0 auto; padding: 26px 40px 70px; }
.fun-hero h2 { color: var(--blue, #58a6ff); font-size: 24px; margin-bottom: 8px; }
.fun-hero p  { color: #9aa7b4; font-size: 14px; line-height: 1.6; margin-bottom: 24px; }
.fun-cards { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 16px; }
.fun-card { background: #161c2a; border: 1px solid #21262d; border-radius: 12px; padding: 18px; cursor: pointer; transition: transform .15s, border-color .15s, box-shadow .15s; }
.fun-card:hover { transform: translateY(-3px); border-color: var(--blue2, #1f6feb); box-shadow: 0 8px 24px rgba(0,0,0,.45); }
.fun-card .emoji { font-size: 34px; line-height: 1; }
.fun-card h3 { color: #e6edf3; font-size: 17px; margin: 10px 0 6px; }
.fun-card p  { color: #9aa7b4; font-size: 13px; line-height: 1.5; min-height: 56px; }
.fun-card .medal { margin-top: 10px; font-weight: 700; font-size: 13.5px; color: #d2c332; }
.fun-play { margin-top: 10px; }
.fun-play-head { display: flex; align-items: center; gap: 14px; margin-bottom: 14px; }
.fun-play-head span { font-weight: 700; color: #e6edf3; font-size: 19px; }
.fun-bar { display: flex; gap: 10px; flex-wrap: wrap; align-items: center; margin-bottom: 14px; font-size: 13px; color: #cdd9e5; }
.fun-bar span { background: #0d1117; border: 1px solid #21262d; border-radius: 6px; padding: 4px 10px; font-weight: 700; }
.fun-board { max-width: 700px; height: 340px; margin: 0 auto 26px; }
#funConfetti { position: absolute; inset: 0; width: 100%; height: 100%; pointer-events: none; z-index: 50; }
.fun-section-title { margin: 38px 0 14px; font-size: 19px; font-weight: 700; color: #e6edf3; }
.fun-section-title span { font-size: 13px; font-weight: 500; color: #9aa7b4; }
.mg-icon { height: 46px; display: flex; align-items: center; }
.mg-icon svg { width: 46px; height: 46px; }
.mg-title-icon svg { width: 24px; height: 24px; vertical-align: middle; margin-right: 8px; }
.mini-play { margin-top: 10px; background: #0d1117; border: 1px solid #21262d; border-radius: 12px; padding: 18px; }
.mini-area { min-height: 90px; margin: 8px 0; }
.mg-row { display: flex; gap: 10px; flex-wrap: wrap; align-items: center; margin-bottom: 12px; }
.mg-row input { background: #161c2a; color: #fff; border: 1px solid #30363d; border-radius: 6px; padding: 8px 10px; font-size: 15px; width: 120px; }
.mg-msg { color: #cdd9e5; font-size: 15px; font-weight: 600; margin-top: 6px; }
.mg-ttt { display: grid; grid-template-columns: repeat(3, 60px); gap: 6px; }
.mg-cell { width: 60px; height: 60px; display: flex; align-items: center; justify-content: center; font-size: 30px; background: #161c2a; border: 1px solid #30363d; border-radius: 8px; cursor: pointer; transition: background .12s; }
.mg-cell:hover { background: #1f2733; }
.mini-code { background: #05080c; border: 1px solid #21262d; border-radius: 8px; padding: 14px; color: #cdd9e5; font-family: 'Cascadia Code','Fira Code',monospace; font-size: 13px; line-height: 1.6; overflow-x: auto; white-space: pre; margin-top: 12px; }
</style>

<div id="panel-fun" class="tab-panel" style="overflow-y:auto;max-height:calc(100vh - 120px)">
  <div class="fun-wrap">
    <canvas id="funConfetti"></canvas>
    <div class="fun-hero">
      <h2>🎉 Défis Fun — le Hanoï déchaîné</h2>
      <p>Tu as terminé les 5 exercices, bravo ! Voici 5 défis bonus, plus durs et plus fun, jouables à la souris. Décroche les médailles 🥇🥈🥉 !</p>
    </div>
    <div id="funCards" class="fun-cards"></div>
    <div id="funPlay" class="fun-play" style="display:none">
      <div class="fun-play-head">
        <button type="button" class="hanoi-btn" onclick="funClose()">← Retour aux défis</button>
        <span id="funTitle"></span>
      </div>
      <div class="fun-bar">
        <span id="funGoal"></span>
        <span id="funMoves">Coups : 0</span>
        <span id="funTime">⏱ 0.0s</span>
        <button type="button" class="hanoi-btn" onclick="funRestart()">↺ Recommencer</button>
        <button type="button" class="hanoi-btn" onclick="funUndo()">↶ Annuler</button>
      </div>
      <div id="funBoard" class="hanoi-board fun-board"></div>
      <div id="funMsg" class="hanoi-msg"></div>
    </div>

    <div class="fun-section-title">🎮 Mini-jeux bonus <span>(rien à voir avec Hanoï — juste pour s\'amuser, avec le code Python expliqué)</span></div>
    <div id="miniCards" class="fun-cards"></div>
    <div id="miniPlay" class="mini-play" style="display:none">
      <div class="fun-play-head">
        <button type="button" class="hanoi-btn" onclick="miniClose()">← Retour</button>
        <span id="miniTitle"></span>
        <button type="button" class="hanoi-btn" id="miniCodeBtn" onclick="miniToggleCode()" style="margin-left:auto">📖 Voir le code Python</button>
      </div>
      <div id="miniArea" class="mini-area"></div>
      <pre id="miniCode" class="mini-code" style="display:none"></pre>
    </div>
  </div>
</div>

<!-- ───────── Volet coulissant : Hanoï jouable ───────── -->
<style>
.hanoi-drawer {
  position: fixed; top: 0; right: 0; height: 100vh; width: 380px;
  background: #0b1622; border-left: 1px solid var(--blue2, #1f6feb);
  box-shadow: -12px 0 30px rgba(0,0,0,.45);
  transform: translateX(380px);
  transition: transform .35s cubic-bezier(.4,0,.2,1);
  z-index: 1200; display: flex; flex-direction: column;
}
.hanoi-drawer.open { transform: translateX(0); }
.hanoi-handle {
  position: absolute; left: -42px; top: 50%; transform: translateY(-50%);
  width: 42px; padding: 20px 0; cursor: pointer;
  border: 1px solid var(--blue2, #1f6feb); border-right: none;
  border-radius: 12px 0 0 12px;
  background: linear-gradient(135deg, var(--blue2, #1f6feb), var(--blue, #58a6ff));
  color: #fff; font-weight: 700; font-size: 13px; letter-spacing: .5px;
  writing-mode: vertical-rl; text-orientation: mixed;
  box-shadow: -4px 0 12px rgba(0,0,0,.35);
}
.hanoi-handle:hover { filter: brightness(1.1); }
.hanoi-inner { position: relative; padding: 20px 18px 24px; overflow-y: auto; height: 100%; box-sizing: border-box; }
.hanoi-head h3 { color: var(--blue, #58a6ff); font-size: 18px; margin: 0 0 6px; }
.hanoi-head p  { color: #9aa7b4; font-size: 13px; line-height: 1.5; margin: 0 0 16px; }
.hanoi-bar { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; margin-bottom: 10px; font-size: 13px; color: #cdd9e5; }
.hanoi-bar select { background: #0d1117; color: #fff; border: 1px solid #30363d; border-radius: 6px; padding: 3px 6px; }
.hanoi-btn { background: #0d1117; color: var(--blue, #58a6ff); border: 1px solid var(--blue2, #1f6feb); border-radius: 6px; padding: 5px 11px; cursor: pointer; font-size: 12px; font-weight: 600; transition: .12s; }
.hanoi-btn:hover { background: var(--blue2, #1f6feb); color: #fff; }
.hanoi-stats { display: flex; justify-content: space-between; gap: 8px; margin-bottom: 12px; font-size: 12.5px; font-weight: 700; color: #cdd9e5; }
.hanoi-stats span { background: #0d1117; border: 1px solid #21262d; border-radius: 6px; padding: 4px 9px; }
.hanoi-board { position: relative; display: flex; justify-content: space-around; align-items: flex-end; gap: 10px; height: 300px; background: radial-gradient(120% 90% at 50% 0%, #111c2b, #0a0f16); border: 1px solid #21262d; border-radius: 10px; padding: 14px 10px; margin-bottom: 26px; user-select: none; -webkit-user-select: none; touch-action: none; }
.hanoi-pole { position: relative; flex: 1; height: 100%; display: flex; flex-direction: column-reverse; align-items: center; cursor: pointer; border-radius: 8px; transition: background .15s; }
.hanoi-pole:hover { background: rgba(88,166,255,.06); }
.hanoi-pole.selected { background: rgba(88,166,255,.14); outline: 2px solid var(--blue, #58a6ff); }
.hanoi-pole.valid { background: rgba(63,185,80,.10); }
.hanoi-pole.valid::after { background: #2ea043; box-shadow: 0 0 12px rgba(46,160,67,.7); }
.hanoi-pole::before { content: ""; position: absolute; bottom: 14px; left: 50%; transform: translateX(-50%); width: 7px; height: calc(100% - 14px); background: linear-gradient(90deg, #2a3340, #475363, #2a3340); border-radius: 4px; }
.hanoi-pole::after  { content: ""; position: absolute; bottom: 6px; left: 8%; width: 84%; height: 9px; background: linear-gradient(90deg, #2a3340, #475363, #2a3340); border-radius: 5px; transition: background .15s, box-shadow .15s; }
.hanoi-disk {
  position: relative; z-index: 1; height: 22px; margin-bottom: 3px; border-radius: 7px;
  background-image: linear-gradient(180deg, rgba(255,255,255,.45), rgba(255,255,255,0) 42%, rgba(0,0,0,.30));
  box-shadow: inset 0 1px 1px rgba(255,255,255,.55), inset 0 -3px 4px rgba(0,0,0,.35), 0 2px 5px rgba(0,0,0,.55);
  border: 1px solid rgba(0,0,0,.30);
}
.hanoi-disk.lifted { outline: 2px solid #fff; box-shadow: 0 0 14px rgba(255,255,255,.5), inset 0 1px 1px rgba(255,255,255,.55); transform: translateY(-8px); }
.hanoi-label { position: absolute; bottom: -22px; left: 50%; transform: translateX(-50%); color: #8b98a5; font-weight: 700; font-size: 14px; }
.hanoi-msg { min-height: 22px; font-weight: 700; font-size: 14px; text-align: center; }
.hanoi-msg.win { color: var(--green, #3fb950); }
.hanoi-msg.bad { color: #ff7070; }
#hanoiConfetti { position: absolute; inset: 0; width: 100%; height: 100%; pointer-events: none; z-index: 50; }
</style>

<div id="hanoiDrawer" class="hanoi-drawer">
  <button type="button" id="hanoiHandle" class="hanoi-handle" onclick="toggleHanoi()">🎮 Joue au Hanoï</button>
  <canvas id="hanoiConfetti"></canvas>
  <div class="hanoi-inner">
    <div class="hanoi-head">
      <h3>Tours de Hanoï</h3>
      <p>Clique un poteau pour <b>prendre</b> l\'anneau du sommet, puis un poteau valide (en vert) pour le <b>poser</b>. Reconstruis la tour sur un autre poteau !</p>
    </div>
    <div class="hanoi-bar">
      <label>Anneaux :
        <select id="hanoiCount" onchange="hanoiReset()">
          <option>3</option><option selected>4</option><option>5</option><option>6</option>
          <option>7</option><option>8</option><option>9</option><option>10</option>
        </select>
      </label>
      <button type="button" class="hanoi-btn" id="hanoiSolveBtn" onclick="hanoiSolveToggle()">✨ Résoudre</button>
      <button type="button" class="hanoi-btn" onclick="hanoiUndo()">↶ Annuler</button>
      <button type="button" class="hanoi-btn" onclick="hanoiReset()">↺ Rejouer</button>
    </div>
    <div class="hanoi-stats">
      <span id="hanoiMoves">Coups : 0</span>
      <span id="hanoiTime">⏱ 0.0s</span>
      <span id="hanoiBest">🏆 —</span>
    </div>
    <div id="hanoiBoard" class="hanoi-board"></div>
    <div id="hanoiMsg" class="hanoi-msg"></div>
  </div>
</div>

</body>
</html>
"""

