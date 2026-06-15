#!/usr/bin/env node
/**
 * Complete HBR2 Decoder V2 - Enhanced decoder for Haxball replay files
 * 
 * This is an improved version of the original decoder with:
 * - Complete sandbox environment with full Canvas/Audio/DOM mocks
 * - Multi-pattern patching strategy for better compatibility
 * - Enhanced data extraction (velocities, physics, complete events)
 * - Robust error handling with fallback mechanisms
 * - Proper initialization flow for custom stadiums
 * 
 * Based on: https://github.com/haxball-replay-analyzer/haxball-replay-analyzer.github.io
 * 
 * Usage:
 *   node scripts/decode_hbr2_complete_v2.js <input.hbr2> [output.json]
 *   npm run decode:v2 -- <input.hbr2> [output.json]
 */

const fs = require('fs');
const path = require('path');
const vm = require('vm');

// Configuration constants
const MAX_RECURSION_DEPTH = 10; // Maximum depth for recursive data extraction
const MIN_COMPLETE_OUTPUT_KB = 10; // Minimum size (KB) for complete extraction warning

// Parse command line arguments
const args = process.argv.slice(2);
if (args.length < 1) {
  console.error('Usage: node decode_hbr2_complete_v2.js <input.hbr2> [output.json]');
  console.error('   or: npm run decode:v2 -- <input.hbr2> [output.json]');
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
function extractData(obj, depth = 0, maxDepth = MAX_RECURSION_DEPTH, seen = new WeakSet()) {
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
 * Extract player information with enhanced physics data
 */
function extractPlayer(player) {
  if (!player) return null;
  
  const playerData = {
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
    // Disc/physics information with velocities
    disc: null
  };
  
  if (player.w) {
    playerData.disc = {
      x: player.w.a ? player.w.a.x : null,
      y: player.w.a ? player.w.a.y : null,
      xSpeed: player.w.G ? player.w.G.x : null,
      ySpeed: player.w.G ? player.w.G.y : null,
      radius: player.w.S,
      // Additional physics properties
      invMass: player.w.Y || null,
      damping: player.w.V || null,
      bCoef: player.w.v || null
    };
  }
  
  return playerData;
}

/**
 * Extract complete game state information with full disc physics
 */
function extractGameState(gameState) {
  if (!gameState) return null;
  
  const state = {
    time: gameState.za,
    timeLimit: gameState.Da,
    scoreLimit: gameState.ma,
    redScore: gameState.Ta,
    blueScore: gameState.$a,
    // Extract complete discs/physics state
    discs: []
  };
  
  if (gameState.Z && gameState.Z.s) {
    state.discs = gameState.Z.s.map(disc => {
      const discData = {
        x: disc.a ? disc.a.x : null,
        y: disc.a ? disc.a.y : null,
        xSpeed: disc.G ? disc.G.x : null,
        ySpeed: disc.G ? disc.G.y : null,
        radius: disc.S
      };
      
      // Add complete physics properties
      if (disc.Y !== undefined) discData.invMass = disc.Y;
      if (disc.V !== undefined) discData.damping = disc.V;
      if (disc.v !== undefined) discData.bCoef = disc.v;
      if (disc.u !== undefined) discData.cGroup = disc.u;
      if (disc.o !== undefined) discData.cMask = disc.o;
      
      return discData;
    });
  }
  
  return state;
}

/**
 * Complete event type mapping (14 event types)
 * Based on the Haxball protocol
 */
function getEventTypeName(kind) {
  const eventTypes = {
    0: 'ANNOUNCEMENT',
    1: 'CHAT',
    2: 'GOAL',
    3: 'TEAM_GOAL',
    4: 'GAME_START',
    5: 'GAME_STOP',
    6: 'PLAYER_JOIN',
    7: 'PLAYER_LEAVE',
    8: 'PLAYER_TEAM_CHANGE',
    9: 'PAUSE',
    10: 'UNPAUSE',
    11: 'ADMIN_CHANGE',
    12: 'STADIUM_CHANGE',
    13: 'KICK',
    14: 'POSITION_CHANGE'
  };
  
  return eventTypes[kind] || `UNKNOWN_${kind}`;
}

/**
 * Extract event timeline from decoder markers
 */
function extractEvents(decoder) {
  if (!decoder.eg || !Array.isArray(decoder.eg)) {
    return [];
  }
  
  const events = [];
  
  for (let i = 0; i < decoder.eg.length; i++) {
    const marker = decoder.eg[i];
    
    if (!marker) continue;
    
    // Extract event information from marker
    const event = {
      index: i,
      // Zk is timestamp as fraction of total duration (0.0 to 1.0)
      timePercent: marker.Zk,
      // Calculate actual time in milliseconds
      time: marker.Zk * decoder.ad,
      // kind is the event type ID
      kind: marker.kind,
      type: getEventTypeName(marker.kind)
    };
    
    events.push(event);
  }
  
  return events;
}

/**
 * Create comprehensive Canvas 2D context mock
 */
function createCanvasContext() {
  const ctx = {
    canvas: null,
    // State
    fillStyle: '#000000',
    strokeStyle: '#000000',
    lineWidth: 1,
    lineCap: 'butt',
    lineJoin: 'miter',
    miterLimit: 10,
    lineDashOffset: 0,
    font: '10px sans-serif',
    textAlign: 'start',
    textBaseline: 'alphabetic',
    direction: 'inherit',
    globalAlpha: 1,
    globalCompositeOperation: 'source-over',
    imageSmoothingEnabled: true,
    shadowBlur: 0,
    shadowColor: 'rgba(0, 0, 0, 0)',
    shadowOffsetX: 0,
    shadowOffsetY: 0,
    // Drawing methods
    clearRect: () => {},
    fillRect: () => {},
    strokeRect: () => {},
    fillText: () => {},
    strokeText: () => {},
    measureText: (text) => ({ width: text.length * 7 }),
    // Path methods
    beginPath: () => {},
    closePath: () => {},
    moveTo: () => {},
    lineTo: () => {},
    arc: () => {},
    arcTo: () => {},
    ellipse: () => {},
    rect: () => {},
    fill: () => {},
    stroke: () => {},
    clip: () => {},
    isPointInPath: () => false,
    isPointInStroke: () => false,
    // Transformations
    rotate: () => {},
    scale: () => {},
    translate: () => {},
    transform: () => {},
    setTransform: () => {},
    resetTransform: () => {},
    // State stack
    save: () => {},
    restore: () => {},
    // Images
    drawImage: () => {},
    createImageData: () => ({ data: new Uint8ClampedArray(4), width: 1, height: 1 }),
    getImageData: () => ({ data: new Uint8ClampedArray(4), width: 1, height: 1 }),
    putImageData: () => {},
    // Gradients and patterns
    createLinearGradient: () => ({
      addColorStop: () => {}
    }),
    createRadialGradient: () => ({
      addColorStop: () => {}
    }),
    createPattern: () => null,
    // Line styles
    setLineDash: () => {},
    getLineDash: () => []
  };
  
  return ctx;
}

/**
 * Create complete sandbox environment with all necessary mocks
 */
function createSandbox() {
  const sandbox = {
    console: console,
    Buffer: Buffer,
    Uint8Array: Uint8Array,
    Uint8ClampedArray: Uint8ClampedArray,
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
    RangeError: RangeError,
    JSON: JSON,
    parseInt: parseInt,
    parseFloat: parseFloat,
    isNaN: isNaN,
    isFinite: isFinite,
    encodeURIComponent: encodeURIComponent,
    decodeURIComponent: decodeURIComponent,
    window: {},
    document: {},
    performance: {
      now: () => Date.now()
    },
    requestAnimationFrame: function(cb) { 
      return setTimeout(cb, 16);
    },
    cancelAnimationFrame: function(id) {
      clearTimeout(id);
    },
    setInterval: setInterval,
    setTimeout: setTimeout,
    clearInterval: clearInterval,
    clearTimeout: clearTimeout,
    // Storage for captured data
    __capturedData: null
  };
  
  // HTMLCanvasElement mock
  const HTMLCanvasElement = function() {
    this.width = 800;
    this.height = 600;
    this.style = {};
    this.getContext = function(contextType) {
      if (contextType === '2d') {
        const ctx = createCanvasContext();
        ctx.canvas = this;
        return ctx;
      }
      return null;
    };
    this.toDataURL = () => 'data:image/png;base64,';
    this.toBlob = () => {};
  };
  
  // Image mock
  const Image = function() {
    this.src = '';
    this.width = 0;
    this.height = 0;
    this.onload = null;
    this.onerror = null;
    this.complete = true;
  };
  
  // Audio context mock
  const AudioContext = function() {
    this.createGain = () => ({
      gain: { value: 1 },
      connect: () => {}
    });
    this.createOscillator = () => ({
      frequency: { value: 440 },
      connect: () => {},
      start: () => {},
      stop: () => {}
    });
    this.destination = {};
    this.currentTime = 0;
  };
  
  // Create document mock with more complete API
  sandbox.document = {
    createElement: function(tag) {
      if (tag === 'canvas') {
        return new HTMLCanvasElement();
      }
      if (tag === 'img') {
        return new Image();
      }
      return {
        textContent: '',
        innerHTML: '',
        className: '',
        id: '',
        style: {},
        classList: {
          add: () => {},
          remove: () => {},
          toggle: () => {},
          contains: () => false
        },
        onclick: null,
        onkeydown: null,
        onmousedown: null,
        onmouseup: null,
        onmousemove: null,
        appendChild: function(child) { return child; },
        removeChild: function(child) { return child; },
        insertBefore: function(newNode, refNode) { return newNode; },
        querySelector: () => null,
        querySelectorAll: () => [],
        getAttribute: () => null,
        setAttribute: () => {},
        removeAttribute: () => {},
        addEventListener: () => {},
        removeEventListener: () => {},
        dispatchEvent: () => true,
        focus: () => {},
        blur: () => {},
        remove: () => {},
        hidden: false,
        disabled: false,
        value: '',
        checked: false,
        parentNode: null,
        children: [],
        firstChild: null,
        lastChild: null,
        nextSibling: null,
        previousSibling: null
      };
    },
    createElementNS: function(ns, tag) {
      return this.createElement(tag);
    },
    createTextNode: (text) => ({ textContent: text, nodeValue: text }),
    getElementById: () => null,
    getElementsByTagName: () => [],
    getElementsByClassName: () => [],
    querySelector: () => null,
    querySelectorAll: () => [],
    addEventListener: () => {},
    removeEventListener: () => {},
    body: null,
    head: null,
    documentElement: null
  };
  
  // Add body, head, documentElement to document
  sandbox.document.body = sandbox.document.createElement('body');
  sandbox.document.head = sandbox.document.createElement('head');
  sandbox.document.documentElement = sandbox.document.createElement('html');
  
  // Window object with circular references
  sandbox.window.document = sandbox.document;
  sandbox.window.window = sandbox.window;
  sandbox.window.self = sandbox.window;
  sandbox.window.top = sandbox.window;
  sandbox.window.parent = sandbox.window;
  sandbox.document.defaultView = sandbox.window;
  
  // Navigator mock
  sandbox.window.navigator = sandbox.navigator = {
    userAgent: 'Mozilla/5.0 (Node.js) HaxballReplayDecoder/2.0',
    platform: 'Linux',
    language: 'en-US',
    languages: ['en-US', 'en'],
    onLine: true,
    hardwareConcurrency: 4
  };
  
  // Screen mock
  sandbox.window.screen = sandbox.screen = {
    width: 1920,
    height: 1080,
    availWidth: 1920,
    availHeight: 1040,
    colorDepth: 24,
    pixelDepth: 24
  };
  
  // Location mock
  sandbox.window.location = sandbox.location = {
    href: 'about:blank',
    protocol: 'about:',
    host: '',
    hostname: '',
    port: '',
    pathname: 'blank',
    search: '',
    hash: '',
    origin: 'null'
  };
  
  // History mock
  sandbox.window.history = sandbox.history = {
    length: 1,
    state: null,
    pushState: () => {},
    replaceState: () => {},
    back: () => {},
    forward: () => {},
    go: () => {}
  };
  
  // LocalStorage and SessionStorage mocks
  const createStorage = () => {
    const storage = {};
    return {
      getItem: (key) => storage[key] || null,
      setItem: (key, value) => { storage[key] = String(value); },
      removeItem: (key) => { delete storage[key]; },
      clear: () => { Object.keys(storage).forEach(k => delete storage[k]); },
      key: (index) => Object.keys(storage)[index] || null,
      get length() { return Object.keys(storage).length; }
    };
  };
  
  sandbox.window.localStorage = sandbox.localStorage = createStorage();
  sandbox.window.sessionStorage = sandbox.sessionStorage = createStorage();
  
  // Additional window properties
  sandbox.window.performance = sandbox.performance;
  sandbox.window.requestAnimationFrame = sandbox.requestAnimationFrame;
  sandbox.window.cancelAnimationFrame = sandbox.cancelAnimationFrame;
  sandbox.window.setTimeout = sandbox.setTimeout;
  sandbox.window.setInterval = sandbox.setInterval;
  sandbox.window.clearTimeout = sandbox.clearTimeout;
  sandbox.window.clearInterval = sandbox.clearInterval;
  sandbox.window.indexedDB = null; // Disable IndexedDB
  sandbox.window.AudioContext = AudioContext;
  sandbox.window.webkitAudioContext = AudioContext;
  sandbox.window.Image = Image;
  sandbox.window.HTMLCanvasElement = HTMLCanvasElement;
  
  // Blob and URL mocks
  sandbox.window.Blob = sandbox.Blob = class Blob {
    constructor(parts, options) {
      this.parts = parts;
      this.options = options || {};
      this.size = 0;
      this.type = this.options.type || '';
    }
  };
  
  sandbox.window.URL = sandbox.URL = {
    createObjectURL: (blob) => 'blob:null/' + Math.random().toString(36).substr(2, 9),
    revokeObjectURL: () => {}
  };
  
  // Event and EventTarget mocks
  sandbox.window.Event = sandbox.Event = class Event {
    constructor(type, options) {
      this.type = type;
      this.bubbles = options?.bubbles || false;
      this.cancelable = options?.cancelable || false;
      this.defaultPrevented = false;
    }
    preventDefault() { this.defaultPrevented = true; }
    stopPropagation() {}
  };
  
  // Add global to sandbox (the script expects it)
  sandbox.global = sandbox.window;
  sandbox.self = sandbox.window;
  
  return sandbox;
}

/**
 * Apply multiple patching strategies to expose internal classes
 */
function patchReplayScript(replayScript) {
  console.log('Applying multi-pattern patch to expose internal classes...');
  
  // Strategy 1: Try to patch before C.cj();
  const pattern1 = /(\s+C\.cj\(\);)/;
  
  // Strategy 2: Try to patch before X.fj(); (alternative pattern)
  const pattern2 = /(\s+X\.fj\(\);)/;
  
  // Strategy 3: Try to patch before common IIFE endings
  const pattern3 = /(\}\)\(window\);?\s*$)/;
  const pattern4 = /(\}\)\(this\);?\s*$)/;
  const pattern5 = /(\}\)\(self\);?\s*$)/;
  const pattern6 = /(\}\)\(global\);?\s*$)/;
  
  // The patch code to expose internal classes
  // Try multiple possible class names based on different minification versions
  const classesToExpose = [
    { name: 'ab', comment: 'Decoder class' },
    { name: 'Jb', comment: 'Alternative Decoder name' },
    { name: 'ca', comment: 'Room class' },
    { name: 'fa', comment: 'Alternative Room name' },
    { name: 'rb', comment: 'Message classes' },
    { name: 'Vb', comment: 'Replay player' },
    { name: 'hb', comment: '' },
    { name: 'C', comment: '' },
    { name: 'g', comment: '' },
    { name: 'T', comment: '' },
    { name: 'I', comment: '' },
    { name: 'O', comment: 'DataView helper' },
    { name: 'F', comment: 'Reader helper' },
    { name: 'p', comment: '' },
    { name: 'k', comment: '' }
  ];
  
  const exposePatch = `
  // Expose internal classes to ub (which is window/global)
  // Multiple names for compatibility across versions
${classesToExpose.map(cls => 
    `  if (typeof ${cls.name} !== 'undefined') ub.${cls.name} = ${cls.name};${cls.comment ? ' // ' + cls.comment : ''}`
  ).join('\n')}
`;
  
  // Try each pattern in order
  if (pattern1.test(replayScript)) {
    console.log('  Using pattern 1: C.cj();');
    return replayScript.replace(pattern1, exposePatch + '$1');
  }
  
  if (pattern2.test(replayScript)) {
    console.log('  Using pattern 2: X.fj();');
    return replayScript.replace(pattern2, exposePatch + '$1');
  }
  
  if (pattern3.test(replayScript)) {
    console.log('  Using pattern 3: })(window);');
    return replayScript.replace(pattern3, exposePatch + '$1');
  }
  
  if (pattern4.test(replayScript)) {
    console.log('  Using pattern 4: })(this);');
    return replayScript.replace(pattern4, exposePatch + '$1');
  }
  
  if (pattern5.test(replayScript)) {
    console.log('  Using pattern 5: })(self);');
    return replayScript.replace(pattern5, exposePatch + '$1');
  }
  
  if (pattern6.test(replayScript)) {
    console.log('  Using pattern 6: })(global);');
    return replayScript.replace(pattern6, exposePatch + '$1');
  }
  
  // Fallback: Add the patch at the end if no pattern matched
  console.log('  Using fallback: appending patch at end');
  return replayScript + '\n' + exposePatch;
}

// Load pako for decompression
try {
  const pako = require('pako');
  global.pako = pako;
} catch (error) {
  console.error('Error: pako module not found. Please run: npm install');
  process.exit(1);
}

console.log('Loading Haxball replay decoder...');

// Load the replay-min.js file
const replayScriptPath = path.join(__dirname, '..', 'original_script', 'replay-min.js');
let replayScript = fs.readFileSync(replayScriptPath, 'utf8');

// Apply multi-pattern patch
replayScript = patchReplayScript(replayScript);

// Create comprehensive sandbox
const sandbox = createSandbox();
sandbox.pako = global.pako;

// Execute the modified script in the sandbox
try {
  vm.createContext(sandbox);
  vm.runInContext(replayScript, sandbox);
  console.log('Decoder loaded successfully');
  
  // Debug: Check what's available now
  const possibleClasses = ['ab', 'Jb', 'ca', 'fa', 'rb', 'Vb', 'hb', 'C', 'g', 'T', 'I', 'O', 'F', 'p', 'k'];
  const exposed = possibleClasses.filter(k => sandbox.window[k]);
  console.log('Exposed classes:', exposed.join(', '));
  
  if (exposed.length === 0) {
    console.error('Warning: No classes were exposed. The patch may have failed.');
    console.error('Available properties in window:', Object.keys(sandbox.window).filter(k => !k.startsWith('_')).slice(0, 20).join(', '));
  }
} catch (error) {
  console.error('Error loading decoder:', error);
  console.error(error.stack);
  process.exit(1);
}

console.log('Decoding replay data...');

// Access the exposed classes from sandbox.window
try {
  // Try primary class names first, then alternatives
  const DecoderClass = sandbox.window.ab || sandbox.window.Jb;
  const RoomClass = sandbox.window.ca || sandbox.window.fa;
  const MessageClass = sandbox.window.rb;
  
  if (!DecoderClass || !RoomClass) {
    throw new Error(`Required classes not exposed. Found: ${Object.keys(sandbox.window).filter(k => !k.startsWith('_') && typeof sandbox.window[k] === 'function').join(', ')}`);
  }
  
  console.log(`  Using decoder class: ${DecoderClass === sandbox.window.ab ? 'ab' : 'Jb'}`);
  console.log(`  Using room class: ${RoomClass === sandbox.window.ca ? 'ca' : 'fa'}`);
  
  // Initialize message classes first (CRITICAL for custom stadiums)
  if (MessageClass && typeof MessageClass.Xe === 'function') {
    console.log('  Initializing message classes for custom stadium support...');
    try {
      MessageClass.Xe();
      console.log('  Message classes initialized successfully');
    } catch (e) {
      console.log(`  Message class initialization warning: ${e.message}`);
    }
  } else {
    console.log('  Message classes not found or already initialized');
  }
  
  console.log('  Creating room instance...');
  
  // Create a room instance
  const room = new RoomClass();
  
  console.log('  Creating decoder instance...');
  
  // Create decoder instance - this will parse the entire replay
  const decoder = new DecoderClass(new Uint8Array(replayData), room, 3);
  
  console.log('  Replay decoded successfully');
  
  console.log('Extracting data from decoded replay...');
  
  // Extract all the data with granular error handling
  const result = {
    metadata: {},
    roomInfo: {},
    stadium: null,
    players: [],
    gameState: null,
    teams: {},
    events: []
  };
  
  // Extract metadata
  try {
    result.metadata = {
      version: 3,
      duration: decoder.ad || 0,
      recordingStart: decoder.le || 0
    };
  } catch (e) {
    console.error(`  Error extracting metadata: ${e.message}`);
    result.metadata = { error: e.message };
  }
  
  // Extract room info
  try {
    result.roomInfo = {
      name: room.Fb || 'Unknown',
      locked: room.Ib || false,
      scoreLimit: room.Da || 0,
      timeLimit: room.ma || 0,
      rules: {
        kickRateLimit: room.fc || 0,
        teamSize: room.Sb || 0,
        bounciness: room.zc || 1
      }
    };
  } catch (e) {
    console.error(`  Error extracting room info: ${e.message}`);
    result.roomInfo = { error: e.message };
  }
  
  // Extract stadium data using the built-in yk() method
  try {
    if (room.I && typeof room.I.yk === 'function') {
      try {
        result.stadium = room.I.yk();
        console.log(`  Stadium: ${result.stadium.name || 'Unknown'} (full export)`);
      } catch (ykError) {
        // yk() failed, try manual extraction
        console.log(`  Stadium yk() failed, attempting manual extraction...`);
        result.stadium = {
          name: room.I.C || 'Unknown',
          width: room.I.kb || 0,
          height: room.I.Ma || 0,
          // Try to extract what we can manually
          canBeStored: room.I.Zb,
          cameraWidth: room.I.Ub,
          cameraHeight: room.I.Tb,
          cameraFollow: room.I.Xb,
          note: 'Manual extraction - yk() method failed'
        };
        console.log(`  Stadium: ${result.stadium.name} (manual extraction)`);
      }
    } else if (room.I) {
      // Fallback: extract basic stadium info
      result.stadium = {
        name: room.I.C || 'Unknown',
        width: room.I.kb || 0,
        height: room.I.Ma || 0,
        canBeStored: room.I.Zb,
        cameraWidth: room.I.Ub,
        cameraHeight: room.I.Tb,
        cameraFollow: room.I.Xb,
        note: 'Basic extraction - yk() method not available'
      };
      console.log(`  Stadium: ${result.stadium.name} (basic extraction)`);
    } else {
      result.stadium = { error: 'Stadium object not found' };
    }
  } catch (e) {
    const errorMsg = e && e.message ? e.message : String(e);
    console.error(`  Error extracting stadium: ${errorMsg}`);
    result.stadium = {
      name: room.I?.C || 'Unknown',
      error: `Could not export stadium data: ${errorMsg}`
    };
  }
  
  // Extract players
  try {
    if (room.L && Array.isArray(room.L)) {
      result.players = room.L.map(extractPlayer).filter(p => p !== null);
      console.log(`  Players: ${result.players.length}`);
    } else {
      console.log('  Players: 0 (no player data found)');
    }
  } catch (e) {
    console.error(`  Error extracting players: ${e.message}`);
    result.players = [];
  }
  
  // Extract game state
  try {
    if (room.D) {
      result.gameState = extractGameState(room.D);
      console.log(`  Game active: Yes (${result.gameState.redScore} - ${result.gameState.blueScore})`);
      console.log(`  Discs tracked: ${result.gameState.discs.length}`);
    } else {
      console.log(`  Game active: No`);
    }
  } catch (e) {
    console.error(`  Error extracting game state: ${e.message}`);
    result.gameState = null;
  }
  
  // Extract team information
  try {
    if (room.Fa && Array.isArray(room.Fa)) {
      result.teams = {
        spectators: room.Fa[0] ? extractData(room.Fa[0], 0, 3) : null,
        red: room.Fa[1] ? extractData(room.Fa[1], 0, 3) : null,
        blue: room.Fa[2] ? extractData(room.Fa[2], 0, 3) : null
      };
    }
  } catch (e) {
    console.error(`  Error extracting teams: ${e.message}`);
    result.teams = { error: e.message };
  }
  
  // Extract events from decoder markers
  try {
    result.events = extractEvents(decoder);
    console.log(`  Events: ${result.events.length}`);
  } catch (e) {
    console.error(`  Error extracting events: ${e.message}`);
    result.events = [];
  }
  
  // Write output
  console.log(`\nWriting output to: ${outputFile}`);
  const jsonOutput = JSON.stringify(result, null, 2);
  fs.writeFileSync(outputFile, jsonOutput);
  
  const outputSize = (jsonOutput.length / 1024).toFixed(1);
  console.log(`Output size: ${outputSize} KB`);
  
  console.log('\n✓ Decoding complete!');
  console.log(`\nSummary:`);
  console.log(`  Room: ${result.roomInfo.name || 'Unknown'}`);
  console.log(`  Stadium: ${result.stadium?.name || 'Unknown'}`);
  console.log(`  Players: ${result.players.length}`);
  console.log(`  Events: ${result.events.length}`);
  console.log(`  Score limit: ${result.roomInfo.scoreLimit}`);
  console.log(`  Time limit: ${result.roomInfo.timeLimit}`);
  if (result.gameState) {
    console.log(`  Current score: ${result.gameState.redScore} - ${result.gameState.blueScore}`);
    console.log(`  Discs: ${result.gameState.discs.length}`);
  }
  
  if (outputSize < MIN_COMPLETE_OUTPUT_KB) {
    console.log(`\n⚠ Warning: Output size is ${outputSize} KB (expected >${MIN_COMPLETE_OUTPUT_KB} KB for complete extraction)`);
  }
  
} catch (error) {
  console.error('\n✗ Error:', error.message);
  console.error(error.stack);
  process.exit(1);
}
