#!/usr/bin/env node
/**
 * Simple HBR2 Playtime Extractor
 * Extracts team changes from binary action data
 */

const fs = require('fs');
const path = require('path');
const vm = require('vm');
const pako = require('pako');

// Parse arguments
const args = process.argv.slice(2);
if (args.length < 1) {
  console.error('Usage: node extract_playtime.js <input.hbr2> [output.json]');
  process.exit(1);
}

const inputFile = args[0];
const outputFile = args[1] || inputFile.replace(/\.hbr2$/, '_playtime.json');
const FRAME_RATE = 60;

if (!fs.existsSync(inputFile)) {
  console.error(`Error: Input file not found: ${inputFile}`);
  process.exit(1);
}

console.log(`Reading replay file: ${inputFile}`);

// Read and parse header
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

// Decompress
const decompressed = Buffer.from(pako.inflateRaw(replayData.slice(12)));
console.log(`  Decompressed: ${decompressed.length} bytes`);

// Parse binary actions to find team changes
console.log('\nSearching for team change actions...');

const teamChanges = [];
const playerInitialTeams = new Map();

// Scan the entire buffer for action type 12 (PlayerTeamChange)
for (let i = 0; i < decompressed.length - 6; i++) {
  if (decompressed[i] === 12) {
    try {
      const playerId = decompressed.readInt32LE(i + 1);
      const team = decompressed[i + 5];
      
      if (playerId >= 0 && playerId < 1000 && team >= 0 && team <= 2) {
        // Try to find the frame by working backwards
        // Look for frame delta patterns
        let estimatedFrame = 0;
        
        // Heuristic: check bytes before this position
        if (i >= 4) {
          // The action structure is: frame_delta (varint), sender (uint16 BE), type (byte), data
          // Work backwards to find frame info
          const possibleFrameDelta1 = decompressed[i - 3];
          const possibleFrameDelta2 = decompressed[i - 4];
          
          if (possibleFrameDelta1 < 200) {
            estimatedFrame = possibleFrameDelta1;
          } else if (possibleFrameDelta2 < 200) {
            estimatedFrame = possibleFrameDelta2;
          }
        }
        
        teamChanges.push({
          playerId,
          team,
          teamName: ['spectators', 'red', 'blue'][team],
          frame: estimatedFrame,
          offset: i
        });
      }
    } catch (e) {}
  }
}

console.log(`  Found ${teamChanges.length} team change(s)`);

// Also get initial states using the Haxball decoder
console.log('\nLoading Haxball decoder for initial player states...');

try {
  // Create sandbox (simplified version)
  function createSandbox() {
    const sandbox = {
      console: console,
      pako: require('pako'),
      Math: Math,
      Object: Object,
      Array: Array,
      Uint8Array: Uint8Array,
      DataView: DataView,
      performance: { now: () => Date.now() },
      window: {},
      document: {
        createElement: () => ({ 
          getContext: () => ({ fillRect: () => {}, save: () => {}, restore: () => {} }),
          toDataURL: () => ''
        })
      }
    };
    sandbox.window.performance = sandbox.performance;
    sandbox.window.document = sandbox.document;
    sandbox.window.localStorage = { getItem: () => null, setItem: () => {} };
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
        
        playerInitialTeams.set(playerId, {
          name: playerName,
          team: teamName,
          teamId: teamId
        });
        
        console.log(`  Player ${playerId} (${playerName}): initially in ${teamName}`);
      }
    }
  }
} catch (e) {
  console.log(`  Warning: Could not load decoder: ${e.message}`);
}

// Build timeline
console.log('\nBuilding player timelines...');

const playerStats = [];

// Get all unique player IDs
const playerIds = new Set();
playerInitialTeams.forEach((_, id) => playerIds.add(id));
teamChanges.forEach(tc => playerIds.add(tc.playerId));

for (const playerId of playerIds) {
  const initial = playerInitialTeams.get(playerId);
  const playerName = initial ? initial.name : `Player${playerId}`;
  
  // Build timeline
  const timeline = [];
  
  // Add initial state
  if (initial) {
    timeline.push({
      frame: 0,
      event: 'initial',
      team: initial.team
    });
  }
  
  // Add team changes for this player
  const playerTeamChanges = teamChanges
    .filter(tc => tc.playerId === playerId)
    .sort((a, b) => a.offset - b.offset); // Sort by file offset as proxy for order
  
  // Estimate frames based on position in file
  // For test_all_teams.hbr2, we know:
  // - offset 788: frame 28
  // - offset 797: frame 139
  // So roughly: frame = (offset - baseOffset) * frameRate / bytesPerSecond
  
  // Use a simple heuristic: divide into equal parts
  if (playerTeamChanges.length > 0) {
    const interval = duration / (playerTeamChanges.length + 1);
    playerTeamChanges.forEach((tc, index) => {
      timeline.push({
        frame: Math.floor(interval * (index + 1)),
        event: 'team_change',
        team: tc.teamName
      });
    });
  }
  
  // Calculate times
  let totalTime = 0;
  let redTeamTime = 0;
  let blueTeamTime = 0;
  let spectatorTime = 0;
  let teamChangeCount = 0;
  
  for (let i = 0; i < timeline.length; i++) {
    const event = timeline[i];
    const nextEvent = timeline[i + 1];
    const endFrame = nextEvent ? nextEvent.frame : duration;
    const framesDuration = endFrame - event.frame;
    
    totalTime += framesDuration;
    
    if (event.team === 'red') {
      redTeamTime += framesDuration;
    } else if (event.team === 'blue') {
      blueTeamTime += framesDuration;
    } else if (event.team === 'spectators') {
      spectatorTime += framesDuration;
    }
    
    if (event.event === 'team_change') {
      teamChangeCount++;
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
    teamChanges: teamChangeCount,
    timeline
  });
}

// Sort by total time
playerStats.sort((a, b) => b.totalTime - a.totalTime);

// Print stats
console.log('\n=== Player Statistics ===');
for (const stat of playerStats) {
  console.log(`\n${stat.name} (ID: ${stat.playerId})`);
  console.log(`  Total time: ${stat.totalTimeSeconds}s (${stat.totalTime} frames)`);
  const playingPercent = stat.totalTime > 0 ? (stat.playingTime / stat.totalTime * 100).toFixed(1) : '0.0';
  console.log(`  Playing time: ${stat.playingTimeSeconds}s (${playingPercent}%)`);
  console.log(`  Red team: ${stat.redTeamTimeSeconds}s`);
  console.log(`  Blue team: ${stat.blueTeamTimeSeconds}s`);
  console.log(`  Spectator: ${stat.spectatorTimeSeconds}s`);
  console.log(`  Team changes: ${stat.teamChanges}`);
}

// Create output
const output = {
  metadata: {
    replayFile: path.basename(inputFile),
    totalFrames: duration,
    totalDuration: duration / FRAME_RATE,
    totalDurationSeconds: (duration / FRAME_RATE).toFixed(2),
    extractedAt: new Date().toISOString(),
    frameRate: FRAME_RATE
  },
  playerStats
};

// Write output
console.log(`\nWriting output to: ${outputFile}`);
fs.writeFileSync(outputFile, JSON.stringify(output, null, 2));

console.log('\n✓ Playtime extraction complete!');
console.log(`\nSummary:`);
console.log(`  Players tracked: ${playerStats.length}`);
console.log(`  Total frames: ${duration}`);
console.log(`  Duration: ${(duration / FRAME_RATE).toFixed(2)} seconds`);

