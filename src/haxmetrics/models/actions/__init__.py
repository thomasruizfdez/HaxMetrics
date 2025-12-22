"""
Actions module - HaxBall replay action parsing.

Exports all action types, enums, and collection classes.
"""

# Core classes
from .action_type import ActionType
from .action_header import ActionHeader
from .base import Action
from .actions_collection import Actions, parse_action

# All 24 action types
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

__all__ = [
    # Core
    "ActionType",
    "ActionHeader",
    "Action",
    "Actions",
    "parse_action",
    # Action types
    "MessageAction",
    "ToggleChatAction",
    "ChangeStadiumAction",
    "PlayerInput",
    "ChatMessageAction",
    "PlayerJoinedAction",
    "PlayerLeftAction",
    "MatchStartAction",
    "MatchStoppedAction",
    "ChangePausedAction",
    "ChangeGameSettingAction",
    "StadiumUpdateAction",
    "PlayerTeamChangeAction",
    "ChangeTeamsLockAction",
    "PlayerAdminChangeAction",
    "AutoTeamBalanceAction",
    "DesyncedAction",
    "BroadcastPingsAction",
    "AvatarChangeAction",
    "TeamColorsChangeAction",
    "PlayerOrderChangeAction",
    "KickRateLimitAction",
    "PlayerAvatarSetAction",
    "DiscUpdateAction",
]
