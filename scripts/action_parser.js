/**
 * Action parser for HBR2 replays
 * Parses the action stream to extract player events (team changes, joins, leaves, etc.)
 */

const BinaryReader = require('./binary_reader');

/**
 * Action types (matching Python parser)
 */
const ACTION_TYPES = {
  PLAYER_JOINED: 0,
  PLAYER_LEFT: 1,
  PLAYER_ADMIN_CHANGE: 2,
  PLAYER_INPUT: 3,
  CHAT_MESSAGE: 4,
  // ... others we don't need for playtime
  PLAYER_TEAM_CHANGE: 12
};

/**
 * Parse actions from the binary reader
 * Returns array of actions with frame, type, and data
 */
function parseActions(reader) {
  const actions = [];
  let frame = 0;
  let actionCount = 0;
  const maxActions = 10000; // Safety limit
  
  const startPos = reader.getPosition();
  console.log(`  Starting action parsing at position: ${startPos}`);
  
  try {
    while (!reader.eof() && actionCount < maxActions) {
      // Read frame delta (varint)
      const frameDelta = reader.readVarint();
      frame += frameDelta;
      
      // Read sender ID (uint16 big-endian)
      const sender = reader.readUInt16BE();
      
      // Read action type (byte)
      const actionType = reader.readByte();
      
      // Parse specific action types we care about
      let action = null;
      
      if (actionType === 0) { // PlayerJoined
        action = parsePlayerJoined(reader);
        action.type = 'PLAYER_JOINED';
      } else if (actionType === 1) { // PlayerLeft
        action = parsePlayerLeft(reader);
        action.type = 'PLAYER_LEFT';
      } else if (actionType === 12) { // PlayerTeamChange
        action = parsePlayerTeamChange(reader);
        action.type = 'PLAYER_TEAM_CHANGE';
      } else {
        // Skip unknown action types
        // We can't properly skip without knowing the action structure
        // So we'll just try to continue and see what happens
        continue;
      }
      
      if (action) {
        action.frame = frame;
        action.sender = sender;
        actions.push(action);
        actionCount++;
      }
    }
  } catch (e) {
    console.log(`  Action parsing stopped at position ${reader.getPosition()}: ${e.message}`);
    console.log(`  Parsed ${actionCount} actions before error`);
  }
  
  console.log(`  Total actions parsed: ${actions.length}`);
  return actions;
}

/**
 * Parse PlayerJoined action
 * Format: player_id (int32), name (string), avatar (string), country (string or null), admin (bool)
 */
function parsePlayerJoined(reader) {
  const playerId = reader.readInt32LE();
  const name = reader.readString();
  const avatar = reader.readString();
  
  // Country is optional (indicated by a flag byte)
  let country = null;
  const hasCountry = reader.readByte();
  if (hasCountry) {
    country = reader.readString();
  }
  
  const isAdmin = reader.readByte() !== 0;
  
  return {
    playerId,
    name,
    avatar,
    country,
    isAdmin
  };
}

/**
 * Parse PlayerLeft action
 * Format: player_id (int32)
 */
function parsePlayerLeft(reader) {
  const playerId = reader.readInt32LE();
  return { playerId };
}

/**
 * Parse PlayerTeamChange action
 * Format: player_id (int32), team (byte: 0=spec, 1=red, 2=blue)
 */
function parsePlayerTeamChange(reader) {
  const playerId = reader.readInt32LE();
  const team = reader.readByte();
  return { playerId, team };
}

module.exports = {
  parseActions,
  ACTION_TYPES
};
