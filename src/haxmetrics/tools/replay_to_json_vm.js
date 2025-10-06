#!/usr/bin/env node
/**
 * .hbr2 -> JSON usando la build web de node-haxball en un VM.
 * Carga UMDs de pako/json5/jszip ANTES de api.js para que existan
 * como variables globales reales (pako/JSON5/JSZip).
 *
 * Uso:
 *   node src/haxmetrics/tools/replay_to_json_vm.js "<ruta>\replay.hbr2" --out "src/out/replay.json"
 */
const fs = require("fs");
const path = require("path");
const vm = require("vm");

// ---------- Args ----------
const args = process.argv.slice(2);
if (args.length < 1) {
  console.error('Usage: node replay_to_json_vm.js <replay.hbr2> [--out out/replay.json]');
  process.exit(2);
}
const inPath = args[0];
let outPath = null;
const oi = args.indexOf("--out");
if (oi !== -1 && args[oi + 1]) outPath = args[oi + 1];

// ---------- Util ----------
function res(p) { return require.resolve(p); }
function resolveApiPath() {
  const candidates = ["node-haxball/src/api.js", "node-haxball/dist/api.js", "node-haxball/api.js"];
  for (const rel of candidates) { try { return require.resolve(rel); } catch {} }
  throw new Error("No pude localizar 'api.js' dentro de node-haxball (probé src/, dist/, api.js).");
}
const API_JS = resolveApiPath();

// ---------- “Navegador” mínimo + CommonJS simulado ----------
const sandbox = {
  console,
  setTimeout, clearTimeout, setInterval, clearInterval,

  // Forzar caminos simples en polyfills
  postMessage: undefined,
  MessageChannel: undefined,

  // DOM mínimo para que algunos bundles no fallen
  document: {
    createElement: (tag) => ({}), // sin onreadystatechange -> caerá a setTimeout
    documentElement: { appendChild: () => {}, removeChild: () => {} },
  },
  window: {},

  navigator: { userAgent: "node" },

  // CommonJS simulado (por si api.js lo usa)
  module: { exports: {} },
  exports: {},
};
sandbox.globalThis = sandbox;
sandbox.global = sandbox;

// ---------- Crear contexto VM (¡ANTES de usarlo!) ----------
const ctx = vm.createContext(sandbox);

// ---------- Cargar bundles UMD como variables globales ----------
// Desactiva CommonJS temporalmente para que los UMD creen 'var pako/JSON5/JSZip' en global.
const saveModule = ctx.module;
const saveExports = ctx.exports;

// En muchos UMD buscan 'self' o 'window' primero; asegúrate de que apuntan al global.
ctx.window = ctx;
ctx.self = ctx;

// Restaura CommonJS en el sandbox
ctx.module = saveModule;
ctx.exports = saveExports;

vm.runInContext(fs.readFileSync(require.resolve("json5/dist/index.min.js"), "utf8"), ctx, { filename: "json5.min.js" });
vm.runInContext(fs.readFileSync(require.resolve("pako/dist/pako.min.js"),  "utf8"), ctx, { filename: "pako.min.js"  });
vm.runInContext(fs.readFileSync(require.resolve("jszip/dist/jszip.min.js"), "utf8"), ctx, { filename: "jszip.min.js" });

// Sanity checks: deben existir variables globales reales
if (typeof ctx.pako === "undefined" || typeof ctx.pako.inflateRaw !== "function") {
  throw new Error("pako no quedó disponible como variable global con inflateRaw().");
}
if (typeof ctx.JSON5 === "undefined") {
  throw new Error("JSON5 no quedó disponible como variable global.");
}
if (typeof ctx.JSZip === "undefined") {
  throw new Error("JSZip no quedó disponible como variable global.");
}

// ---------- Cargar api.js de node-haxball en el MISMO contexto ----------
const apiSource = fs.readFileSync(API_JS, "utf8");
vm.runInContext(apiSource, ctx, { filename: path.basename(API_JS) });

// Recuperar factoría
let APIctor = null;
if (typeof ctx.module?.exports === "function") APIctor = ctx.module.exports;
else if (typeof ctx.exports === "function")    APIctor = ctx.exports;
else if (typeof ctx.abcHaxballAPI === "function") APIctor = ctx.abcHaxballAPI;
else if (typeof ctx.window?.abcHaxballAPI === "function") APIctor = ctx.window.abcHaxballAPI;
if (!APIctor) throw new Error("abcHaxballAPI no disponible tras cargar api.js.");

// Instanciar API (sin red; sólo Replay)
const API = APIctor(ctx.window, { JSON5: ctx.JSON5, pako: ctx.pako, JSZip: ctx.JSZip });
const { Replay } = API;
if (!Replay || typeof Replay.readAll !== "function") throw new Error("Replay.readAll no disponible.");

// ---------- Parseo ----------
const raw = fs.readFileSync(inPath);
const u8  = new Uint8Array(raw.buffer, raw.byteOffset, raw.byteLength);
const replayData = Replay.readAll(u8);

// ---------- Salida ----------
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
