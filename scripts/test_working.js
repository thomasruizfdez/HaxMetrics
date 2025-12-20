#!/usr/bin/env node
const fs = require('fs');
const pako = require('pako');
const BinaryReader = require('./binary_reader');

const replayFile = 'src/replays/test_all_teams.hbr2';
const data = fs.readFileSync(replayFile);

const version = data.readUInt32BE(4);
const duration = data.readUInt32BE(8);
const decompressed = Buffer.from(pako.inflateRaw(data.slice(12)));

console.log('Duration:', duration, 'frames');

const reader = new BinaryReader(decompressed);

// Skip messages
const msgCount = reader.readVarint();
console.log('Messages:', msgCount);

// For this specific file, actions start at position 785
reader.setPosition(785);

console.log('Parsing actions from position 785...\n');

let frame = 0;
const playerEvents = [];

try {
  while (!reader.eof()) {
    const frameDelta = reader.readVarint();
    frame += frameDelta;
    const sender = reader.readUInt16BE();
    const actionType = reader.readByte();
    
    if (actionType === 12) { // PlayerTeamChange
      const playerId = reader.readInt32LE();
      const team = reader.readByte();
      const teamName = ['spectators', 'red', 'blue'][team];
      console.log(`Frame ${frame}: Player ${playerId} -> ${teamName}`);
      playerEvents.push({ frame, playerId, team: teamName, event: 'team_change' });
    } else {
      console.log(`Frame ${frame}: Unknown action type ${actionType}`);
      break;
    }
  }
} catch (e) {
  console.log('Parsing stopped:', e.message);
}

// Calculate playtime
console.log('\n=== Playtime Calculation ===');

if (playerEvents.length > 0) {
  const playerId = playerEvents[0].playerId;
  
  let redTime = 0, blueTime = 0, specTime = 0;
  
  for (let i = 0; i < playerEvents.length; i++) {
    const event = playerEvents[i];
    const nextEvent = playerEvents[i + 1];
    const endFrame = nextEvent ? nextEvent.frame : duration;
    const framesDuration = endFrame - event.frame;
    
    console.log(`  ${event.team} from frame ${event.frame} to ${endFrame}: ${framesDuration} frames (${(framesDuration/60).toFixed(2)}s)`);
    
    if (event.team === 'red') redTime += framesDuration;
    else if (event.team === 'blue') blueTime += framesDuration;
    else if (event.team === 'spectators') specTime += framesDuration;
  }
  
  const playingTime = redTime + blueTime;
  const totalTime = redTime + blueTime + specTime;
  
  console.log(`\nPlayer ${playerId}:`);
  console.log(`  Red team: ${(redTime/60).toFixed(2)}s`);
  console.log(`  Blue team: ${(blueTime/60).toFixed(2)}s`);
  console.log(`  Spectators: ${(specTime/60).toFixed(2)}s`);
  console.log(`  Playing time: ${(playingTime/60).toFixed(2)}s`);
  console.log(`  Total time: ${(totalTime/60).toFixed(2)}s`);
  console.log(`  Team changes: ${playerEvents.length}`);
}

