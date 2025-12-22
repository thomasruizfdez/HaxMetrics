"""
Type 7: Match start action.

Match/game starts.
"""

from dataclasses import dataclass
from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from haxmetrics.binary_reader import BinaryReader

from .base import Action
from .action_header import ActionHeader


@dataclass(frozen=True)
class MatchStartAction(Action):
    """
    Match start action (Type 7).
    
    Represents the start of a match/game.
    
    No additional data after header.
    """

    @classmethod
    def parse(cls, header: ActionHeader, reader: 'BinaryReader') -> 'MatchStartAction':
        """Parse match start action from binary data (no additional data)."""
        return cls(header=header)

    def to_dict(self) -> Dict:
        """Convert to dictionary representation."""
        return {
            "type": "match_start",
            "frame_delta": self.frame_delta,
            "sender": self.sender
        }
