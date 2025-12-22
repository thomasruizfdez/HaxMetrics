# Debug Utilities

This directory contains debug utilities for troubleshooting HBR2 parsing issues.

## Files

- **`debug_utils.py`** - Core debug utilities (DebugParser, hex_dump)
- **`test_debug_parsing.py`** (in tests/) - Example debug tests

## Quick Start

### 1. Enable BinaryReader Logging

```python
import logging
from haxmetrics.binary_reader import BinaryReader

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(message)s')

# Create reader with logging
reader = BinaryReader(data, enable_logging=True)

# Every read will be logged:
value = reader.read_uint32_be()
# Output: [0000] read_uint32_be       = 0x00000003 (3)
```

### 2. Track Parsing Progress

```python
from haxmetrics.debug_utils import DebugParser

debug = DebugParser()

# Start section
debug.start_section("Header", reader.position)
header = Header.parse(reader)
debug.log_field("magic", header.magic)
debug.log_field("version", header.version)
debug.end_section(reader.position)

# Save results
debug.save_to_file("debug.json")
```

### 3. Display Hex Dumps

```python
from haxmetrics.debug_utils import hex_dump

# Show hex around failure point
try:
    # ... parsing code ...
except Exception as e:
    print(hex_dump(data, reader.position, context=32))
```

## Documentation

See **[docs/DEBUG_GUIDE.md](../../docs/DEBUG_GUIDE.md)** for complete documentation.

## Example Output

### DebugParser JSON

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
    }
  ],
  "total_sections": 1,
  "has_errors": false
}
```

### hex_dump Output

```
Hex dump (offset 613 to 665, failure at 645):
======================================================================
0265  32 00 00 03 65 73 00 00  00 00 0A 42 61 6E 64 6F  |2...es.....Bando|
0275  6C 65 72 6F 00 00 00 00  00 00 00 01 00 01 00 05  |lero............|
0285  >00< 00 FF FF FF 01 00 E5  6E 56 00 00 FF FF FF 01  |........nV......|
======================================================================
```

## Tests

Run debug tests to see examples:

```bash
python -m pytest src/tests/unit/test_debug_parsing.py -v -s
```

The `-s` flag shows all debug output.
