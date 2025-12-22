"""
Type 23: Disc update action.

Updates disc/physics state.
"""

from dataclasses import dataclass
from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from haxmetrics.binary_reader import BinaryReader

from .base import Action
from .action_header import ActionHeader


@dataclass(frozen=True)
class DiscUpdateAction(Action):
    """
    Disc update action (Type 23).
    
    Updates the position and velocity of a disc (ball or player disc).
    
    Attributes:
        disc_id (int): Disc ID (uint16_be)
        pos_x (float): Position X (float64_be)
        pos_y (float): Position Y (float64_be)
        speed_x (float): Velocity X (float64_be)
        speed_y (float): Velocity Y (float64_be)
        
    Parsing:
        Field   | Method | Type        | Size | Notes
        --------|--------|-------------|------|-------
        disc_id | Bb()   | uint16_be   | 2    | Disc ID
        pos_x   | w()    | float64_be  | 8    | Position X
        pos_y   | w()    | float64_be  | 8    | Position Y
        speed_x | w()    | float64_be  | 8    | Velocity X
        speed_y | w()    | float64_be  | 8    | Velocity Y
    """
    disc_id: int
    pos_x: float
    pos_y: float
    speed_x: float
    speed_y: float

    @classmethod
    def parse(cls, header: ActionHeader, reader: 'BinaryReader') -> 'DiscUpdateAction':
        """Parse disc update action from binary data."""
        disc_id = reader.read_uint16_be()   # Bb() - uint16_be
        pos_x = reader.read_float64_be()    # w() - float64_be
        pos_y = reader.read_float64_be()    # w() - float64_be
        speed_x = reader.read_float64_be()  # w() - float64_be
        speed_y = reader.read_float64_be()  # w() - float64_be
        
        return cls(
            header=header,
            disc_id=disc_id,
            pos_x=pos_x,
            pos_y=pos_y,
            speed_x=speed_x,
            speed_y=speed_y
        )

    def to_dict(self) -> Dict:
        """Convert to dictionary representation."""
        return {
            "type": "disc_update",
            "frame_delta": self.frame_delta,
            "sender": self.sender,
            "disc_id": self.disc_id,
            "pos_x": self.pos_x,
            "pos_y": self.pos_y,
            "speed_x": self.speed_x,
            "speed_y": self.speed_y
        }
