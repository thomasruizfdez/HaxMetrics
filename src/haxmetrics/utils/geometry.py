import math
from typing import Tuple


Vec2 = Tuple[float, float]


def v_add(a: Vec2, b: Vec2) -> Vec2: return (a[0]+b[0], a[1]+b[1])
def v_sub(a: Vec2, b: Vec2) -> Vec2: return (a[0]-b[0], a[1]-b[1])
def v_mul(a: Vec2, s: float) -> Vec2: return (a[0]*s, a[1]*s)
def v_len(a: Vec2) -> float: return math.hypot(a[0], a[1])