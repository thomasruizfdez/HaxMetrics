from models.actions.player_joined import PlayerJoined
from models.actions.player_left import PlayerLeft
from models.actions.chat_message import ChatMessage
from models.actions.logic_update import LogicUpdate
from models.actions.match_start import MatchStart
from models.actions.match_stopped import MatchStopped
from models.actions.disc_move import DiscMove
from models.actions.player_team_change import PlayerTeamChange
from models.actions.change_teams_lock import ChangeTeamsLock
from models.actions.change_game_setting import ChangeGameSetting
from models.actions.player_avatar_change import PlayerAvatarChange
from models.actions.desynced import Desynced
from models.actions.player_admin_change import PlayerAdminChange
from models.actions.change_stadium import ChangeStadium
from models.actions.change_paused import ChangePaused
from haxball_replay_parser_py.models.actions.broadcast_pings import BroadcastPings
from models.actions.player_handicap_change import PlayerHandicapChange
from models.actions.change_colors import ChangeColors

ACTION_TYPES = [
    PlayerJoined,
    PlayerLeft,
    ChatMessage,
    LogicUpdate,
    MatchStart,
    MatchStopped,
    DiscMove,
    PlayerTeamChange,
    ChangeTeamsLock,
    ChangeGameSetting,
    PlayerAvatarChange,
    Desynced,
    PlayerAdminChange,
    ChangeStadium,
    ChangePaused,
    BroadcastPings,
    PlayerHandicapChange,
    ChangeColors,
]
