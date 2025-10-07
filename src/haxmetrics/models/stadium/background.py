from dataclasses import dataclass
from typing import Any


@dataclass
class Background:
    type: str
    width: float
    height: float
    kick_off_radius: float
    corner_radius: float
    goal_line: float
    color: str

    @staticmethod
    def parse(reader):
        # reader: debe tener métodos read_uint8(), read_double(), read_uint32()
        type_val = reader.read_uint8()
        if type_val == 2:
            bg_type = "hockey"
        elif type_val == 1:
            bg_type = "grass"
        else:
            bg_type = "none"
        width = reader.read_double()
        height = reader.read_double()
        kick_off_radius = reader.read_double()
        corner_radius = reader.read_double()
        goal_line = reader.read_double()
        if goal_line != goal_line:  # NaN check
            goal_line = 0.0
        color = format(reader.read_uint32(), "x")
        return Background(
            type=bg_type,
            width=width,
            height=height,
            kick_off_radius=kick_off_radius,
            corner_radius=corner_radius,
            goal_line=goal_line,
            color=color,
        )

    def to_json(self):
        return {
            "type": self.type,
            "width": self.width,
            "height": self.height,
            "kickOffRadius": self.kick_off_radius,
            "cornerRadius": self.corner_radius,
            "goalLine": self.goal_line,
            "color": self.color,
        }
