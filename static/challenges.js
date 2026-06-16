// Onglet « Défis Fun » — moteur des 5 défis Hanoï (plateau, animation, glisser-déposer).
// Dépend de : trophies.js (médailles) et de popConfetti() (app/hanoi).

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
    lab.innerHTML = names[i] + (i === cfg.goal ? ' <span class="goal-ico">' + SVG_TARGET + '</span>' : '');
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
    funRenderScore();
  }
}

function funStartTimer() { if (!funTimer) { funT0 = Date.now(); funTimer = setInterval(funUpdateTime, 200); } }

function funStopTimer() { if (funTimer) { clearInterval(funTimer); funTimer = null; } }

function funUpdateTime() {
  const s = funT0 ? (Date.now() - funT0) / 1000 : 0;
  const el = document.getElementById('funTime'); if (el) el.textContent = '⏱ ' + s.toFixed(1) + 's';
}

const FUN_HOST = () => document.querySelector('#panel-fun .fun-wrap');

function funBoom() { popConfetti(document.getElementById('funConfetti'), FUN_HOST()); }
