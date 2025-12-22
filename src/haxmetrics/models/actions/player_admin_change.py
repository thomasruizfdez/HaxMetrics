"""
Type 14: Player admin change action.

Changes admin status of a player.
"""

from dataclasses import dataclass
from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from haxmetrics.binary_reader import BinaryReader

from .base import Action
from .action_header import ActionHeader


@dataclass(frozen=True)
class PlayerAdminChangeAction(Action):
    """
    Player admin change action (Type 14).
    
    Changes the admin status of a player.
    
    Attributes:
        player_id (int): Player ID (uint32_be)
        admin (int): Admin status (0=no admin, 1=admin)
        
    Parsing:
        Field     | Method | Type       | Size | Notes
        ----------|--------|------------|------|-------
        player_id | N()    | uint32_be  | 4    | Player ID
        admin     | F()    | byte       | 1    | 0=no admin, 1=admin
    """
    player_id: int
    admin: int

    @classmethod
    def parse(cls, header: ActionHeader, reader: 'BinaryReader') -> 'PlayerAdminChangeAction':
        """Parse player admin change action from binary data."""
        player_id = reader.read_uint32_be()  # N() - uint32_be
        admin = reader.read_byte()           # F() - byte
        
        return cls(header=header, player_id=player_id, admin=admin)

    def to_dict(self) -> Dict:
        """Convert to dictionary representation."""
        return {
            "type": "player_admin_change",
            "frame_delta": self.frame_delta,
            "sender": self.sender,
            "player_id": self.player_id,
            "admin": self.admin,
            "is_admin": self.admin != 0
        }
