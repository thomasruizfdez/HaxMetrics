from typing import Any, Dict
from haxmetrics.models.stadium.stadium import Stadium


class Room:
    def __init__(self, version: int):
        self.version = version
        self.state = None
        self.idk1 = None
        self.idk2 = None
        self.frame = None
        self.name = None
        self.locked = None
        self.score_limit = None
        self.time_limit = None
        self.rules_timer = None
        self.kick_off_taken = None
        self.kick_off_team = None
        self.ball_x = None
        self.ball_y = None
        self.score_red = None
        self.score_blue = None
        self.match_time = None
        self.pause_timer = None
        self.stadium = None
        self.in_progress = None

    @classmethod
    def parse(cls, reader, version):
        room = cls(version)
        # room.set_frame(reader.read_uint32_be())
        # room.idk1 = reader.read_uint32_be()
        # room.idk2 = reader.read_uint32_be()
        room.set_state(reader.read_uint16())
        if room.get_state() != 0:
            print(f"Unknown room state: {room.get_state()}")
            reader.read_bytes(10)

        room.set_name(reader.read_string_auto())
        room.set_locked(reader.read_uint8())
        room.set_score_limit(reader.read_uint32_be())
        room.set_time_limit(reader.read_uint32_be())

        print(f"32 bytes: {reader.read_bytes(4)}")

        print(f"State: {room.get_state()}")
        print(f"Parsed Room Name: {room.name}")
        print(f"Is Locked: {room.locked}")
        print(f"Score Limit: {room.score_limit}")
        print(f"Time Limit: {room.time_limit}")

        room.set_stadium(Stadium.parse(reader))
        # room.set_rules_timer(reader.read_uint16())
        # room.set_kick_off_taken(reader.read_uint8())
        # room.set_kick_off_team(reader.read_uint8())
        # room.set_ball_x(reader.read_double())
        # room.set_ball_y(reader.read_double())
        # room.set_score_red(reader.read_uint32_be())
        # room.set_score_blue(reader.read_uint32_be())
        # room.set_match_time(reader.read_double())
        # room.set_pause_timer(reader.read_uint8())
        # room.set_in_progress(reader.read_uint8())
        # If stadium is custom, read extra bits (not implemented here)
        # if room.get_stadium() and room.get_stadium().is_custom():
        #     reader.read_bytes(32)

        exit(1)
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
    def set_state(self, state):
        self.state = int(state)
        return self

    def get_state(self):
        return self.state

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
