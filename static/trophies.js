// Onglet « Défis Fun » — médailles, rangs et vitrine de trophées (#funScore).

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

// ── Suivi des mini-jeux : « essayé » + meilleur score → médaille ──
function lsGet(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }

function funMiniPlayed(id) { try { localStorage.setItem('hanoi_mp_' + id, '1'); } catch (e) {} funRenderScore(); }

// Config de score d'un mini-jeu (objet MG_SCORE défini dans minigames.js)
function funMiniCfg(id) { return (typeof MG_SCORE !== 'undefined' && MG_SCORE[id]) || null; }

// Meilleur score enregistré (nombre) ou null
function funMiniBest(id) { const v = lsGet('hanoi_ms_' + id); return v === null ? null : Number(v); }

// Enregistre un résultat : garde le MEILLEUR selon la direction (haut/bas) du jeu
function funMiniScore(id, value) {
  const cfg = funMiniCfg(id);
  try {
    const cur = funMiniBest(id);
    let best = value;
    if (cur !== null && cfg) best = cfg.by === 'low' ? Math.min(cur, value) : Math.max(cur, value);
    localStorage.setItem('hanoi_ms_' + id, String(best));
    localStorage.setItem('hanoi_mp_' + id, '1');   // a forcément été joué
  } catch (e) {}
  funRenderScore();
  if (typeof miniRenderCards === 'function') miniRenderCards();
}

// Médaille obtenue ('gold'|'silver'|'bronze') ou null selon le meilleur score
function funMiniMedal(id) {
  const cfg = funMiniCfg(id); if (!cfg) return null;
  const b = funMiniBest(id); if (b === null) return null;
  if (cfg.by === 'low') return b <= cfg.gold ? 'gold' : b <= cfg.silver ? 'silver' : b <= cfg.bronze ? 'bronze' : null;
  return b >= cfg.gold ? 'gold' : b >= cfg.silver ? 'silver' : b >= cfg.bronze ? 'bronze' : null;
}

// Objectifs médailles d'un jeu, rendus en pastilles colorées (or/argent/bronze).
function funMedalGoals(id) {
  const cfg = funMiniCfg(id); if (!cfg) return '';
  const E = (typeof MEDAL_EMOJI !== 'undefined') ? MEDAL_EMOJI : { gold: '🥇', silver: '🥈', bronze: '🥉' };
  const chip = (cls, emoji, txt) => '<span class="goal-chip ' + cls + '">' + emoji + ' ' + txt + '</span>';
  if (cfg.names) {
    const clean = s => s.replace(' battu !', '').replace(' battu', '');
    return chip('g', E.gold, clean(cfg.names[3])) + chip('s', E.silver, clean(cfg.names[2])) +
           chip('b', E.bronze, clean(cfg.names[1]));
  }
  const op = cfg.by === 'low' ? '≤' : '≥';
  const unit = cfg.label ? '<span class="goal-unit">' + cfg.label + '</span>' : '';
  return chip('g', E.gold, op + cfg.gold) + chip('s', E.silver, op + cfg.silver) +
         chip('b', E.bronze, op + cfg.bronze) + unit;
}

// Affichage lisible d'un score (ex. « 7 essais », « 240 ms », « Imbattable »)
function funFmtScore(cfg, v) {
  if (!cfg) return String(v);
  if (cfg.names) return cfg.names[v] || ('niveau ' + v);
  return v + ' ' + cfg.label;
}

// Compat : ancien appel funMiniWon(id) → score « réussite » minimal
function funMiniWon(id) { funMiniScore(id, funMiniCfg(id) && funMiniCfg(id).by === 'low' ? (funMiniCfg(id).bronze) : (funMiniCfg(id) ? funMiniCfg(id).bronze : 1)); }

// ── Vitrine des trophées : anneau de progression, rang, stats, grille ──
// Cible (remplace l'emoji 🎯) — réutilisée pour le rang Novice et le poteau-objectif
const SVG_TARGET = '<svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="10" fill="#e04646"/><circle cx="12" cy="12" r="7" fill="#f4f6f8"/><circle cx="12" cy="12" r="4.2" fill="#e04646"/><circle cx="12" cy="12" r="1.6" fill="#f4f6f8"/></svg>';

// Icônes SVG des rangs (remplacent 🌱 🛡️ ⭐ 🔥 👑)
const SVG_SPROUT = '<svg viewBox="0 0 24 24" fill="none" stroke="#50b450" stroke-width="2" stroke-linecap="round"><path d="M12 21v-8"/><path d="M12 14c0-3-2-5-5-5 0 3 2 5 5 5z" fill="#50b450" stroke="none"/><path d="M12 12c0-3 2-5 5-5 0 3-2 5-5 5z" fill="#7ee787" stroke="none"/></svg>';

const SVG_SHIELD = '<svg viewBox="0 0 24 24" fill="none"><path d="M12 2l8 3v6c0 5-3.5 8.5-8 11-4.5-2.5-8-6-8-11V5z" fill="#3c82d2" stroke="#2a5ea0" stroke-width="1" stroke-linejoin="round"/><path d="M8.5 12l2.3 2.3L15.5 9.5" stroke="#fff" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/></svg>';

const SVG_STAR = '<svg viewBox="0 0 24 24" fill="#f2cc4b" stroke="#d2a90f" stroke-width="0.8" stroke-linejoin="round"><path d="M12 2l2.9 6.3 6.8.7-5 4.6 1.4 6.7L12 17.8 5.9 20.3l1.4-6.7-5-4.6 6.8-.7z"/></svg>';

const SVG_FLAME = '<svg viewBox="0 0 24 24" fill="none"><path d="M12 2c1 4 5 5 5 10a5 5 0 0 1-10 0c0-2 1-3 1-3 0 1 1 2 2 2 0-3-2-4 2-9z" fill="#e8732e" stroke="#c0431b" stroke-width="0.8" stroke-linejoin="round"/><path d="M12 13c1.6 0 2.6 1.2 2.6 2.8A2.6 2.6 0 0 1 12 18.4 2.3 2.3 0 0 1 9.9 16c0-1 .8-1.6.8-1.6 .2 1.6 1.3 1.5 1.3-1.4z" fill="#f2cc4b"/></svg>';

const SVG_CROWN = '<svg viewBox="0 0 24 24" fill="none"><path d="M3 8l3.6 4L12 5l5.4 7L21 8l-1.5 11h-15z" fill="#e9c83a" stroke="#b8941f" stroke-width="1" stroke-linejoin="round"/><circle cx="3" cy="8" r="1.6" fill="#e9c83a"/><circle cx="21" cy="8" r="1.6" fill="#e9c83a"/><circle cx="12" cy="4.6" r="1.6" fill="#e9c83a"/><rect x="5" y="18.4" width="14" height="2.2" rx="1" fill="#b8941f"/></svg>';

function funRank(pct) {
  const w = s => '<span class="tw-rank-ico">' + s + '</span>';
  if (pct >= 1)    return { name: 'Grand Maître',       icon: w(SVG_CROWN) };
  if (pct >= 0.85) return { name: 'Légende du Hanoï',   icon: w(SVG_FLAME) };
  if (pct >= 0.6)  return { name: 'Maître des Tours',   icon: w(SVG_STAR) };
  if (pct >= 0.33) return { name: 'Aventurier',         icon: w(SVG_SHIELD) };
  if (pct > 0)     return { name: 'Apprenti des Tours', icon: w(SVG_SPROUT) };
  return { name: 'Novice', icon: w(SVG_TARGET) };
}

function funTroph(icon, title, state, badge, tint, sub) {
  return '<div class="troph ' + state + (tint ? ' ' + tint : '') + '" title="' + title + '">' +
    '<div class="troph-badge">' + badge + '</div>' +
    '<div class="troph-icon">' + icon + '</div>' +
    '<div class="troph-name">' + title + '</div>' +
    '<div class="troph-sub">' + sub + '</div>' +
  '</div>';
}

function funRenderScore() {
  const box = document.getElementById('funScore');
  if (!box) return;

  let golds = 0, silvers = 0, bronzes = 0, points = 0, earned = 0;
  const chTrophies = FUN_CHALLENGES.map(c => {
    const m = funGetMedal(c.id);
    if (m) earned++;
    if (m === 'gold')   { golds++;   points += 3; }
    if (m === 'silver') { silvers++; points += 2; }
    if (m === 'bronze') { bronzes++; points += 1; }
    if (m) return funTroph(c.icon, c.title, 'earned', MEDAL_EMOJI[m], 'm-' + m,
                           m === 'gold' ? 'Médaille d’or' : (m === 'silver' ? 'Médaille d’argent' : 'Médaille de bronze'));
    return funTroph(c.icon, c.title, 'locked', '🔒', '', 'À décrocher');
  }).join('');

  let won = 0, played = 0;
  const miTrophies = MINI_GAMES.map(g => {
    const m = funMiniMedal(g.id), cfg = funMiniCfg(g.id), best = funMiniBest(g.id);
    const rec = (best !== null && cfg) ? funFmtScore(cfg, best) : '';
    if (m) {
      won++; earned++;
      if (m === 'gold')   { golds++;   points += 3; }
      if (m === 'silver') { silvers++; points += 2; }
      if (m === 'bronze') { bronzes++; points += 1; }
      return funTroph(g.icon, g.title, 'earned', MEDAL_EMOJI[m], 'm-' + m, 'Record : ' + rec);
    }
    if (lsGet('hanoi_mp_' + g.id)) { played++; return funTroph(g.icon, g.title, 'tried', '✓', '', rec ? 'Record : ' + rec : 'Essayé'); }
    return funTroph(g.icon, g.title, 'locked', '🔒', '', 'Pas encore joué');
  }).join('');

  const total = FUN_CHALLENGES.length + MINI_GAMES.length;
  const pct = total ? earned / total : 0;
  const rank = funRank(pct);
  const R = 34, CIRC = 2 * Math.PI * R, off = CIRC * (1 - pct);
  const ring =
    '<svg class="tw-ring" viewBox="0 0 80 80" width="84" height="84">' +
      '<circle class="tw-ring-bg" cx="40" cy="40" r="' + R + '"/>' +
      '<circle class="tw-ring-fg" cx="40" cy="40" r="' + R + '" ' +
        'stroke-dasharray="' + CIRC.toFixed(1) + '" stroke-dashoffset="' + off.toFixed(1) + '"/>' +
      '<text class="tw-ring-txt" x="40" y="46">' + Math.round(pct * 100) + '%</text>' +
    '</svg>';

  box.innerHTML =
    '<div class="tw-top">' + ring +
      '<div class="tw-rank">' +
        '<div class="tw-rank-name">' + rank.icon + ' ' + rank.name + '</div>' +
        '<div class="tw-rank-sub">' + earned + ' / ' + total + ' trophées · ' + points + ' points</div>' +
        '<div class="tw-stats">' +
          '<span class="tw-stat g">🥇 ' + golds + '</span>' +
          '<span class="tw-stat s">🥈 ' + silvers + '</span>' +
          '<span class="tw-stat b">🥉 ' + bronzes + '</span>' +
          '<span class="tw-stat w">🏆 ' + won + '</span>' +
          '<span class="tw-stat t">🎮 ' + played + '</span>' +
        '</div>' +
      '</div>' +
    '</div>' +
    '<div class="tw-cat">Défis Hanoï</div>' +
    '<div class="tw-grid">' + chTrophies + '</div>' +
    '<div class="tw-cat">Mini-jeux</div>' +
    '<div class="tw-grid">' + miTrophies + '</div>';
}
