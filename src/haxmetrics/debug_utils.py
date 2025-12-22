"""
Debug utilities for HBR2 parsing.

This module provides tools for debugging binary parsing issues:
- DebugParser: Tracks parsing progress and generates incremental JSON output
- hex_dump: Displays hex dump around failure points
"""

import json
import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class ParseSection:
    """Represents a parsing section"""
    section: str
    offset_before: int
    offset_after: Optional[int] = None
    data: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    
    def to_dict(self) -> Dict:
        result = {
            "section": self.section,
            "offset_before": self.offset_before,
        }
        if self.offset_after is not None:
            result["offset_after"] = self.offset_after
            result["bytes_read"] = self.offset_after - self.offset_before
        if self.data:
            result["data"] = self.data
        if self.error:
            result["error"] = self.error
        return result


class DebugParser:
    """
    Tracks parsing progress and generates incremental JSON output.
    
    Usage:
        debug = DebugParser()
        
        debug.start_section("Header", reader.position)
        debug.log_field("signature", "HBR2")
        debug.log_field("version", 3)
        debug.end_section(reader.position)
        
        # On error:
        debug.end_section(reader.position, error="Failed to parse field X")
        
        # Get JSON:
        json_output = debug.to_json()
    """
    
    def __init__(self):
        self.sections: List[ParseSection] = []
        self.current_section: Optional[ParseSection] = None
    
    def start_section(self, name: str, offset: int):
        """Start a new parsing section"""
        if self.current_section is not None:
            # Auto-close previous section if not closed
            logger.warning(f"Section '{self.current_section.section}' was not closed, auto-closing")
            self.end_section(offset)
        
        self.current_section = ParseSection(
            section=name,
            offset_before=offset
        )
    
    def log_field(self, field_name: str, value: Any):
        """Log a parsed field in the current section"""
        if self.current_section is None:
            logger.warning(f"Trying to log field '{field_name}' but no section is active")
            return
        
        self.current_section.data[field_name] = value
    
    def end_section(self, offset: int, error: Optional[str] = None):
        """End the current parsing section"""
        if self.current_section is None:
            logger.warning("Trying to end section but no section is active")
            return
        
        self.current_section.offset_after = offset
        self.current_section.error = error
        
        self.sections.append(self.current_section)
        self.current_section = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "parsing_log": [section.to_dict() for section in self.sections],
            "total_sections": len(self.sections),
            "has_errors": any(section.error for section in self.sections)
        }
    
    def to_json(self, indent: int = 2) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), indent=indent)
    
    def save_to_file(self, filepath: str):
        """Save to JSON file"""
        with open(filepath, 'w') as f:
            f.write(self.to_json())


def hex_dump(data: bytes, offset: int, context: int = 32) -> str:
    """
    Generate hex dump around a specific offset.
    
    Args:
        data: Binary data
        offset: Offset to center on
        context: Number of bytes before/after to show
    
    Returns:
        Formatted hex dump string
    """
    start = max(0, offset - context)
    end = min(len(data), offset + context)
    
    lines = []
    lines.append(f"Hex dump (offset {start} to {end}, failure at {offset}):")
    lines.append("=" * 70)
    
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
                    hex_bytes.append(f"{byte:02X}")
            else:
                hex_bytes.append("  ")
        
        line += " ".join(hex_bytes[:8]) + "  " + " ".join(hex_bytes[8:])
        
        # ASCII representation
        ascii_repr = ""
        for j in range(16):
            if i + j < end:
                byte = data[i + j]
                ascii_repr += chr(byte) if 32 <= byte < 127 else "."
        
        line += f"  |{ascii_repr}|"
        lines.append(line)
    
    lines.append("=" * 70)
    return "\n".join(lines)
