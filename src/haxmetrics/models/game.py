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
        Based on HaxBall's Game.ma(a, room) method.
        """
        game = cls()
        
        # Parse frame number (uint32_be)
        game.frame = reader.read_uint32_be()
        
        # Parse scores (uint8 each)
        game.score_red = reader.read_uint8()
        game.score_blue = reader.read_uint8()
        
        # Parse match time (float64)
        game.match_time = reader.read_float64()
        
        # Parse pause timer (nullable float64)
        has_pause_timer = reader.read_bool()
        if has_pause_timer:
            game.pause_timer = reader.read_float64()
        
        # Parse kick-off team (nullable uint8)
        has_kickoff_team = reader.read_bool()
        if has_kickoff_team:
            game.kick_off_team = reader.read_uint8()
        
        # Parse kick-off taken flag (bool)
        game.kick_off_taken = reader.read_bool()
        
        # Parse rules timer (nullable float64)
        has_rules_timer = reader.read_bool()
        if has_rules_timer:
            game.rules_timer = reader.read_float64()
        
        # Parse ball position (2 float64s)
        game.ball_x = reader.read_float64()
        game.ball_y = reader.read_float64()
        
        # Parse disc count and states
        disc_count = reader.read_uint8()
        for _ in range(disc_count):
            # For each disc, parse its state
            # Position (x, y), velocity (vx, vy) - all float64
            disc_state = {
                'x': reader.read_float64(),
                'y': reader.read_float64(),
                'vx': reader.read_float64(),
                'vy': reader.read_float64(),
            }
            game.discs.append(disc_state)
        
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
