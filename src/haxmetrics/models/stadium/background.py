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
        # reader: debe tener métodos read_uint32_be(), read_double_be()
        type_val = reader.read_uint32_be()
        if type_val == 2:
            bg_type = "hockey"
        elif type_val == 1:
            bg_type = "grass"
        else:
            bg_type = "none"
        width = reader.read_double_be()
        height = reader.read_double_be()
        kick_off_radius = reader.read_double_be()
        corner_radius = reader.read_double_be()
        goal_line = reader.read_double_be()
        if goal_line != goal_line:  # NaN check
            goal_line = 0.0
        color = format(reader.read_uint32_be(), "x")
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
