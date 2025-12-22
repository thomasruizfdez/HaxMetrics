"""
Actions collection and factory function.

Provides a collection wrapper for actions with helper methods.
"""

from dataclasses import dataclass
from typing import List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from haxmetrics.binary_reader import BinaryReader

from .action_type import ActionType
from .action_header import ActionHeader
from .base import Action

# Import all action types
from .message import MessageAction
from .toggle_chat import ToggleChatAction
from .change_stadium import ChangeStadiumAction
from .player_input import PlayerInput
from .chat_message import ChatMessageAction
from .player_joined import PlayerJoinedAction
from .player_left import PlayerLeftAction
from .match_start import MatchStartAction
from .match_stopped import MatchStoppedAction
from .change_paused import ChangePausedAction
from .change_game_setting import ChangeGameSettingAction
from .stadium_update import StadiumUpdateAction
from .player_team_change import PlayerTeamChangeAction
from .change_teams_lock import ChangeTeamsLockAction
from .player_admin_change import PlayerAdminChangeAction
from .auto_team_balance import AutoTeamBalanceAction
from .desynced import DesyncedAction
from .broadcast_pings import BroadcastPingsAction
from .avatar_change import AvatarChangeAction
from .team_colors_change import TeamColorsChangeAction
from .player_order_change import PlayerOrderChangeAction
from .kick_rate_limit import KickRateLimitAction
from .player_avatar_set import PlayerAvatarSetAction
from .disc_update import DiscUpdateAction


def parse_action(header: ActionHeader, reader: 'BinaryReader') -> Action:
    """
    Factory function to parse action based on type.
    
    Args:
        header: Already-parsed action header
        reader: BinaryReader positioned after header
        
    Returns:
        Concrete Action subclass instance
        
    Raises:
        ValueError: If action type is unknown
    """
    # Map of action types to parser classes
    ACTION_PARSERS = {
        ActionType.MESSAGE: MessageAction,
        ActionType.TOGGLE_CHAT: ToggleChatAction,
        ActionType.CHANGE_STADIUM: ChangeStadiumAction,
        ActionType.PLAYER_INPUT: PlayerInput,
        ActionType.CHAT_MESSAGE: ChatMessageAction,
        ActionType.PLAYER_JOINED: PlayerJoinedAction,
        ActionType.PLAYER_LEFT: PlayerLeftAction,
        ActionType.MATCH_START: MatchStartAction,
        ActionType.MATCH_STOPPED: MatchStoppedAction,
        ActionType.CHANGE_PAUSED: ChangePausedAction,
        ActionType.CHANGE_GAME_SETTING: ChangeGameSettingAction,
        ActionType.STADIUM_UPDATE: StadiumUpdateAction,
        ActionType.PLAYER_TEAM_CHANGE: PlayerTeamChangeAction,
        ActionType.CHANGE_TEAMS_LOCK: ChangeTeamsLockAction,
        ActionType.PLAYER_ADMIN_CHANGE: PlayerAdminChangeAction,
        ActionType.AUTO_TEAM_BALANCE: AutoTeamBalanceAction,
        ActionType.DESYNCED: DesyncedAction,
        ActionType.BROADCAST_PINGS: BroadcastPingsAction,
        ActionType.AVATAR_CHANGE: AvatarChangeAction,
        ActionType.TEAM_COLORS_CHANGE: TeamColorsChangeAction,
        ActionType.PLAYER_ORDER_CHANGE: PlayerOrderChangeAction,
        ActionType.KICK_RATE_LIMIT: KickRateLimitAction,
        ActionType.PLAYER_AVATAR_SET: PlayerAvatarSetAction,
        ActionType.DISC_UPDATE: DiscUpdateAction,
    }
    
    parser_class = ACTION_PARSERS.get(header.action_type)
    
    if parser_class is None:
        raise ValueError(f"Unknown action type: {header.action_type}")
    
    return parser_class.parse(header, reader)


@dataclass(frozen=True)
class Actions:
    """
    Collection of actions in chronological order.
    
    Provides iteration, filtering, and helper methods for working
    with action sequences.
    
    Attributes:
        actions (List[Action]): List of all actions in chronological order
    """
    actions: List[Action]
    
    @classmethod
    def parse(cls, reader: 'BinaryReader') -> 'Actions':
        """
        Parse all actions from reader.
        
        Continues parsing actions until EOF or reader exhausted.
        Each action starts with an ActionHeader followed by action-specific data.
        
        Args:
            reader: BinaryReader positioned at actions section
            
        Returns:
            Actions: Collection of parsed actions
        """
        actions = []
        
        while not reader.is_eof():
            try:
                # Parse header
                header = ActionHeader.parse(reader)
                
                # Parse action based on type
                action = parse_action(header, reader)
                actions.append(action)
                
            except EOFError:
                # Reached end of data
                break
        
        return cls(actions=actions)
    
    def __len__(self) -> int:
        """Get number of actions."""
        return len(self.actions)
    
    def __iter__(self):
        """Iterate over actions."""
        return iter(self.actions)
    
    def __getitem__(self, index: int) -> Action:
        """Get action by index."""
        return self.actions[index]
    
    def filter_by_type(self, action_type: ActionType) -> List[Action]:
        """
        Get all actions of specific type.
        
        Args:
            action_type: Type of actions to filter
            
        Returns:
            List of actions matching the type
        """
        return [a for a in self.actions if a.action_type == action_type]
    
    def filter_by_sender(self, sender: int) -> List[Action]:
        """
        Get all actions from specific player.
        
        Args:
            sender: Player ID to filter (0 = system)
            
        Returns:
            List of actions from the specified sender
        """
        return [a for a in self.actions if a.sender == sender]
    
    def get_absolute_frames(self) -> List[int]:
        """
        Calculate absolute frame numbers for all actions.
        
        Frame deltas are relative to the previous action.
        This method accumulates them to get absolute frame numbers.
        
        Returns:
            List where each element is the absolute frame of that action
        """
        absolute_frames = []
        current_frame = 0
        
        for action in self.actions:
            current_frame += action.frame_delta
            absolute_frames.append(current_frame)
        
        return absolute_frames
    
    def to_dict(self) -> Dict:
        """
        Convert to dictionary representation.
        
        Returns:
            Dictionary with count and list of action dictionaries
        """
        return {
            "count": len(self.actions),
            "actions": [a.to_dict() for a in self.actions]
        }
