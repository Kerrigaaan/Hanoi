# Page principale du TP — le HTML reference des fichiers statiques (static/).
# CSS  : static/style.css   JS : static/app.js, static/hanoi.js, static/games.js

HTML = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>TP — Tours de Hanoï</title>
<link rel="stylesheet" href="/static/style.css">
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
    <p>Fais les exercices <b>dans l'ordre</b> — chaque exercice se débloque quand le précédent est réussi.</p>
  </div>
  <div class="hdr-right">
    <span id="statusMsg" class="info">Commence par l'exercice 1 !</span>
  </div>
</header>

<!-- barre d'onglets -->
<div class="tabs">
  <button type="button" class="tab-btn active" id="tab-accueil"   onclick="switchTab('accueil')">Accueil</button>
  <button type="button" class="tab-btn" id="tab-exercises" onclick="switchTab('exercises')">Exercices</button>
  <button type="button" class="tab-btn" id="tab-docs"      onclick="switchTab('docs')">Documentation Python</button>
  <button type="button" class="tab-btn fun-tab hidden" id="tab-fun" onclick="switchTab('fun')"><span class="fun-ico-sm"><svg viewBox="0 0 24 24" fill="none"><path d="M3 21l5.5-11 5.5 5.5z" fill="#e68c32"/><path d="M3 21l5.5-11 2.6 2.6z" fill="#d2c332"/><circle cx="15.5" cy="6" r="1.3" fill="#e04646"/><circle cx="19.5" cy="9.5" r="1.3" fill="#3c82d2"/><circle cx="18" cy="4" r="1.1" fill="#50b450"/><circle cx="21" cy="13.5" r="1.1" fill="#8c50c8"/><path d="M14 9.5l2.2-2.2M16.5 12.5l2.4-1M13.2 6.5l1.4-2.6" stroke="#d2c332" stroke-width="1.3" stroke-linecap="round"/></svg></span> Défis Fun</button>
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

<script>var EXS = %EXERCISES_JSON%;</script>
<script src="/static/app.js"></script>
<script src="/static/hanoi.js"></script>
<script src="/static/games.js"></script>

<!-- ───────── Onglet « Défis Fun » ───────── -->


<div id="panel-fun" class="tab-panel" style="overflow-y:auto;max-height:calc(100vh - 120px)">
  <div class="fun-wrap">
    <canvas id="funConfetti"></canvas>
    <div class="fun-hero">
      <h2><span class="fun-ico-lg"><svg viewBox="0 0 24 24" fill="none"><path d="M3 21l5.5-11 5.5 5.5z" fill="#e68c32"/><path d="M3 21l5.5-11 2.6 2.6z" fill="#d2c332"/><circle cx="15.5" cy="6" r="1.3" fill="#e04646"/><circle cx="19.5" cy="9.5" r="1.3" fill="#3c82d2"/><circle cx="18" cy="4" r="1.1" fill="#50b450"/><circle cx="21" cy="13.5" r="1.1" fill="#8c50c8"/><path d="M14 9.5l2.2-2.2M16.5 12.5l2.4-1M13.2 6.5l1.4-2.6" stroke="#d2c332" stroke-width="1.3" stroke-linecap="round"/></svg></span> Défis Fun — le Hanoï déchaîné</h2>
      <p>Tu as terminé les 5 exercices, bravo ! Voici 5 défis bonus, plus durs et plus fun, jouables à la souris. Décroche les médailles 🥇🥈🥉 !</p>
    </div>
    <div class="fun-section-title">🏅 Mes trophées</div>
    <div id="funScore" class="fun-score"></div>
    <div class="fun-section-title">🗼 Défis Hanoï</div>
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

    <div class="fun-section-title">🎮 Mini-jeux bonus <span>(rien à voir avec Hanoï — juste pour s'amuser, avec le code Python expliqué)</span></div>
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


<div id="hanoiDrawer" class="hanoi-drawer">
  <button type="button" id="hanoiHandle" class="hanoi-handle" onclick="toggleHanoi()">🎮 Joue au Hanoï</button>
  <canvas id="hanoiConfetti"></canvas>
  <div class="hanoi-inner">
    <div class="hanoi-head">
      <h3>Tours de Hanoï</h3>
      <p>Clique un poteau pour <b>prendre</b> l'anneau du sommet, puis un poteau valide (en vert) pour le <b>poser</b>. Reconstruis la tour sur un autre poteau !</p>
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
