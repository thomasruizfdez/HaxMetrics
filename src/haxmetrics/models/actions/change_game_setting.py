"""
Type 10: Change game setting action.

Changes game settings like score_limit or time_limit.
"""

from dataclasses import dataclass
from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from haxmetrics.binary_reader import BinaryReader

from .base import Action
from .action_header import ActionHeader


@dataclass(frozen=True)
class ChangeGameSettingAction(Action):
    """
    Change game setting action (Type 10).
    
    Changes game settings like score_limit, time_limit, etc.
    
    Attributes:
        key (str): Setting key (e.g., "score_limit", "time_limit")
        value (str): Setting value
        
    Parsing:
        Field | Method | Type   | Size | Notes
        ------|--------|--------|------|-------
        key   | Ab()   | string | var  | Setting key (e.g., "score_limit", "time_limit")
        value | Ab()   | string | var  | Setting value
    """
    key: str
    value: str

    @classmethod
    def parse(cls, header: ActionHeader, reader: 'BinaryReader') -> 'ChangeGameSettingAction':
        """Parse change game setting action from binary data."""
        key = reader.read_string()    # Ab() - string
        value = reader.read_string()  # Ab() - string
        
        return cls(
            header=header,
            key=key or "",
            value=value or ""
        )

    def to_dict(self) -> Dict:
        """Convert to dictionary representation."""
        return {
            "type": "change_game_setting",
            "frame_delta": self.frame_delta,
            "sender": self.sender,
            "key": self.key,
            "value": self.value
        }
