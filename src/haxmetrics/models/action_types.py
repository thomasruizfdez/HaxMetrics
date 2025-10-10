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
from .actions.avatar_change import AvatarChange
from .actions.team_colors_change import TeamColorsChange
from .actions.player_order_change import PlayerOrderChange
from .actions.kick_rate_limit import KickRateLimit
from .actions.player_avatar_set import PlayerAvatarSet
from .actions.disc_update import DiscUpdate

ACTION_TYPES = [
    PlayerJoined,           # 0 (Eb in original)
    PlayerLeft,             # 1 (Ha in original)
    PlayerAdminChange,      # 2 (cb in original)
    PlayerAvatarChange,     # 3 (La in original - but actually player input)
    PlayerTeamChange,       # 4 (Ya in original - but actually chat)
    PlayerHandicapChange,   # 5 (Na in original - but actually join)
    MatchStart,             # 6 (ma in original - but actually leave)
    MatchStopped,           # 7 (Va in original)
    ChangePaused,           # 8 (Wa in original)
    ChangeTeamsLock,        # 9 (Za in original)
    ChangeGameSetting,      # 10 (va in original)
    ChangeStadium,          # 11 (Ea in original)
    ChangeColors,           # 12 (fa in original)
    BroadcastPings,         # 13 (Fa in original - but actually lock)
    DiscMove,               # 14 (Ga in original - but actually admin)
    LogicUpdate,            # 15 (Xa in original)
    ChatMessage,            # 16 (Da in original - but actually desync)
    Desynced,               # 17 (Ma in original - but actually ping)
    AvatarChange,           # 18 (Qa in original)
    TeamColorsChange,       # 19 (bb in original)
    PlayerOrderChange,      # 20 (Fb in original)
    KickRateLimit,          # 21 (Pa in original)
    PlayerAvatarSet,        # 22 (Gb in original)
    DiscUpdate,             # 23 (Hb in original)
]
