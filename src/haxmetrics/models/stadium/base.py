"""
Base Stadium class for HaxBall HBR2 replay parsing.

This module defines the abstract base class for all stadium types.
"""

from abc import ABC, abstractmethod
from typing import Dict, List


class Stadium(ABC):
    """
    Abstract base class for all stadium types.
    
    Stadiums can be either predefined (types 0-11) or custom (type 255).
    Each type is parsed differently according to HBR2_PARSING_GUIDE.md section 6.2.
    """
    
    # Collision masks used in stadium components
    MASKS = {
        1: "ball",
        2: "red",
        4: "blue",
        8: "redKO",
        16: "blueKO",
        32: "wall"
    }
    
    # Team names
    TEAMS = ["Spectators", "Red", "Blue"]
    
    @classmethod
    @abstractmethod
    def parse(cls, reader, *args, **kwargs):
        """
        Parse stadium from binary reader.
        
        Args:
            reader: BinaryReader instance positioned at stadium data
            *args: Additional arguments specific to stadium type
            **kwargs: Additional keyword arguments specific to stadium type
            
        Returns:
            Stadium: Parsed stadium instance (PredefinedStadium or CustomStadium)
        """
        pass
    
    @abstractmethod
    def to_dict(self) -> Dict:
        """
        Convert stadium to dictionary representation.
        
        Returns:
            Dict: Dictionary with stadium data
        """
        pass
    
    @classmethod
    def parse_mask(cls, val: int) -> List[str]:
        """
        Parse collision mask value into list of mask names.
        
        Args:
            val: Collision mask integer value
            
        Returns:
            List[str]: List of mask names (e.g., ["ball", "wall"])
        """
        if val == -1 or val == 0xFFFFFFFF:
            return ["all"]
        masks = []
        for key in sorted(cls.MASKS.keys(), reverse=True):
            if val & key:
                masks.append(cls.MASKS[key])
        return masks if masks else []
    
    @classmethod
    def parse_team(cls, team: int) -> str:
        """
        Parse team ID into team name.
        
        Args:
            team: Team ID (0=Spectators, 1=Red, 2=Blue)
            
        Returns:
            str: Team name
        """
        if 0 <= team < len(cls.TEAMS):
            return cls.TEAMS[team]
        return cls.TEAMS[0]  # Default to Spectators
