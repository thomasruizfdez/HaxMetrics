#!/usr/bin/env python3
"""
Generate annotated hex dumps of HBR2 replay sections.

This script extracts and displays hex dumps with annotations for:
- Header section
- Stadium section
- Player section
- Team colors section
- Action samples
"""

import sys
import os
import zlib
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from haxmetrics.binary_reader import BinaryReader


def hex_dump(data: bytes, offset: int = 0, max_bytes: int = 256, width: int = 16) -> str:
    """
    Create a formatted hex dump of binary data.
    
    Args:
        data: Binary data to dump
        offset: Starting offset for display
        max_bytes: Maximum number of bytes to display
        width: Number of bytes per line
    
    Returns:
        Formatted hex dump string
    """
    lines = []
    end = min(len(data), max_bytes)
    
    for i in range(0, end, width):
        # Offset
        line_offset = offset + i
        hex_str = f"{line_offset:08X}: "
        
        # Hex bytes
        hex_bytes = []
        ascii_bytes = []
        for j in range(width):
            if i + j < end:
                byte = data[i + j]
                hex_bytes.append(f"{byte:02X}")
                # ASCII representation
                if 32 <= byte <= 126:
                    ascii_bytes.append(chr(byte))
                else:
                    ascii_bytes.append(".")
            else:
                hex_bytes.append("  ")
                ascii_bytes.append(" ")
        
        # Format line
        hex_str += " ".join(hex_bytes[:8]) + "  " + " ".join(hex_bytes[8:])
        hex_str += "  |" + "".join(ascii_bytes) + "|"
        lines.append(hex_str)
    
    if len(data) > max_bytes:
        lines.append(f"... ({len(data) - max_bytes} more bytes)")
    
    return "\n".join(lines)


def analyze_header(data: bytes) -> dict:
    """Analyze and dump the HBR2 header."""
    print("\n" + "="*80)
    print("HEADER SECTION (12 bytes)")
    print("="*80)
    
    reader = BinaryReader(data)
    
    # Read header
    magic = reader.read_fixed_string(4)
    version = reader.read_uint32_be()
    duration = reader.read_uint32_be()
    
    print(f"\nMagic: '{magic}' (0x{data[0:4].hex()})")
    print(f"Version: {version} (0x{data[4:8].hex()})")
    print(f"Duration: {duration} frames = {duration/60.0:.2f}s (0x{data[8:12].hex()})")
    
    print("\nHex Dump:")
    print(hex_dump(data[:12], offset=0, max_bytes=12))
    
    return {
        "magic": magic,
        "version": version,
        "duration": duration,
        "header_size": 12
    }


def analyze_compressed_body(data: bytes, offset: int = 12) -> bytes:
    """Decompress and return the body data."""
    print("\n" + "="*80)
    print("COMPRESSED BODY")
    print("="*80)
    
    compressed = data[offset:]
    print(f"\nCompressed size: {len(compressed)} bytes")
    
    # Decompress
    decompressed = zlib.decompress(compressed, wbits=-15)
    print(f"Decompressed size: {len(decompressed)} bytes")
    print(f"Compression ratio: {len(compressed) / len(decompressed):.2%}")
    
    return decompressed


def analyze_messages(data: bytes) -> tuple:
    """Analyze messages section."""
    print("\n" + "="*80)
    print("MESSAGES SECTION")
    print("="*80)
    
    reader = BinaryReader(data)
    start_pos = 0
    
    # Read message count
    count = reader.read_uint16_be()
    print(f"\nMessage count: {count}")
    
    # Show hex dump of messages header
    print(f"\nHex Dump (first 64 bytes):")
    print(hex_dump(data[start_pos:], offset=start_pos, max_bytes=64))
    
    return reader.position, count


def analyze_room(data: bytes, offset: int) -> tuple:
    """Analyze room section."""
    print("\n" + "="*80)
    print("ROOM SECTION")
    print("="*80)
    
    reader = BinaryReader(data[offset:])
    start_pos = offset
    
    # Room name
    name = reader.read_string()
    print(f"\nRoom name: '{name}'")
    
    # Teams locked
    teams_locked = reader.read_byte()
    print(f"Teams locked: {teams_locked}")
    
    # Limits
    score_limit = reader.read_uint32_be()
    time_limit = reader.read_uint32_be()
    print(f"Score limit: {score_limit}")
    print(f"Time limit: {time_limit}")
    
    # Kick settings
    kick_burst = reader.read_uint16_be()
    kick_rate = reader.read_byte()
    kick_timeout = reader.read_byte()
    print(f"Kick burst: {kick_burst}")
    print(f"Kick rate: {kick_rate}")
    print(f"Kick timeout: {kick_timeout}")
    
    print(f"\nHex Dump (first 128 bytes):")
    print(hex_dump(data[start_pos:], offset=start_pos, max_bytes=128))
    
    return offset + reader.position, name


def analyze_stadium(data: bytes, offset: int) -> tuple:
    """Analyze stadium section."""
    print("\n" + "="*80)
    print("STADIUM SECTION")
    print("="*80)
    
    reader = BinaryReader(data[offset:])
    start_pos = offset
    
    # Stadium type
    stadium_type = reader.read_byte()
    print(f"\nStadium type byte: 0x{stadium_type:02X} ({stadium_type})")
    
    if stadium_type == 0xFF:
        print("→ CUSTOM STADIUM (0xFF)")
        
        # Stadium name
        name = reader.read_string()
        print(f"Stadium name: '{name}'")
        
        # Show more of custom stadium structure
        print(f"\nHex Dump (first 256 bytes of stadium data):")
        print(hex_dump(data[start_pos:], offset=start_pos, max_bytes=256))
    else:
        print(f"→ PREDEFINED STADIUM (type {stadium_type})")
        print(f"\nHex Dump:")
        print(hex_dump(data[start_pos:start_pos+16], offset=start_pos, max_bytes=16))
    
    return offset + reader.position, stadium_type


def analyze_file(replay_path: str):
    """Analyze a complete replay file."""
    print(f"\n{'#'*80}")
    print(f"# Analyzing: {os.path.basename(replay_path)}")
    print(f"# Full path: {replay_path}")
    print(f"{'#'*80}")
    
    with open(replay_path, "rb") as f:
        data = f.read()
    
    print(f"\nTotal file size: {len(data)} bytes")
    
    # 1. Header
    header_info = analyze_header(data)
    
    # 2. Decompress body
    decompressed = analyze_compressed_body(data, offset=header_info["header_size"])
    
    # 3. Messages
    messages_end, msg_count = analyze_messages(decompressed)
    
    # 4. Room (starts after messages)
    room_end, room_name = analyze_room(decompressed, messages_end)
    
    # Note: Stadium is part of room parsing, but we can peek at it
    # by analyzing from the current reader position
    
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"File: {os.path.basename(replay_path)}")
    print(f"Version: {header_info['version']}")
    print(f"Duration: {header_info['duration']} frames ({header_info['duration']/60:.2f}s)")
    print(f"Room: {room_name}")
    print(f"Messages: {msg_count}")
    print(f"Decompressed size: {len(decompressed)} bytes")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python hex_dump_sections.py <replay_file> [replay_file2 ...]")
        print("\nExample:")
        print("  python hex_dump_sections.py src/replays/LIRS/Albania-Poland3.hbr2")
        sys.exit(1)
    
    for replay_path in sys.argv[1:]:
        try:
            analyze_file(replay_path)
        except Exception as e:
            print(f"\n❌ Error analyzing {replay_path}: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()
