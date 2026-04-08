# Page documentation Python — onglet Documentation

DOCS = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>Documentation Python — TP Hanoï</title>
<style>
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
  font-size: 13px;
  font-weight: 700;
  color: #c8d0e0;
  text-transform: uppercase;
  letter-spacing: .08em;
  padding: 0 10px 10px;
}
.nav-link {
  display: block;
  padding: 11px 14px;
  border-radius: 8px;
  font-size: 15px;
  color: #ffffff;
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
.doc-head h2 { font-size: 18px; font-weight: 700; color: #ffffff; }
.doc-body {
  padding: 26px 28px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* ── sous-sections ── */
.sub { display: flex; flex-direction: column; gap: 10px; }
.sub-title {
  font-size: 16px;
  font-weight: 700;
  color: var(--blue);
  border-bottom: 1px solid var(--border);
  padding-bottom: 6px;
}
.sub p, .sub li {
  font-size: 16px;
  line-height: 2;
  color: #ffffff;
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
  padding: 8px 16px;
  background: var(--panel);
  border-bottom: 1px solid var(--border);
  font-size: 13px;
  color: #c8d0e0;
  text-transform: uppercase;
  letter-spacing: .06em;
}
pre {
  padding: 18px 20px;
  font-family: 'Cascadia Code','Fira Code','Courier New', monospace;
  font-size: 15px;
  line-height: 2;
  overflow-x: auto;
  color: #ffffff;
}
/* coloration syntaxique manuelle */
.kw  { color: #e0a0ff; }   /* keywords */
.fn  { color: #80c8ff; }   /* fonctions */
.st  { color: #b5f0a0; }   /* strings */
.nb  { color: #ffd080; }   /* nombres */
.cm  { color: #8090a8; font-style: italic; }   /* commentaires */
.op  { color: #80e0f0; }   /* opérateurs */
.var { color: #ff9090; }   /* variables / noms */

/* ── astuce / attention ── */
.tip {
  display: flex; gap: 12px; align-items: flex-start;
  background: #0e2010; border: 1px solid #1e5c28;
  border-radius: 10px; padding: 16px 18px;
  font-size: 14px; line-height: 1.7; color: #b6e4be;
}
.warn {
  display: flex; gap: 12px; align-items: flex-start;
  background: #1c1205; border: 1px solid #7a5010;
  border-radius: 10px; padding: 16px 18px;
  font-size: 15px; line-height: 1.9; color: #ffffff;
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

<header>
  <div class="hdr-left">
    <h1>Documentation Python</h1>
  </div>
  <a class="back-btn" href="/tp">← Retour aux exercices</a>
</header>

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

<script>
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
</script>
</body>
</html>
"""

