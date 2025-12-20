#!/usr/bin/env node
/**
 * Test script - Parse actions from decompressed HBR2 data
 */
const fs = require('fs');
const pako = require('pako');

const replayFile = process.argv[2] || 'src/replays/test_all_teams.hbr2';
console.log(`Reading: ${replayFile}\n`);

// Read file
const data = fs.readFileSync(replayFile);

// Check header
const magic = data.toString('utf8', 0, 4);
if (magic !== 'HBR2') {
  console.error('Not a valid HBR2 file');
  process.exit(1);
}

// Read version and duration (big-endian)
const version = data.readUInt32BE(4);
const duration = data.readUInt32BE(8);
console.log('Version:', version);
console.log('Duration:', duration, 'frames');

// Decompress with wbits=-15 (raw deflate)
const compressed = data.slice(12);
const decompressed = Buffer.from(pako.inflateRaw(compressed));
console.log('Decompressed size:', decompressed.length, 'bytes\n');

// Simple reader class
class Reader {
  constructor(buffer) {
    this.buffer = buffer;
    this.pos = 0;
  }
  
  readByte() {
    return this.buffer[this.pos++];
  }
  
  readUInt16BE() {
    const val = this.buffer.readUInt16BE(this.pos);
    this.pos += 2;
    return val;
  }
  
  readInt32LE() {
    const val = this.buffer.readInt32LE(this.pos);
    this.pos += 4;
    return val;
  }
  
  readVarint() {
    let result = 0;
    let shift = 0;
    let byte;
    do {
      byte = this.readByte();
      result |= (byte & 0x7F) << shift;
      shift += 7;
    } while (byte & 0x80);
    return result;
  }
  
  eof() {
    return this.pos >= this.buffer.length;
  }
  
  skip(n) {
    this.pos += n;
  }
  
  peekBytes(n) {
    return this.buffer.slice(this.pos, this.pos + n);
  }
}

const reader = new Reader(decompressed);

// Skip messages (we don't need them for team tracking)
// Messages start with count as varint
console.log('Skipping messages...');
const messageCount = reader.readVarint();
console.log(`Message count: ${messageCount}`);

// Skip each message (simplified - just skip until we find room data)
// This is complex, so let's try to find a pattern instead

// According to Python code, Room parsing comes after messages
// Let's try to find where actions start by looking for patterns

// For now, let's try the Python approach: skip known structures
// Actually, let me try a simpler approach: use the Python parser output as reference

console.log('\nTrying to find actions by pattern matching...');
console.log('Looking for action type 12 (PlayerTeamChange) patterns...');

// Action format:
// - frame_delta (varint)
// - sender (uint16 BE)  
// - action_type (byte)
// - action data...

// PlayerTeamChange (type 12):
// - player_id (int32 LE)
// - team (byte): 0=spec, 1=red, 2=blue

// Let's scan the whole buffer
let found = 0;
for (let i = 0; i < decompressed.length - 10 && found < 10; i++) {
  const actionType = decompressed[i];
  if (actionType === 12) {
    // Check if this looks like a valid action
    // Read player_id and team
    try {
      const playerId = decompressed.readInt32LE(i + 1);
      const team = decompressed[i + 5];
      
      // Validate: player_id should be reasonable (0-1000), team should be 0-2
      if (playerId >= 0 && playerId < 1000 && team >= 0 && team <= 2) {
        console.log(`\nPotential PlayerTeamChange at offset ${i}:`);
        console.log(`  Player ID: ${playerId}`);
        console.log(`  Team: ${team} (${['spectators', 'red', 'blue'][team]})`);
        console.log(`  Context: ${decompressed.slice(Math.max(0, i - 5), i + 10).toString('hex')}`);
        found++;
      }
    } catch (e) {
      // Skip invalid
    }
  }
}

if (found === 0) {
  console.log('No team change actions found.');
  console.log('\nLet me try searching more broadly...');
  
  // Try to find any byte sequence that matches team changes (0, 1, or 2)
  console.log('\nLooking for sequences that might indicate team changes...');
  for (let i = 0; i < Math.min(1000, decompressed.length); i += 50) {
    console.log(`Offset ${i.toString().padStart(4)}: ${decompressed.slice(i, i + 50).toString('hex')}`);
  }
}

