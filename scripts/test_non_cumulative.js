const fs = require('fs');
const pako = require('pako');

const replayData = fs.readFileSync('src/replays/test_all_teams.hbr2');
const duration = replayData.readUInt32BE(8);
const decompressed = Buffer.from(pako.inflateRaw(replayData.slice(12)));

console.log('Testing if frame deltas are NON-cumulative (each relative to frame 0):\n');

console.log('Action 1: frame_delta=28 -> frame=28');
console.log('Action 2: frame_delta=111 -> frame=111 (not 28+111=139)');
console.log('Action 3: frame_delta=41 -> frame=41 (not 139+41=180)');

console.log('\nIf non-cumulative, timeline would be:');
console.log('  Frame 0-28: red (0.47s)');
console.log('  Frame 28-41: spectators (0.22s) <- way too short!');
console.log('  Frame 41-111: ??? (1.17s)');
console.log('  Frame 111-603: blue (8.20s)');

console.log('\nThis doesn\'t make sense. Frame deltas must be cumulative.');

console.log('\n\nActual (cumulative) timeline:');
console.log('  Frame 0-28: red (0.47s)');
console.log('  Frame 28-139: spectators (1.85s)');
console.log('  Frame 139-603: blue (7.73s)');

