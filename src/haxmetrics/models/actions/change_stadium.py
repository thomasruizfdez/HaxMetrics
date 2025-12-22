"""
Type 2: Change stadium action.

Changes the stadium/map.
"""

from dataclasses import dataclass
from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from haxmetrics.binary_reader import BinaryReader

from .base import Action
from .action_header import ActionHeader


@dataclass(frozen=True)
class ChangeStadiumAction(Action):
    """
    Change stadium action (Type 2).
    
    Changes the stadium/map configuration.
    
    Attributes:
        stadium_json (str): Stadium configuration as JSON string
        
    Parsing:
        Field        | Method | Type   | Size | Notes
        -------------|--------|--------|------|-------
        stadium_json | Ab()   | string | var  | Stadium JSON
    """
    stadium_json: str

    @classmethod
    def parse(cls, header: ActionHeader, reader: 'BinaryReader') -> 'ChangeStadiumAction':
        """Parse change stadium action from binary data."""
        stadium_json = reader.read_string()  # Ab() - string
        
        return cls(
            header=header,
            stadium_json=stadium_json or ""
        )

    def to_dict(self) -> Dict:
        """Convert to dictionary representation."""
        return {
            "type": "change_stadium",
            "frame_delta": self.frame_delta,
            "sender": self.sender,
            "stadium_json": self.stadium_json
        }
