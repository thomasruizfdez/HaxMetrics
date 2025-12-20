const fs = require('fs');
const pako = require('pako');
const BinaryReader = require('./binary_reader');

const replayData = fs.readFileSync('src/replays/test_all_teams.hbr2');
const duration = replayData.readUInt32BE(8);
const decompressed = Buffer.from(pako.inflateRaw(replayData.slice(12)));

console.log('Total duration:', duration, 'frames =', (duration/60).toFixed(2), 'seconds');
console.log('Decompressed size:', decompressed.length, 'bytes');

// Parse from position 785 (we know this is where actions start)
const reader = new BinaryReader(decompressed);
reader.setPosition(785);

console.log('\nParsing actions from position 785...');

let frame = 0;
const actions = [];

try {
  for (let i = 0; i < 10; i++) {
    const startPos = reader.getPosition();
    const frameDelta = reader.readVarint();
    frame += frameDelta;
    const sender = reader.readUInt16BE();
    const actionType = reader.readByte();
    
    console.log(`\nAction ${i+1} at pos ${startPos}:`);
    console.log(`  Frame delta: ${frameDelta}`);
    console.log(`  Total frame: ${frame}`);
    console.log(`  Sender: ${sender}`);
    console.log(`  Action type: ${actionType}`);
    
    if (actionType === 12) {
      const playerId = reader.readInt32LE();
      const team = reader.readByte();
      const teamName = ['spectators', 'red', 'blue'][team];
      
      console.log(`  -> PlayerTeamChange: player ${playerId} to ${teamName}`);
      
      actions.push({
        frame,
        playerId,
        team: teamName,
        frameDelta
      });
    } else {
      console.log(`  -> Unknown action type, stopping`);
      break;
    }
  }
} catch (e) {
  console.log('Error:', e.message);
}

console.log('\n=== Summary ===');
console.log('Actions found:', actions.length);

if (actions.length > 0) {
  console.log('\n=== Time Breakdown ===');
  console.log('Frame 0 to', actions[0].frame, ': RED (initial)', 
              `= ${actions[0].frame} frames = ${(actions[0].frame/60).toFixed(2)}s`);
  
  for (let i = 0; i < actions.length; i++) {
    const action = actions[i];
    const nextAction = actions[i + 1];
    const endFrame = nextAction ? nextAction.frame : duration;
    const frames = endFrame - action.frame;
    const seconds = (frames / 60).toFixed(2);
    
    console.log(`Frame ${action.frame} to ${endFrame}: ${action.team.toUpperCase()}`,
                `= ${frames} frames = ${seconds}s`);
  }
  
  console.log('\nExpected by user:');
  console.log('  Red: ~2 seconds');
  console.log('  Spectators: ~2 seconds');
  console.log('  Blue: ~2 seconds');
}

