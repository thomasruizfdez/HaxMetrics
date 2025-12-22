"""
Type 12: Player team change action.

Changes a player's team assignment.
"""

from dataclasses import dataclass
from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from haxmetrics.binary_reader import BinaryReader

from .base import Action
from .action_header import ActionHeader


@dataclass(frozen=True)
class PlayerTeamChangeAction(Action):
    """
    Player team change action (Type 12).
    
    Changes a player's team assignment.
    
    Attributes:
        player_id (int): Player ID (uint32_be)
        team_id (int): Team ID (signed byte: -1 to 2, where 0=spec, 1=red, 2=blue)
        
    Parsing:
        Field     | Method | Type        | Size | Notes
        ----------|--------|-------------|------|-------
        player_id | N()    | uint32_be   | 4    | Player ID
        team_id   | zf()   | signed byte | 1    | -1 to 2 (0=spec, 1=red, 2=blue)
    """
    player_id: int
    team_id: int

    @classmethod
    def parse(cls, header: ActionHeader, reader: 'BinaryReader') -> 'PlayerTeamChangeAction':
        """Parse player team change action from binary data."""
        player_id = reader.read_uint32_be()   # N() - uint32_be
        team_id = reader.read_signed_byte()   # zf() - signed byte
        
        return cls(header=header, player_id=player_id, team_id=team_id)

    def to_dict(self) -> Dict:
        """Convert to dictionary representation."""
        return {
            "type": "player_team_change",
            "frame_delta": self.frame_delta,
            "sender": self.sender,
            "player_id": self.player_id,
            "team_id": self.team_id
        }
