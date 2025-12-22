"""
Type 22: Player avatar set action.

Sets a player's avatar (admin action).
"""

from dataclasses import dataclass
from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from haxmetrics.binary_reader import BinaryReader

from .base import Action
from .action_header import ActionHeader


@dataclass(frozen=True)
class PlayerAvatarSetAction(Action):
    """
    Player avatar set action (Type 22).
    
    Sets a player's avatar (typically an admin action).
    
    Note: Untested with real fixture (rare in real games).
    
    Attributes:
        player_id (int): Player ID (uint32_be)
        avatar (str): Avatar string
        
    Parsing:
        Field     | Method | Type       | Size | Notes
        ----------|--------|------------|------|-------
        player_id | N()    | uint32_be  | 4    | Player ID
        avatar    | Ab()   | string     | var  | Avatar
    """
    player_id: int
    avatar: str

    @classmethod
    def parse(cls, header: ActionHeader, reader: 'BinaryReader') -> 'PlayerAvatarSetAction':
        """Parse player avatar set action from binary data."""
        player_id = reader.read_uint32_be()  # N() - uint32_be
        avatar = reader.read_string()        # Ab() - string
        
        return cls(
            header=header,
            player_id=player_id,
            avatar=avatar or ""
        )

    def to_dict(self) -> Dict:
        """Convert to dictionary representation."""
        return {
            "type": "player_avatar_set",
            "frame_delta": self.frame_delta,
            "sender": self.sender,
            "player_id": self.player_id,
            "avatar": self.avatar
        }
