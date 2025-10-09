from dataclasses import dataclass, field, asdict
from typing import Any


@dataclass
class Plane:
    normal_x: float
    normal_y: float
    dist: float
    b_coef: float
    c_mask: Any = field(default=None)
    c_group: Any = field(default=None)

    @staticmethod
    def parse(reader, stadium_cls):
        normal_x = float(reader.read_double_be())
        normal_y = float(reader.read_double_be())
        dist = float(reader.read_double_be())
        b_coef = float(reader.read_double_be())
        c_mask = stadium_cls.parse_mask(reader.read_uint32())
        c_group = stadium_cls.parse_mask(reader.read_uint32())
        return Plane(
            normal_x=normal_x,
            normal_y=normal_y,
            dist=dist,
            b_coef=b_coef,
            c_mask=c_mask,
            c_group=c_group,
        )

    def to_json(self):
        return {
            "normal": [self.normal_x, self.normal_y],
            "dist": self.dist,
            "b_coef": self.b_coef,
            "c_mask": self.c_mask,
            "c_group": self.c_group,
        }
