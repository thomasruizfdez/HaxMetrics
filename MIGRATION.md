# Migration Guide: Old Parser → New Modular Parser

## Overview

Version 1.0.0 introduces a new modular parser that follows the official
HBR2 format specification byte-by-byte, as documented in `docs/HBR2_PARSING_GUIDE.md`.

This guide helps you migrate from the legacy `Parser` class to the new modular architecture.

## Quick Migration

### Before (deprecated)
```python
from haxmetrics.parser import Parser

# Old approach - single Parser class
parser = Parser(replay_data)
result = parser.parse()

# Access data from result dict
header_version = result["version"]
messages = result["messages"]
players = result["players"]
```

### After (new)
```python
import zlib
from haxmetrics.binary_reader import BinaryReader
from haxmetrics.models.header import Header
from haxmetrics.models.messages import Messages
from haxmetrics.models.room import RoomBasic

# New approach - modular parsing
# 1. Read header
reader = BinaryReader(replay_data)
header = Header.parse(reader)

# 2. Decompress data
compressed = reader.get_remaining_bytes()
decompressed = zlib.decompress(compressed, wbits=-15)
reader = BinaryReader(decompressed)

# 3. Parse sections in order
messages = Messages.parse(reader)
room = RoomBasic.parse(reader)

# Access data from typed objects
header_version = header.version
message_count = messages.count
room_name = room.name

# More sections coming in future PRs (stadium, players, actions)...
```

## Benefits of New Parser

### ✅ Type Safety
```python
# Old: Untyped dict access
duration = result["duration"]  # Could be anything

# New: Strongly typed
duration: int = header.duration  # Type-checked
```

### ✅ Modular Design
```python
# Old: Parse everything at once
result = parser.parse()  # All or nothing

# New: Parse only what you need
header = Header.parse(reader)  # Just the header
messages = Messages.parse(reader)  # Just the messages
# Skip room parsing if not needed
```

### ✅ Better Error Messages
```python
# Old: Generic parsing errors
# "Failed to parse at position 1234"

# New: Specific validation errors
# "Invalid HBR2 magic bytes: expected 'HBR2', got 'FAKE'"
# "Message count must be non-negative, got -1"
```

### ✅ Documentation
```python
# Old: Limited documentation
parser.parse()  # What does this return?

# New: Full docstrings with types
Header.parse(reader)  # Returns Header object with magic, version, duration
```

## Feature Parity

| Feature | Old Parser | New Parser | Status |
|---------|-----------|------------|--------|
| Header | ✅ | ✅ | Complete (PR #1) |
| Messages | ✅ | ✅ | Complete (PR #1) |
| Room Basic | ✅ | ✅ | Complete (PR #2) |
| Stadium | ✅ | 🚧 | In Progress (PR #3) |
| Game State | ✅ | 🚧 | Planned (PR #4) |
| Players | ✅ | 🚧 | Planned (PR #5) |
| Team Colors | ✅ | 🚧 | Planned (PR #6) |
| Actions | ✅ | 🚧 | Planned (PR #7+) |

## Deprecation Timeline

- **v1.0.0** (Current): Old parser marked deprecated, still functional
  - Deprecation warnings in console
  - Full backwards compatibility maintained
  
- **v1.5.0** (Q2 2025): Enhanced deprecation notices
  - More prominent warnings
  - Documentation updated with migration examples
  
- **v2.0.0** (Q3 2025): Old parser removed
  - Breaking change: `parser.py` and `replay_messages.py` removed
  - Must migrate to new modular parser

## Common Migration Patterns

### Pattern 1: Basic Replay Info
```python
# Old
parser = Parser(data)
result = parser.parse()
print(f"Version: {result['version']}, Duration: {result['duration']}")

# New
reader = BinaryReader(data)
header = Header.parse(reader)
print(f"Version: {header.version}, Duration: {header.duration}")
```

### Pattern 2: Message Processing
```python
# Old
parser = Parser(data)
result = parser.parse()
for msg in result["messages"]:
    print(msg.type, msg.delta_time)

# New
reader = BinaryReader(data)
header = Header.parse(reader)
compressed = reader.get_remaining_bytes()
decompressed = zlib.decompress(compressed, wbits=-15)
reader = BinaryReader(decompressed)
messages = Messages.parse(reader)
for msg in messages:
    print(msg.type, msg.frame)
```

### Pattern 3: Room Information
```python
# Old
parser = Parser(data)
result = parser.parse()
room = result["room_info"]
print(f"Room: {room.name}, Locked: {room.locked}")

# New
reader = BinaryReader(data)
header = Header.parse(reader)
compressed = reader.get_remaining_bytes()
decompressed = zlib.decompress(compressed, wbits=-15)
reader = BinaryReader(decompressed)
messages = Messages.parse(reader)
room = RoomBasic.parse(reader)
print(f"Room: {room.name}, Locked: {room.locked}")
```

## Migration Checklist

When migrating your code:

- [ ] Replace `from haxmetrics.parser import Parser` with modular imports
- [ ] Replace `Parser(data).parse()` with step-by-step parsing
- [ ] Update dict access to object property access
- [ ] Add proper error handling for each parsing step
- [ ] Update type hints to use new classes
- [ ] Run tests to ensure functionality preserved
- [ ] Suppress deprecation warnings once migration complete

## Need Help?

- 📖 Read `docs/HBR2_PARSING_GUIDE.md` for format specification
- 🔍 Check `src/tests/unit/` for usage examples
- 🐛 Report issues on GitHub
- 💬 Ask questions in discussions

## Example: Complete Migration

### Old Code
```python
from haxmetrics.parser import Parser

def analyze_replay(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()
    
    parser = Parser(data)
    result = parser.parse()
    
    return {
        'version': result['version'],
        'duration_seconds': result['duration'] / 60,
        'message_count': len(result['messages']),
        'room_name': result['room_info'].name if result['room_info'] else None,
    }
```

### New Code
```python
import zlib
from haxmetrics.binary_reader import BinaryReader
from haxmetrics.models.header import Header
from haxmetrics.models.messages import Messages
from haxmetrics.models.room import RoomBasic

def analyze_replay(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()
    
    # Parse header
    reader = BinaryReader(data)
    header = Header.parse(reader)
    
    # Decompress and parse content
    compressed = reader.get_remaining_bytes()
    decompressed = zlib.decompress(compressed, wbits=-15)
    reader = BinaryReader(decompressed)
    
    # Parse sections
    messages = Messages.parse(reader)
    room = RoomBasic.parse(reader)
    
    return {
        'version': header.version,
        'duration_seconds': header.duration_seconds,
        'message_count': messages.count,
        'room_name': room.name,
    }
```

## See Also

- `docs/HBR2_PARSING_GUIDE.md` - Complete format specification
- `CHANGELOG.md` - Version history and changes
- `README.md` - Project overview
