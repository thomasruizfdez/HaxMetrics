"""
Type 4: Chat message action.

Chat message from player.
"""

from dataclasses import dataclass
from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from haxmetrics.binary_reader import BinaryReader

from .base import Action
from .action_header import ActionHeader


@dataclass(frozen=True)
class ChatMessageAction(Action):
    """
    Chat message action (Type 4).
    
    Represents a chat message from a player.
    
    Attributes:
        message (str): Chat message text (max 140 characters)
        
    Parsing:
        Field   | Method | Type   | Size | Notes
        --------|--------|--------|------|-------
        message | Ab()   | string | var  | Chat message text
    """
    message: str

    @classmethod
    def parse(cls, header: ActionHeader, reader: 'BinaryReader') -> 'ChatMessageAction':
        """Parse chat message action from binary data."""
        message = reader.read_string()  # Ab() - string
        if message and len(message) > 140:
            raise ValueError("Chat message too long (max 140 characters)")
        
        return cls(
            header=header,
            message=message or ""
        )

    def to_dict(self) -> Dict:
        """Convert to dictionary representation."""
        return {
            "type": "chat_message",
            "frame_delta": self.frame_delta,
            "sender": self.sender,
            "message": self.message
        }
