"""
Type 19: Team colors change action.

Changes team color configuration.
"""

from dataclasses import dataclass
from typing import List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from haxmetrics.binary_reader import BinaryReader

from .base import Action
from .action_header import ActionHeader


@dataclass(frozen=True)
class TeamColorsChangeAction(Action):
    """
    Team colors change action (Type 19).
    
    Changes the color configuration of a team.
    
    Attributes:
        team (int): Team ID (1=red, 2=blue)
        angle (int): Angle (byte)
        text_color (int): Text color ARGB (uint32_be)
        num_stripes (int): Number of color stripes (byte, max 3)
        stripes (List[int]): Array of stripe colors ARGB (uint32_be each)
        
    Parsing:
        Field       | Method | Type      | Size | Notes
        ------------|--------|-----------|------|-------
        team        | F()    | byte      | 1    | 1=red, 2=blue
        team_color  | ...    | TeamColor | var  | TeamColor structure (see section 6.5)
        
    TeamColor structure:
        Field       | Method | Type       | Size | Notes
        ------------|--------|------------|------|-------
        angle       | F()    | byte       | 1    | Angle (0-255)
        text_color  | N()    | uint32_be  | 4    | Text color ARGB
        num_stripes | F()    | byte       | 1    | Number of stripes (max 3)
        stripes     | N()... | uint32_be  | 4*N  | Array of stripe colors ARGB
    """
    team: int
    angle: int
    text_color: int
    num_stripes: int
    stripes: List[int]

    @classmethod
    def parse(cls, header: ActionHeader, reader: 'BinaryReader') -> 'TeamColorsChangeAction':
        """Parse team colors change action from binary data."""
        team = reader.read_byte()  # F() - byte
        
        # Parse TeamColor structure (ta.ma() in game-min.js)
        angle = reader.read_byte()          # F() - byte
        text_color = reader.read_uint32_be()  # N() - uint32_be
        num_stripes = reader.read_byte()    # F() - byte
        
        if num_stripes > 3:
            raise ValueError("Too many stripes (max 3)")
        
        stripes = []
        for _ in range(num_stripes):
            stripes.append(reader.read_uint32_be())  # N() - uint32_be
        
        return cls(
            header=header,
            team=team,
            angle=angle,
            text_color=text_color,
            num_stripes=num_stripes,
            stripes=stripes
        )

    def to_dict(self) -> Dict:
        """Convert to dictionary representation."""
        return {
            "type": "team_colors_change",
            "frame_delta": self.frame_delta,
            "sender": self.sender,
            "team": self.team,
            "angle": self.angle,
            "text_color": self.text_color,
            "num_stripes": self.num_stripes,
            "stripes": self.stripes
        }
