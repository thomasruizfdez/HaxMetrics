# Import action classes based on correct mapping from game-min.js
from .actions.message import Message
from .actions.toggle_chat import ToggleChat
from .actions.change_stadium import ChangeStadium
from .actions.player_input import PlayerInput
from .actions.chat_message import ChatMessage
from .actions.player_joined import PlayerJoined
from .actions.player_left import PlayerLeft
from .actions.match_start import MatchStart
from .actions.match_stopped import MatchStopped
from .actions.change_paused import ChangePaused
from .actions.change_game_setting import ChangeGameSetting
from .actions.stadium_update import StadiumUpdate
from .actions.player_team_change import PlayerTeamChange
from .actions.change_teams_lock import ChangeTeamsLock
from .actions.player_admin_change import PlayerAdminChange
from .actions.auto_team_balance import AutoTeamBalance
from .actions.desynced import Desynced
from .actions.broadcast_pings import BroadcastPings
from .actions.avatar_change import AvatarChange
from .actions.team_colors_change import TeamColorsChange
from .actions.player_order_change import PlayerOrderChange
from .actions.kick_rate_limit import KickRateLimit
from .actions.player_avatar_set import PlayerAvatarSet
from .actions.disc_update import DiscUpdate

# Correct action type mapping based on game-min.js lines 4259-4282
# This matches the order in which actions are registered via p.Ja() calls
ACTION_TYPES = [
    Message,                # 0  (Eb) - Message/notification with color and style
    ToggleChat,             # 1  (Ha) - Toggle chat indicator
    ChangeStadium,          # 2  (cb) - Stadium change (loads from compressed bytes)
    PlayerInput,            # 3  (La) - Player input (movement, kick)
    ChatMessage,            # 4  (Ya) - Chat message from player
    PlayerJoined,           # 5  (Na) - Player joins room
    PlayerLeft,             # 6  (ma) - Player leaves/kicked
    MatchStart,             # 7  (Va) - Game start
    MatchStopped,           # 8  (Wa) - Game stop
    ChangePaused,           # 9  (Za) - Pause toggle
    ChangeGameSetting,      # 10 (va) - Game settings change
    StadiumUpdate,          # 11 (Ea) - Stadium data update
    PlayerTeamChange,       # 12 (fa) - Player team change
    ChangeTeamsLock,        # 13 (Fa) - Lock teams
    PlayerAdminChange,      # 14 (Ga) - Admin change
    AutoTeamBalance,        # 15 (Xa) - Auto team balance
    Desynced,               # 16 (Da) - Desync notification
    BroadcastPings,         # 17 (Ma) - Ping updates
    AvatarChange,           # 18 (Qa) - Avatar change
    TeamColorsChange,       # 19 (bb) - Team colors change
    PlayerOrderChange,      # 20 (Fb) - Player order change
    KickRateLimit,          # 21 (Pa) - Kick rate limit
    PlayerAvatarSet,        # 22 (Gb) - Player avatar set
    DiscUpdate,             # 23 (Hb) - Disc/physics update
]
