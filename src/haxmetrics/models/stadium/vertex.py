from dataclasses import dataclass, field, asdict
from typing import Any


@dataclass
class Vertex:
    x: float
    y: float
    b_coef: float
    c_mask: Any = field(default=None)
    c_group: Any = field(default=None)

    @staticmethod
    def parse(reader, stadium_cls):
        # reader: debe tener métodos read_double_be() y read_uint32()
        # stadium_cls: clase Stadium con método parse_mask
        x = reader.read_double_be()
        y = reader.read_double_be()
        b_coef = reader.read_double_be()
        c_mask = stadium_cls.parse_mask(reader.read_uint32())
        c_group = stadium_cls.parse_mask(reader.read_uint32())
        return Vertex(x=x, y=y, b_coef=b_coef, c_mask=c_mask, c_group=c_group)

    def to_json(self):
        # Si usas dataclasses, puedes usar asdict(self)
        return asdict(self)
