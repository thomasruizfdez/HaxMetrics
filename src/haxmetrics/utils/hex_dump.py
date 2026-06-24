"""
Hex dump utility for debugging binary parsing failures.
"""


def hex_dump(data: bytes, offset: int, context: int = 32) -> str:
    """
    Generate hex dump around a specific offset.
    
    Args:
        data: Binary data
        offset: Offset to center on (marks failure point)
        context: Number of bytes before/after to show
    
    Returns:
        Formatted hex dump string with failure point marked
    """
    start = max(0, offset - context)
    end = min(len(data), offset + context)
    
    lines = []
    lines.append(f"Hex dump (bytes {start}-{end}, failure at offset {offset}):")
    lines.append("=" * 78)
    
    for i in range(start, end, 16):
        # Offset
        line = f"{i:04X}  "
        
        # Hex bytes
        hex_bytes = []
        for j in range(16):
            if i + j < end:
                byte = data[i + j]
                if i + j == offset:
                    hex_bytes.append(f">{byte:02X}<")  # Mark failure point
                else:
                    hex_bytes.append(f" {byte:02X} ")
            else:
                hex_bytes.append("    ")
        
        # Split into two groups of 8
        line += "".join(hex_bytes[:8]) + " " + "".join(hex_bytes[8:])
        
        # ASCII representation
        ascii_repr = ""
        for j in range(16):
            if i + j < end:
                byte = data[i + j]
                if i + j == offset:
                    ascii_repr += "!"  # Mark failure in ASCII too
                else:
                    ascii_repr += chr(byte) if 32 <= byte < 127 else "."
            else:
                ascii_repr += " "
        
        line += f" |{ascii_repr}|"
        lines.append(line)
    
    lines.append("=" * 78)
    lines.append(f"Failure at offset {offset} (marked with >XX< in hex, ! in ASCII)")
    
    return "\n".join(lines)
