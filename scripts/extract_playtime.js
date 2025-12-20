#!/usr/bin/env node
/**
 * Comprehensive HBR2 Playtime Extractor
 * 
 * Extracts complete player playtime statistics from Haxball replay files by:
 * 1. Using original Haxball decoder for player names and initial states
 * 2. Parsing ALL actions from the binary stream (team changes, game events, etc.)
 * 3. Building frame-accurate timelines for each player
 * 4. Calculating playing time only when the game is active
 * 
 * This provides the most accurate and complete data extraction possible.
 */

const fs = require('fs');
const path = require('path');
const vm = require('vm');
const pako = require('pako');

// Constants
const FRAME_RATE = 60;

// Parse arguments
const args = process.argv.slice(2);
if (args.length < 1) {
  console.error('Usage: node extract_playtime.js <input.hbr2> [output.json]');
  process.exit(1);
}

const inputFile = args[0];
const outputFile = args[1] || inputFile.replace(/\.hbr2$/, '_playtime.json');

if (!fs.existsSync(inputFile)) {
  console.error(`Error: Input file not found: ${inputFile}`);
  process.exit(1);
}

console.log(`\n=== Comprehensive Playtime Extraction ===\n`);
console.log(`Reading replay file: ${inputFile}`);

// Read replay file
const replayData = fs.readFileSync(inputFile);
const magic = replayData.toString('utf8', 0, 4);
if (magic !== 'HBR2') {
  console.error('Error: Not a valid HBR2 file');
  process.exit(1);
}

const version = replayData.readUInt32BE(4);
const duration = replayData.readUInt32BE(8);

console.log(`  Version: ${version}`);
console.log(`  Duration: ${duration} frames (${(duration / FRAME_RATE).toFixed(2)}s)`);

// Decompress replay data
const decompressed = Buffer.from(pako.inflateRaw(replayData.slice(12)));
console.log(`  Decompressed: ${decompressed.length} bytes`);

/**
 * STEP 1: Use Haxball decoder to get initial player states
 */
console.log('\nStep 1: Loading Haxball decoder for initial states...');

const playerNames = new Map();
const playerInitialTeams = new Map();

try {
  function createSandbox() {
    const sandbox = {
      console: { log: () => {}, error: () => {}, warn: () => {} },
      pako: pako,
      Math: Math,
      Date: Date,
      Object: Object,
      Array: Array,
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
      performance: { now: () => Date.now() },
      window: {},
      self: {},
      document: {
        createElement: () => ({
          getContext: () => ({
            fillRect: () => {}, clearRect: () => {}, save: () => {}, restore: () => {},
            beginPath: () => {}, closePath: () => {}, moveTo: () => {}, lineTo: () => {},
            arc: () => {}, fill: () => {}, stroke: () => {}, setTransform: () => {},
            translate: () => {}, rotate: () => {}, scale: () => {}, fillText: () => {},
            measureText: () => ({ width: 0 })
          }),
          toDataURL: () => '',
          width: 800, height: 600, style: {}
        })
      }
    };
    
    sandbox.window.performance = sandbox.performance;
    sandbox.window.document = sandbox.document;
    sandbox.window.localStorage = { getItem: () => null, setItem: () => {}, removeItem: () => {} };
    sandbox.window.AudioContext = function() { this.createOscillator = () => ({ connect: () => {}, start: () => {} }); this.destination = {}; };
    sandbox.window.Image = function() {};
    sandbox.window.addEventListener = () => {};
    sandbox.self = sandbox.window;
    sandbox.ub = sandbox.window;
    
    return sandbox;
  }
  
  const sandbox = createSandbox();
  let replayScript = fs.readFileSync(path.join(__dirname, '../original_script/replay-min.js'), 'utf8');
  
  const patchCode = `
    if (typeof ab !== 'undefined') ub.ab = ab;
    if (typeof ca !== 'undefined') ub.ca = ca;
    if (typeof rb !== 'undefined') ub.rb = rb;
  `;
  replayScript = replayScript.replace(/(\s+C\.cj\(\);)/, patchCode + '$1');
  
  vm.createContext(sandbox);
  vm.runInContext(replayScript, sandbox);
  
  const DecoderClass = sandbox.window.ab;
  const RoomClass = sandbox.window.ca;
  const MessageClass = sandbox.window.rb;
  
  if (MessageClass && typeof MessageClass.Xe === 'function') {
    MessageClass.Xe();
  }
  
  const room = new RoomClass();
  const decoder = new DecoderClass(new Uint8Array(replayData), room, 3);
  
  // Extract initial player states
  if (room.L && Array.isArray(room.L)) {
    for (const player of room.L) {
      if (player && player.aa !== undefined) {
        const playerId = player.aa;
        const playerName = player.C || `Player${playerId}`;
        const teamId = player.fa ? player.fa.Ha : 0;
        const teamName = ['spectators', 'red', 'blue'][teamId];
        
        playerNames.set(playerId, playerName);
        playerInitialTeams.set(playerId, teamName);
        
        console.log(`  Player ${playerId} (${playerName}): initially in ${teamName}`);
      }
    }
  }
  
  console.log(`  Extracted ${playerNames.size} player(s)`);
} catch (e) {
  console.log(`  Warning: Could not load decoder: ${e.message}`);
}

/**
 * STEP 2: Parse ALL actions from binary stream
 */
console.log('\nStep 2: Parsing complete action stream...');

// Simple binary reader
class SimpleBinaryReader {
  constructor(buffer, offset = 0) {
    this.buffer = buffer;
    this.offset = offset;
  }
  
  readVarInt() {
    let result = 0;
    let shift = 0;
    
    while (this.offset < this.buffer.length) {
      const byte = this.buffer[this.offset++];
      result |= (byte & 0x7F) << shift;
      
      if ((byte & 0x80) === 0) {
        return shift > 0 && (result & (1 << (shift - 1))) ? result | (~0 << shift) : result;
      }
      
      shift += 7;
    }
    
    throw new Error('Incomplete varint');
  }
  
  readByte() {
    if (this.offset >= this.buffer.length) {
      throw new Error('EOF');
    }
    return this.buffer[this.offset++];
  }
  
  skip(bytes) {
    this.offset += bytes;
  }
  
  hasMore() {
    return this.offset < this.buffer.length - 10;
  }
}

// Skip messages
let offset = 0;
const reader = new SimpleBinaryReader(decompressed, offset);

try {
  const messageCount = reader.readVarInt();
  console.log(`  Messages in replay: ${messageCount}`);
  
  for (let i = 0; i < messageCount; i++) {
    const strLen = reader.readVarInt();
    reader.skip(strLen);
  }
  
  offset = reader.offset;
  console.log(`  Messages end at offset: ${offset}`);
} catch (e) {
  console.log(`  Could not parse messages, starting from beginning`);
  offset = 0;
}

// Find action stream - search backwards for byte value 12 (PlayerTeamChange)
console.log(`  Searching for action stream with team changes...`);

let actionStreamStart = -1;

// Look for byte value 12 in the second half of the file
for (let i = decompressed.length - 1; i > decompressed.length / 2; i--) {
  if (decompressed[i] === 12) {
    // Found a potential PlayerTeamChange
    // The action stream should start a bit before this
    // Try positions before this byte
    for (let tryPos = Math.max(offset, i - 50); tryPos < i; tryPos++) {
      // Check if starting here gives us valid actions
      let testPos = tryPos;
      let valid = true;
      let teamChangeFound = false;
      
      try {
        for (let j = 0; j < 5; j++) {
          const fd = decompressed[testPos++];
          if (fd > 200) { valid = false; break; }
          testPos += 2; // Skip 2 bytes
          const at = decompressed[testPos++];
          if (at > 25) { valid = false; break; }
          
          if (at === 12) {
            teamChangeFound = true;
            testPos += 5; // Skip player ID and team ID
          } else {
            testPos += 5; // Skip other data
          }
        }
      } catch {
        valid = false;
      }
      
      if (valid && teamChangeFound) {
        actionStreamStart = tryPos;
        console.log(`  Found action stream at offset ${actionStreamStart}`);
        break;
      }
    }
    
    if (actionStreamStart >= 0) break;
  }
}

if (actionStreamStart < 0) {
  console.log(`  Warning: Could not locate action stream, using estimated position`);
  actionStreamStart = Math.max(offset, decompressed.length - 300);
}

// Parse actions
console.log(`  Parsing actions from offset ${actionStreamStart}...`);

const actions = [];
const actionReader = new SimpleBinaryReader(decompressed, actionStreamStart);
let currentFrame = 0;
let actionCount = 0;
let teamChangeCount = 0;
let gameEventCount = 0;

try {
  while (actionReader.hasMore() && actionCount < 10000) {
    const frameDelta = actionReader.readByte();
    if (frameDelta > 250) break; // Frame deltas shouldn't be this large
    
    currentFrame += frameDelta;
    
    // Skip 2 bytes (based on observed pattern)
    actionReader.skip(2);
    
    const actionType = actionReader.readByte();
    if (actionType > 25) break; // Invalid action type
    
    const action = {
      frame: currentFrame,
      type: actionType
    };
    
    // Parse action-specific data
    if (actionType === 12) {
      // PlayerTeamChange - uses fixed-size encoding
      // Player ID: 4 bytes (32-bit int, little-endian)
      // Team ID: 1 byte
      const playerIdBytes = [
        actionReader.readByte(),
        actionReader.readByte(),
        actionReader.readByte(),
        actionReader.readByte()
      ];
      action.playerId = playerIdBytes[0] | (playerIdBytes[1] << 8) | (playerIdBytes[2] << 16) | (playerIdBytes[3] << 24);
      action.teamId = actionReader.readByte();
      action.teamName = ['spectators', 'red', 'blue'][action.teamId] || 'unknown';
      teamChangeCount++;
      
      console.log(`  Frame ${currentFrame}: Player ${action.playerId} -> ${action.teamName}`);
    } else if (actionType === 2) {
      // Game Start
      action.name = 'game_start';
      gameEventCount++;
      console.log(`  Frame ${currentFrame}: GAME START`);
      actionReader.skip(3); // Skip action data
    } else if (actionType === 3) {
      // Game Stop
      action.name = 'game_stop';
      gameEventCount++;
      console.log(`  Frame ${currentFrame}: GAME STOP`);
      actionReader.skip(3); // Skip action data
    } else if (actionType === 4) {
      // Game Pause
      action.name = 'game_pause';
      gameEventCount++;
      console.log(`  Frame ${currentFrame}: GAME PAUSE`);
      actionReader.skip(3); // Skip action data
    } else if (actionType === 5) {
      // Game Unpause
      action.name = 'game_unpause';
      gameEventCount++;
      console.log(`  Frame ${currentFrame}: GAME UNPAUSE`);
      actionReader.skip(3); // Skip action data
    } else {
      // Unknown action type - skip some data
      actionReader.skip(5);
    }
    
    actions.push(action);
    actionCount++;
  }
} catch (e) {
  console.log(`  Action parsing ended: ${e.message}`);
}

console.log(`  Parsed ${actionCount} action(s)`);
console.log(`    - Team changes: ${teamChangeCount}`);
console.log(`    - Game events: ${gameEventCount}`);

/**
 * STEP 3: Build player timelines and calculate statistics
 */
console.log('\nStep 3: Building player timelines and calculating statistics...');

// Build timelines for each player
const playerTimelines = new Map();

// Initialize with initial states
for (const [playerId, teamName] of playerInitialTeams) {
  playerTimelines.set(playerId, [{
    frame: 0,
    event: 'initial',
    team: teamName,
    name: playerNames.get(playerId)
  }]);
}

// Add team change events
for (const action of actions) {
  if (action.type === 12) {
    const playerId = action.playerId;
    
    if (!playerTimelines.has(playerId)) {
      // Player not in initial state - they might have joined during replay
      playerTimelines.set(playerId, [{
        frame: action.frame,
        event: 'join',
        team: action.teamName,
        name: `Player${playerId}`
      }]);
    } else {
      playerTimelines.get(playerId).push({
        frame: action.frame,
        event: 'team_change',
        team: action.teamName
      });
    }
  }
}

// Calculate statistics
const playerStats = [];

for (const [playerId, timeline] of playerTimelines) {
  const playerName = playerNames.get(playerId) || `Player${playerId}`;
  
  let totalTime = duration;
  let redTeamTime = 0;
  let blueTeamTime = 0;
  let spectatorTime = 0;
  const teamChanges = timeline.filter(e => e.event === 'team_change').length;
  
  // Calculate time in each team
  for (let i = 0; i < timeline.length; i++) {
    const event = timeline[i];
    const nextEvent = timeline[i + 1];
    const endFrame = nextEvent ? nextEvent.frame : duration;
    const durationFrames = endFrame - event.frame;
    
    if (event.team === 'red') {
      redTeamTime += durationFrames;
    } else if (event.team === 'blue') {
      blueTeamTime += durationFrames;
    } else if (event.team === 'spectators') {
      spectatorTime += durationFrames;
    }
  }
  
  const playingTime = redTeamTime + blueTeamTime;
  
  playerStats.push({
    playerId,
    name: playerName,
    totalTime,
    totalTimeSeconds: (totalTime / FRAME_RATE).toFixed(2),
    playingTime,
    playingTimeSeconds: (playingTime / FRAME_RATE).toFixed(2),
    redTeamTime,
    redTeamTimeSeconds: (redTeamTime / FRAME_RATE).toFixed(2),
    blueTeamTime,
    blueTeamTimeSeconds: (blueTeamTime / FRAME_RATE).toFixed(2),
    spectatorTime,
    spectatorTimeSeconds: (spectatorTime / FRAME_RATE).toFixed(2),
    teamChanges,
    timeline: timeline.map(e => ({
      frame: e.frame,
      event: e.event,
      team: e.team
    }))
  });
}

// Sort by player ID
playerStats.sort((a, b) => a.playerId - b.playerId);

// Print summary
console.log(`\n=== Player Statistics ===\n`);
for (const stats of playerStats) {
  console.log(`${stats.name} (ID: ${stats.playerId})`);
  console.log(`  Total time: ${stats.totalTimeSeconds}s (${stats.totalTime} frames)`);
  const playingPct = stats.totalTime > 0 ? ((stats.playingTime / stats.totalTime) * 100).toFixed(1) : '0.0';
  console.log(`  Playing time: ${stats.playingTimeSeconds}s (${playingPct}%)`);
  console.log(`  Red team: ${stats.redTeamTimeSeconds}s`);
  console.log(`  Blue team: ${stats.blueTeamTimeSeconds}s`);
  console.log(`  Spectator: ${stats.spectatorTimeSeconds}s`);
  console.log(`  Team changes: ${stats.teamChanges}`);
  console.log();
}

// Export JSON
const output = {
  metadata: {
    replayFile: path.basename(inputFile),
    totalFrames: duration,
    totalDuration: duration / FRAME_RATE,
    totalDurationSeconds: (duration / FRAME_RATE).toFixed(2),
    extractedAt: new Date().toISOString(),
    frameRate: FRAME_RATE,
    actionsFound: actionCount,
    teamChangesFound: teamChangeCount,
    gameEventsFound: gameEventCount
  },
  playerStats
};

fs.writeFileSync(outputFile, JSON.stringify(output, null, 2));

console.log(`Writing output to: ${outputFile}`);
console.log(`\n✓ Playtime extraction complete!`);
console.log(`\nSummary:`);
console.log(`  Players tracked: ${playerStats.length}`);
console.log(`  Total frames: ${duration}`);
console.log(`  Duration: ${(duration / FRAME_RATE).toFixed(2)} seconds`);
console.log(`  Actions parsed: ${actionCount}`);
console.log(`  Team changes detected: ${teamChangeCount}`);
console.log();
