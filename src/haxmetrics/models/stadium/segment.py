from dataclasses import dataclass, field, asdict
from typing import Any


@dataclass
class Segment:
    v0: float
    v1: float
    b_coef: float
    c_mask: Any = field(default=None)
    c_group: Any = field(default=None)
    curve: float = 0.0
    vis: bool = False
    color: str = ""

    @staticmethod
    def parse(reader, stadium_cls):
        # reader: debe tener métodos read_uint8(), read_double(), read_uint32()
        v0 = float(reader.read_uint8())
        v1 = float(reader.read_uint8())
        b_coef = float(reader.read_double())
        c_mask = stadium_cls.parse_mask(reader.read_uint32())
        c_group = stadium_cls.parse_mask(reader.read_uint32())
        curve = reader.read_double()
        if curve != curve:  # NaN check
            curve = 0.0
        vis = bool(reader.read_uint8())
        color = format(reader.read_uint32(), "x")  # hexadecimal string
        return Segment(
            v0=v0,
            v1=v1,
            b_coef=b_coef,
            c_mask=c_mask,
            c_group=c_group,
            curve=curve,
            vis=vis,
            color=color,
        )

    def to_json(self):
        return asdict(self)
