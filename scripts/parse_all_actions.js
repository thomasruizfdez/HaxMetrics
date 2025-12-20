const fs = require('fs');
const pako = require('pako');
const BinaryReader = require('./binary_reader');

const replayData = fs.readFileSync('src/replays/test_all_teams.hbr2');
const duration = replayData.readUInt32BE(8);
const decompressed = Buffer.from(pako.inflateRaw(replayData.slice(12)));

console.log('Total duration:', duration, 'frames\n');

const reader = new BinaryReader(decompressed);
reader.setPosition(785);

console.log('Parsing ALL actions (not stopping at unknown types)...\n');

let frame = 0;
const allActions = [];

try {
  while (!reader.eof() && allActions.length < 50) {
    const startPos = reader.getPosition();
    const frameDelta = reader.readVarint();
    frame += frameDelta;
    const sender = reader.readUInt16BE();
    const actionType = reader.readByte();
    
    console.log(`Frame ${frame} (delta=${frameDelta}): Action type ${actionType} at pos ${startPos}`);
    
    const action = {
      frame,
      frameDelta,
      type: actionType,
      position: startPos
    };
    
    if (actionType === 12) {
      const playerId = reader.readInt32LE();
      const team = reader.readByte();
      action.playerId = playerId;
      action.team = ['spectators', 'red', 'blue'][team];
      console.log(`  -> PlayerTeamChange: player ${playerId} to ${action.team}`);
    } else if (actionType === 0) {
      console.log(`  -> PlayerJoined (can't parse without full structure)`);
      break; // Too complex
    } else {
      console.log(`  -> Unknown action type ${actionType}`);
      // Try to continue even with unknown types
      // Just skip some bytes and see what happens
    }
    
    allActions.push(action);
    
    // Safety: if we've gone too far past the known team changes, stop
    if (startPos > 850) break;
  }
} catch (e) {
  console.log(`\nStopped at position ${reader.getPosition()}: ${e.message}`);
}

console.log(`\n=== Summary ===`);
console.log(`Total actions parsed: ${allActions.length}`);

const teamChanges = allActions.filter(a => a.type === 12);
console.log(`Team changes: ${teamChanges.length}`);

for (const tc of teamChanges) {
  console.log(`  Frame ${tc.frame}: Player ${tc.playerId} -> ${tc.team}`);
}

