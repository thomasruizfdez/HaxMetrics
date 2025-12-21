"""
Stadium parsing module for HaxBall HBR2 replays.

Exports:
    - Stadium: Abstract base class
    - PredefinedStadium: Predefined stadiums (types 0-11)
    - CustomStadium: Custom stadiums (type 255)
    - parse_stadium: Factory method to parse any stadium type
    - Component classes: Vertex, Segment, Plane, Goal, StadiumDisc, Joint, PlayerPhysics
"""

from .base import Stadium
from .components import (
    Goal,
    Joint,
    Plane,
    PlayerPhysics,
    Segment,
    StadiumDisc,
    Vertex,
)
from .custom import CustomStadium
from .predefined import PredefinedStadium


def parse_stadium(reader):
    """
    Factory method to parse stadium based on type.
    
    Reads the first byte to determine stadium type:
    - 0-11: Predefined stadium (Classic, Easy, Small, etc.)
    - 255: Custom stadium (full definition follows)
    
    Args:
        reader: BinaryReader instance positioned at stadium data
        
    Returns:
        Stadium: Either PredefinedStadium or CustomStadium instance
        
    Raises:
        ValueError: If stadium type is invalid (not 0-11 or 255)
        
    Example:
        >>> reader = BinaryReader(data)
        >>> stadium = parse_stadium(reader)
        >>> if isinstance(stadium, PredefinedStadium):
        ...     print(f"Predefined: {stadium.name}")
        ... else:
        ...     print(f"Custom: {stadium.name} with {len(stadium.vertices)} vertices")
    """
    stadium_type = reader.read_byte()
    
    if stadium_type == 255:
        # Custom stadium - parse full definition
        return CustomStadium.parse(reader)
    elif 0 <= stadium_type <= 11:
        # Predefined stadium - just type and name
        return PredefinedStadium.parse(reader, stadium_type)
    else:
        raise ValueError(f"Invalid stadium type: {stadium_type}")


__all__ = [
    "Stadium",
    "PredefinedStadium",
    "CustomStadium",
    "parse_stadium",
    "Vertex",
    "Segment",
    "Plane",
    "Goal",
    "StadiumDisc",
    "Joint",
    "PlayerPhysics",
]
