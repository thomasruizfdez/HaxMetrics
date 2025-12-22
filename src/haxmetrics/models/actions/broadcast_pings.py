"""
Type 17: Broadcast pings action.

Broadcasts player ping information.
"""

from dataclasses import dataclass
from typing import List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from haxmetrics.binary_reader import BinaryReader

from .base import Action
from .action_header import ActionHeader


@dataclass(frozen=True)
class BroadcastPingsAction(Action):
    """
    Broadcast pings action (Type 17).
    
    Broadcasts ping information for all players.
    
    Note: Based on game-min.js, this action stores ping values only (not player IDs).
    The ping values are stored as varints in the same order as players.
    
    Attributes:
        count (int): Number of pings
        pings (List[int]): Array of ping values (varint each)
        
    Parsing:
        Field | Method | Type  | Size | Notes
        ------|--------|-------|------|-------
        count | Bb()   | varint| 1-5  | Number of pings
        pings | Bb()...| varint| var  | Array of ping values (varint each)
    """
    count: int
    pings: List[int]

    @classmethod
    def parse(cls, header: ActionHeader, reader: 'BinaryReader') -> 'BroadcastPingsAction':
        """Parse broadcast pings action from binary data."""
        count = reader.read_varint()  # Bb() - varint count
        pings = []
        for _ in range(count):
            ping = reader.read_varint()  # Bb() - varint ping value
            pings.append(ping)
        
        return cls(header=header, count=count, pings=pings)

    def to_dict(self) -> Dict:
        """Convert to dictionary representation."""
        return {
            "type": "broadcast_pings",
            "frame_delta": self.frame_delta,
            "sender": self.sender,
            "count": self.count,
            "pings": self.pings
        }
