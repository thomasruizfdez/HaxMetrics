"""
Action type identifiers (0-23).

Based on HBR2 Parsing Guide Section 7 and game-min.js action registration.
"""

from enum import IntEnum


class ActionType(IntEnum):
    """
    Action type identifiers.
    
    Each action type corresponds to a specific event that occurred during replay.
    """
    MESSAGE = 0                  # Type 0: Message/notification with color and style (Eb)
    TOGGLE_CHAT = 1              # Type 1: Toggle chat indicator (Ha)
    CHANGE_STADIUM = 2           # Type 2: Stadium change (cb)
    PLAYER_INPUT = 3             # Type 3: Player input (movement, kick) (La)
    CHAT_MESSAGE = 4             # Type 4: Chat message from player (Ya)
    PLAYER_JOINED = 5            # Type 5: Player joins room (Na)
    PLAYER_LEFT = 6              # Type 6: Player leaves/kicked (ma)
    MATCH_START = 7              # Type 7: Game start (Va)
    MATCH_STOPPED = 8            # Type 8: Game stop (Wa)
    CHANGE_PAUSED = 9            # Type 9: Pause toggle (Za)
    CHANGE_GAME_SETTING = 10     # Type 10: Game settings change (va)
    STADIUM_UPDATE = 11          # Type 11: Stadium data update (Ea)
    PLAYER_TEAM_CHANGE = 12      # Type 12: Player team change (fa)
    CHANGE_TEAMS_LOCK = 13       # Type 13: Lock teams (Fa)
    PLAYER_ADMIN_CHANGE = 14     # Type 14: Admin change (Ga)
    AUTO_TEAM_BALANCE = 15       # Type 15: Auto team balance (Xa)
    DESYNCED = 16                # Type 16: Desync notification (Da)
    BROADCAST_PINGS = 17         # Type 17: Ping updates (Ma)
    AVATAR_CHANGE = 18           # Type 18: Avatar change (Qa)
    TEAM_COLORS_CHANGE = 19      # Type 19: Team colors change (bb)
    PLAYER_ORDER_CHANGE = 20     # Type 20: Player order change (Fb)
    KICK_RATE_LIMIT = 21         # Type 21: Kick rate limit (Pa)
    PLAYER_AVATAR_SET = 22       # Type 22: Player avatar set (Gb)
    DISC_UPDATE = 23             # Type 23: Disc/physics update (Hb)
