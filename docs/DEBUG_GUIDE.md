# 🐛 HBR2 Parsing Debug Guide

**Version:** 1.0  
**Date:** 2025-12-22

---

## 📋 Table of Contents

1. [Introduction](#introduction)
2. [Debug Infrastructure Overview](#debug-infrastructure)
3. [Using BinaryReader Logging](#binaryreader-logging)
4. [Using DebugParser](#debugparser)
5. [Using hex_dump](#hex-dump)
6. [Example Debug Session](#example-session)
7. [Troubleshooting Common Issues](#troubleshooting)

---

## 1. Introduction {#introduction}

This guide explains how to use the debug infrastructure added to HaxMetrics for debugging HBR2 binary parsing issues. The debug tools help:

- **Track parsing progress** through different sections
- **Log every binary read operation** with offsets and values
- **Generate incremental JSON output** showing what was successfully parsed
- **Display hex dumps** around failure points
- **Identify exact byte offsets** where parsing fails

---

## 2. Debug Infrastructure Overview {#debug-infrastructure}

The debug infrastructure consists of three main components:

### 2.1 Enhanced BinaryReader

**File:** `src/haxmetrics/binary_reader.py`

BinaryReader now supports optional logging of all read operations:

```python
from haxmetrics.binary_reader import BinaryReader

# Enable logging
reader = BinaryReader(data, enable_logging=True)

# Now every read operation will be logged
value = reader.read_uint32_be()
# Logs: [0000] read_uint32_be       = 0x00000003 (3)
```

### 2.2 DebugParser

**File:** `src/haxmetrics/debug_utils.py`

Tracks parsing progress by section and generates incremental JSON output:

```python
from haxmetrics.debug_utils import DebugParser

debug = DebugParser()

# Start a section
debug.start_section("Header", reader.position)
# Log fields
debug.log_field("magic", "HBR2")
debug.log_field("version", 3)
# End section
debug.end_section(reader.position)

# On error
debug.end_section(reader.position, error="Failed to parse field X")

# Generate JSON
json_output = debug.to_json()
debug.save_to_file("debug_output.json")
```

### 2.3 hex_dump Utility

**File:** `src/haxmetrics/debug_utils.py`

Displays hex dump around a specific offset:

```python
from haxmetrics.debug_utils import hex_dump

# Show 32 bytes before and after offset 100
print(hex_dump(data, offset=100, context=32))
```

---

## 3. Using BinaryReader Logging {#binaryreader-logging}

### 3.1 Enable Logging

```python
import logging
from haxmetrics.binary_reader import BinaryReader

# Configure logging to see debug messages
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s: %(message)s'
)

# Create reader with logging enabled
data = b'\x48\x42\x52\x32\x00\x00\x00\x03\x00\x00\x00\x12'
reader = BinaryReader(data, enable_logging=True)
```

### 3.2 Read Operations

Every read operation will be logged with:
- **Offset:** Position in the data before the read
- **Method name:** The read method called
- **Value:** The value read (with hex for integers)

```python
magic = reader.read_fixed_string(4)
# Logs: [0000] read_byte            = 0x00000048 (72)
# Logs: [0001] read_byte            = 0x00000042 (66)
# Logs: [0002] read_byte            = 0x00000052 (82)
# Logs: [0003] read_byte            = 0x00000032 (50)

version = reader.read_uint32_be()
# Logs: [0004] read_uint32_be       = 0x00000003 (3)

duration = reader.read_uint32_be()
# Logs: [0008] read_uint32_be       = 0x00000012 (18)
```

### 3.3 Logged Methods

The following methods log their operations:
- `read_byte()` - logs value in hex
- `read_signed_byte()` - logs signed value
- `read_uint16_be()` - logs value in hex
- `read_int16_be()` - logs signed value
- `read_uint32_be()` - logs value in hex
- `read_int32_be()` - logs signed value
- `read_float64_be()` - logs float value
- `read_float64()` - logs float value
- `read_varint()` - logs final value and bytes consumed
- `read_string()` - logs string content in quotes

---

## 4. Using DebugParser {#debugparser}

### 4.1 Basic Usage

```python
from haxmetrics.debug_utils import DebugParser

debug = DebugParser()

# Start parsing header
debug.start_section("Header", reader.position)
header = Header.parse(reader)
debug.log_field("magic", header.magic)
debug.log_field("version", header.version)
debug.log_field("duration", header.duration)
debug.end_section(reader.position)

# Start parsing messages
debug.start_section("Messages", reader.position)
messages = Messages.parse(reader)
debug.log_field("count", len(messages))
debug.end_section(reader.position)
```

### 4.2 Handling Errors

```python
try:
    debug.start_section("GameState", reader.position)
    game_state = parse_game_state(reader)
    debug.log_field("game_active", game_state is not None)
    if game_state:
        debug.log_field("frame", game_state.frame)
        debug.log_field("score_red", game_state.score_red)
    debug.end_section(reader.position)
except Exception as e:
    # Log the error with the section
    debug.end_section(reader.position, error=str(e))
    raise
```

### 4.3 Generate Output

```python
# Get as dictionary
output_dict = debug.to_dict()
print(f"Total sections: {output_dict['total_sections']}")
print(f"Has errors: {output_dict['has_errors']}")

# Get as JSON string
json_str = debug.to_json(indent=2)
print(json_str)

# Save to file
debug.save_to_file("parsing_debug.json")
```

### 4.4 Example JSON Output

```json
{
  "parsing_log": [
    {
      "section": "Header",
      "offset_before": 0,
      "offset_after": 12,
      "bytes_read": 12,
      "data": {
        "magic": "HBR2",
        "version": 3,
        "duration": 18
      }
    },
    {
      "section": "GameState",
      "offset_before": 22,
      "offset_after": 605,
      "bytes_read": 583,
      "data": {
        "game_active": 1,
        "frame": 0,
        "score_red": 0,
        "score_blue": 0,
        "disc_count": 6
      }
    },
    {
      "section": "Players",
      "offset_before": 605,
      "offset_after": 645,
      "bytes_read": 40,
      "data": {
        "player_count": 1
      },
      "error": "Not enough bytes to read string"
    }
  ],
  "total_sections": 3,
  "has_errors": true
}
```

This output shows:
- Header parsed successfully (12 bytes)
- GameState parsed successfully (583 bytes)
- Players parsing failed at offset 645

---

## 5. Using hex_dump {#hex-dump}

### 5.1 Basic Usage

```python
from haxmetrics.debug_utils import hex_dump

# Show hex dump around failure point
try:
    # ... parsing code ...
except Exception as e:
    print(f"Error at offset {reader.position}: {e}")
    print(hex_dump(data, reader.position, context=32))
```

### 5.2 Example Output

```
Hex dump (offset 613 to 665, failure at 645):
======================================================================
0265  32 00 00 03 65 73 00 00  00 00 0A 42 61 6E 64 6F  |2...es.....Bando|
0275  6C 65 72 6F 00 00 00 00  00 00 00 01 00 01 00 05  |lero............|
0285  >00< 00 FF FF FF 01 00 E5  6E 56 00 00 FF FF FF 01  |........nV......|
0295  00 56 89 E5                                       |.V..|
======================================================================
```

The `>00<` markers indicate the byte at the failure offset.

### 5.3 Parameters

```python
hex_dump(
    data,           # Binary data to dump
    offset,         # Offset where error occurred
    context=32      # Bytes before/after to show (default: 32)
)
```

---

## 6. Example Debug Session {#example-session}

Here's a complete example of debugging a parsing issue:

```python
import logging
import zlib
from pathlib import Path

from haxmetrics.binary_reader import BinaryReader
from haxmetrics.debug_utils import DebugParser, hex_dump
from haxmetrics.models.header import Header
from haxmetrics.models.messages import Messages
from haxmetrics.models.room import RoomBasic
from haxmetrics.models.stadium import parse_stadium
from haxmetrics.models.game_state import parse_game_state

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s: %(message)s'
)

# Load file
with open("replay.hbr2", "rb") as f:
    data = f.read()

# Create readers and debug tracker
reader = BinaryReader(data, enable_logging=True)
debug = DebugParser()

try:
    # Parse Header
    debug.start_section("Header", reader.position)
    header = Header.parse(reader)
    debug.log_field("magic", header.magic)
    debug.log_field("version", header.version)
    debug.log_field("duration", header.duration)
    debug.end_section(reader.position)
    
    # Decompress
    debug.start_section("Decompression", reader.position)
    compressed_data = reader.read_remaining()
    decompressed = zlib.decompress(compressed_data, wbits=-15)
    debug.log_field("compressed_size", len(compressed_data))
    debug.log_field("decompressed_size", len(decompressed))
    debug.end_section(reader.position)
    
    # Create new reader for decompressed data
    reader = BinaryReader(decompressed, enable_logging=True)
    
    # Parse Messages
    debug.start_section("Messages", reader.position)
    messages = Messages.parse(reader)
    debug.log_field("message_count", len(messages))
    debug.end_section(reader.position)
    
    # Parse RoomBasic
    debug.start_section("RoomBasic", reader.position)
    room_basic = RoomBasic.parse(reader)
    debug.log_field("name", room_basic.name)
    debug.log_field("locked", room_basic.locked)
    debug.end_section(reader.position)
    
    # Parse Stadium
    debug.start_section("Stadium", reader.position)
    stadium = parse_stadium(reader)
    debug.log_field("stadium_parsed", True)
    debug.end_section(reader.position)
    
    # Parse GameState
    debug.start_section("GameState", reader.position)
    game_state = parse_game_state(reader)
    debug.log_field("game_active", game_state is not None)
    if game_state:
        debug.log_field("frame", game_state.frame)
        debug.log_field("score_red", game_state.score_red)
        debug.log_field("disc_count", len(game_state.discs))
    debug.end_section(reader.position)
    
except Exception as e:
    debug.end_section(reader.position, error=str(e))
    print(f"\nParsing failed at offset {reader.position}: {e}")
    print(f"Bytes remaining: {reader.bytes_remaining}")
    
    # Show hex dump around failure point
    print("\n=== Hex dump around failure ===")
    print(hex_dump(decompressed, reader.position, context=32))

# Save debug output
debug.save_to_file("debug_output.json")
print(f"\n=== Debug output saved to: debug_output.json ===")
print(debug.to_json())
```

---

## 7. Troubleshooting Common Issues {#troubleshooting}

### 7.1 "Not enough bytes to read X"

**Symptom:** EOFError when trying to read data

**Diagnosis:**
1. Check the hex dump around the failure point
2. Check if previous parsing consumed too many bytes
3. Check if field order is correct

**Solution:**
- Verify the parsing order matches the binary format
- Check if there are conditional fields that weren't parsed

### 7.2 Wrong values parsed

**Symptom:** Values don't match expected data

**Diagnosis:**
1. Enable BinaryReader logging to see all values read
2. Check the JSON output to see where values diverge
3. Compare byte offsets with expected structure

**Solution:**
- Check endianness (big-endian vs little-endian)
- Check data types (signed vs unsigned)
- Check if there are missing fields

### 7.3 Offset misalignment

**Symptom:** Parsing succeeds but values are wrong

**Diagnosis:**
1. Check JSON output to see bytes_read for each section
2. Compare with expected section sizes
3. Look for varint or string length issues

**Solution:**
- Verify varint decoding is correct
- Check if strings include null terminators
- Check for optional fields that might be skipped

---

## 8. Debug Test Examples {#test-examples}

See `src/tests/unit/test_debug_parsing.py` for complete examples of:

- `TestDebugGameStateParsing` - Debug tests for GameState parsing
- `TestDebugTeamColorsParsing` - Debug tests for TeamColors parsing
- `TestHexDumpUtility` - Tests for hex_dump utility

Run debug tests with:

```bash
python -m pytest src/tests/unit/test_debug_parsing.py -v -s
```

The `-s` flag shows all print output including debug logs.

---

## 9. Best Practices {#best-practices}

1. **Start with BinaryReader logging disabled** for sections that work
2. **Enable logging** only for the problematic section
3. **Use DebugParser** to track high-level progress
4. **Save JSON output** for later analysis
5. **Use hex_dump** to inspect binary data around errors
6. **Compare offsets** between successful and failed parses
7. **Test with multiple fixtures** to identify patterns

---

## 10. References {#references}

- **Main parsing guide:** `docs/HBR2_PARSING_GUIDE.md`
- **Debug utils source:** `src/haxmetrics/debug_utils.py`
- **BinaryReader source:** `src/haxmetrics/binary_reader.py`
- **Debug tests:** `src/tests/unit/test_debug_parsing.py`
