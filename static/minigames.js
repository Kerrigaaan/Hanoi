// Onglet « Défis Fun » — les 15 mini-jeux bonus (avec code Python) et l'init du DOM.

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
  anagram: '<svg viewBox="0 0 24 24" fill="none"><rect x="2.5" y="8.5" width="8" height="8" rx="1.5" stroke="#e68c32" stroke-width="2"/><rect x="13" y="6" width="8" height="8" rx="1.5" stroke="#e68c32" stroke-width="2" transform="rotate(11 17 10)"/><text x="6.5" y="14.5" font-size="6" fill="#e68c32" text-anchor="middle" font-family="sans-serif" font-weight="700">A</text><text x="17" y="12" font-size="6" fill="#e68c32" text-anchor="middle" font-family="sans-serif" font-weight="700" transform="rotate(11 17 10)">Z</text></svg>',
  snake: '<svg viewBox="0 0 24 24" fill="none" stroke="#50b450" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6h6a3 3 0 0 1 0 6H8a3 3 0 0 0 0 6h8"/><circle cx="18" cy="18" r="1.4" fill="#50b450" stroke="none"/></svg>',
  g2048: '<svg viewBox="0 0 24 24" fill="none"><rect x="3" y="3" width="18" height="18" rx="3" stroke="#e68c32" stroke-width="2"/><rect x="5.5" y="5.5" width="5.5" height="5.5" rx="1" fill="#d2c332"/><rect x="13" y="5.5" width="5.5" height="5.5" rx="1" fill="#e68c32"/><rect x="5.5" y="13" width="5.5" height="5.5" rx="1" fill="#e68c32" opacity=".6"/><rect x="13" y="13" width="5.5" height="5.5" rx="1" fill="#e04646"/></svg>',
  mines: '<svg viewBox="0 0 24 24" fill="none" stroke="#e04646" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="13" r="5" fill="#e04646" stroke="none"/><path d="M12 3v3M12 20v1M3 13h3M18 13h3M6 7l2 2M18 7l-2 2"/></svg>'
};

// ═══════════ Barème des médailles par mini-jeu ═══════════
// by:'high' → plus c'est grand mieux c'est ; by:'low' → plus c'est petit mieux c'est.
// Seuils or / argent / bronze, et libellé affiché (« Record : … »).
const MG_SCORE = {
  guess:      { by:'low',  gold:5,   silver:8,   bronze:12,  label:'essais' },
  rps:        { by:'high', gold:5,   silver:3,   bronze:1,   label:'série' },
  ttt:        { by:'high', gold:3,   silver:2,   bronze:1,   label:'',
                names:['', 'Facile battu', 'Moyen battu', 'Imbattable battu !'] },
  hangman:    { by:'high', gold:5,   silver:3,   bronze:1,   label:'vies restantes' },
  fizzbuzz:   { by:'high', gold:15,  silver:8,   bronze:3,   label:'série' },
  times:      { by:'high', gold:15,  silver:8,   bronze:3,   label:'série' },
  simon:      { by:'high', gold:8,   silver:5,   bronze:2,   label:'niveau' },
  reflex:     { by:'low',  gold:250, silver:350, bronze:550, label:'ms' },
  memory:     { by:'low',  gold:8,   silver:12,  bronze:20,  label:'coups' },
  quiz:       { by:'high', gold:6,   silver:4,   bronze:2,   label:'/ 6' },
  mastermind: { by:'low',  gold:4,   silver:6,   bronze:10,  label:'essais' },
  anagram:    { by:'high', gold:6,   silver:3,   bronze:1,   label:'mots' },
  snake:      { by:'high', gold:20,  silver:10,  bronze:3,   label:'score' },
  g2048:      { by:'high', gold:2048,silver:512, bronze:128, label:'meilleure tuile' },
  mines:      { by:'low',  gold:30,  silver:60,  bronze:120, label:'s' }
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
    print("Non, c'était", mot)` },
  { id:'snake', icon:MG_ICONS.snake, title:'Snake', init: mgSnake,
    desc:'Le serpent classique : mange les pommes, grandis, et évite ta propre queue ! (flèches du clavier)',
    code:
`# Snake se code avec pygame (boucle de jeu temps réel).
import pygame, random

pygame.init()
ecran = pygame.display.set_mode((400, 400))
horloge = pygame.time.Clock()
serpent = [(10, 10)]
direction = (1, 0)
pomme = (15, 15)

while True:
    for e in pygame.event.get():
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_UP:    direction = (0, -1)
            if e.key == pygame.K_DOWN:  direction = (0, 1)
            if e.key == pygame.K_LEFT:  direction = (-1, 0)
            if e.key == pygame.K_RIGHT: direction = (1, 0)
    tete = (serpent[0][0] + direction[0], serpent[0][1] + direction[1])
    serpent.insert(0, tete)
    if tete == pomme:
        pomme = (random.randint(0, 19), random.randint(0, 19))
    else:
        serpent.pop()       # avance sans grandir
    horloge.tick(10)` },
  { id:'g2048', icon:MG_ICONS.g2048, title:'2048', init: mg2048,
    desc:'Fusionne les tuiles identiques avec les flèches pour atteindre 2048 !',
    code:
`# Idée : une grille 4x4. On compacte une ligne vers la gauche,
# puis on fusionne les voisines égales.
def compacter(ligne):
    nums = [x for x in ligne if x != 0]      # enlève les zéros
    i = 0
    while i < len(nums) - 1:
        if nums[i] == nums[i + 1]:
            nums[i] *= 2                      # fusion
            nums.pop(i + 1)
        i += 1
    return nums + [0] * (4 - len(nums))       # complète avec des zéros

print(compacter([2, 2, 4, 0]))   # -> [4, 4, 0, 0]
print(compacter([2, 0, 2, 2]))   # -> [4, 2, 0, 0]` },
  { id:'mines', icon:MG_ICONS.mines, title:'Démineur', init: mgMines,
    desc:'Découvre toutes les cases sans mine. Clic = révéler, clic droit = drapeau.',
    code:
`import random

# Place les mines et compte les voisines pour chaque case.
TAILLE, NB_MINES = 8, 10
mines = set()
while len(mines) < NB_MINES:
    mines.add((random.randint(0, 7), random.randint(0, 7)))

def voisines(x, y):
    return sum((x + dx, y + dy) in mines
               for dx in (-1, 0, 1) for dy in (-1, 0, 1)
               if (dx, dy) != (0, 0))

print("Mines voisines de (0,0) :", voisines(0, 0))` }
];

let miniCur = null, miniCleanup = null;
let mgAnagramStreak = 0;   // série d'anagrammes réussies d'affilée (survit au changement de mot)

function miniRenderCards() {
  const wrap = document.getElementById('miniCards');
  if (!wrap) return;
  wrap.innerHTML = '';
  MINI_GAMES.forEach(g => {
    const card = document.createElement('div');
    card.className = 'fun-card';
    card.onclick = () => miniStart(g.id);
    // Pastille de score : médaille + record, ou « Essayé », ou « ▶ Jouer »
    const m = (typeof funMiniMedal === 'function') ? funMiniMedal(g.id) : null;
    const cfg = (typeof funMiniCfg === 'function') ? funMiniCfg(g.id) : null;
    const best = (typeof funMiniBest === 'function') ? funMiniBest(g.id) : null;
    const rec = (best !== null && cfg) ? funFmtScore(cfg, best) : '';
    let medal, cls = 'medal';
    if (m) { medal = (typeof MEDAL_EMOJI !== 'undefined' ? MEDAL_EMOJI[m] : '🏅') + ' Record : ' + rec; cls += ' m-' + m; }
    else if (rec) medal = '▶ Rejouer · record : ' + rec;
    else medal = '▶ Jouer';
    const goals = (typeof funMedalGoals === 'function') ? funMedalGoals(g.id) : '';
    card.innerHTML = '<div class="mg-icon">' + g.icon + '</div><h3>' + g.title +
      '</h3><p>' + g.desc + '</p>' +
      (goals ? '<div class="mg-goals">' + goals + '</div>' : '') +
      '<div class="' + cls + '">' + medal + '</div>';
    wrap.appendChild(card);
  });
}

function miniStart(id) {
  if (miniCleanup) { miniCleanup(); miniCleanup = null; }   // arrête le jeu précédent (timers, écouteurs)
  miniCur = MINI_GAMES.find(g => g.id === id);
  if (!miniCur) return;
  document.getElementById('miniTitle').innerHTML = '<span class="mg-title-icon">' + miniCur.icon + '</span>' + miniCur.title;
  const code = document.getElementById('miniCode');
  code.style.display = 'none'; code.textContent = miniCur.code;
  document.getElementById('miniCodeBtn').textContent = '📖 Voir le code Python';
  document.getElementById('miniPlay').style.display = 'block';
  const goals = document.getElementById('miniGoals');                        // objectifs médailles
  if (goals) goals.innerHTML = '<span class="mini-goals-lbl">Objectifs médailles</span>' +
    '<span class="mini-goals-chips">' + funMedalGoals(id) + '</span>';
  funMiniPlayed(id);                                                         // marque le jeu comme essayé
  miniCleanup = miniCur.init(document.getElementById('miniArea')) || null;   // init peut renvoyer un nettoyage
  document.getElementById('miniPlay').scrollIntoView({ behavior:'smooth', block:'start' });
}

function miniClose() {
  if (miniCleanup) { miniCleanup(); miniCleanup = null; }
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
      funMiniScore('guess', tries);
      popConfetti(document.getElementById('funConfetti'), document.querySelector('#panel-fun .fun-wrap'));
    }
    input.value = ''; input.focus();
  }
  area.querySelector('#mgGuessBtn').addEventListener('click', go);
  input.addEventListener('keydown', e => { if (e.key === 'Enter') go(); });
  input.focus();
}

// ── Jeu : Pierre-Feuille-Ciseaux (IA qui apprend tes habitudes) ──
function mgRPS(area) {
  let win = 0, lose = 0, streak = 0, best = 0;
  const choices = [['pierre', '🪨'], ['feuille', '📄'], ['ciseaux', '✂️']];
  const hist = [];   // historique des coups du joueur
  area.innerHTML =
    '<div class="mg-row">' +
    choices.map((c, i) => '<button class="hanoi-btn" data-i="' + i + '">' + c[1] + ' ' + c[0] + '</button>').join('') +
    '</div><div id="mgRpsMsg" class="mg-msg">L’ordi observe tes coups et tente de te contrer. Fais la plus longue série !</div>' +
    '<div id="mgRpsScore" class="mg-msg">Toi 0 / Ordi 0 · série 0 (record 0)</div>';
  const msg = area.querySelector('#mgRpsMsg'), sc = area.querySelector('#mgRpsScore');
  // Prédit le prochain coup du joueur (transition depuis le dernier coup, sinon fréquence)
  function predict() {
    if (hist.length < 3 || Math.random() < 0.18) return Math.floor(Math.random() * 3);
    const last = hist[hist.length - 1], trans = [0, 0, 0], freq = [0, 0, 0];
    for (let k = 0; k < hist.length; k++) { freq[hist[k]]++; if (k > 0 && hist[k - 1] === last) trans[hist[k]]++; }
    const pool = (trans[0] + trans[1] + trans[2]) > 0 ? trans : freq;
    let p = 0; for (let i = 1; i < 3; i++) if (pool[i] > pool[p]) p = i;
    return p;
  }
  area.querySelectorAll('[data-i]').forEach(b => b.addEventListener('click', () => {
    const me = parseInt(b.dataset.i, 10);
    const ai = (predict() + 1) % 3;          // joue le coup qui bat la prédiction
    let r;
    if (me === ai) { r = 'Égalité !'; streak = 0; }
    else if ((me + 2) % 3 === ai) { r = 'Gagné ! 🎉'; win++; streak++; if (streak > best) best = streak; funMiniScore('rps', best); }
    else { r = 'Perdu… 😅'; lose++; streak = 0; }
    hist.push(me);
    msg.textContent = 'Toi ' + choices[me][1] + '  vs  ' + choices[ai][1] + ' Ordi  →  ' + r;
    sc.textContent = 'Toi ' + win + ' / Ordi ' + lose + ' · série ' + streak + ' (record ' + best + ')';
  }));
}

// ── Jeu : Morpion (vs IA réglable : Facile / Moyen / Imbattable par minimax) ──
function mgTTT(area) {
  const LEVELS = [['facile', 'Facile'], ['moyen', 'Moyen'], ['imbattable', 'Imbattable']];
  const LVALUE = { facile: 1, moyen: 2, imbattable: 3 };
  const labelOf = l => ({ facile: 'Facile', moyen: 'Moyen', imbattable: 'Imbattable' }[l]);
  let board = Array(9).fill(''), over = false, level = 'moyen';
  area.innerHTML =
    '<div class="mg-row" id="tttLvl">' +
      LEVELS.map(l => '<button class="hanoi-btn" data-l="' + l[0] + '">' + l[1] + '</button>').join('') +
    '</div>' +
    '<div id="mgTTT" class="mg-ttt"></div>' +
    '<div id="mgTTTmsg" class="mg-msg">À toi (❌). Clique une case.</div>' +
    '<button class="hanoi-btn" id="mgTTTreset" style="margin-top:10px">↺ Rejouer</button>';
  const grid = area.querySelector('#mgTTT'), msg = area.querySelector('#mgTTTmsg');
  const L = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]];
  const wins = (b, p) => L.some(l => l.every(i => b[i] === p));
  const full = b => b.every(x => x);
  const free = () => board.map((v, i) => v ? -1 : i).filter(i => i >= 0);
  // Minimax : ⭕ (l'ordi) maximise, ❌ (le joueur) minimise. Jeu parfait.
  function minimax(b, player) {
    if (wins(b, '⭕')) return { score: 1 };
    if (wins(b, '❌')) return { score: -1 };
    if (full(b)) return { score: 0 };
    let bestMove = -1, bestScore = player === '⭕' ? -2 : 2;
    for (let i = 0; i < 9; i++) if (!b[i]) {
      b[i] = player;
      const s = minimax(b, player === '⭕' ? '❌' : '⭕').score;
      b[i] = '';
      if (player === '⭕' ? s > bestScore : s < bestScore) { bestScore = s; bestMove = i; }
    }
    return { score: bestScore, move: bestMove };
  }
  function aiMove() {
    const f = free();
    if (level === 'facile') return f[Math.floor(Math.random() * f.length)];          // hasard
    if (level === 'moyen' && Math.random() < 0.45) return f[Math.floor(Math.random() * f.length)]; // erreurs
    return minimax(board.slice(), '⭕').move;                                          // parfait
  }
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
    if (wins(board, '❌')) { msg.textContent = '🎉 Tu as gagné (' + labelOf(level) + ') !'; over = true; funMiniScore('ttt', LVALUE[level]); draw(); return; }
    if (full(board)) { msg.textContent = 'Match nul !'; over = true; draw(); return; }
    const mv = aiMove(); if (mv >= 0) board[mv] = '⭕';
    if (wins(board, '⭕')) { msg.textContent = 'L’ordi gagne… 😅'; over = true; }
    else if (full(board)) msg.textContent = 'Match nul !';
    draw();
  }
  function resetGame() { board = Array(9).fill(''); over = false; msg.textContent = 'À toi (❌) — niveau ' + labelOf(level) + '.'; draw(); }
  function setLevel(l) {
    level = l;
    area.querySelectorAll('#tttLvl [data-l]').forEach(b =>
      b.style.boxShadow = b.dataset.l === l ? '0 0 0 2px #58a6ff inset' : '');
    resetGame();
  }
  area.querySelectorAll('#tttLvl [data-l]').forEach(b => b.addEventListener('click', () => setLevel(b.dataset.l)));
  area.querySelector('#mgTTTreset').addEventListener('click', resetGame);
  setLevel('moyen');
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
      m.textContent = '🎉 Gagné ! Le mot était ' + word + ' (' + lives + ' vies restantes)';
      funMiniScore('hangman', lives);
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
    if (b.dataset.o === correct(n)) { score++; msg.textContent = '✅ Correct !'; funMiniScore('fizzbuzz', score); }
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
    if (v === a * b) { score++; msg.textContent = '✅ Bravo !'; funMiniScore('times', score); }
    else { msg.textContent = '❌ Non, ' + a + ' × ' + b + ' = ' + (a * b); score = 0; }
    sc.textContent = 'Bonnes réponses d’affilée : ' + score;
    inp.value = ''; inp.focus(); nextQ();
  }
  area.querySelector('#tqBtn').addEventListener('click', go);
  inp.addEventListener('keydown', e => { if (e.key === 'Enter') go(); });
  nextQ(); inp.focus();
}

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
    if (pos === seq.length) { accepting = false; funMiniScore('simon', level); addStep(); setTimeout(playSeq, 550); }
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
      funMiniScore('reflex', ms);
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
        if (matched.length === deck.length) { msg.textContent = '🎉 Gagné en ' + moves + ' coups !'; funBoom(); funMiniScore('memory', moves); }
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
      funMiniScore('quiz', score);
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
    if (fb[0] === N) { over = true; msg.textContent = '🎉 Code trouvé en ' + rows + ' essais !'; funBoom(); funMiniScore('mastermind', rows); }
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
    if (inp.value.trim().toUpperCase() === word) {
      mgAnagramStreak++;
      msg.textContent = '🎉 Bravo, c’était ' + word + ' ! (série : ' + mgAnagramStreak + ') — clique « Autre mot »';
      funBoom(); funMiniScore('anagram', mgAnagramStreak);
    } else { mgAnagramStreak = 0; msg.textContent = '❌ Pas encore… essaie encore.'; }
  }
  area.querySelector('#anOk').addEventListener('click', check);
  inp.addEventListener('keydown', e => { if (e.key === 'Enter') check(); });
  area.querySelector('#anNew').addEventListener('click', () => mgAnagram(area));
  inp.focus();
}

// ── Jeu : Snake (renvoie une fonction de nettoyage) ──
function mgSnake(area) {
  area.innerHTML =
    '<canvas id="snk" width="320" height="320" style="background:#0d1117;border:1px solid #30363d;border-radius:8px"></canvas>' +
    '<div id="snkMsg" class="mg-msg">Flèches du clavier pour bouger. Mange les pommes !</div>';
  const ctx = area.querySelector('#snk').getContext('2d'), msg = area.querySelector('#snkMsg');
  const N = 20, S = 16;
  let snake, dir, nextDir, apple, dead;
  function spawn() { let p; do { p = { x: Math.floor(Math.random() * N), y: Math.floor(Math.random() * N) }; } while (snake && snake.some(s => s.x === p.x && s.y === p.y)); return p; }
  function reset() { snake = [{ x: 10, y: 10 }]; dir = { x: 1, y: 0 }; nextDir = dir; apple = spawn(); dead = false; msg.textContent = 'Score : 0'; }
  function key(e) {
    const k = e.key;
    if (k === 'ArrowUp' && dir.y === 0) nextDir = { x: 0, y: -1 };
    else if (k === 'ArrowDown' && dir.y === 0) nextDir = { x: 0, y: 1 };
    else if (k === 'ArrowLeft' && dir.x === 0) nextDir = { x: -1, y: 0 };
    else if (k === 'ArrowRight' && dir.x === 0) nextDir = { x: 1, y: 0 };
    else if (dead && (k === ' ' || k === 'Enter')) { reset(); draw(); return; }
    else return;
    e.preventDefault();
  }
  function step() {
    if (dead) return;
    dir = nextDir;
    const head = { x: snake[0].x + dir.x, y: snake[0].y + dir.y };
    if (head.x < 0 || head.x >= N || head.y < 0 || head.y >= N || snake.some(s => s.x === head.x && s.y === head.y)) {
      dead = true; msg.textContent = '💀 Perdu ! Score : ' + (snake.length - 1) + ' — Espace pour rejouer'; funMiniScore('snake', snake.length - 1); return;
    }
    snake.unshift(head);
    if (head.x === apple.x && head.y === apple.y) { apple = spawn(); msg.textContent = 'Score : ' + (snake.length - 1); funMiniScore('snake', snake.length - 1); }
    else snake.pop();
    draw();
  }
  function draw() {
    ctx.clearRect(0, 0, 320, 320);
    ctx.fillStyle = '#e04646'; ctx.fillRect(apple.x * S + 2, apple.y * S + 2, S - 4, S - 4);
    snake.forEach((s, i) => { ctx.fillStyle = i === 0 ? '#7ee787' : '#50b450'; ctx.fillRect(s.x * S + 1, s.y * S + 1, S - 2, S - 2); });
  }
  document.addEventListener('keydown', key);
  reset(); draw();
  const timer = setInterval(step, 110);
  return () => { clearInterval(timer); document.removeEventListener('keydown', key); };
}

// ── Jeu : 2048 (renvoie une fonction de nettoyage) ──
function mg2048(area) {
  const COL = { 2:'#3c4a5e', 4:'#3f5a78', 8:'#e68c32', 16:'#e0762e', 32:'#e0562e', 64:'#e04646', 128:'#d2c332', 256:'#d2b820', 512:'#c7a90f', 1024:'#50b450', 2048:'#2ea043' };
  area.innerHTML =
    '<div id="g2grid" style="display:grid;grid-template-columns:repeat(4,64px);gap:8px;background:#161c2a;padding:8px;border-radius:8px;width:max-content"></div>' +
    '<div id="g2msg" class="mg-msg">Flèches pour fusionner. Objectif : 2048 !</div>' +
    '<button class="hanoi-btn" id="g2reset" style="margin-top:10px">↺ Rejouer</button>';
  const gridEl = area.querySelector('#g2grid'), msg = area.querySelector('#g2msg');
  let grid;
  function reset() { grid = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]; add(); add(); msg.textContent = 'Objectif : 2048 !'; draw(); }
  function add() { const free = []; for (let r = 0; r < 4; r++) for (let c = 0; c < 4; c++) if (!grid[r][c]) free.push([r, c]); if (!free.length) return; const [r, c] = free[Math.floor(Math.random() * free.length)]; grid[r][c] = Math.random() < 0.9 ? 2 : 4; }
  function draw() {
    gridEl.innerHTML = '';
    for (let r = 0; r < 4; r++) for (let c = 0; c < 4; c++) {
      const v = grid[r][c], cell = document.createElement('div');
      cell.style.cssText = 'width:64px;height:64px;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:' + (v >= 1024 ? 18 : 22) + 'px;border-radius:6px;color:#fff;background:' + (v ? (COL[v] || '#2ea043') : '#0d1117');
      cell.textContent = v || '';
      gridEl.appendChild(cell);
    }
  }
  function compact(row) { const n = row.filter(x => x); for (let i = 0; i < n.length - 1; i++) if (n[i] === n[i + 1]) { n[i] *= 2; n.splice(i + 1, 1); } while (n.length < 4) n.push(0); return n; }
  function rotate(g) { const r = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]; for (let i = 0; i < 4; i++) for (let j = 0; j < 4; j++) r[j][3 - i] = g[i][j]; return r; }
  function move(k) {
    let rot = { ArrowLeft:0, ArrowDown:1, ArrowRight:2, ArrowUp:3 }[k];
    if (rot === undefined) return;
    let g = grid.map(r => r.slice());
    for (let i = 0; i < rot; i++) g = rotate(g);
    g = g.map(compact);
    for (let i = 0; i < (4 - rot) % 4; i++) g = rotate(g);
    if (JSON.stringify(g) !== JSON.stringify(grid)) { grid = g; add(); draw(); check(); }
  }
  function check() {
    let maxTile = 0;
    for (let r = 0; r < 4; r++) for (let c = 0; c < 4; c++) if (grid[r][c] > maxTile) maxTile = grid[r][c];
    funMiniScore('g2048', maxTile);
    if (maxTile >= 2048) { msg.textContent = '🎉 2048 atteint, bravo !'; funBoom(); return; }
    let can = false;
    for (let r = 0; r < 4; r++) for (let c = 0; c < 4; c++) { if (!grid[r][c]) can = true; if (c < 3 && grid[r][c] === grid[r][c + 1]) can = true; if (r < 3 && grid[r][c] === grid[r + 1][c]) can = true; }
    if (!can) msg.textContent = 'Plus aucun coup possible. (Rejouer)';
  }
  function key(e) { if (['ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].includes(e.key)) { e.preventDefault(); move(e.key); } }
  document.addEventListener('keydown', key);
  area.querySelector('#g2reset').addEventListener('click', reset);
  reset();
  return () => document.removeEventListener('keydown', key);
}

// ── Jeu : Démineur ──
function mgMines(area) {
  const N = 8, M = 10;
  let mines, revealed, flagged, over, startTime;
  area.innerHTML =
    '<div id="mnGrid" style="display:grid;grid-template-columns:repeat(8,34px);gap:3px"></div>' +
    '<div id="mnMsg" class="mg-msg">Clic = révéler · clic droit = drapeau.</div>' +
    '<button class="hanoi-btn" id="mnReset" style="margin-top:10px">↺ Rejouer</button>';
  const gridEl = area.querySelector('#mnGrid'), msg = area.querySelector('#mnMsg');
  const NUM_COL = ['', '#58a6ff', '#50b450', '#e68c32', '#e04646', '#d2c332', '#8c50c8', '#fff', '#fff'];
  function reset() { mines = new Set(); while (mines.size < M) mines.add(Math.floor(Math.random() * N * N)); revealed = new Set(); flagged = new Set(); over = false; startTime = Date.now(); msg.className = 'mg-msg'; msg.textContent = 'Clic = révéler · clic droit = drapeau.'; draw(); }
  function neighbors(i) { const x = i % N, y = Math.floor(i / N), out = []; for (let dx = -1; dx <= 1; dx++) for (let dy = -1; dy <= 1; dy++) { if (!dx && !dy) continue; const nx = x + dx, ny = y + dy; if (nx >= 0 && nx < N && ny >= 0 && ny < N) out.push(ny * N + nx); } return out; }
  function nb(i) { return neighbors(i).filter(j => mines.has(j)).length; }
  function reveal(i) { if (over || revealed.has(i) || flagged.has(i)) return; revealed.add(i); if (mines.has(i)) { over = true; return; } if (nb(i) === 0) neighbors(i).forEach(reveal); }
  function draw(showMines) {
    gridEl.innerHTML = '';
    for (let i = 0; i < N * N; i++) {
      const c = document.createElement('div'), r = revealed.has(i), f = flagged.has(i), mine = mines.has(i);
      c.style.cssText = 'width:34px;height:34px;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:15px;border-radius:5px;cursor:pointer;user-select:none;border:1px solid #30363d;color:#fff;background:' + (r ? '#0d1117' : '#2b3340');
      if (r && mine) { c.textContent = '✷'; c.style.color = '#e04646'; }
      else if (r) { const n = nb(i); if (n) { c.textContent = n; c.style.color = NUM_COL[n]; } }
      else if (f) { c.textContent = '⚑'; c.style.color = '#d2c332'; }
      else if (showMines && mine) { c.textContent = '✷'; c.style.color = '#e04646'; }
      c.addEventListener('click', () => {
        if (over || flagged.has(i)) return;
        reveal(i);
        if (mines.has(i)) { msg.className = 'mg-msg bad'; msg.textContent = '💥 Boum ! Perdu.'; draw(true); return; }
        if (revealed.size === N * N - M) { over = true; const secs = Math.round((Date.now() - startTime) / 1000); msg.className = 'mg-msg win'; msg.textContent = '🎉 Gagné en ' + secs + ' s !'; funBoom(); funMiniScore('mines', secs); }
        draw();
      });
      c.addEventListener('contextmenu', e => { e.preventDefault(); if (over || revealed.has(i)) return; flagged.has(i) ? flagged.delete(i) : flagged.add(i); draw(); });
      gridEl.appendChild(c);
    }
  }
  area.querySelector('#mnReset').addEventListener('click', reset);
  reset();
  return () => {};
}

// Init : cartes + révèle l'onglet s'il a déjà été débloqué.
// On attend le DOM : le panneau #panel-fun est inséré plus bas que ce script.
document.addEventListener('DOMContentLoaded', () => {
  funRenderCards();
  miniRenderCards();
  funRenderScore();
  try { if (localStorage.getItem('hanoi_fun_unlocked') === '1') revealFunTab(); } catch (e) {}
});
