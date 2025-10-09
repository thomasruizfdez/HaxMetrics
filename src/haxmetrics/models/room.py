from typing import Any, Dict, Optional
from haxmetrics.models.stadium.stadium import Stadium
from haxmetrics.models.game import Game


class Room:
    def __init__(self, version: int):
        self.version = version

        self.kick_timeout = 2
        self.kick_rate_limit = 0
        self.kick_rate_limit_burst = 1

        self.score_limit = None
        self.time_limit = None

        self.teams_locked = None
        self.team_colors = None

        self.name = None

        self.game = None
        self.in_progress = False

        self.players = None
        self.stadium = None

    @classmethod
    def parse(cls, reader, version):
        """
        Parse room info from binary data according to HaxBall original scripts.
        The structure follows the ma(a) method from the original code.
        """
        room = cls(version)

        # 1. Room name (string with varint length)
        room.set_name(reader.read_string())
        
        # 2. Teams locked (1 byte)
        room.set_locked(reader.read_byte())
        
        # 3. Score limit (4 bytes, big-endian)
        room.set_score_limit(reader.read_uint32_be())
        
        # 4. Time limit (4 bytes, big-endian)
        room.set_time_limit(reader.read_uint32_be())
        
        # 5. Kick rate limit burst (2 bytes, big-endian)
        room.kick_rate_limit_burst = reader.read_uint16_be()
        
        # 6. Kick rate limit (1 byte)
        room.kick_rate_limit = reader.read_byte()
        
        # 7. Kick timeout (1 byte)
        room.kick_timeout = reader.read_byte()
        
        # 8. Stadium
        room.set_stadium(Stadium.parse(reader))
        
        # 9. Game active flag (1 byte)
        game_active = reader.read_byte() != 0
        
        # 10. If game is active, parse game state
        if game_active:
            room.set_in_progress(True)
            room.game = Game.parse(reader, room)
            print(f"Game is active - parsed game state at frame {room.game.frame}")
        else:
            room.set_in_progress(False)

        print(f"Parsed Room Name: {room.name}")
        print(f"Is Locked: {room.locked}")
        print(f"Score Limit: {room.score_limit}")
        print(f"Time Limit: {room.time_limit}")
        print(f"Game Active: {game_active}")

        return room

    def json_serialize(self) -> Dict[str, Any]:
        return {
            "frame": self.frame,
            "name": self.name,
            "locked": bool(self.locked),
            "scoreLimit": self.score_limit,
            "timeLimit": self.time_limit,
            "rulesTimer": self.rules_timer,
            "kickOffTaken": bool(self.kick_off_taken),
            "kickOffTeam": self.kick_off_team,
            "ball": {"x": self.ball_x, "y": self.ball_y},
            "score": {"red": self.score_red, "blue": self.score_blue},
            "matchTime": self.match_time,
            "pauseTimer": self.pause_timer,
            "stadium": self.stadium,  # Should be serialized if implemented
            "inProgress": bool(self.in_progress),
        }

    # Setters and Getters
    def set_frame(self, frame):
        self.frame = int(frame)
        return self

    def get_frame(self):
        return self.frame

    def set_name(self, name):
        self.name = str(name)
        return self

    def get_name(self):
        return self.name

    def set_locked(self, status):
        self.locked = bool(status)
        return self

    def get_locked(self):
        return self.locked

    def set_score_limit(self, limit):
        self.score_limit = int(limit)
        return self

    def get_score_limit(self):
        return self.score_limit

    def set_time_limit(self, limit):
        self.time_limit = int(limit)
        return self

    def get_time_limit(self):
        return self.time_limit

    def set_rules_timer(self, rules_timer):
        self.rules_timer = int(rules_timer)
        return self

    def get_rules_timer(self):
        return self.rules_timer

    def set_kick_off_taken(self, state):
        self.kick_off_taken = bool(state)
        return self

    def get_kick_off_taken(self):
        return self.kick_off_taken

    def set_kick_off_team(self, team):
        self.kick_off_team = str(team)
        return self

    def get_kick_off_team(self):
        return self.kick_off_team

    def set_ball_x(self, pos):
        self.ball_x = float(pos)
        return self

    def get_ball_x(self):
        return self.ball_x

    def set_ball_y(self, pos):
        self.ball_y = float(pos)
        return self

    def get_ball_y(self):
        return self.ball_y

    def set_score_red(self, score):
        self.score_red = int(score)
        return self

    def get_score_red(self):
        return self.score_red

    def set_score_blue(self, score):
        self.score_blue = int(score)
        return self

    def get_score_blue(self):
        return self.score_blue

    def set_match_time(self, timer):
        self.match_time = float(timer)
        return self

    def get_match_time(self):
        return self.match_time

    def set_pause_timer(self, timer):
        # version 8 special handling could be implemented here
        self.pause_timer = bool(timer) if self.version == 8 else int(timer)
        return self

    def get_pause_timer(self):
        return self.pause_timer

    def set_stadium(self, stadium):
        self.stadium = stadium
        return self

    def get_stadium(self):
        return self.stadium

    def set_in_progress(self, state):
        self.in_progress = bool(state)
        return self

    def get_in_progress(self):
        return self.in_progress

    def is_playing(self):
        return bool(self.in_progress)
