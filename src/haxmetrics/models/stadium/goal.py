from dataclasses import asdict, dataclass
from typing import Any, List


@dataclass
class Goal:
    pos_start: List[float]
    pos_end: List[float]
    team: Any

    @staticmethod
    def parse(reader, stadium_cls):
        # reader: must have read_double_be() and read_uint8() methods
        # stadium_cls: Stadium class with parse_team method
        pos_start = [reader.read_double_be(), reader.read_double_be()]
        pos_end = [reader.read_double_be(), reader.read_double_be()]
        team_val = reader.read_uint8()
        team = stadium_cls.parse_team(1 if team_val else 2)

        print(f"    Goal - p0: {pos_start}, p1: {pos_end}, team: {team}")
        return Goal(pos_start=pos_start, pos_end=pos_end, team=team)

    def to_json(self):
        return {"p0": self.pos_start, "p1": self.pos_end, "team": self.team}
