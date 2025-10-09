from dataclasses import dataclass, field
from typing import Any


@dataclass
class BallPhysics:
    radius: float = 0.0
    b_coef: float = 0.0
    inv_mass: float = 0.0
    damping: float = 0.0
    color: str = ""
    c_mask: Any = field(default=None)
    c_group: Any = field(default=None)

    @staticmethod
    def parse(reader, stadium_cls):
        radius = reader.read_double_be()
        b_coef = reader.read_double_be()
        inv_mass = reader.read_double_be()
        damping = reader.read_double_be()
        color = format(reader.read_uint32(), "x")
        c_mask = stadium_cls.parse_mask(reader.read_uint32())
        c_group = stadium_cls.parse_mask(reader.read_uint32())
        return BallPhysics(
            radius=radius,
            b_coef=b_coef,
            inv_mass=inv_mass,
            damping=damping,
            color=color,
            c_mask=c_mask,
            c_group=c_group,
        )

    def to_json(self):
        data = {}
        if self.radius > 0:
            data["radius"] = self.radius
        if self.b_coef > 0:
            data["bCoef"] = self.b_coef
        if self.damping:
            data["damping"] = self.damping
        if self.color:
            data["color"] = self.color
        if self.c_mask:
            data["cMask"] = self.c_mask
        if self.c_group:
            data["cGroup"] = self.c_group
        return data
