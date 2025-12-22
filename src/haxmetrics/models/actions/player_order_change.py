"""
Type 20: Player order change action.

Changes the order of players in the player list.
"""

from dataclasses import dataclass
from typing import List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from haxmetrics.binary_reader import BinaryReader

from .base import Action
from .action_header import ActionHeader


@dataclass(frozen=True)
class PlayerOrderChangeAction(Action):
    """
    Player order change action (Type 20).
    
    Changes the order of players in the player list.
    
    Note: Untested with real fixture (rare in real games).
    
    Attributes:
        count (int): Number of players
        player_ids (List[int]): Array of player IDs in new order
        
    Parsing:
        Field       | Method | Type      | Size | Notes
        ------------|--------|-----------|------|-------
        count       | F()    | byte      | 1    | Number of players
        player_ids  | ...    | uint32_be | var  | Array of player IDs in new order
    """
    count: int
    player_ids: List[int]

    @classmethod
    def parse(cls, header: ActionHeader, reader: 'BinaryReader') -> 'PlayerOrderChangeAction':
        """Parse player order change action from binary data."""
        count = reader.read_byte()  # F() - byte
        player_ids = []
        for _ in range(count):
            player_ids.append(reader.read_uint32_be())  # N() - uint32_be
        
        return cls(header=header, count=count, player_ids=player_ids)

    def to_dict(self) -> Dict:
        """Convert to dictionary representation."""
        return {
            "type": "player_order_change",
            "frame_delta": self.frame_delta,
            "sender": self.sender,
            "count": self.count,
            "player_ids": self.player_ids
        }
