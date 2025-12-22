"""
Action header structure.

Universal header that appears before every action in the replay.
"""

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from haxmetrics.binary_reader import BinaryReader

from .action_type import ActionType


@dataclass(frozen=True)
class ActionHeader:
    """
    Universal header for all actions.
    
    Every action in the replay starts with this header, followed by
    action-specific data based on the action_type.
    
    Attributes:
        frame_delta (int): Frames since last action (varint, 1-5 bytes)
        sender (int): Player ID who caused action (uint16_be, 0 = system)
        action_type (ActionType): Type of action (byte, 0-23)
        
    Parsing:
        Field        | Method | Type      | Size | Notes
        -------------|--------|-----------|------|-------
        frame_delta  | Cg()   | varint    | 1-5  | Frames since last action
        sender       | Bb()   | uint16_be | 2    | Player ID (0 = system)
        type         | F()    | byte      | 1    | Action type (0-23)
    """
    frame_delta: int
    sender: int
    action_type: ActionType
    
    @classmethod
    def parse(cls, reader: 'BinaryReader') -> 'ActionHeader':
        """
        Parse action header from binary data.
        
        Args:
            reader: BinaryReader positioned at start of action header
            
        Returns:
            ActionHeader: Parsed action header
            
        Raises:
            EOFError: If not enough data to read header
            ValueError: If action type is invalid
        """
        frame_delta = reader.read_varint()         # Cg() - varint
        sender = reader.read_uint16_be()           # Bb() - uint16_be
        action_type = ActionType(reader.read_byte())  # F() - byte
        
        return cls(
            frame_delta=frame_delta,
            sender=sender,
            action_type=action_type
        )
    
    def to_dict(self) -> dict:
        """
        Convert to dictionary representation.
        
        Returns:
            dict: Dictionary with frame_delta, sender, action_type
        """
        return {
            "frame_delta": self.frame_delta,
            "sender": self.sender,
            "action_type": self.action_type.value,
            "action_type_name": self.action_type.name
        }
