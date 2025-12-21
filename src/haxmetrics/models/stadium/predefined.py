"""
Predefined Stadium class for HaxBall HBR2 replay parsing.

Predefined stadiums (types 0-11) only store the stadium type and name.
No additional data is parsed from the replay.
"""

from dataclasses import dataclass
from typing import Dict

from .base import Stadium


@dataclass(frozen=True)
class PredefinedStadium(Stadium):
    """
    Predefined stadium (types 0-11).
    
    These stadiums are built into HaxBall and only require a type ID.
    No component data is stored in the replay.
    
    Attributes:
        stadium_type: Stadium type ID (0-11)
        name: Human-readable stadium name
    """
    
    stadium_type: int
    name: str
    
    # Stadium type to name mapping
    STADIUM_NAMES = {
        0: "Classic",
        1: "Easy",
        2: "Small",
        3: "Big",
        4: "Rounded",
        5: "Hockey",
        6: "Big Hockey",
        7: "Big Easy",
        8: "Big Rounded",
        9: "Huge",
        10: "Unknown",
        11: "Unknown"
    }
    
    def __post_init__(self):
        """Validate stadium type."""
        if not 0 <= self.stadium_type <= 11:
            raise ValueError(f"Stadium type must be 0-11, got {self.stadium_type}")
    
    @classmethod
    def parse(cls, reader, stadium_type: int) -> "PredefinedStadium":
        """
        Parse predefined stadium.
        
        For predefined stadiums, no additional bytes are read.
        Only the stadium type (already read) is used.
        
        Args:
            reader: BinaryReader (not used for predefined stadiums)
            stadium_type: Stadium type ID (0-11)
            
        Returns:
            PredefinedStadium: Parsed stadium with type and name
        """
        name = cls._get_stadium_name(stadium_type)
        return cls(stadium_type=stadium_type, name=name)
    
    @staticmethod
    def _get_stadium_name(stadium_type: int) -> str:
        """
        Get stadium name from type ID.
        
        Args:
            stadium_type: Stadium type ID (0-11)
            
        Returns:
            str: Stadium name
        """
        return PredefinedStadium.STADIUM_NAMES.get(stadium_type, "Unknown")
    
    def to_dict(self) -> Dict:
        """
        Convert to dictionary representation.
        
        Returns:
            Dict: Dictionary with stadium type and name
        """
        return {
            "type": self.stadium_type,
            "name": self.name,
            "custom": False
        }
