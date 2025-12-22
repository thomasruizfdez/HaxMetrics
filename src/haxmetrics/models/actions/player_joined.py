"""
Type 5: Player joined action.

Player joins the room.
"""

from dataclasses import dataclass
from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from haxmetrics.binary_reader import BinaryReader

from .base import Action
from .action_header import ActionHeader


@dataclass(frozen=True)
class PlayerJoinedAction(Action):
    """
    Player joined action (Type 5).
    
    Represents a player joining the room.
    
    Attributes:
        player_id (int): Player ID (uint32_be)
        name (str): Player name
        country (str): Country code (e.g., "es")
        avatar (str): Avatar string
        conn_id (int): Connection ID (byte)
        
    Parsing:
        Field     | Method | Type       | Size | Notes
        ----------|--------|------------|------|-------
        player_id | N()    | uint32_be  | 4    | Player ID
        name      | Ab()   | string     | var  | Player name
        country   | Ab()   | string     | var  | Country code
        avatar    | Ab()   | string     | var  | Avatar string
        conn_id   | F()    | byte       | 1    | Connection ID
    """
    player_id: int
    name: str
    country: str
    avatar: str
    conn_id: int

    @classmethod
    def parse(cls, header: ActionHeader, reader: 'BinaryReader') -> 'PlayerJoinedAction':
        """Parse player joined action from binary data."""
        player_id = reader.read_uint32_be()  # N() - uint32_be
        name = reader.read_string()          # Ab() - string
        country = reader.read_string()       # Ab() - string
        avatar = reader.read_string()        # Ab() - string
        conn_id = reader.read_byte()         # F() - byte
        
        return cls(
            header=header,
            player_id=player_id,
            name=name or "",
            country=country or "",
            avatar=avatar or "",
            conn_id=conn_id
        )

    def to_dict(self) -> Dict:
        """Convert to dictionary representation."""
        return {
            "type": "player_joined",
            "frame_delta": self.frame_delta,
            "sender": self.sender,
            "player_id": self.player_id,
            "name": self.name,
            "country": self.country,
            "avatar": self.avatar,
            "conn_id": self.conn_id
        }
