#!/usr/bin/env node
/**
 * HaxMetrics extractor (S2 tracer bullet, issue #28).
 *
 * Re-simula una replay `.hbr2` con node-haxball y escribe Parquet en <outdir>:
 *   meta.parquet, events.parquet, players.parquet, frames.parquet
 *
 *   node scripts/extract_replay.js <replay.hbr2> <outdir>
 *   npm run extract -- <replay.hbr2> <outdir>
 *
 * Mapeo del estado: ver docs/spikes/s1-node-haxball-state.md
 *   - discos en gameState.physicsState.discs; balón = discs[0];
 *   - disco de jugador <=> disc.playerId; coordenadas disc.pos/.speed = {x,y};
 *   - equipo = player.team.id (0 spec / 1 rojo / 2 azul);
 *   - goalMarker.teamId = equipo que ENCAJA -> scoring_team = 3 - teamId.
 */

'use strict';

const fs = require('fs');
const path = require('path');
const parquet = require('@dsnp/parquetjs');

async function main() {
  const replayPath = process.argv[2];
  const outDir = process.argv[3];
  if (!replayPath || !outDir) {
    console.error('Usage: node scripts/extract_replay.js <replay.hbr2> <outdir>');
    process.exit(1);
  }
  if (!fs.existsSync(replayPath)) {
    console.error(`Replay not found: ${replayPath}`);
    process.exit(1);
  }
  fs.mkdirSync(outDir, { recursive: true });

  const bytes = new Uint8Array(fs.readFileSync(replayPath));
  const { Replay } = require('node-haxball')();

  // --- ReplayData estática: totalFrames + goles ---------------------------
  const data = Replay.readAll(bytes);
  if (data.version !== 3) {
    console.error(`Unsupported replay version: ${data.version} (expected 3)`);
    process.exit(1);
  }
  const goalMarkers = data.goalMarkers || [];

  // --- reader con RAF manual ("pump") para steppear determinista ----------
  let pendingCb = null;
  let vclock = 0;
  const reader = Replay.read(bytes, {}, {
    requestAnimationFrame: (cb) => { pendingCb = cb; return 1; },
    cancelAnimationFrame: () => { pendingCb = null; },
  });
  const STEP_MS = 2000;
  const MAX_TICKS = 5000000;
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
  }

  const maxFrame = reader.maxFrameNo;
  const durationMs = reader.length();

  // --- frames.parquet -----------------------------------------------------
  const framesSchema = new parquet.ParquetSchema({
    frame_no: { type: 'INT64' },
    object_kind: { type: 'UTF8' },
    object_id: { type: 'INT32', optional: true },
    x: { type: 'DOUBLE' },
    y: { type: 'DOUBLE' },
    vx: { type: 'DOUBLE' },
    vy: { type: 'DOUBLE' },
    radius: { type: 'DOUBLE' },
    kicking: { type: 'BOOLEAN' },
    input_bitmask: { type: 'INT32' },
    team: { type: 'INT32', optional: true },
  });
  const framesWriter = await parquet.ParquetWriter.openFile(
    framesSchema, path.join(outDir, 'frames.parquet'));

  // Goles marcados DURANTE la replay, contando incrementos del marcador.
  // El primer frame puede traer un marcador pre-existente (grabación iniciada
  // a mitad de partido): se toma como baseline y NO cuenta como gol. Entre
  // partidos el marcador se reinicia (descenso): los descensos se ignoran.
  let baseRed = null;
  let baseBlue = null;
  let prevRed = 0;
  let prevBlue = 0;
  let simRed = 0;
  let simBlue = 0;
  let lastRoster = [];
  let stadiumName = '';

  for (let f = 0; f <= maxFrame; f++) {
    pumpToFrame(f);
    const gs = reader.gameState;
    if (!gs) continue; // sin juego activo (antes del saque / fin de partido)

    if (baseRed === null) {
      baseRed = gs.redScore; baseBlue = gs.blueScore;
      prevRed = gs.redScore; prevBlue = gs.blueScore;
    }
    if (gs.redScore > prevRed) simRed += gs.redScore - prevRed;
    if (gs.blueScore > prevBlue) simBlue += gs.blueScore - prevBlue;
    prevRed = gs.redScore; prevBlue = gs.blueScore;

    const discs = (gs.physicsState && gs.physicsState.discs) || [];
    if (!discs.length) continue;

    const players = (reader.state && reader.state.players) || [];
    const teamById = new Map();
    const kickingById = new Map();
    const inputById = new Map();
    for (const p of players) {
      const tid = p.team ? p.team.id : 0;
      if (tid) { lastRoster = players; stadiumName = gs.stadium ? gs.stadium.name : stadiumName; }
      teamById.set(p.id, tid);
      kickingById.set(p.id, !!p.isKicking);
      inputById.set(p.id, p.input | 0);
    }

    // balón
    const ball = discs[0];
    await framesWriter.appendRow({
      frame_no: f, object_kind: 'ball',
      x: ball.pos.x, y: ball.pos.y, vx: ball.speed.x, vy: ball.speed.y,
      radius: ball.radius, kicking: false, input_bitmask: 0,
    });
    // discos de jugador
    for (const d of discs) {
      if (d.playerId == null) continue;
      await framesWriter.appendRow({
        frame_no: f, object_kind: 'player', object_id: d.playerId,
        x: d.pos.x, y: d.pos.y, vx: d.speed.x, vy: d.speed.y,
        radius: d.radius,
        kicking: kickingById.get(d.playerId) || false,
        input_bitmask: inputById.get(d.playerId) || 0,
        team: teamById.has(d.playerId) ? teamById.get(d.playerId) : undefined,
      });
    }
  }
  await framesWriter.close();

  // --- meta.parquet -------------------------------------------------------
  const metaSchema = new parquet.ParquetSchema({
    total_frames: { type: 'INT64' },
    duration_ms: { type: 'DOUBLE' },
    recorded_red: { type: 'INT32' },
    recorded_blue: { type: 'INT32' },
    initial_red: { type: 'INT32' },
    initial_blue: { type: 'INT32' },
    score_limit: { type: 'INT32' },
    time_limit: { type: 'INT32' },
    stadium_name: { type: 'UTF8' },
    num_players: { type: 'INT32' },
  });
  const metaWriter = await parquet.ParquetWriter.openFile(
    metaSchema, path.join(outDir, 'meta.parquet'));
  await metaWriter.appendRow({
    total_frames: data.totalFrames,
    duration_ms: durationMs,
    recorded_red: simRed,
    recorded_blue: simBlue,
    initial_red: baseRed || 0,
    initial_blue: baseBlue || 0,
    score_limit: (reader.state && reader.state.scoreLimit) | 0,
    time_limit: (reader.state && reader.state.timeLimit) | 0,
    stadium_name: stadiumName,
    num_players: lastRoster.length,
  });
  await metaWriter.close();

  // --- events.parquet (goles + start/stop) --------------------------------
  const eventsSchema = new parquet.ParquetSchema({
    frame_no: { type: 'INT64' },
    kind: { type: 'UTF8' },
    team_id: { type: 'INT32', optional: true },
    scoring_team: { type: 'INT32', optional: true },
  });
  const eventsWriter = await parquet.ParquetWriter.openFile(
    eventsSchema, path.join(outDir, 'events.parquet'));
  await eventsWriter.appendRow({ frame_no: 0, kind: 'start' });
  for (const g of goalMarkers) {
    await eventsWriter.appendRow({
      frame_no: g.frameNo, kind: 'goal',
      team_id: g.teamId, scoring_team: 3 - g.teamId,
    });
  }
  await eventsWriter.appendRow({ frame_no: maxFrame, kind: 'stop' });
  await eventsWriter.close();

  // --- players.parquet (roster) ------------------------------------------
  const playersSchema = new parquet.ParquetSchema({
    player_id: { type: 'INT32' },
    name: { type: 'UTF8' },
    team_id: { type: 'INT32' },
  });
  const playersWriter = await parquet.ParquetWriter.openFile(
    playersSchema, path.join(outDir, 'players.parquet'));
  for (const p of lastRoster) {
    await playersWriter.appendRow({
      player_id: p.id, name: p.name || '', team_id: p.team ? p.team.id : 0,
    });
  }
  await playersWriter.close();

  try { reader.destroy(); } catch (_) {}
  console.error(`extracted ${data.totalFrames} frames -> ${outDir} (goals ${simRed}-${simBlue}, initial ${baseRed || 0}-${baseBlue || 0})`);
}

main().catch((e) => {
  console.error('Extractor error:', e && e.message ? e.message : String(e));
  process.exit(1);
});
