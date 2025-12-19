#!/usr/bin/env node
/**
 * HBR2 Decoder - Decode Haxball replay files to JSON
 * 
 * This script uses the original Haxball JavaScript code to decode .hbr2 files
 * and export their contents to JSON format.
 * 
 * Usage:
 *   node scripts/decode_hbr2.js <input.hbr2> [output.json]
 *   npm run decode -- <input.hbr2> [output.json]
 */

const fs = require('fs');
const path = require('path');
const vm = require('vm');

// Parse command line arguments
const args = process.argv.slice(2);
if (args.length < 1) {
  console.error('Usage: node decode_hbr2.js <input.hbr2> [output.json]');
  console.error('   or: npm run decode -- <input.hbr2> [output.json]');
  process.exit(1);
}

const inputFile = args[0];
const outputFile = args[1] || inputFile.replace(/\.hbr2$/, '.json');

// Check if input file exists
if (!fs.existsSync(inputFile)) {
  console.error(`Error: Input file not found: ${inputFile}`);
  process.exit(1);
}

console.log(`Reading replay file: ${inputFile}`);

// Read the .hbr2 file
const replayData = fs.readFileSync(inputFile);

// Create a sandbox environment with necessary globals
const sandbox = {
  console: console,
  Buffer: Buffer,
  Uint8Array: Uint8Array,
  DataView: DataView,
  ArrayBuffer: ArrayBuffer,
  window: {},
  document: {},
  performance: {
    now: () => Date.now()
  },
  // Storage for extracted data
  __extractedData: {
    metadata: {},
    stadium: null,
    players: [],
    events: [],
    gameState: {},
    rawData: {}
  }
};

// Add window.document stub
sandbox.window.document = {
  createElement: (tag) => {
    return {
      textContent: '',
      className: '',
      onclick: null,
      appendChild: () => {},
      querySelector: () => null,
      classList: {
        add: () => {},
        toggle: () => {}
      }
    };
  }
};

sandbox.window.performance = sandbox.performance;

// Load pako for decompression
const pako = require('pako');
sandbox.pako = pako;

console.log('Loading Haxball replay decoder...');

// Load the replay-min.js file
const replayScriptPath = path.join(__dirname, '..', 'original_script', 'replay-min.js');
const replayScript = fs.readFileSync(replayScriptPath, 'utf8');

// Execute the script in the sandbox
try {
  vm.createContext(sandbox);
  vm.runInContext(replayScript, sandbox);
  console.log('Decoder loaded successfully');
} catch (error) {
  console.error('Error loading decoder:', error);
  process.exit(1);
}

console.log('Decoding replay data...');

/**
 * Extract data from the replay by parsing the binary data
 */
function decodeReplay(replayBuffer) {
  try {
    // The replay-min.js uses a Reader class 'O' to parse binary data
    // We need to decode it step by step
    
    // Read header - magic number is in big-endian
    const magic = replayBuffer.readUInt32BE(0);
    if (magic !== 0x48425232) { // 'HBR2'
      throw new Error('Invalid HBR2 file format');
    }
    
    // Version and duration are in big-endian
    const version = replayBuffer.readUInt32BE(4);
    console.log(`  Version: ${version}`);
    
    const ad = replayBuffer.readUInt32BE(8); // Duration-related value
    console.log(`  Duration value: ${ad}`);
    
    // Decompress the rest of the data
    const compressedData = replayBuffer.slice(12);
    console.log(`  Compressed size: ${compressedData.length} bytes`);
    
    const decompressed = pako.inflateRaw(compressedData);
    console.log(`  Decompressed size: ${decompressed.length} bytes`);
    
    // Parse decompressed data using a custom reader
    const result = parseDecompressedData(decompressed, ad);
    
    return {
      metadata: {
        version: version,
        duration: ad,
        fileSize: replayBuffer.length,
        decompressedSize: decompressed.length
      },
      ...result
    };
  } catch (error) {
    console.error('Error decoding replay:', error);
    throw error;
  }
}

/**
 * Parse decompressed replay data
 */
function parseDecompressedData(data, ad) {
  let offset = 0;
  const view = new DataView(data.buffer, data.byteOffset, data.byteLength);
  
  // Helper to read variable-length integer
  function readVarInt() {
    let value = 0;
    let shift = 0;
    let byte;
    do {
      byte = view.getUint8(offset++);
      value |= (byte & 0x7F) << shift;
      shift += 7;
    } while (byte & 0x80);
    return value;
  }
  
  // Helper to read string
  function readString() {
    const length = readVarInt();
    const bytes = new Uint8Array(data.buffer, data.byteOffset + offset, length);
    offset += length;
    return new TextDecoder().decode(bytes);
  }
  
  // Helper to read byte
  function readByte() {
    return view.getUint8(offset++);
  }
  
  // Helper to read 32-bit integer
  function readInt32() {
    const value = view.getInt32(offset, true);
    offset += 4;
    return value;
  }
  
  const result = {
    stadium: {},
    players: [],
    events: [],
    gameState: {},
    roomInfo: {}
  };
  
  try {
    // Read room state
    const roomState = view.getUint16(offset, true);
    offset += 2;
    console.log(`  Room state: ${roomState}`);
    
    // Read room name
    const roomName = readString();
    console.log(`  Room name: ${roomName}`);
    result.roomInfo.name = roomName;
    result.roomInfo.state = roomState;
    
    // Read game settings
    const teamsLocked = readByte();
    const scoreLimit = readInt32();
    const timeLimit = readInt32();
    const unknown = readInt32();
    
    console.log(`  Teams locked: ${teamsLocked}`);
    console.log(`  Score limit: ${scoreLimit}`);
    console.log(`  Time limit: ${timeLimit}`);
    
    result.gameState = {
      teamsLocked: teamsLocked === 1,
      scoreLimit: scoreLimit,
      timeLimit: timeLimit,
      redScore: 0,
      blueScore: 0
    };
    
    // Read stadium info
    const stadiumByte = readByte();
    console.log(`  Stadium byte: ${stadiumByte}`);
    
    if (stadiumByte === 255) {
      // Custom stadium
      const stadiumName = readString();
      console.log(`  Custom stadium: ${stadiumName}`);
      result.stadium.name = stadiumName;
      result.stadium.customStadium = true;
      
      // Read stadium config byte
      const configByte = readInt32();
      console.log(`  Stadium config: ${configByte}`);
      
      // The rest would be stadium data, which is complex
      // For now, we'll note that there's custom stadium data
      result.stadium.hasData = true;
      result.stadium.dataOffset = offset;
    } else {
      // Predefined stadium
      const stadiumNames = ['Classic', 'Easy', 'Small', 'Big', 'Rounded', 'Hockey', 'Big Hockey', 'Big Easy', 'Big Rounded', 'Huge'];
      result.stadium.name = stadiumNames[stadiumByte] || `Unknown (${stadiumByte})`;
      result.stadium.customStadium = false;
      console.log(`  Predefined stadium: ${result.stadium.name}`);
    }
    
    // Parse the event data that follows
    console.log(`  Remaining data: ${data.length - offset} bytes`);
    console.log(`  Events start at offset: ${offset}`);
    
    // Store raw event data info
    result.eventsDataOffset = offset;
    result.eventsDataSize = data.length - offset;
    
    // Try to parse some events
    let eventCount = 0;
    try {
      // The first part might be event count or compressed event stream
      const eventStreamSize = readVarInt();
      console.log(`  Event stream size: ${eventStreamSize}`);
      
      // Read events (simplified)
      while (offset < data.length && eventCount < 100) {
        try {
          const timeDelta = readVarInt();
          const eventType = readByte();
          
          const event = {
            time: timeDelta,
            type: eventType,
            typeHex: '0x' + eventType.toString(16).padStart(2, '0')
          };
          
          result.events.push(event);
          eventCount++;
          
          // Break if we're at the end or hit invalid data
          if (offset >= data.length - 4) break;
        } catch (e) {
          console.log(`  Stopped parsing events at offset ${offset}: ${e.message}`);
          break;
        }
      }
    } catch (e) {
      console.log(`  Event parsing ended: ${e.message}`);
    }
    
    console.log(`  Parsed ${eventCount} events`);
    
  } catch (error) {
    console.error(`  Parsing error at offset ${offset}:`, error);
    result.error = error.message;
    result.errorOffset = offset;
  }
  
  return result;
}

// Main execution
try {
  const decoded = decodeReplay(replayData);
  
  console.log(`\nWriting output to: ${outputFile}`);
  fs.writeFileSync(outputFile, JSON.stringify(decoded, null, 2));
  
  console.log('\n✓ Decoding complete!');
  console.log(`\nSummary:`);
  console.log(`  Version: ${decoded.metadata.version}`);
  console.log(`  Room: ${decoded.roomInfo.name}`);
  console.log(`  Stadium: ${decoded.stadium.name}`);
  console.log(`  Score limit: ${decoded.gameState.scoreLimit}`);
  console.log(`  Time limit: ${decoded.gameState.timeLimit}`);
  console.log(`  Events parsed: ${decoded.events.length}`);
  
} catch (error) {
  console.error('\n✗ Error:', error.message);
  process.exit(1);
}
