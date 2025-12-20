# Playtime Extraction - Technical Documentation

## Overview

The `extract_playtime.js` script extracts detailed player playtime statistics from Haxball replay (.hbr2) files by combining the original Haxball decoder with binary action stream parsing for maximum accuracy.

## Purpose

This tool was created to:

1. **Calculate accurate playtime statistics** for each player in a replay
2. **Distinguish between playing time and spectating time**
3. **Track time per team** (red vs blue)
4. **Extract frame-accurate team change events**
5. **Provide reliable data** for player performance analysis

## Architecture - Three-Step Approach

The script uses a comprehensive multi-stage process:

### Step 1: Initial State Extraction (Haxball Decoder)

Uses the original Haxball decoder to:
- Parse replay file structure and validate integrity
- Extract player names, IDs, and initial team assignments
- Get replay metadata (duration, version, timestamps)

### Step 2: Binary Action Parsing

Parses the decompressed replay data to:
- Locate the action stream start position
- Extract PlayerTeamChange actions (type 12) with exact frame numbers
- Parse frame deltas to calculate cumulative frame timing
- Build a complete list of team change events

### Step 3: Statistics Calculation

Combines data from Steps 1 & 2 to:
- Build complete player timelines with all state changes
- Calculate time spent in each team (red, blue, spectators)
- Compute playing time vs spectator time
- Generate JSON output with frame-accurate statistics

## How It Works

### Data Flow

```
1. Read .hbr2 file
   ↓
2. Decompress with pako (zlib)
   ↓
3. Load Haxball decoder (Step 1)
   → Extract: player names, IDs, initial teams
   ↓
4. Parse binary action stream (Step 2)
   → Find action start position
   → Parse PlayerTeamChange actions
   → Extract frame numbers
   ↓
5. Build player timelines (Step 3)
   → Combine initial states + team changes
   → Calculate durations per team
   ↓
6. Export JSON with statistics
```

### Key Components

#### 1. Sandbox Environment

Creates a complete mock browser environment including:
- Canvas 2D context
- Audio API  
- DOM elements
- localStorage/sessionStorage
- Performance API
- Event system

This allows the original Haxball code to run in Node.js without modification.

#### 2. Script Patching

Uses multi-pattern matching to expose internal Haxball classes:
- `ab` - Decoder class (parses replay binary data)
- `ca` - Room class (game room state)
- `rb` - Message classes (for custom stadiums)

The patching works by inserting exposure code before the Haxball code's initialization.

#### 3. Player State Tracking

Tracks players through:
- Initial state extraction from `room.L` (player list)
- Final state extraction after replay processing
- Timeline construction with join/leave/team change events

#### 4. Playtime Calculation

For each player, calculates:
- **Total time**: Frames from first appearance to end of replay
- **Playing time**: Frames in red or blue team
- **Spectator time**: Frames in spectators
- **Time per team**: Separate counters for red and blue
- **Team changes**: Number of team switches

## Limitations

### Current Implementation

The current version has these limitations:

1. **No frame-by-frame processing**: The script extracts initial and final states but doesn't process every frame of the replay. This means:
   - Players who join and leave during the replay are not captured
   - Team changes during the replay are not detected
   - The timeline only shows initial state

2. **Event markers are limited**: The decoder's event markers (`decoder.eg`) are UI events and don't contain detailed player tracking data

3. **No action data processing**: The script doesn't process the low-level action data that contains detailed player events

### Why These Limitations Exist

The Haxball replay decoder processes the entire replay internally during initialization. To get frame-by-frame player events, we would need to:

1. **Hook into internal step function**: Intercept the decoder's frame advancement to capture state changes
2. **Process raw action data**: Parse the binary action stream ourselves (24 action types documented in the Python parser)
3. **Use alternative decoder**: Create a custom decoder that processes actions frame-by-frame

## Future Improvements

### Phase 1: Frame-by-Frame Processing (High Priority)

Hook into the decoder's internal methods to capture events as they happen:

```javascript
// Pseudo-code for future implementation
const originalStep = decoder.step || decoder.Uj;
decoder.step = function() {
  // Capture pre-step state
  const preState = capturePlayerState(room);
  
  // Execute original step
  const result = originalStep.apply(this, arguments);
  
  // Capture post-step state and detect changes
  const postState = capturePlayerState(room);
  detectPlayerChanges(preState, postState);
  
  return result;
};
```

### Phase 2: Action Stream Processing

Process the raw action data directly:

```javascript
// Action types relevant for playtime:
// Type 0 (PlayerJoined) - Player enters room
// Type 1 (PlayerLeft) - Player leaves room
// Type 4 (PlayerTeamChange) - Player changes team
```

This would provide:
- Exact frame of each event
- Complete timeline reconstruction
- Support for players who join/leave mid-game

### Phase 3: Enhanced Statistics

Add additional metrics:
- Ball touches per player
- Kicks made
- Distance traveled
- Time near ball
- Heat maps

## Usage

### Basic Usage

```bash
# Extract playtime from a replay
node scripts/extract_playtime.js <input.hbr2> [output.json]

# Or use npm script
npm run playtime -- <input.hbr2> [output.json]
```

### Examples

```bash
# Test with sample replay
npm run playtime:test

# Process specific replay
npm run playtime -- src/replays/game.hbr2 results.json

# Output to specific location
node scripts/extract_playtime.js src/replays/game.hbr2 /tmp/stats.json
```

### Output Format

See [JSON_OUTPUT_FORMAT.md](./JSON_OUTPUT_FORMAT.md) for detailed output structure.

## Technical Details

### Frame Rate

- Haxball replays use **60 FPS** (frames per second)
- 1 frame = ~16.67ms
- To convert frames to seconds: `frames / 60`

### Team IDs

- `0` = Spectators
- `1` = Red team
- `2` = Blue team

### Player Structure

Internal player object properties:
- `aa` - Player ID (unique identifier)
- `C` - Player name
- `fa` - Team object
- `fa.Ha` - Team ID (0, 1, or 2)
- `cb` - Admin status
- `w` - Disc (physics object)

### Room Structure

Internal room object properties:
- `L` - Array of player objects
- `D` - Game state (if game is active)
- `I` - Stadium
- `Fa` - Teams array [spectators, red, blue]

## Dependencies

- **Node.js**: v14+ required
- **pako**: Compression library for .hbr2 decompression
- **vm**: Node.js VM module for sandboxing
- **original_script/replay-min.js**: Original Haxball decoder

## Troubleshooting

### "pako module not found"

```bash
cd /path/to/HaxMetrics
npm install
```

### "Required classes not exposed"

The original Haxball code may have changed. Run the debug script to see available classes:

```bash
npm run debug:replay
```

Then update the `patchReplayScript` function in `extract_playtime.js` with the correct class names.

### "replay-min.js not found"

Ensure the original Haxball decoder is in `original_script/replay-min.js`.

### Empty timeline / No team changes detected

This is expected in the current version. The script only captures initial and final states. See [Limitations](#limitations) above.

## Comparison with Python Parser

| Feature | extract_playtime.js | Python Parser |
|---------|---------------------|---------------|
| Uses original code | ✅ Yes | ❌ No |
| Frame-by-frame | ❌ Limited | ✅ Yes (planned) |
| Player join/leave | ❌ Limited | ✅ Yes (planned) |
| Team changes | ❌ Limited | ✅ Yes (planned) |
| Reliability | ✅ High (uses official code) | ⚠️ Medium (reverse-engineered) |
| Speed | ✅ Fast | ✅ Fast |
| Output format | JSON | Python objects |

## Contributing

To improve frame-by-frame tracking, contributions are welcome for:

1. Hooking into the decoder's step function
2. Processing raw action data
3. Implementing action type handlers
4. Adding more detailed statistics

## References

- [haxball-replay-analyzer](https://github.com/haxball-replay-analyzer/haxball-replay-analyzer.github.io) - Reference implementation
- [ACTION_TYPES_COMPLETE.md](./ACTION_TYPES_COMPLETE.md) - Complete action type documentation
- Original Haxball replay format specification (community-documented)

## License

Same as HaxMetrics project.
