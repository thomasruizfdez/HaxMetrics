const fs = require('fs');
const pako = require('pako');

const replayData = fs.readFileSync('src/replays/test_all_teams.hbr2');
const decompressed = Buffer.from(pako.inflateRaw(replayData.slice(12)));

console.log('Manual byte-by-byte parsing from offset 785:\n');

console.log('Offset 785-809:');
for (let i = 785; i < 810; i++) {
  const byte = decompressed[i];
  console.log(`  ${i}: 0x${byte.toString(16).padStart(2, '0')} (${byte})`);
}

console.log('\n=== Parsing first action at 785 ===');
console.log('785: 0x1c (28) - This should be frame delta');
console.log('786-787: 0x00 0x00 (0) - Sender ID (uint16 BE)');
console.log('788: 0x0c (12) - Action type (PlayerTeamChange)');
console.log('789-792: 0x00 0x00 0x00 0x00 (0) - Player ID (int32 LE)');
console.log('793: 0x00 (0) - Team (spectators)');

console.log('\n=== Parsing second action at 794 ===');
console.log('794: 0x6f (111) - Frame delta');
console.log('795-796: 0x00 0x00 (0) - Sender ID');
console.log('797: 0x0c (12) - Action type');
console.log('798-801: 0x00 0x00 0x00 0x00 (0) - Player ID');
console.log('802: 0x02 (2) - Team (blue)');

console.log('\n=== Parsing third action at 803 ===');
console.log('803: 0x29 (41) - Frame delta');
console.log('804-805: 0x00 0x00 (0) - Sender ID');
console.log('806: 0x11 (17) - Action type (unknown)');

console.log('\nFrame calculation:');
console.log('  Action 1: frame = 0 + 28 = 28');
console.log('  Action 2: frame = 28 + 111 = 139');
console.log('  Action 3: frame = 139 + 41 = 180');

