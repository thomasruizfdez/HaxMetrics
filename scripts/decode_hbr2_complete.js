#!/usr/bin/env node
/**
 * Complete HBR2 Decoder - Decode Haxball replay files to complete JSON
 * 
 * This script uses the ORIGINAL Haxball JavaScript code to fully decode .hbr2 files
 * by intercepting and extracting data from the internal objects.
 * 
 * Usage:
 *   node scripts/decode_hbr2_complete.js <input.hbr2> [output.json]
 *   npm run decode:full -- <input.hbr2> [output.json]
 */

const fs = require('fs');
const path = require('path');
const vm = require('vm');

// Parse command line arguments
const args = process.argv.slice(2);
if (args.length < 1) {
  console.error('Usage: node decode_hbr2_complete.js <input.hbr2> [output.json]');
  console.error('   or: npm run decode:full -- <input.hbr2> [output.json]');
  process.exit(1);
}

const inputFile = args[0];
const outputFile = args[1] || inputFile.replace(/\.hbr2$/, '.json');

// Check if input file exists
if (!fs.existsSync(inputFile)) {
  console.error(`Error: Input file not found: ${inputFile}`);
  process.exit(1);
}

console.log(`Reading replay file: ${inputFile}`);

// Read the .hbr2 file
const replayData = fs.readFileSync(inputFile);

/**
 * Recursively extract data from objects, handling circular references
 */
function extractData(obj, depth = 0, maxDepth = 10, seen = new WeakSet()) {
  // Prevent infinite recursion
  if (depth > maxDepth) return '[Max Depth Reached]';
  
  // Handle primitives
  if (obj === null || obj === undefined) return obj;
  if (typeof obj !== 'object') return obj;
  
  // Handle circular references
  if (seen.has(obj)) return '[Circular]';
  seen.add(obj);
  
  // Handle arrays
  if (Array.isArray(obj)) {
    return obj.map(item => extractData(item, depth + 1, maxDepth, seen));
  }
  
  // Handle special objects
  if (obj instanceof Uint8Array || obj instanceof ArrayBuffer || obj instanceof DataView) {
    return '[Binary Data]';
  }
  
  // Extract plain object properties
  const result = {};
  for (const key in obj) {
    // Skip function properties and private-looking properties
    if (typeof obj[key] === 'function') continue;
    if (key.startsWith('__')) continue;
    
    try {
      result[key] = extractData(obj[key], depth + 1, maxDepth, seen);
    } catch (e) {
      result[key] = '[Error extracting]';
    }
  }
  
  return result;
}

/**
 * Extract player information
 */
function extractPlayer(player) {
  if (!player) return null;
  
  return {
    id: player.aa,
    name: player.C,
    admin: player.cb,
    position: player.Sa,
    avatar: player.Jb,
    country: player.mc,
    // Team information
    team: player.fa ? {
      id: player.fa.Ha,
      name: player.fa.C
    } : null,
    // Disc/physics information
    disc: player.w ? {
      x: player.w.a ? player.w.a.x : null,
      y: player.w.a ? player.w.a.y : null,
      radius: player.w.S
    } : null
  };
}

/**
 * Extract game state information
 */
function extractGameState(gameState) {
  if (!gameState) return null;
  
  return {
    time: gameState.za,
    timeLimit: gameState.Da,
    scoreLimit: gameState.ma,
    redScore: gameState.Ta,
    blueScore: gameState.$a,
    // Extract discs/physics state
    discs: gameState.Z && gameState.Z.s ? gameState.Z.s.map(disc => ({
      x: disc.a ? disc.a.x : null,
      y: disc.a ? disc.a.y : null,
      xSpeed: disc.G ? disc.G.x : null,
      ySpeed: disc.G ? disc.G.y : null,
      radius: disc.S
    })) : []
  };
}

// Create a sandbox environment with necessary globals
const sandbox = {
  console: console,
  Buffer: Buffer,
  Uint8Array: Uint8Array,
  DataView: DataView,
  ArrayBuffer: ArrayBuffer,
  Int8Array: Int8Array,
  Int16Array: Int16Array,
  Int32Array: Int32Array,
  Uint16Array: Uint16Array,
  Uint32Array: Uint32Array,
  Float32Array: Float32Array,
  Float64Array: Float64Array,
  Map: Map,
  Set: Set,
  WeakMap: WeakMap,
  WeakSet: WeakSet,
  Promise: Promise,
  Object: Object,
  Array: Array,
  String: String,
  Number: Number,
  Boolean: Boolean,
  Math: Math,
  Date: Date,
  RegExp: RegExp,
  Error: Error,
  TypeError: TypeError,
  window: {},
  document: {},
  performance: {
    now: () => Date.now()
  },
  requestAnimationFrame: (cb) => { /* noop */ },
  setInterval: (cb, ms) => { /* noop */ },
  setTimeout: (cb, ms) => { /* noop */ },
  clearInterval: (id) => { /* noop */ },
  clearTimeout: (id) => { /* noop */ },
  // Storage for captured data
  __capturedData: null
};

// Create minimal DOM mocks
sandbox.window.document = {
  createElement: (tag) => ({
    textContent: '',
    innerHTML: '',
    className: '',
    classList: {
      add: () => {},
      remove: () => {},
      toggle: () => {}
    },
    onclick: null,
    onkeydown: null,
    appendChild: () => {},
    querySelector: () => null,
    querySelectorAll: () => [],
    addEventListener: () => {},
    removeEventListener: () => {},
    focus: () => {},
    remove: () => {},
    hidden: false
  }),
  addEventListener: () => {},
  removeEventListener: () => {},
  body: {
    appendChild: () => {},
    classList: { add: () => {} }
  }
};

sandbox.document = sandbox.window.document;
sandbox.window.performance = sandbox.performance;
sandbox.window.requestAnimationFrame = sandbox.requestAnimationFrame;
sandbox.window.setInterval = sandbox.setInterval;
sandbox.window.setTimeout = sandbox.setTimeout;
sandbox.window.indexedDB = null; // Disable IndexedDB

// Add global to sandbox (the script expects it)
sandbox.global = sandbox.window;
sandbox.self = sandbox.window;

// Load pako for decompression
const pako = require('pako');
sandbox.pako = pako;

console.log('Loading Haxball replay decoder...');

// Load the replay-min.js file
const replayScriptPath = path.join(__dirname, '..', 'original_script', 'replay-min.js');
let replayScript = fs.readFileSync(replayScriptPath, 'utf8');

// Modify the script to expose internal classes
// Insert code right before C.cj(); at the end
const exposePatch = `
  // Expose internal classes to window for extraction
  ub.ab = ab;
  ub.ca = ca;
  ub.hb = hb;
  ub.C = C;
  ub.g = g;
  ub.T = T;
  ub.I = I;
  ub.O = O;
  ub.p = p;
`;

// Replace the C.cj(); line to add our patch before it
replayScript = replayScript.replace(/(\s+C\.cj\(\);)/, exposePatch + '$1');

// Execute the modified script in the sandbox
try {
  vm.createContext(sandbox);
  vm.runInContext(replayScript, sandbox);
  console.log('Decoder loaded successfully');
  
  // Debug: Check what's available now
  const exposed = ['ab', 'ca', 'hb', 'C', 'g', 'T', 'I', 'O', 'p'].filter(k => sandbox.window[k]);
  console.log('Exposed classes:', exposed.join(', '));
  
  if (exposed.length === 0) {
    console.error('Warning: No classes were exposed. The patch may have failed.');
  }
} catch (error) {
  console.error('Error loading decoder:', error);
  console.error(error.stack);
  process.exit(1);
}

console.log('Decoding replay data...');

// Now we can directly access the exposed classes
try {
  const ab = sandbox.window.ab;
  const ca = sandbox.window.ca;
  
  if (!ab || !ca) {
    throw new Error('Required classes (ab, ca) not exposed properly');
  }
  
  console.log('  Creating room instance...');
  
  // Create a room instance
  const room = new ca();
  
  console.log('  Creating decoder instance...');
  
  // Create decoder instance - this will parse the entire replay
  const decoder = new ab(new Uint8Array(replayData), room, 3);
  
  console.log('  Replay decoded successfully');
  
  const { decoder: _, room: __ } = { decoder, room }; // Keep the names consistent with later code
  
  console.log('Extracting data from decoded replay...');
  
  // Extract all the data
  const result = {
    metadata: {
      version: 3,
      duration: decoder.ad,
      recordingStart: decoder.le
    },
    roomInfo: {
      name: room.Fb,
      locked: room.Ib,
      scoreLimit: room.Da,
      timeLimit: room.ma,
      rules: {
        kickRateLimit: room.fc,
        teamSize: room.Sb,
        bounciness: room.zc
      }
    },
    stadium: null,
    players: [],
    gameState: null,
    teams: {}
  };
  
  // Extract stadium data using the built-in yk() method
  if (room.I && typeof room.I.yk === 'function') {
    try {
      result.stadium = room.I.yk();
      console.log(`  Stadium: ${result.stadium.name || 'Unknown'}`);
    } catch (e) {
      console.log(`  Stadium extraction warning: ${e.message}`);
      result.stadium = {
        name: room.I.C || 'Unknown',
        error: 'Could not export full stadium data'
      };
    }
  }
  
  // Extract players
  if (room.L && Array.isArray(room.L)) {
    result.players = room.L.map(extractPlayer).filter(p => p !== null);
    console.log(`  Players: ${result.players.length}`);
  }
  
  // Extract game state
  if (room.D) {
    result.gameState = extractGameState(room.D);
    console.log(`  Game active: Yes (${result.gameState.redScore} - ${result.gameState.blueScore})`);
  } else {
    console.log(`  Game active: No`);
  }
  
  // Extract team information
  if (room.Fa && Array.isArray(room.Fa)) {
    result.teams = {
      spectators: room.Fa[0] ? extractData(room.Fa[0], 0, 3) : null,
      red: room.Fa[1] ? extractData(room.Fa[1], 0, 3) : null,
      blue: room.Fa[2] ? extractData(room.Fa[2], 0, 3) : null
    };
  }
  
  // Write output
  console.log(`\nWriting output to: ${outputFile}`);
  fs.writeFileSync(outputFile, JSON.stringify(result, null, 2));
  
  console.log('\n✓ Decoding complete!');
  console.log(`\nSummary:`);
  console.log(`  Room: ${result.roomInfo.name}`);
  console.log(`  Stadium: ${result.stadium?.name || 'Unknown'}`);
  console.log(`  Players: ${result.players.length}`);
  console.log(`  Score limit: ${result.roomInfo.scoreLimit}`);
  console.log(`  Time limit: ${result.roomInfo.timeLimit}`);
  if (result.gameState) {
    console.log(`  Current score: ${result.gameState.redScore} - ${result.gameState.blueScore}`);
  }
  
} catch (error) {
  console.error('\n✗ Error:', error.message);
  console.error(error.stack);
  process.exit(1);
}
