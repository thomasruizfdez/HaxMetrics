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
        self.discs: List = []  # List of disc states

    @classmethod
    def parse(cls, reader, room):
        """
        Parse game state from binary data.
        Based on HaxBall's Game.ma(a, room) method from game-min.js.
        
        Order matches JavaScript Y.ma() method:
        1. Physics state (disc count + discs) - via this.va.ma(a) -> Sa.ma(a) -> qa.ma(a)
        2. Game fields (yc, Cb, Tb, Ob, Nc, Ta, ke)
        """
        game = cls()
        
        # Parse disc count and disc states FIRST (this.va.ma(a))
        disc_count = reader.read_uint8()
        
        for _ in range(disc_count):
            # Each disc has extensive data (qa.ma(a) method)
            disc_state = {
                # Position vector (this.a)
                'x': reader.read_double_be(),
                'y': reader.read_double_be(),
                # Velocity vector (this.G)
                'vx': reader.read_double_be(),
                'vy': reader.read_double_be(),
                # Unknown vector (this.ra)
                'ra_x': reader.read_double_be(),
                'ra_y': reader.read_double_be(),
                # Radius (this.V)
                'radius': reader.read_double_be(),
                # Bounce coefficient (this.o)
                'bcoef': reader.read_double_be(),
                # Inverse mass (this.ca)
                'inv_mass': reader.read_double_be(),
                # Damping (this.Ea)
                'damping': reader.read_double_be(),
                # Color (this.S) - uint32, NOT nullable (jb() method)
                'color': reader.read_uint32_be(),
                # Collision masks (this.i, this.B) - both int32
                'c_mask': reader.read_int32(),
                'c_group': reader.read_int32(),
            }
            
            game.discs.append(disc_state)
        
        # Now parse game fields (rest of Y.ma() method)
        # this.yc = a.N();
        yc = reader.read_int32()
        
        # this.Cb = a.N(); - game phase/state
        cb = reader.read_int32()
        
        # this.Tb = a.N(); - appears to be red team score
        game.score_red = reader.read_int32()
        
        # this.Ob = a.N(); - appears to be blue team score
        game.score_blue = reader.read_int32()
        
        # this.Nc = a.w(); - match time
        game.match_time = reader.read_double_be()
        
        # this.Ta = a.N(); - timer/pause counter
        ta = reader.read_int32()
        
        # a = a.zf(); - team indicator (signed byte, NOT nullable)
        # this.ke = 1 == a ? u.ia : 2 == a ? u.Da : u.Oa;
        # zf() is getInt8 - reads a signed byte
        ke_value_byte = reader.read_byte()
        # Interpret as signed byte
        ke_value = ke_value_byte if ke_value_byte < 128 else ke_value_byte - 256
        
        if ke_value == 1:
            game.kick_off_team = 1  # red
        elif ke_value == 2:
            game.kick_off_team = 2  # blue
        else:
            game.kick_off_team = None
        
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
