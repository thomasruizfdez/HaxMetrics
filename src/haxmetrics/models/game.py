from typing import List, Optional, Any, Dict


class Game:
    """Represents the state of an active game in a HaxBall replay."""

    def __init__(self):
        self.frame: Optional[int] = None
        self.score_red: int = 0
        self.score_blue: int = 0
        self.match_time: float = 0.0
        self.pause_timer: Optional[float] = None
        self.kick_off_team: Optional[int] = None
        self.kick_off_taken: bool = False
        self.rules_timer: Optional[float] = None
        self.ball_x: float = 0.0
        self.ball_y: float = 0.0
        self.discs: List = []

    @classmethod
    def parse(cls, reader, room):
        """
        Parse game state from binary data.
        Follows game-min.js class Y, method ma(a, room).

        Order (must match game-min.js exactly):
        1. Disc array (Sa.ma): disc_count byte then each disc's 13 fields
        2. Game fields: 4x uint32_be, 1x float64_be, 1x uint32_be, 1x signed_byte
        """
        game = cls()

        # 1. Disc array (this.va.ma(a))
        disc_count = reader.read_byte()

        for _ in range(disc_count):
            disc_state = {
                'x':         reader.read_float64_be(),  # a.x
                'y':         reader.read_float64_be(),  # a.y
                'vx':        reader.read_float64_be(),  # G.x
                'vy':        reader.read_float64_be(),  # G.y
                'damping_x': reader.read_float64_be(),  # ra.x
                'damping_y': reader.read_float64_be(),  # ra.y
                'radius':    reader.read_float64_be(),  # V
                'bounce':    reader.read_float64_be(),  # o
                'inv_mass':  reader.read_float64_be(),  # ca
                'damping':   reader.read_float64_be(),  # Ea
                'color':     reader.read_uint32_be(),   # S — jb() is uint32_be per format spec
                'c_mask':    reader.read_uint32_be(),   # i
                'c_group':   reader.read_uint32_be(),   # B
            }
            game.discs.append(disc_state)

        # 2. Game fields
        game.frame          = reader.read_uint32_be()   # yc
        field_cb            = reader.read_uint32_be()   # Cb (unknown)
        game.score_red      = reader.read_uint32_be()   # Tb
        game.score_blue     = reader.read_uint32_be()   # Ob
        game.match_time     = reader.read_float64_be()  # Nc
        game.pause_timer    = reader.read_uint32_be()   # Ta
        game.kick_off_team  = reader.read_signed_byte() # ke

        return game

    def json_serialize(self) -> Dict[str, Any]:
        """Serialize game state to JSON-compatible dict."""
        return {
            'frame': self.frame,
            'score': {
                'red': self.score_red,
                'blue': self.score_blue,
            },
            'matchTime': self.match_time,
            'pauseTimer': self.pause_timer,
            'kickOffTeam': self.kick_off_team,
            'kickOffTaken': self.kick_off_taken,
            'rulesTimer': self.rules_timer,
            'ball': {
                'x': self.ball_x,
                'y': self.ball_y,
            },
            'discs': self.discs,
        }
