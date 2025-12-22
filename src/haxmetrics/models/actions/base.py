"""
Abstract base class for all actions.

Defines the interface that all action types must implement.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from haxmetrics.binary_reader import BinaryReader

from .action_header import ActionHeader
from .action_type import ActionType


@dataclass(frozen=True)
class Action(ABC):
    """
    Abstract base class for all actions.
    
    All action types must inherit from this and implement parse() and to_dict().
    Actions are immutable dataclasses (frozen=True).
    
    Attributes:
        header (ActionHeader): Universal action header
    """
    header: ActionHeader
    
    @classmethod
    @abstractmethod
    def parse(cls, header: ActionHeader, reader: 'BinaryReader') -> 'Action':
        """
        Parse action-specific data.
        
        This method is called after the header has been parsed.
        Each action type implements its own parsing logic based on
        the action type specification.
        
        Args:
            header: Already-parsed action header
            reader: BinaryReader positioned after header
            
        Returns:
            Concrete action instance
            
        Raises:
            EOFError: If not enough data to parse action
        """
        pass
    
    @property
    def frame_delta(self) -> int:
        """Get frame delta from header."""
        return self.header.frame_delta
    
    @property
    def sender(self) -> int:
        """Get sender ID from header."""
        return self.header.sender
    
    @property
    def action_type(self) -> ActionType:
        """Get action type from header."""
        return self.header.action_type
    
    @abstractmethod
    def to_dict(self) -> Dict:
        """
        Convert to dictionary representation.
        
        Each action type must implement this method to provide
        a dictionary representation of its data.
        
        Returns:
            Dictionary with action data
        """
        pass
