"""
Type 8: Match stopped action.

Match/game stops.
"""

from dataclasses import dataclass
from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from haxmetrics.binary_reader import BinaryReader

from .base import Action
from .action_header import ActionHeader


@dataclass(frozen=True)
class MatchStoppedAction(Action):
    """
    Match stopped action (Type 8).
    
    Represents the stop of a match/game.
    
    No additional data after header.
    """

    @classmethod
    def parse(cls, header: ActionHeader, reader: 'BinaryReader') -> 'MatchStoppedAction':
        """Parse match stopped action from binary data (no additional data)."""
        return cls(header=header)

    def to_dict(self) -> Dict:
        """Convert to dictionary representation."""
        return {
            "type": "match_stopped",
            "frame_delta": self.frame_delta,
            "sender": self.sender
        }
