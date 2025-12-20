const fs = require('fs');
const pako = require('pako');
const BinaryReader = require('./binary_reader');

const replayData = fs.readFileSync('src/replays/test_all_teams.hbr2');
const decompressed = Buffer.from(pako.inflateRaw(replayData.slice(12)));

console.log('Searching for actions BEFORE position 785...\n');

// Try parsing from different earlier positions
const positions = [700, 720, 740, 760, 770, 775, 780];

for (const startPos of positions) {
  console.log(`\n=== Trying position ${startPos} ===`);
  
  const reader = new BinaryReader(decompressed);
  reader.setPosition(startPos);
  
  try {
    let frame = 0;
    for (let i = 0; i < 5; i++) {
      const fd = reader.readVarint();
      frame += fd;
      const sender = reader.readUInt16BE();
      const type = reader.readByte();
      
      console.log(`  Frame ${frame} (delta=${fd}): type=${type}`);
      
      if (type === 12) {
        const pid = reader.readInt32LE();
        const team = reader.readByte();
        console.log(`    -> TeamChange: player ${pid} to ${['spec', 'red', 'blue'][team]}`);
      } else if (type > 20) {
        break;
      }
    }
  } catch (e) {
    console.log(`  Failed: ${e.message}`);
  }
}

