# Stadium Parsing Implementation

## Overview

This document describes the implementation of the Stadium parsing functionality for the HaxMetrics project. The implementation allows parsing of both predefined and custom HaxBall stadiums from replay files.

## Implementation Details

### Key Classes

1. **Stadium** - Main class for representing and parsing stadiums
   - Supports both predefined stadiums (Classic, Easy, Small, Big, etc.)
   - Supports custom stadiums with full parsing of all properties

2. **Stadium Elements**:
   - **Background** - Stadium background configuration (type, dimensions, colors)
   - **Vertex** - Stadium vertices with position and physics properties
   - **Segment** - Segments connecting vertices (walls, barriers)
   - **Plane** - Collision planes defining stadium boundaries
   - **Goal** - Goal positions and team assignments
   - **Disc** - Disc objects including the ball
   - **PlayerPhysics** - Player physics configuration
   - **BallPhysics** - Ball physics configuration (not stored in custom stadiums)

### Binary Format

The stadium data is stored in **big-endian** format, which is different from the rest of the replay file. Key methods added to BinaryReader:

- `read_double_be()` - Read double-precision floats in big-endian
- `read_uint32_be()` - Read 32-bit unsigned integers in big-endian

### Stadium Parsing Flow

#### Predefined Stadiums (type < 255)
1. Read stadium type (1 byte)
2. If type < 10, it's a predefined stadium - just set the name and return

#### Custom Stadiums (type == 255)
1. Read stadium type (1 byte = 255)
2. Read stadium name (string with varint length)
3. Parse Background:
   - Type (uint32_be): 0=none, 1=grass, 2=hockey
   - Width (double_be)
   - Height (double_be)
   - Kick-off radius (double_be)
   - Corner radius (double_be)
   - Goal line (double_be)
   - Color (uint32_be)
4. Read max view dimensions:
   - Max view width (double_be)
   - Max view height (double_be)
5. Read spawn distance (double_be)
6. Parse PlayerPhysics (7 doubles_be):
   - Bounce coefficient
   - Inverse mass
   - Damping
   - Acceleration
   - Kicking acceleration
   - Kicking damping
   - Kick strength
7. Read additional flags:
   - Max view width override (nullable int32)
   - Camera follow (uint8)
   - Can be stored (uint8)
   - Full reset after goal (uint8)
8. Parse stadium elements (each with count byte followed by elements):
   - Vertices (count + array of Vertex)
   - Segments (count + array of Segment)
   - Planes (count + array of Plane)
   - Goals (count + array of Goal)
   - Discs (count + array of Disc)
   - Joints (count only, parsing not yet implemented)
9. Parse spawn points:
   - Red team spawn points (count + array of (x, y) double_be pairs)
   - Blue team spawn points (count + array of (x, y) double_be pairs)

## Testing

Comprehensive tests have been added in `src/tests/test_stadium.py`:

1. **test_predefined_stadium()** - Verifies predefined stadium parsing
2. **test_custom_stadium_basic()** - Tests custom stadium parsing with synthetic data
3. **test_stadium_with_replay()** - Validates parsing with real replay file

All tests pass successfully.

## Usage Example

```python
from haxmetrics.binary_reader import BinaryReader
from haxmetrics.models.stadium.stadium import Stadium

# Parse from replay data
reader = BinaryReader(stadium_bytes)
stadium = Stadium.parse(reader)

# Access stadium properties
print(f"Stadium: {stadium.name}")
print(f"Custom: {stadium.custom}")
if stadium.custom:
    print(f"Background: {stadium.background.type}")
    print(f"Dimensions: {stadium.background.width}x{stadium.background.height}")
    print(f"Vertices: {len(stadium.vertexes)}")
    print(f"Goals: {len(stadium.goals)}")
```

## Compatibility

The implementation is fully compatible with the HaxBall original format specification. It has been tested with:
- Predefined stadiums (types 0-9)
- Custom stadiums from actual replay files
- Various stadium configurations and properties

## Future Improvements

1. **Joint parsing** - Currently joints count is read but elements are not parsed
2. **Spawn points storage** - Currently parsed but not stored in Stadium object
3. **Additional validation** - Could add validation for physics values and dimensions
4. **Serialization** - Add methods to serialize Stadium back to binary format

## References

- Original HaxBall code structure documented in README.md
- Binary format specification for replay files
- HaxBall stadium file format (.hbs)
