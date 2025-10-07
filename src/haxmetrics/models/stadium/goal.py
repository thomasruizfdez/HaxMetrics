from dataclasses import dataclass, asdict
from typing import List, Any


@dataclass
class Goal:
    pos_start: List[float]
    pos_end: List[float]
    team: Any

    @staticmethod
    def parse(reader, stadium_cls):
        # reader: debe tener métodos read_double() y read_uint8()
        # stadium_cls: clase Stadium con método parse_team
        pos_start = [reader.read_double(), reader.read_double()]
        pos_end = [reader.read_double(), reader.read_double()]
        team_val = reader.read_uint8()
        team = stadium_cls.parse_team(1 if team_val else 2)
        return Goal(pos_start=pos_start, pos_end=pos_end, team=team)

    def to_json(self):
        return {"p0": self.pos_start, "p1": self.pos_end, "team": self.team}
