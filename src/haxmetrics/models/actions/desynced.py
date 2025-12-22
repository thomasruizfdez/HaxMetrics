"""
Type 16: Desynced action.

Desync notification (client out of sync with server).
"""

from dataclasses import dataclass
from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from haxmetrics.binary_reader import BinaryReader

from .base import Action
from .action_header import ActionHeader


@dataclass(frozen=True)
class DesyncedAction(Action):
    """
    Desynced action (Type 16).
    
    Notification that a client has desynchronized from the server.
    
    Note: Untested with real fixture (rare in real games).
    
    No additional data after header.
    """

    @classmethod
    def parse(cls, header: ActionHeader, reader: 'BinaryReader') -> 'DesyncedAction':
        """Parse desynced action from binary data (no additional data)."""
        return cls(header=header)

    def to_dict(self) -> Dict:
        """Convert to dictionary representation."""
        return {
            "type": "desynced",
            "frame_delta": self.frame_delta,
            "sender": self.sender
        }
