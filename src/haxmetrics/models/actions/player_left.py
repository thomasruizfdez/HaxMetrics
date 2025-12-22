"""
Type 6: Player left action.

Player leaves or is kicked from the room.
"""

from dataclasses import dataclass
from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from haxmetrics.binary_reader import BinaryReader

from .base import Action
from .action_header import ActionHeader


@dataclass(frozen=True)
class PlayerLeftAction(Action):
    """
    Player left action (Type 6).
    
    Represents a player leaving or being kicked from the room.
    
    Attributes:
        player_id (int): Player ID (uint32_be)
        
    Parsing:
        Field     | Method | Type       | Size | Notes
        ----------|--------|------------|------|-------
        player_id | N()    | uint32_be  | 4    | Player ID
    """
    player_id: int

    @classmethod
    def parse(cls, header: ActionHeader, reader: 'BinaryReader') -> 'PlayerLeftAction':
        """Parse player left action from binary data."""
        player_id = reader.read_uint32_be()  # N() - uint32_be
        
        return cls(header=header, player_id=player_id)

    def to_dict(self) -> Dict:
        """Convert to dictionary representation."""
        return {
            "type": "player_left",
            "frame_delta": self.frame_delta,
            "sender": self.sender,
            "player_id": self.player_id
        }
