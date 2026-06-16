// Party-popper SVG (remplace l'emoji 🎉 dans le message de déblocage)
const SVG_PARTY = '<svg viewBox="0 0 24 24" fill="none"><path d="M3 21l5.5-11 5.5 5.5z" fill="#e68c32"/><path d="M3 21l5.5-11 2.6 2.6z" fill="#d2c332"/><circle cx="15.5" cy="6" r="1.3" fill="#e04646"/><circle cx="19.5" cy="9.5" r="1.3" fill="#3c82d2"/><circle cx="18" cy="4" r="1.1" fill="#50b450"/><circle cx="21" cy="13.5" r="1.1" fill="#8c50c8"/><path d="M14 9.5l2.2-2.2M16.5 12.5l2.4-1M13.2 6.5l1.4-2.6" stroke="#d2c332" stroke-width="1.3" stroke-linecap="round"/></svg>';

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

/* EXS est fourni par le bootstrap inline dans la page */

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
      <pre class="hl" id="hl${ex.id}" aria-hidden="true"><code></code></pre>
      <textarea id="c${ex.id}" spellcheck="false"
        oninput="hlUpdate('${ex.id}')" onscroll="hlSync('${ex.id}')"
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

// ── Coloration syntaxique Python (couche .hl sous le textarea) ──
function hlEscape(s) { return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
function hlPy(src) {
  // un seul passage : commentaires, chaînes, mots-clés, nombres
  const re = /(#[^\n]*)|("{3}[\s\S]*?"{3}|'{3}[\s\S]*?'{3}|"(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*')|\b(def|return|if|elif|else|for|while|in|and|or|not|yield|from|import|pass|break|continue|class|lambda|is|None|True|False|print|range|len)\b|\b(\d+\.?\d*)\b/g;
  let out = '', last = 0, m;
  while ((m = re.exec(src)) !== null) {
    out += hlEscape(src.slice(last, m.index));
    if (m[1]) out += '<span class="t-com">' + hlEscape(m[1]) + '</span>';
    else if (m[2]) out += '<span class="t-str">' + hlEscape(m[2]) + '</span>';
    else if (m[3]) out += '<span class="t-kw">' + hlEscape(m[3]) + '</span>';
    else if (m[4]) out += '<span class="t-num">' + hlEscape(m[4]) + '</span>';
    last = re.lastIndex;
  }
  out += hlEscape(src.slice(last));
  return out;
}
function hlUpdate(exId) {
  const ta = document.getElementById('c' + exId);
  const code = document.querySelector('#hl' + exId + ' code');
  if (!ta || !code) return;
  code.innerHTML = hlPy(ta.value) + '\n';   // saut de ligne final : la derniere ligne garde sa hauteur
}
function hlSync(exId) {
  const ta = document.getElementById('c' + exId), pre = document.getElementById('hl' + exId);
  if (ta && pre) { pre.scrollTop = ta.scrollTop; pre.scrollLeft = ta.scrollLeft; }
}

// applique l'auto-resize + restaure le code sauvegardé au chargement
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('textarea').forEach(ta => {
    const exId = ta.id.replace(/^c/, '');
    ta.value = loadCode(exId, ta.value);  // restaure si sauvegardé
    autoResize(ta);
    hlUpdate(exId);                        // colore le contenu initial
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
  hlUpdate(t.id.replace(/^c/, ''));   // re-colore après insertion de la tabulation
  saveCode(t.id.replace(/^c/, ''), t.value);
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
      const sm = document.getElementById('statusMsg');
      sm.className = 'ok';
      sm.innerHTML = '<span class="fun-ico-sm">' + SVG_PARTY + '</span> Exercice 5 réussi ! L\'onglet « Défis Fun » est débloqué !';
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
