"""
Type 17: Broadcast pings action.

Broadcasts player ping information.
"""

from dataclasses import dataclass
from typing import List, Tuple, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from haxmetrics.binary_reader import BinaryReader

from .base import Action
from .action_header import ActionHeader


@dataclass(frozen=True)
class BroadcastPingsAction(Action):
    """
    Broadcast pings action (Type 17).
    
    Broadcasts ping information for all players.
    
    Attributes:
        count (int): Number of pings
        pings (List[Tuple[int, int]]): Array of (player_id, ping) tuples
        
    Parsing:
        Field | Method | Type  | Size | Notes
        ------|--------|-------|------|-------
        count | F()    | byte  | 1    | Number of pings
        pings | ...    | array | var  | Array of (player_id: uint32_be, ping: uint16_be)
    """
    count: int
    pings: List[Tuple[int, int]]

    @classmethod
    def parse(cls, header: ActionHeader, reader: 'BinaryReader') -> 'BroadcastPingsAction':
        """Parse broadcast pings action from binary data."""
        count = reader.read_byte()  # F() - byte
        pings = []
        for _ in range(count):
            player_id = reader.read_uint32_be()  # N() - uint32_be
            ping = reader.read_uint16_be()       # Bb() - uint16_be
            pings.append((player_id, ping))
        
        return cls(header=header, count=count, pings=pings)

    def to_dict(self) -> Dict:
        """Convert to dictionary representation."""
        return {
            "type": "broadcast_pings",
            "frame_delta": self.frame_delta,
            "sender": self.sender,
            "count": self.count,
            "pings": [{"player_id": pid, "ping": p} for pid, p in self.pings]
        }
