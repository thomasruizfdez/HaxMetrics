from .actions.player_joined import PlayerJoined
from .actions.player_left import PlayerLeft
from .actions.player_admin_change import PlayerAdminChange
from .actions.player_avatar_change import PlayerAvatarChange
from .actions.player_team_change import PlayerTeamChange
from .actions.player_handicap_change import PlayerHandicapChange
from .actions.match_start import MatchStart
from .actions.match_stopped import MatchStopped
from .actions.change_paused import ChangePaused
from .actions.change_teams_lock import ChangeTeamsLock
from .actions.change_game_setting import ChangeGameSetting
from .actions.change_stadium import ChangeStadium
from .actions.change_colors import ChangeColors
from .actions.broadcast_pings import BroadcastPings
from .actions.disc_move import DiscMove
from .actions.logic_update import LogicUpdate
from .actions.chat_message import ChatMessage
from .actions.desynced import Desynced

ACTION_TYPES = [
    PlayerJoined,
    PlayerLeft,
    PlayerAdminChange,
    PlayerAvatarChange,
    PlayerTeamChange,
    PlayerHandicapChange,
    MatchStart,
    MatchStopped,
    ChangePaused,
    ChangeTeamsLock,
    ChangeGameSetting,
    ChangeStadium,
    ChangeColors,
    BroadcastPings,
    DiscMove,
    LogicUpdate,
    ChatMessage,
    Desynced,
]
