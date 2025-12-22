"""
Type 1: Toggle chat action.

Enable or disable chat indicator.
"""

from dataclasses import dataclass
from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from haxmetrics.binary_reader import BinaryReader

from .base import Action
from .action_header import ActionHeader


@dataclass(frozen=True)
class ToggleChatAction(Action):
    """
    Toggle chat action (Type 1).
    
    Enables or disables chat indicator.
    
    Attributes:
        value (int): 0=off, 1=on
        
    Parsing:
        Field  | Method | Type | Size | Notes
        -------|--------|------|------|-------
        value  | F()    | byte | 1    | 0=off, 1=on
    """
    value: int

    @classmethod
    def parse(cls, header: ActionHeader, reader: 'BinaryReader') -> 'ToggleChatAction':
        """Parse toggle chat action from binary data."""
        value = reader.read_byte()  # F() - byte
        
        return cls(header=header, value=value)

    def to_dict(self) -> Dict:
        """Convert to dictionary representation."""
        return {
            "type": "toggle_chat",
            "frame_delta": self.frame_delta,
            "sender": self.sender,
            "value": self.value,
            "enabled": self.value != 0
        }
