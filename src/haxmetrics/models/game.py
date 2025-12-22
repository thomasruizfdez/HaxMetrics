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
        Based on HaxBall's Game.ma(a, room) method from game-min.js (class Y, line 7674).
        
        Order (CRITICAL - must match game-min.js exactly):
        1. Parse disc array (Sa.ma - line 77)
        2. Parse game fields (6x uint32_be, 1x float64_be, 1x signed_byte)
        """
        game = cls()
        
        print(f'DEBUG Game.parse: starting at position {reader.position}')
        
        # 1. Parse disc array first (this.va.ma(a) in game-min.js)
        # Sa.ma(a) - line 77: reads disc count (F() = byte), then parses each disc
        disc_count = reader.read_byte()
        print(f'DEBUG Game.parse: disc_count={disc_count}, position={reader.position}')
        
        for i in range(disc_count):
            # qa.ma(a) - line 8016: each disc has 13 fields
            disc_state = {
                # Position (a)
                'x': reader.read_float64_be(),      # w()
                'y': reader.read_float64_be(),      # w()
                # Velocity (G)
                'vx': reader.read_float64_be(),     # w()
                'vy': reader.read_float64_be(),     # w()
                # Damping (ra)
                'damping_x': reader.read_float64_be(),  # w()
                'damping_y': reader.read_float64_be(),  # w()
                # Radius (V)
                'radius': reader.read_float64_be(),     # w()
                # Bounce (o)
                'bounce': reader.read_float64_be(),     # w()
                # Inverse mass (ca)
                'inv_mass': reader.read_float64_be(),   # w()
                # Damping (Ea)
                'damping': reader.read_float64_be(),    # w()
                # Color (S)
                'color': reader.read_varint(),          # jb()
                # Collision mask (i)
                'c_mask': reader.read_uint32_be(),      # N()
                # Collision group (B)
                'c_group': reader.read_uint32_be(),     # N()
            }
            game.discs.append(disc_state)
            print(f'DEBUG Game.parse: parsed disc {i}, position={reader.position}')
        
        print(f'DEBUG Game.parse: after all discs, position={reader.position}')
        
        # 2. Parse game fields (this.yc, this.Cb, this.Tb, this.Ob, this.Nc, this.Ta)
        # Line 7675-7680 in game-min.js
        field_1 = reader.read_uint32_be()  # this.yc = a.N()
        field_2 = reader.read_uint32_be()  # this.Cb = a.N()
        field_3 = reader.read_uint32_be()  # this.Ob = a.N()
        field_4 = reader.read_uint32_be()  # this.Ob = a.N()
        field_5 = reader.read_float64_be() # this.Nc = a.w()
        field_6 = reader.read_uint32_be()  # this.Ta = a.N()
        team_enum = reader.read_signed_byte()  # a.zf() - team enum
        
        print(f'DEBUG Game.parse: field_1={field_1}, after game fields position={reader.position}')
        
        # Store in game object (mapping unclear, so store as-is for now)
        game.frame = field_1
        game.score_red = field_2 if field_2 < 256 else 0
        game.score_blue = field_3 if field_3 < 256 else 0
        game.match_time = field_5
        game.pause_timer = field_6
        game.kick_off_team = team_enum
        
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
