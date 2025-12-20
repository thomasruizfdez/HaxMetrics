const fs = require('fs');
const pako = require('pako');

const replayData = fs.readFileSync('src/replays/test_all_teams.hbr2');
const decompressed = Buffer.from(pako.inflateRaw(replayData.slice(12)));

console.log('Bytes around position 88:');
for (let i = 85; i < 95; i++) {
  console.log(`  ${i}: 0x${decompressed[i].toString(16).padStart(2, '0')} (${decompressed[i]})`);
}

