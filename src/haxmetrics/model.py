from dataclasses import dataclass, field
from typing import Dict, List, Tuple


Vec2 = Tuple[float, float]


@dataclass
class PlayerInfo:
  id: str
  name: str
  team: str # "red" | "blue" | "spec"
  active: bool = True


@dataclass
class PlayerState:
  id: str
  pos: Vec2
  vel: Vec2
  team: str
  on_field: bool = True


@dataclass
class BallState:
  pos: Vec2
  vel: Vec2


@dataclass
class TickState:
  tick: int
  players: Dict[str, PlayerState]
  ball: BallState
  playing: bool


@dataclass
class Touch:
  tick: int
  player_id: str
  team: str
  ball_pos: Vec2


@dataclass
class Header:
  map_name: str
  tps: int
  players: List[PlayerInfo]