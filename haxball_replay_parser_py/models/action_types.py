from models.actions.player_joined import PlayerJoined
from models.actions.player_left import PlayerLeft
from models.actions.player_admin_change import PlayerAdminChange
from models.actions.player_avatar_change import PlayerAvatarChange
from models.actions.player_team_change import PlayerTeamChange
from models.actions.player_handicap_change import PlayerHandicapChange
from models.actions.match_start import MatchStart
from models.actions.match_stopped import MatchStopped
from models.actions.change_paused import ChangePaused
from models.actions.change_teams_lock import ChangeTeamsLock
from models.actions.change_game_setting import ChangeGameSetting
from models.actions.change_stadium import ChangeStadium
from models.actions.change_colors import ChangeColors
from models.actions.broadcast_pings import BroadcastPings
from models.actions.disc_move import DiscMove
from models.actions.logic_update import LogicUpdate
from models.actions.chat_message import ChatMessage
from models.actions.desynced import Desynced

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
