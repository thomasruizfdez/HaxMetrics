"""
Type 15: Auto team balance action.

Enables or disables auto team balance.
"""

from dataclasses import dataclass
from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from haxmetrics.binary_reader import BinaryReader

from .base import Action
from .action_header import ActionHeader


@dataclass(frozen=True)
class AutoTeamBalanceAction(Action):
    """
    Auto team balance action (Type 15).
    
    Enables or disables automatic team balancing.
    
    Attributes:
        enabled (int): Enable state (0=disabled, 1=enabled)
        
    Parsing:
        Field   | Method | Type | Size | Notes
        --------|--------|------|------|-------
        enabled | F()    | byte | 1    | 0=disabled, 1=enabled
    """
    enabled: int

    @classmethod
    def parse(cls, header: ActionHeader, reader: 'BinaryReader') -> 'AutoTeamBalanceAction':
        """Parse auto team balance action from binary data."""
        enabled = reader.read_byte()  # F() - byte
        
        return cls(header=header, enabled=enabled)

    def to_dict(self) -> Dict:
        """Convert to dictionary representation."""
        return {
            "type": "auto_team_balance",
            "frame_delta": self.frame_delta,
            "sender": self.sender,
            "enabled": self.enabled,
            "is_enabled": self.enabled != 0
        }
