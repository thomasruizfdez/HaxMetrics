#!/usr/bin/env node
// --- Polyfills mínimos para entorno Node ---
try {
  global.DOMException = global.DOMException || require('node-domexception');
} catch (_) {
  // si ya existe o no se puede cargar, seguimos; sólo es para Node antiguos / libs que lo requieren
}
globalThis.window ||= {};              // algunas libs miran "window"
globalThis.navigator ||= { userAgent: "node" };

// --- tu script real a partir de aquí ---
const fs = require("fs");
const path = require("path");

// IMPORTA node-haxball *DESPUÉS* de los polyfills
const Haxball = require("node-haxball");
const API = Haxball();
const { Replay } = API;

function parseArgs() {
  const args = process.argv.slice(2);
  if (args.length < 1) {
    console.error("Usage: node replay_to_json.js <replay.hbr2> [--out out/replay.json]");
    process.exit(2);
  }
  const inPath = args[0];
  let outPath = null;
  const i = args.indexOf("--out");
  if (i !== -1 && args[i + 1]) outPath = args[i + 1];
  return { inPath, outPath };
}

function ensureDirFor(filePath) {
  const dir = path.dirname(filePath);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

(function main() {
  const { inPath, outPath } = parseArgs();
  const raw = fs.readFileSync(inPath);
  const u8 = new Uint8Array(raw.buffer, raw.byteOffset, raw.byteLength);

  const replayData = Replay.readAll(u8);
  const out = {
    version: replayData.version,
    totalFrames: replayData.totalFrames,
    roomData: replayData.roomData,
    goalMarkers: replayData.goalMarkers,
    events: replayData.events
  };

  const json = JSON.stringify(out);
  if (outPath) {
    ensureDirFor(outPath);
    fs.writeFileSync(outPath, json);
    console.log(`Wrote ${outPath}`);
  } else {
    process.stdout.write(json);
  }
})();
