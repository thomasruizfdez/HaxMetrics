#!/usr/bin/env node
/**
 * ============================================================================
 *  DESECHABLE — Spike S3 (issue #29)
 * ============================================================================
 * Sonda de investigación para averiguar qué contiene `Replay.readAll(bytes).events[]`
 * en node-haxball@2.3.0: ¿trae el autor de un gol? ¿eventos de join/leave/team_change?
 *
 * NO es código de producción. No se registra en package.json. Se ejecuta:
 *
 *   node scripts/spikes/s3_probe_events.js
 *
 * Estrategia:
 *   1) Corre sobre las 14 replays reales del corpus y sobre las replays sintéticas
 *      de un solo tipo de acción (player_joined_action.hbr2, player_left_action.hbr2,
 *      player_team_changed_action.hbr2) usadas por el parser Python deprecado —
 *      si node-haxball puede leerlas, son la señal más directa posible.
 *   2) Descubre el discriminador de `events[]` (kind/type) y sus valores.
 *   3) Cruza eventos cuyo frameNo caiga cerca de un goalMarker.frameNo conocido.
 * ============================================================================
 */

'use strict';

const fs = require('fs');
const path = require('path');
const os = require('os');

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
      out[k] = friendlyViewShallow(v);
    }
  }
  return out;
}

function friendlyViewShallow(obj) {
  if (obj == null || typeof obj !== 'object') return obj;
  const out = {};
  for (const k of protoProps(obj)) {
    let v;
    try { v = obj[k]; } catch (_) { continue; }
    const t = typeof v;
    if (t === 'function') continue;
    if (v == null || t === 'number' || t === 'string' || t === 'boolean') out[k] = v;
    else if (Array.isArray(v)) out[k] = `[array len=${v.length}]`;
    else if (t === 'object') out[k] = '[object]';
  }
  return out;
}

const ACTIONS_DIR = path.join(__dirname, '..', '..', 'src', 'tests', 'fixtures', 'actions');

const CORPUS = [
  'HBReplay-2025-12-22-22h17m.hbr2', 'HBReplay-2025-12-22-22h49m.hbr2',
  'HBReplay-2025-12-22-23h43m.hbr2', 'HBReplay-2026-01-08-22h58m.hbr2',
  'HBReplay-2026-01-09-22h08m.hbr2', 'HBReplay-2026-01-09-22h17m.hbr2',
  'HBReplay-2026-01-11-23h03m.hbr2', 'HBReplay-2026-01-18-22h42m.hbr2',
  'HBReplay-2026-03-24-22h52m.hbr2', 'HBReplay-2026-03-24-23h13m.hbr2',
  'HBReplay-2026-03-24-23h30m.hbr2', 'HBReplay-2026-04-16-22h49m.hbr2',
  'HBReplay-2026-04-27-22h33m.hbr2', 'HBReplay-2026-04-28-23h50m.hbr2',
];

const TARGETED = [
  'player_joined_action.hbr2',
  'player_left_action.hbr2',
  'player_team_changed_action.hbr2',
  'match_started_action.hbr2',
  'match_stopped_action.hbr2',
];

const API = require('node-haxball')();
const { Replay } = API;

const report = { corpus: [], targeted: [] };

function probe(filename) {
  const p = path.join(ACTIONS_DIR, filename);
  if (!fs.existsSync(p)) return { filename, error: 'not found' };
  const bytes = new Uint8Array(fs.readFileSync(p));
  let data;
  try {
    data = Replay.readAll(bytes);
  } catch (e) {
    return { filename, error: `readAll threw: ${e.message}` };
  }
  const events = data.events || [];
  const kinds = new Set(events.map((e) => e.kind ?? e.type ?? '[no kind/type field]'));
  const goalMarkers = (data.goalMarkers || []).map((g) => friendlyView(g));
  const eventSamples = events.slice(0, 5).map((e) => friendlyView(e));

  // Cruce: eventos cerca de cada goalMarker.frameNo (+/- 5 frames)
  const nearGoals = [];
  for (const g of data.goalMarkers || []) {
    const near = events.filter((e) => {
      const fn = e.frameNo ?? e.frame_no ?? e.frame;
      return fn != null && Math.abs(fn - g.frameNo) <= 5;
    }).map((e) => friendlyView(e));
    nearGoals.push({ goalFrameNo: g.frameNo, teamId: g.teamId, nearbyEvents: near });
  }

  return {
    filename,
    version: data.version,
    totalFrames: data.totalFrames,
    numEvents: events.length,
    eventKinds: [...kinds],
    goalMarkers,
    eventSamples,
    nearGoals,
  };
}

console.log('=== Corpus (14 replays reales) ===');
for (const f of CORPUS) {
  const r = probe(f);
  report.corpus.push(r);
  console.log(`\n--- ${f} ---`);
  console.log(JSON.stringify(r, null, 2));
}

console.log('\n\n=== Fixtures sintéticas de un solo tipo de acción ===');
for (const f of TARGETED) {
  const r = probe(f);
  report.targeted.push(r);
  console.log(`\n--- ${f} ---`);
  console.log(JSON.stringify(r, null, 2));
}

const outPath = path.join(os.tmpdir(), 's3-events-dump.json');
fs.writeFileSync(outPath, JSON.stringify(report, null, 2));
console.log(`\nJSON crudo: ${outPath}`);
