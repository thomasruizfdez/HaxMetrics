"""
Type 21: Kick rate limit action.

Sets kick rate limiting parameters.
"""

from dataclasses import dataclass
from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from haxmetrics.binary_reader import BinaryReader

from .base import Action
from .action_header import ActionHeader


@dataclass(frozen=True)
class KickRateLimitAction(Action):
    """
    Kick rate limit action (Type 21).
    
    Sets parameters for kick rate limiting.
    
    Note: Untested with real fixture (rare in real games).
    
    Attributes:
        min (int): Minimum value (uint32_be)
        rate (int): Rate value (uint32_be)
        burst (int): Burst value (uint32_be)
        
    Parsing:
        Field | Method | Type       | Size | Notes
        ------|--------|------------|------|-------
        min   | N()    | uint32_be  | 4    | Minimum
        rate  | N()    | uint32_be  | 4    | Rate
        burst | N()    | uint32_be  | 4    | Burst
    """
    min: int
    rate: int
    burst: int

    @classmethod
    def parse(cls, header: ActionHeader, reader: 'BinaryReader') -> 'KickRateLimitAction':
        """Parse kick rate limit action from binary data."""
        min_val = reader.read_uint32_be()   # N() - uint32_be
        rate = reader.read_uint32_be()      # N() - uint32_be
        burst = reader.read_uint32_be()     # N() - uint32_be
        
        return cls(header=header, min=min_val, rate=rate, burst=burst)

    def to_dict(self) -> Dict:
        """Convert to dictionary representation."""
        return {
            "type": "kick_rate_limit",
            "frame_delta": self.frame_delta,
            "sender": self.sender,
            "min": self.min,
            "rate": self.rate,
            "burst": self.burst
        }
