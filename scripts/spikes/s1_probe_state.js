#!/usr/bin/env node
/**
 * ============================================================================
 *  DESECHABLE — Spike S1 (issue #27)
 * ============================================================================
 * Sonda de investigación para MAPEAR la forma real del objeto `state` que
 * expone `node-haxball` al reproducir una replay `.hbr2` (version 3).
 *
 * NO es código de producción. No se registra en package.json. Se ejecuta:
 *
 *   node scripts/spikes/s1_probe_state.js [ruta.hbr2] [frames=10]
 *
 * Hallazgos clave que esta sonda resuelve (acceptance criteria de #27):
 *   - el estado expone su API "amistosa" como GETTERS NO ENUMERABLES en el
 *     prototipo (Object.keys sólo ve los campos minificados internos), así que
 *     descubrimos los nombres con getOwnPropertyNames sobre la cadena de
 *     prototipos y evaluamos cada getter;
 *   - `setCurrentFrameNo` REPRODUCE hasta el frame destino vía el bucle de
 *     requestAnimationFrame; sin un RAF que avance, el reader se queda en el
 *     frame 0. Aquí controlamos un RAF manual con reloj virtual ("pump") para
 *     avanzar de forma determinista y sincrónica.
 * ============================================================================
 */

'use strict';

const fs = require('fs');
const path = require('path');
const os = require('os');

// ---------------------------------------------------------------------------
// Args
// ---------------------------------------------------------------------------
const DEFAULT_REPLAY = path.join(
  __dirname, '..', '..',
  'src', 'tests', 'fixtures', 'actions', 'HBReplay-2026-04-28-23h50m.hbr2'
);
const replayPath = process.argv[2] || DEFAULT_REPLAY;
const numSamples = parseInt(process.argv[3], 10) || 10;

if (!fs.existsSync(replayPath)) {
  console.error(`Replay no encontrada: ${replayPath}`);
  process.exit(1);
}
console.log(`Replay: ${replayPath}`);
const bytes = new Uint8Array(fs.readFileSync(replayPath));

// ---------------------------------------------------------------------------
// Introspección que VE getters no enumerables del prototipo
// ---------------------------------------------------------------------------
function protoProps(obj) {
  const names = new Set();
  let o = obj;
  while (o && o !== Object.prototype && o !== Array.prototype) {
    for (const k of Object.getOwnPropertyNames(o)) {
      if (k === 'constructor') continue;
      names.add(k);
    }
    o = Object.getPrototypeOf(o);
  }
  return [...names];
}

// Evalúa cada propiedad "amistosa" de forma segura, devolviendo escalares /
// resúmenes (no recursivo profundo) para inspección humana.
function friendlyView(obj) {
  if (obj == null || typeof obj !== 'object') return obj;
  const out = {};
  for (const k of protoProps(obj)) {
    let v;
    try { v = obj[k]; } catch (_) { out[k] = '[throws]'; continue; }
    const t = typeof v;
    if (t === 'function') continue;
    if (v == null || t === 'number' || t === 'string' || t === 'boolean') {
      out[k] = v;
    } else if (Array.isArray(v)) {
      out[k] = `[array len=${v.length}]`;
    } else if (t === 'object') {
      out[k] = '[object]';
    }
  }
  return out;
}

// ---------------------------------------------------------------------------
// node-haxball: el módulo se invoca como función para obtener la API.
// ---------------------------------------------------------------------------
const API = require('node-haxball')();
const { Replay } = API;

const dump = { replay: path.basename(replayPath), readAll: null, discovery: {}, samples: [] };

// ---------------------------------------------------------------------------
// 1) readAll -> ReplayData estática (cross-check + totalFrames + goles)
// ---------------------------------------------------------------------------
const data = Replay.readAll(bytes);
const goalMarkers = data.goalMarkers || [];
dump.readAll = {
  version: data.version,
  totalFrames: data.totalFrames,
  numGoalMarkers: goalMarkers.length,
  goalMarkers: goalMarkers.map((g) => friendlyView(g)),
  numEvents: (data.events || []).length,
};
console.log('\n=== readAll ===');
console.log(JSON.stringify(dump.readAll, null, 2));

// ---------------------------------------------------------------------------
// 2) read -> reader, con RAF manual controlado ("pump") y reloj virtual.
// ---------------------------------------------------------------------------
let pendingCb = null;
let vclock = 0;
const raf = (cb) => { pendingCb = cb; return 1; };
const cancel = () => { pendingCb = null; };

const reader = Replay.read(bytes, {}, {
  requestAnimationFrame: raf,
  cancelAnimationFrame: cancel,
});

const STEP_MS = 2000;            // avance de reloj virtual por tick
const MAX_TICKS = 2000000;       // tope de seguridad

function pumpToFrame(target) {
  let ticks = 0;
  reader.setCurrentFrameNo(target);
  while (pendingCb && reader.getCurrentFrameNo() < target && ticks < MAX_TICKS) {
    const cb = pendingCb;
    pendingCb = null;
    vclock += STEP_MS;
    cb(vclock);
    ticks++;
  }
  return ticks;
}

const maxFrame = reader.maxFrameNo;
console.log('\n=== reader ===');
console.log('reader props:', protoProps(reader).join(', '));
console.log('maxFrameNo:', maxFrame, ' length(ms):', reader.length());

// ---------------------------------------------------------------------------
// 3) Descubrimiento de la forma del estado en un frame de juego activo
// ---------------------------------------------------------------------------
const midFrame = Math.round(maxFrame * 0.6);
pumpToFrame(midFrame);

const state = reader.state;
const gs = reader.gameState;
dump.discovery.atFrame = reader.getCurrentFrameNo();
dump.discovery.stateProps = state ? protoProps(state) : null;
dump.discovery.gameStateProps = gs ? protoProps(gs) : null;

// localizar la colección de discos: probamos rutas candidatas
function findDiscs(st, g) {
  const candidates = [];
  if (st && Array.isArray(st.discs)) candidates.push(['state.discs', st.discs]);
  if (st && st.physicsState && Array.isArray(st.physicsState.discs)) candidates.push(['state.physicsState.discs', st.physicsState.discs]);
  if (g && Array.isArray(g.discs)) candidates.push(['gameState.discs', g.discs]);
  if (g && g.physicsState && Array.isArray(g.physicsState.discs)) candidates.push(['gameState.physicsState.discs', g.physicsState.discs]);
  return candidates;
}
const discCandidates = findDiscs(state, gs);
dump.discovery.discPaths = discCandidates.map(([p, a]) => `${p} (len=${a.length})`);

const players = (state && state.players) || (gs && gs.players) || [];
dump.discovery.numPlayers = players.length;
dump.discovery.playerSample = players.length ? friendlyView(players.find((p) => p) || players[0]) : null;

let discArr = discCandidates.length ? discCandidates[0][1] : [];
dump.discovery.discPathUsed = discCandidates.length ? discCandidates[0][0] : null;
dump.discovery.ballSample = discArr.length ? friendlyView(discArr[0]) : null;

// disc -> player: el enlace es disc.playerId (player.disc es null en el reader)
dump.discovery.discPlayerMap = discArr.map((d, i) => ({
  index: i,
  playerId: safe(() => d.playerId),
  pos: discPos(d),
  radius: safe(() => d.radius),
  color: safe(() => d.color),
})).filter((d) => d.playerId != null);

// equipos: volcamos el objeto team de un jugador en cancha (team != 0)
const onField = players.find((p) => safe(() => p.team && (p.team.id || p.team)) ) || null;
dump.discovery.teamObject = onField ? friendlyView(onField.team) : null;
dump.discovery.onFieldPlayers = players
  .map((p) => ({ id: safe(() => p.id), name: safe(() => p.name), teamId: safe(() => p.team && (p.team.id != null ? p.team.id : p.team)) }))
  .filter((p) => p.teamId);

// estadio: límites para anclar la escala de x/y
const stadium = (state && state.stadium) || (gs && gs.stadium) || null;
dump.discovery.stadium = stadium ? friendlyView(stadium) : null;

console.log('\n=== discovery @frame', dump.discovery.atFrame, '===');
console.log('stateProps:', JSON.stringify(dump.discovery.stateProps));
console.log('gameStateProps:', JSON.stringify(dump.discovery.gameStateProps));
console.log('discPaths:', JSON.stringify(dump.discovery.discPaths));
console.log('ball (disc[0]) friendly:', JSON.stringify(dump.discovery.ballSample, null, 2));
console.log('disc->player map (playerId!=null):', JSON.stringify(dump.discovery.discPlayerMap, null, 2));
console.log('team object:', JSON.stringify(dump.discovery.teamObject, null, 2));
console.log('on-field players:', JSON.stringify(dump.discovery.onFieldPlayers));
console.log('stadium:', JSON.stringify(dump.discovery.stadium, null, 2));

// ---------------------------------------------------------------------------
// 4) Muestreo temporal: posiciones de balón + discos de jugador
// ---------------------------------------------------------------------------
function discPos(disc) {
  if (!disc) return null;
  // candidatos comunes: .pos {x,y} | .pos [x,y] | .x/.y
  const pos = disc.pos;
  if (pos && typeof pos === 'object') {
    if (Array.isArray(pos)) return { x: pos[0], y: pos[1] };
    if ('x' in pos || 'y' in pos) return { x: pos.x, y: pos.y };
  }
  if ('x' in disc || 'y' in disc) return { x: disc.x, y: disc.y };
  return null;
}
function discVel(disc) {
  const sp = disc && disc.speed;
  if (sp && typeof sp === 'object') {
    if (Array.isArray(sp)) return { x: sp[0], y: sp[1] };
    return { x: sp.x, y: sp.y };
  }
  return null;
}

const targets = [];
for (let i = 0; i < numSamples; i++) targets.push(Math.round((maxFrame * i) / (numSamples - 1)));
const sampleFrames = Array.from(new Set(targets)).sort((a, b) => a - b);

console.log('\n=== muestras temporales ===');
for (const f of sampleFrames) {
  pumpToFrame(f);
  const st = reader.state;
  const g = reader.gameState;
  const cands = findDiscs(st, g);
  const discs = cands.length ? cands[0][1] : [];
  const ps = (st && st.players) || [];
  const sample = {
    requestedFrame: f,
    currentFrame: reader.getCurrentFrameNo(),
    numDiscs: discs.length,
    ball: discs.length ? { pos: discPos(discs[0]), vel: discVel(discs[0]) } : null,
    players: ps.map((p) => {
      let pd = null;
      try { pd = p.disc; } catch (_) {}
      return {
        id: safe(() => p.id),
        name: safe(() => p.name),
        team: safe(() => p.team && (p.team.id != null ? p.team.id : p.team)),
        discId: safe(() => p.disc && (p.disc.id != null ? p.disc.id : null)),
        pos: pd ? discPos(pd) : null,
      };
    }),
    score: g ? { red: safe(() => g.redScore), blue: safe(() => g.blueScore), time: safe(() => g.timeElapsed != null ? g.timeElapsed : g.time) } : null,
  };
  dump.samples.push(sample);
  console.log(`\n--- frame ${f} (cur=${sample.currentFrame}) discs=${sample.numDiscs} score=${JSON.stringify(sample.score)}`);
  console.log('  ball:', JSON.stringify(sample.ball));
  if (sample.players[0]) console.log('  player[0]:', JSON.stringify(sample.players[0]));
}

function safe(fn) { try { return fn(); } catch (_) { return undefined; } }

// ---------------------------------------------------------------------------
// Volcado JSON crudo
// ---------------------------------------------------------------------------
const outPath = path.join(os.tmpdir(), 's1-state-dump.json');
fs.writeFileSync(outPath, JSON.stringify(dump, null, 2));
console.log(`\nJSON crudo: ${outPath}`);

try { reader.destroy(); } catch (_) {}
