#!/usr/bin/env node
/**
 * Test script to parse actions from HBR2 file directly
 */
const fs = require('fs');
const pako = require('pako');

const replayFile = process.argv[2] || 'src/replays/test_all_teams.hbr2';
console.log(`Reading: ${replayFile}`);

// Read and decompress
const data = fs.readFileSync(replayFile);

// Check header
const magic = data.toString('utf8', 0, 4);
console.log('Magic:', magic);

if (magic !== 'HBR2') {
  console.error('Not a valid HBR2 file');
  process.exit(1);
}

// Read version
const version = data.readUInt32LE(4);
console.log('Version:', version);

// Decompress the rest
const compressed = data.slice(8);
const decompressed = pako.inflate(compressed);

console.log('Decompressed size:', decompressed.length, 'bytes');

// Try to find action patterns
// According to Python code, actions are at the end of the file
// Let's look for patterns that might indicate team changes

// Action type 12 is PlayerTeamChange (fa)
// It should have: player_id (4 bytes int32) + team (1 byte uint8)

console.log('\nSearching for potential team change patterns...');
console.log('Looking at last 500 bytes of decompressed data...');

const start = Math.max(0, decompressed.length - 500);
for (let i = start; i < decompressed.length - 5; i++) {
  // Look for action type marker
  const actionType = decompressed[i];
  if (actionType === 12) { // PlayerTeamChange
    console.log(`Found action type 12 at offset ${i}`);
    console.log(`  Next 10 bytes: ${Array.from(decompressed.slice(i, i + 10)).map(b => b.toString(16).padStart(2, '0')).join(' ')}`);
  }
}

// Let's also check the beginning structure
console.log('\nFirst 100 bytes:');
console.log(Array.from(decompressed.slice(0, 100)).map((b, i) => {
  if (i % 16 === 0) return '\n' + i.toString().padStart(4, '0') + ': ' + b.toString(16).padStart(2, '0');
  return b.toString(16).padStart(2, '0');
}).join(' '));

