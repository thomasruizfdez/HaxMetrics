const fs = require('fs');
const pako = require('pako');

const replayData = fs.readFileSync('src/replays/test_all_teams.hbr2');
const decompressed = Buffer.from(pako.inflateRaw(replayData.slice(12)));

console.log('Searching entire buffer for action type 12 (PlayerTeamChange)...\n');

const found = [];

for (let i = 0; i < decompressed.length - 6; i++) {
  if (decompressed[i] === 12) {
    try {
      const playerId = decompressed.readInt32LE(i + 1);
      const team = decompressed[i + 5];
      
      if (playerId >= 0 && playerId < 100 && team >= 0 && team <= 2) {
        const teamName = ['spectators', 'red', 'blue'][team];
        console.log(`Offset ${i}: PlayerTeamChange - player ${playerId} to ${teamName}`);
        console.log(`  Bytes: ${decompressed.slice(i, i + 10).toString('hex')}`);
        found.push({ offset: i, playerId, team: teamName });
      }
    } catch (e) {}
  }
}

console.log(`\nTotal PlayerTeamChange actions found: ${found.length}`);

// Also search for other potential action types
console.log('\n\nSearching for action type 0 (PlayerJoined)...');
for (let i = 0; i < decompressed.length - 20; i++) {
  if (decompressed[i] === 0) {
    // Check if next bytes look like player_id (int32)
    try {
      const playerId = decompressed.readInt32LE(i + 1);
      if (playerId >= 0 && playerId < 100) {
        console.log(`Offset ${i}: Possible PlayerJoined - player ${playerId}`);
      }
    } catch (e) {}
  }
}

