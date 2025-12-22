"""
Type 0: Message action.

System message or notification with color and style.
"""

from dataclasses import dataclass
from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from haxmetrics.binary_reader import BinaryReader

from .base import Action
from .action_header import ActionHeader


@dataclass(frozen=True)
class MessageAction(Action):
    """
    Message action (Type 0).
    
    Represents a system message or notification with formatting.
    
    Attributes:
        message (str): Message text (max 1000 characters)
        color (int): Color in ARGB format (uint32_be)
        style (int): Style flags (byte)
        sound (int): Sound flag (0=no sound, 1=sound) (byte)
        
    Parsing:
        Field    | Method | Type       | Size | Notes
        ---------|--------|------------|------|-------
        message  | Ab()   | string     | var  | Message text
        color    | N()    | uint32_be  | 4    | Color ARGB
        style    | F()    | byte       | 1    | Style flags
        sound    | F()    | byte       | 1    | Sound (0=no, 1=yes)
    """
    message: str
    color: int
    style: int
    sound: int

    @classmethod
    def parse(cls, header: ActionHeader, reader: 'BinaryReader') -> 'MessageAction':
        """Parse message action from binary data."""
        message = reader.read_string()  # Ab() - string
        if message and len(message) > 1000:
            raise ValueError("Message too long (max 1000 characters)")
        
        color = reader.read_uint32_be()  # N() - uint32_be
        style = reader.read_byte()       # F() - byte
        sound = reader.read_byte()       # F() - byte
        
        return cls(
            header=header,
            message=message or "",
            color=color,
            style=style,
            sound=sound
        )

    def to_dict(self) -> Dict:
        """Convert to dictionary representation."""
        return {
            "type": "message",
            "frame_delta": self.frame_delta,
            "sender": self.sender,
            "message": self.message,
            "color": self.color,
            "style": self.style,
            "sound": self.sound
        }
