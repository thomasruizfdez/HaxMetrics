"""
Type 9: Change paused action.

Toggle pause state of the game.
"""

from dataclasses import dataclass
from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from haxmetrics.binary_reader import BinaryReader

from .base import Action
from .action_header import ActionHeader


@dataclass(frozen=True)
class ChangePausedAction(Action):
    """
    Change paused action (Type 9).
    
    Toggles the pause state of the game.
    
    Attributes:
        paused (int): Pause state (0=unpaused, 1=paused)
        
    Parsing:
        Field  | Method | Type | Size | Notes
        -------|--------|------|------|-------
        paused | F()    | byte | 1    | 0=unpaused, 1=paused
    """
    paused: int

    @classmethod
    def parse(cls, header: ActionHeader, reader: 'BinaryReader') -> 'ChangePausedAction':
        """Parse change paused action from binary data."""
        paused = reader.read_byte()  # F() - byte
        
        return cls(header=header, paused=paused)

    def to_dict(self) -> Dict:
        """Convert to dictionary representation."""
        return {
            "type": "change_paused",
            "frame_delta": self.frame_delta,
            "sender": self.sender,
            "paused": self.paused,
            "is_paused": self.paused != 0
        }
