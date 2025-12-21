from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class Vertex:
    x: float
    y: float
    b_coef: float
    c_mask: Any = None
    c_group: Any = None

    @staticmethod
    def parse(reader, stadium_cls):
        # reader: must have read_double_be() and read_uint32() methods
        # stadium_cls: Stadium class with parse_mask method
        x = reader.read_double_be()
        y = reader.read_double_be()
        b_coef = reader.read_double_be()
        c_mask = stadium_cls.parse_mask(reader.read_uint32())
        c_group = stadium_cls.parse_mask(reader.read_uint32())

        print(
            f"    Vertex - x: {x}, y: {y}, b_coef: {b_coef}, c_mask: {c_mask}, c_group: {c_group}"
        )
        return Vertex(x=x, y=y, b_coef=b_coef, c_mask=c_mask, c_group=c_group)

    def to_json(self):
        # If using dataclasses, you can use asdict(self)
        return asdict(self)
