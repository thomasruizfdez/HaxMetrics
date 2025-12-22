"""
Type 3: Player input action.

Player keyboard/mouse input (movement and kick).
"""

from dataclasses import dataclass
from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from haxmetrics.binary_reader import BinaryReader

from .base import Action
from .action_header import ActionHeader


@dataclass(frozen=True)
class PlayerInput(Action):
    """
    Player input action (Type 3).
    
    Represents player keyboard/mouse input.
    
    Attributes:
        input (int): Input bitfield (uint16_be)
                     bit0=left, bit1=right, bit2=up, bit3=down, bit4=kick
        
    Parsing:
        Field | Method | Type      | Size | Notes
        ------|--------|-----------|------|--------------------------------
        input | Bb()   | uint16_be | 2    | Bitfield: bit0=left, bit1=right, bit2=up, bit3=down, bit4=kick
    """
    input: int

    @classmethod
    def parse(cls, header: ActionHeader, reader: 'BinaryReader') -> 'PlayerInput':
        """Parse player input action from binary data."""
        input_value = reader.read_uint16_be()  # Bb() - uint16_be
        
        return cls(header=header, input=input_value)
    
    @property
    def is_left(self) -> bool:
        """Check if left key is pressed."""
        return (self.input & 0b00001) != 0
    
    @property
    def is_right(self) -> bool:
        """Check if right key is pressed."""
        return (self.input & 0b00010) != 0
    
    @property
    def is_up(self) -> bool:
        """Check if up key is pressed."""
        return (self.input & 0b00100) != 0
    
    @property
    def is_down(self) -> bool:
        """Check if down key is pressed."""
        return (self.input & 0b01000) != 0
    
    @property
    def is_kick(self) -> bool:
        """Check if kick key is pressed."""
        return (self.input & 0b10000) != 0

    def to_dict(self) -> Dict:
        """Convert to dictionary representation."""
        return {
            "type": "player_input",
            "frame_delta": self.frame_delta,
            "sender": self.sender,
            "input": self.input,
            "is_left": self.is_left,
            "is_right": self.is_right,
            "is_up": self.is_up,
            "is_down": self.is_down,
            "is_kick": self.is_kick
        }
