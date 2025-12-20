/**
 * Helper module to find where actions start in a decompressed HBR2 buffer
 */

const BinaryReader = require('./binary_reader');

/**
 * Find the start position of the action stream in decompressed data
 * Returns the position or -1 if not found
 */
function findActionsStart(decompressed, messagesEndPos) {
  // Strategy: Search backwards from the end for valid action patterns
  // Then work forward to find the actual start
  
  const searchStart = messagesEndPos;
  const searchEnd = decompressed.length - 50;
  
  // Look for action type 12 (PlayerTeamChange) which has a distinctive pattern
  let lastGoodActionPos = -1;
  
  for (let i = searchEnd; i >= searchStart; i--) {
    if (decompressed[i] === 12) { // Action type 12
      try {
        const playerId = decompressed.readInt32LE(i + 1);
        const team = decompressed[i + 5];
        
        if (playerId >= 0 && playerId < 1000 && team >= 0 && team <= 2) {
          lastGoodActionPos = i;
          break;
        }
      } catch (e) {}
    }
  }
  
  if (lastGoodActionPos < 0) {
    // No PlayerTeamChange found, look for other action types
    // Try to find any byte sequence that looks like actions
    // Actions typically start with small varint (frame delta < 1000)
    // followed by uint16 BE (sender < 1000)
    // followed by action type (< 20)
    
    for (let pos = searchEnd - 100; pos >= searchStart; pos--) {
      try {
        const reader = new BinaryReader(decompressed);
        reader.setPosition(pos);
        
        // Try to parse one action
        const frameDelta = reader.readVarint();
        if (frameDelta > 10000) continue; // Too large
        
        const sender = reader.readUInt16BE();
        if (sender > 10000) continue; // Too large
        
        const actionType = reader.readByte();
        if (actionType >= 0 && actionType < 20) {
          lastGoodActionPos = pos + 3; // Approximate action data start
          break;
        }
      } catch (e) {}
    }
  }
  
  if (lastGoodActionPos < 0) {
    return -1; // Could not find actions
  }
  
  // Now work backwards from lastGoodActionPos to find the actual start
  // Actions are sequential, so we look for the first valid action
  
  for (let pos = lastGoodActionPos - 200; pos < lastGoodActionPos; pos++) {
    try {
      const reader = new BinaryReader(decompressed);
      reader.setPosition(pos);
      
      // Try to parse several actions and see if we eventually reach lastGoodActionPos
      let currentPos = pos;
      let foundTarget = false;
      
      for (let i = 0; i < 50; i++) {
        const startPos = reader.getPosition();
        const frameDelta = reader.readVarint();
        const sender = reader.readUInt16BE();
        const actionType = reader.readByte();
        
        // Check if we're near our known good position
        if (Math.abs(startPos - lastGoodActionPos) < 10) {
          foundTarget = true;
          return pos;
        }
        
        // Try to skip action data
        if (actionType === 0) { // PlayerJoined
          reader.readInt32LE();
          reader.readString();
          reader.readString();
          const hasCountry = reader.readByte();
          if (hasCountry) reader.readString();
          reader.readByte();
        } else if (actionType === 1) { // PlayerLeft
          reader.readInt32LE();
        } else if (actionType === 12) { // PlayerTeamChange
          reader.readInt32LE();
          reader.readByte();
        } else {
          break; // Unknown action
        }
        
        if (reader.getPosition() >= decompressed.length - 10) break;
      }
      
      if (foundTarget) {
        return pos;
      }
    } catch (e) {}
  }
  
  // Fallback: return a position slightly before lastGoodActionPos
  return Math.max(searchStart, lastGoodActionPos - 100);
}

module.exports = { findActionsStart };
