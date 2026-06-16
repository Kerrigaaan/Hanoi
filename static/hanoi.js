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
