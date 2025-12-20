#!/usr/bin/env node
const fs = require('fs');
const vm = require('vm');
const path = require('path');
const pako = require('pako');

const replayData = fs.readFileSync(path.join(__dirname, '../src/replays/test_all_teams.hbr2'));

// Minimal sandbox
function createSandbox() {
  const sandbox = {
    console: console,
    Buffer: Buffer,
    Uint8Array: Uint8Array,
    Math: Math,
    Date: Date,
    Object: Object,
    Array: Array,
    pako: pako,
    window: {},
    performance: { now: () => Date.now() },
    setTimeout: setTimeout,
    clearTimeout: clearTimeout
  };
  
  sandbox.document = {
    createElement: () => ({
      getContext: () => ({ fillRect: () => {}, clearRect: () => {}, save: () => {}, restore: () => {} }),
      toDataURL: () => ''
    })
  };
  
  sandbox.window.document = sandbox.document;
  sandbox.window.performance = sandbox.performance;
  sandbox.window.localStorage = { getItem: () => null, setItem: () => {} };
  sandbox.ub = sandbox.window;
  
  return sandbox;
}

console.log('Loading decoder...');
const sandbox = createSandbox();

let replayScript = fs.readFileSync(path.join(__dirname, '../original_script/replay-min.js'), 'utf8');

const patchCode = `
  if (typeof ab !== 'undefined') ub.ab = ab;
  if (typeof ca !== 'undefined') ub.ca = ca;
`;

const pattern1 = /(\s+C\.cj\(\);)/;
replayScript = replayScript.replace(pattern1, patchCode + '$1');

vm.createContext(sandbox);
vm.runInContext(replayScript, sandbox);

const DecoderClass = sandbox.window.ab;
const RoomClass = sandbox.window.ca;

const room = new RoomClass();
const decoder = new DecoderClass(new Uint8Array(replayData), room, 3);

console.log('\n=== Decoder Properties ===');
console.log('Duration:', decoder.ad, 'frames');

// Check decoder properties
const decoderKeys = Object.keys(decoder).filter(k => !k.startsWith('_'));
console.log('Decoder keys (first 20):', decoderKeys.slice(0, 20).join(', '));

// Check for step-like methods
console.log('\n=== Checking for methods ===');
for (const key of decoderKeys) {
  if (typeof decoder[key] === 'function' && key.length < 4) {
    console.log(`Function: ${key}`);
  }
}

// Check initial state
console.log('\n=== Initial Room State ===');
console.log('Players:', room.L ? room.L.length : 0);
if (room.L && room.L.length > 0) {
  const player = room.L[0];
  console.log('Player 0:');
  console.log('  ID:', player.aa);
  console.log('  Name:', player.C);
  console.log('  Team ID:', player.fa ? player.fa.Ha : 'unknown');
  console.log('  Team name:', player.fa ? player.fa.C : 'unknown');
}

console.log('\n=== Game State ===');
console.log('Has game state (D):', room.D ? 'yes' : 'no');
if (room.D) {
  console.log('Game time:', room.D.za);
  console.log('Red score:', room.D.Ta);
  console.log('Blue score:', room.D.$a);
}

