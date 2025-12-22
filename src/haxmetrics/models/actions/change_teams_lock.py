"""
Type 13: Change teams lock action.

Lock or unlock team changes.
"""

from dataclasses import dataclass
from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from haxmetrics.binary_reader import BinaryReader

from .base import Action
from .action_header import ActionHeader


@dataclass(frozen=True)
class ChangeTeamsLockAction(Action):
    """
    Change teams lock action (Type 13).
    
    Locks or unlocks team changes.
    
    Attributes:
        locked (int): Lock state (0=unlocked, 1=locked)
        
    Parsing:
        Field  | Method | Type | Size | Notes
        -------|--------|------|------|-------
        locked | F()    | byte | 1    | 0=unlocked, 1=locked
    """
    locked: int

    @classmethod
    def parse(cls, header: ActionHeader, reader: 'BinaryReader') -> 'ChangeTeamsLockAction':
        """Parse change teams lock action from binary data."""
        locked = reader.read_byte()  # F() - byte
        
        return cls(header=header, locked=locked)

    def to_dict(self) -> Dict:
        """Convert to dictionary representation."""
        return {
            "type": "change_teams_lock",
            "frame_delta": self.frame_delta,
            "sender": self.sender,
            "locked": self.locked,
            "is_locked": self.locked != 0
        }
