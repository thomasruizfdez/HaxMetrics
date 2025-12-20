# JSON Output Format - Playtime Extraction

This document describes the JSON output format produced by `extract_playtime.js`.

## Overview

The output is a JSON file containing metadata about the replay and detailed playtime statistics for each player.

## Root Structure

```json
{
  "metadata": { ... },
  "playerStats": [ ... ]
}
```

## Metadata Section

Contains information about the replay file and extraction process.

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `replayFile` | string | Name of the input .hbr2 file |
| `totalFrames` | number | Total number of frames in the replay |
| `totalDuration` | number | Total duration in seconds (calculated from frames) |
| `totalDurationSeconds` | string | Total duration formatted as string with 2 decimals |
| `recordingStart` | number | Unix timestamp (ms) when recording started |
| `recordingStartISO` | string | ISO 8601 formatted recording start time |
| `extractedAt` | string | ISO 8601 formatted time when extraction was performed |
| `frameRate` | number | Replay frame rate (always 60 FPS for Haxball) |

### Example

```json
{
  "metadata": {
    "replayFile": "game.hbr2",
    "totalFrames": 212157,
    "totalDuration": 3535.95,
    "totalDurationSeconds": "3535.95",
    "recordingStart": 1727562440000,
    "recordingStartISO": "2024-09-28T23:07:20.000Z",
    "extractedAt": "2024-12-20T19:00:00.000Z",
    "frameRate": 60
  }
}
```

## Player Statistics Section

Array of player statistics objects, sorted by total time (descending).

### Player Stats Object

| Field | Type | Description |
|-------|------|-------------|
| `playerId` | number | Unique player ID assigned by Haxball |
| `name` | string | Player's display name |
| `totalTime` | number | Total frames player was in the room |
| `totalTimeSeconds` | string | Total time in seconds (2 decimals) |
| `playingTime` | number | Total frames playing (red or blue team) |
| `playingTimeSeconds` | string | Playing time in seconds (2 decimals) |
| `redTeamTime` | number | Frames spent in red team |
| `redTeamTimeSeconds` | string | Red team time in seconds (2 decimals) |
| `blueTeamTime` | number | Frames spent in blue team |
| `blueTeamTimeSeconds` | string | Blue team time in seconds (2 decimals) |
| `spectatorTime` | number | Frames spent spectating |
| `spectatorTimeSeconds` | string | Spectator time in seconds (2 decimals) |
| `teamChanges` | number | Number of times player changed teams |
| `timeline` | array | Array of timeline events (see below) |

### Timeline Event Object

| Field | Type | Description |
|-------|------|-------------|
| `frame` | number | Frame number when event occurred |
| `event` | string | Event type: "initial", "team_change", "join", "leave" |
| `team` | string | Team after event: "spectators", "red", or "blue" |
| `name` | string | Player name at time of event |

### Example

```json
{
  "playerStats": [
    {
      "playerId": 445,
      "name": "Cubone",
      "totalTime": 212157,
      "totalTimeSeconds": "3535.95",
      "playingTime": 212157,
      "playingTimeSeconds": "3535.95",
      "redTeamTime": 212157,
      "redTeamTimeSeconds": "3535.95",
      "blueTeamTime": 0,
      "blueTeamTimeSeconds": "0.00",
      "spectatorTime": 0,
      "spectatorTimeSeconds": "0.00",
      "teamChanges": 0,
      "timeline": [
        {
          "frame": 0,
          "event": "initial",
          "team": "red",
          "name": "Cubone"
        }
      ]
    },
    {
      "playerId": 475,
      "name": "Bi Tık Futbol",
      "totalTime": 212157,
      "totalTimeSeconds": "3535.95",
      "playingTime": 0,
      "playingTimeSeconds": "0.00",
      "redTeamTime": 0,
      "redTeamTimeSeconds": "0.00",
      "blueTeamTime": 0,
      "blueTeamTimeSeconds": "0.00",
      "spectatorTime": 212157,
      "spectatorTimeSeconds": "3535.95",
      "teamChanges": 0,
      "timeline": [
        {
          "frame": 0,
          "event": "initial",
          "team": "spectators",
          "name": "Bi Tık Futbol"
        }
      ]
    }
  ]
}
```

## Complete Example

```json
{
  "metadata": {
    "replayFile": "prueba.hbr2",
    "totalFrames": 34,
    "totalDuration": 0.5666666666666667,
    "totalDurationSeconds": "0.57",
    "recordingStart": 1766257390305,
    "recordingStartISO": "2025-12-20T19:03:10.305Z",
    "extractedAt": "2025-12-20T19:03:10.307Z",
    "frameRate": 60
  },
  "playerStats": [
    {
      "playerId": 0,
      "name": "Bandolero",
      "totalTime": 34,
      "totalTimeSeconds": "0.57",
      "playingTime": 0,
      "playingTimeSeconds": "0.00",
      "redTeamTime": 0,
      "redTeamTimeSeconds": "0.00",
      "blueTeamTime": 0,
      "blueTeamTimeSeconds": "0.00",
      "spectatorTime": 34,
      "spectatorTimeSeconds": "0.57",
      "teamChanges": 0,
      "timeline": [
        {
          "frame": 0,
          "event": "initial",
          "team": "spectators",
          "name": "Bandolero"
        }
      ]
    }
  ]
}
```

## Data Types

### Frame Numbers

- **Type**: Integer
- **Range**: 0 to totalFrames
- **Unit**: Frames (60 FPS)
- **Conversion**: `seconds = frames / 60`

### Time Strings

- **Format**: Decimal string with 2 decimal places
- **Unit**: Seconds
- **Example**: `"3535.95"`

### Team Names

- **Valid values**: `"spectators"`, `"red"`, `"blue"`
- **Case**: Lowercase
- **Usage**: Indicates which team a player is on

### Event Types

| Event Type | Description |
|------------|-------------|
| `"initial"` | Initial state when replay starts |
| `"team_change"` | Player changed teams |
| `"join"` | Player joined the room (future) |
| `"leave"` | Player left the room (future) |

Note: Currently only `"initial"` events are captured. See [PLAYTIME_EXTRACTION.md](./PLAYTIME_EXTRACTION.md#limitations) for details.

## Calculations

### Time Calculations

```javascript
// Total time = sum of all periods
totalTime = sum(duration of each timeline segment)

// Playing time = time in red + time in blue
playingTime = redTeamTime + blueTeamTime

// Spectator time = total time - playing time
spectatorTime = totalTime - playingTime

// Verify: these should be equal
totalTime === (playingTime + spectatorTime)
```

### Percentage Calculations

```javascript
// Playing percentage
playingPercent = (playingTime / totalTime) * 100

// Team distribution (of playing time)
redPercent = (redTeamTime / playingTime) * 100
bluePercent = (blueTeamTime / playingTime) * 100
```

### Frame to Time Conversion

```javascript
// Frames to seconds
seconds = frames / 60

// Frames to minutes
minutes = frames / 3600

// Frames to milliseconds
milliseconds = frames * (1000 / 60)
```

## Usage Examples

### JavaScript

```javascript
const fs = require('fs');

// Load the JSON
const data = JSON.parse(fs.readFileSync('game_playtime.json', 'utf8'));

// Get total replay duration
console.log(`Replay duration: ${data.metadata.totalDurationSeconds}s`);

// Find longest playing player
const longestPlayer = data.playerStats[0]; // Already sorted
console.log(`${longestPlayer.name} played for ${longestPlayer.playingTimeSeconds}s`);

// Calculate average playing time
const avgPlayingTime = data.playerStats.reduce((sum, p) => sum + p.playingTime, 0) / data.playerStats.length;
console.log(`Average playing time: ${(avgPlayingTime / 60).toFixed(2)}s`);

// Filter players who actually played (not just spectating)
const activePlayers = data.playerStats.filter(p => p.playingTime > 0);
console.log(`Active players: ${activePlayers.length}`);
```

### Python

```python
import json

# Load the JSON
with open('game_playtime.json', 'r') as f:
    data = json.load(f)

# Get total replay duration
print(f"Replay duration: {data['metadata']['totalDurationSeconds']}s")

# Find players who changed teams
team_changers = [p for p in data['playerStats'] if p['teamChanges'] > 0]
print(f"Players who changed teams: {len(team_changers)}")

# Calculate red vs blue team balance
red_total = sum(p['redTeamTime'] for p in data['playerStats'])
blue_total = sum(p['blueTeamTime'] for p in data['playerStats'])
print(f"Red team total: {red_total / 60:.2f}s")
print(f"Blue team total: {blue_total / 60:.2f}s")

# Get player by ID
def get_player_stats(player_id):
    return next((p for p in data['playerStats'] if p['playerId'] == player_id), None)

player = get_player_stats(445)
if player:
    print(f"{player['name']}: {player['playingTimeSeconds']}s playing time")
```

## Validation

### Required Fields

All fields in the metadata and playerStats objects are required and should always be present.

### Constraints

```javascript
// Time constraints
totalTime === playingTime + spectatorTime
playingTime === redTeamTime + blueTeamTime

// Team changes
teamChanges >= 0
teamChanges === max(0, timeline.length - 1)  // Minus initial event

// Timeline
timeline.length >= 1  // Always has at least initial state
timeline[0].frame === 0  // First event is at frame 0
timeline[0].event === "initial"  // First event is initial state
```

### Common Issues

1. **Negative times**: Should never occur
2. **Time sum mismatch**: `totalTime` should equal sum of team times
3. **Empty timeline**: Every player should have at least initial state
4. **Invalid team names**: Only "spectators", "red", "blue" are valid

## File Size

Expected file sizes:

- **Small replay** (< 1 minute): ~1-2 KB
- **Medium replay** (5-10 minutes): ~2-5 KB
- **Large replay** (> 30 minutes): ~5-20 KB

File size depends on:
- Number of players
- Length of timeline arrays
- Number of team changes

## Comparison with Python Parser Output

The JavaScript extractor output is designed to be compatible with the Python parser output for validation purposes.

### Differences

| Aspect | JavaScript Output | Python Output |
|--------|------------------|---------------|
| Format | JSON file | Python objects |
| Frame data | Frames (60 FPS) | Frames (60 FPS) |
| Time format | Both frames and seconds | Usually frames |
| Timeline | Simplified | Complete (future) |
| Team names | lowercase strings | Enums or constants |

### Conversion

To compare outputs, convert Python objects to JSON with the same structure:

```python
import json

# Convert Python parser output to JSON format
def to_json_format(python_output):
    return {
        "metadata": {
            "replayFile": python_output.filename,
            "totalFrames": python_output.total_frames,
            # ... etc
        },
        "playerStats": [
            {
                "playerId": player.id,
                "name": player.name,
                # ... etc
            }
            for player in python_output.players
        ]
    }

# Save for comparison
with open('python_output.json', 'w') as f:
    json.dump(to_json_format(output), f, indent=2)
```

## Related Documentation

- [PLAYTIME_EXTRACTION.md](./PLAYTIME_EXTRACTION.md) - Technical documentation
- [ACTION_TYPES_COMPLETE.md](./ACTION_TYPES_COMPLETE.md) - Action type reference
- [README.md](../README.md) - Project overview

## License

Same as HaxMetrics project.
