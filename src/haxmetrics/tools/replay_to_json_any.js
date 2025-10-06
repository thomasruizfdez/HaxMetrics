#!/usr/bin/env node
/**
 * Convierte un .hbr2 a JSON usando la API de node-haxball, sea CJS, ESM o build web en VM.
 * Uso:
 *   node src/haxmetrics/tools/replay_to_json_any.js "<ruta>\replay.hbr2" --out "src/out/replay.json"
 */

const fs = require("fs");
const path = require("path");
const vm = require("vm");

const args = process.argv.slice(2);
if (args.length < 1) {
  console.error('Usage: node replay_to_json_any.js <replay.hbr2> [--out out/replay.json]');
  process.exit(2);
}
const inPath = args[0];
let outPath = null;
const i = args.indexOf("--out");
if (i !== -1 && args[i + 1]) outPath = args[i + 1];

globalThis.JSON5 = require("json5");
globalThis.pako  = require("pako");
globalThis.JSZip = require("jszip");

function resolveApiCandidates() {
  const candidates = [];
  const bases = ["node-haxball/src/api.js", "node-haxball/dist/api.js", "node-haxball/api.js"];
  for (const rel of bases) {
    try { candidates.push(require.resolve(rel)); } catch {}
  }
  if (candidates.length === 0) {
    throw new Error("No pude localizar api.js dentro de node-haxball (probé src/, dist/, api.js).");
  }
  return candidates;
}

function tryLoadCJS(apiPath) {
  try {
    const mod = require(apiPath);
    let fn = null;
    if (typeof mod === "function") fn = mod;
    else if (mod && typeof mod.default === "function") fn = mod.default;
    else if (mod && typeof mod.abcHaxballAPI === "function") fn = mod.abcHaxballAPI;
    return fn || null;
  } catch (e) {
    // Si es ESM o falla, devolvemos null para que otra estrategia lo intente
    return null;
  }
}

async function tryLoadESM(apiPath) {
  try {
    const mod = await import(apiPathToFileURL(apiPath));
    if (typeof mod.default === "function") return mod.default;
    if (typeof mod.abcHaxballAPI === "function") return mod.abcHaxballAPI;
  } catch (e) {}
  return null;
}

function apiPathToFileURL(p) {
  let u = path.resolve(p).replace(/\\/g, "/");
  if (!u.startsWith("/")) u = "/" + u;
  return "file://" + u;
}

function loadViaVM(apiPath) {
  // Cargamos el código y lo ejecutamos en un VM “navegador” con dependencias inyectadas
  const source = fs.readFileSync(apiPath, "utf8");
  const JSON5 = require("json5");
  const pako = require("pako");
  const JSZip = require("jszip");

  const sandbox = {
    window: {},
    document: {},
    navigator: { userAgent: "node" },
    console,
    setTimeout, clearTimeout, setInterval, clearInterval,
    JSON5, pako, JSZip,
  };
  sandbox.globalThis = sandbox;
  vm.createContext(sandbox);
  vm.runInContext(source, sandbox, { filename: path.basename(apiPath) });

  // Algunas versiones exponen abcHaxballAPI; otras ponen la función como export default y
  // la registran en window. Buscamos candidatos razonables:
  const fn = typeof sandbox.abcHaxballAPI === "function"
    ? sandbox.abcHaxballAPI
    : (typeof sandbox.window.abcHaxballAPI === "function"
        ? sandbox.window.abcHaxballAPI
        : null);

  if (!fn) {
    // Como último recurso, heurística: buscar en sandbox funciones cuyo nombre tenga 'Haxball'
    const keys = Object.keys(sandbox).filter(k => typeof sandbox[k] === "function");
    const guess = keys.find(k => /haxball/i.test(k));
    if (guess) return sandbox[guess];
    throw new Error("abcHaxballAPI no disponible tras VM. Versión del paquete distinta.");
  }
  return fn;
}

async function getAPIConstructor() {
  const candidates = resolveApiCandidates();

  // 1) CJS
  for (const p of candidates) {
    const fn = tryLoadCJS(p);
    if (fn) return fn;
  }
  // 2) ESM
  for (const p of candidates) {
    const fn = await tryLoadESM(p);
    if (fn) return fn;
  }
  // 3) VM web
  for (const p of candidates) {
    const fn = loadViaVM(p);
    if (fn) return fn;
  }
  throw new Error("No se pudo obtener la función de API de node-haxball.");
}

(async function main() {
  const APIctor = await getAPIConstructor();
  // Instanciar API: muchas versiones aceptan (window, options?)
  // No necesitamos red ni WebRTC; pasamos objeto vacío.
  const API = APIctor(globalThis.window || {}, {
    JSON5: globalThis.JSON5,
    pako:  globalThis.pako,
    JSZip: globalThis.JSZip,
  });
  const { Replay } = API;
  if (!Replay || typeof Replay.readAll !== "function") {
    throw new Error("Replay.readAll no disponible en la API de node-haxball.");
  }

  const raw = fs.readFileSync(inPath);
  const u8 = new Uint8Array(raw.buffer, raw.byteOffset, raw.byteLength);
  const replayData = Replay.readAll(u8);

  const out = {
    version: replayData.version,
    totalFrames: replayData.totalFrames,
    roomData: replayData.roomData,
    goalMarkers: replayData.goalMarkers,
    events: replayData.events,
  };

  const json = JSON.stringify(out);
  if (outPath) {
    const dir = path.dirname(outPath);
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(outPath, json);
    console.log(`Wrote ${outPath}`);
  } else {
    process.stdout.write(json);
  }
})().catch(err => {
  console.error(err.stack || String(err));
  process.exit(1);
});
