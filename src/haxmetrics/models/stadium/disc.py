from dataclasses import dataclass, field
from typing import Any


@dataclass
class Disc:
    pos_x: float
    pos_y: float
    velocity_x: float
    velocity_y: float
    radius: float
    b_coef: float
    inv_mass: float
    damping: float
    color: str
    c_mask: Any = field(default=None)
    c_group: Any = field(default=None)

    @staticmethod
    def parse(reader, stadium_cls):
        pos_x = float(reader.read_double())
        pos_y = float(reader.read_double())
        velocity_x = float(reader.read_double())
        velocity_y = float(reader.read_double())
        radius = float(reader.read_double())
        b_coef = float(reader.read_double())
        inv_mass = float(reader.read_double())
        damping = float(reader.read_double())
        color = format(reader.read_uint32(), "x")
        c_mask = stadium_cls.parse_mask(reader.read_uint32())
        c_group = stadium_cls.parse_mask(reader.read_uint32())
        return Disc(
            pos_x=pos_x,
            pos_y=pos_y,
            velocity_x=velocity_x,
            velocity_y=velocity_y,
            radius=radius,
            b_coef=b_coef,
            inv_mass=inv_mass,
            damping=damping,
            color=color,
            c_mask=c_mask,
            c_group=c_group,
        )

    def to_json(self):
        return {
            "pos": {"x": self.pos_x, "y": self.pos_y},
            "velocity": {"x": self.velocity_x, "y": self.velocity_y},
            "radius": self.radius,
            "bCeof": self.b_coef,
            "invMass": self.inv_mass,
            "damping": self.damping,
            "color": self.color,
            "collisionMask": self.c_mask,
            "collisionGroup": self.c_group,
        }
