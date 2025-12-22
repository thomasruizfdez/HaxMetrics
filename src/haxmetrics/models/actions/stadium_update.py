"""
Type 11: Stadium update action.

Updates the stadium configuration.
"""

from dataclasses import dataclass
from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from haxmetrics.binary_reader import BinaryReader

from .base import Action
from .action_header import ActionHeader


@dataclass(frozen=True)
class StadiumUpdateAction(Action):
    """
    Stadium update action (Type 11).
    
    Updates the stadium configuration during the game.
    
    Note: Untested with real fixture (rare in real games).
    
    Attributes:
        stadium_json (str): Updated stadium configuration as JSON string
        
    Parsing:
        Field        | Method | Type   | Size | Notes
        -------------|--------|--------|------|-------
        stadium_json | Ab()   | string | var  | Stadium JSON
    """
    stadium_json: str

    @classmethod
    def parse(cls, header: ActionHeader, reader: 'BinaryReader') -> 'StadiumUpdateAction':
        """Parse stadium update action from binary data."""
        stadium_json = reader.read_string()  # Ab() - string
        
        return cls(
            header=header,
            stadium_json=stadium_json or ""
        )

    def to_dict(self) -> Dict:
        """Convert to dictionary representation."""
        return {
            "type": "stadium_update",
            "frame_delta": self.frame_delta,
            "sender": self.sender,
            "stadium_json": self.stadium_json
        }
