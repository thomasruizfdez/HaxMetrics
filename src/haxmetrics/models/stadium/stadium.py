from typing import Any, Dict, List, Optional
from .vertex import Vertex
from .segment import Segment
from .plane import Plane
from .goal import Goal
from .disc import Disc
from .joint import Joint
from .player_physics import PlayerPhysics
from .ball_physics import BallPhysics
from .background import Background
from .masked_item import MaskedItem


class Stadium:
    # Predefined stadiums and masks
    STADIUMS = [
        "Classic",
        "Easy",
        "Small",
        "Big",
        "Rounded",
        "Hockey",
        "Big Hockey",
        "Big Easy",
        "Big Rounded",
        "Huge",
    ]
    MASKS = {1: "ball", 2: "red", 4: "blue", 8: "redKO", 16: "blueKO", 32: "wall"}
    TEAMS = ["Spectators", "Red", "Blue"]

    def __init__(self):
        self.type: Optional[int] = None
        self.name: Optional[str] = None
        self.custom: bool = False
        self.width: Optional[float] = None
        self.height: Optional[float] = None
        self.spawn_distance: Optional[float] = None
        self.background: Optional[Background] = None
        self.player_physics: Optional[PlayerPhysics] = None
        self.ball_physics: Optional[BallPhysics] = None
        self.vertexes: List[Vertex] = []
        self.segments: List[Segment] = []
        self.planes: List[Plane] = []
        self.goals: List[Goal] = []
        self.discs: List[Disc] = []
        self.joints: List[Joint] = []

    @classmethod
    def parse(cls, reader):
        """
        Parse stadium from binary data according to HaxBall original scripts.
        If type < 255, it's a predefined stadium. If type == 255, it's custom.
        """
        stadium = cls()

        # Read stadium type (1 byte)
        stadium.type = reader.read_byte()

        # If it's a predefined stadium (< 255), just set the name and return
        if stadium.type < len(cls.STADIUMS):
            stadium.set_name(cls.STADIUMS[stadium.type])
            stadium.set_custom(False)
            return stadium

        # Custom stadium (type == 255)
        stadium.set_custom(True)
        stadium.set_name(reader.read_string())

        # Parse custom stadium properties
        stadium.set_background(Background.parse(reader))
        
        # Max view width and height (not the same as background width/height)
        max_view_width = reader.read_double_be()
        max_view_height = reader.read_double_be()
        
        # Spawn distance
        stadium.set_spawn_distance(reader.read_double_be())
        
        # Player physics
        stadium.set_player_physics(PlayerPhysics.parse(reader))
        
        # Additional fields from ws() method
        # max_view_width_override (nullable int32 using Sb() method)
        max_view_width_override = reader.read_nullable_int32()
        
        # Camera follow (uint8/bool)
        camera_follow = reader.read_uint8()
        
        # Can be stored (uint8/bool)
        can_be_stored = reader.read_uint8() != 0
        
        # Full reset after goal (uint8/bool)  
        full_reset = reader.read_uint8() != 0
        
        # Now parse the stadium elements
        stadium.set_vertexes(cls.parse_multiple(reader, Vertex, cls))
        stadium.set_segments(cls.parse_multiple(reader, Segment, cls))
        stadium.set_planes(cls.parse_multiple(reader, Plane, cls))
        stadium.set_goals(cls.parse_multiple(reader, Goal, cls))
        stadium.set_discs(cls.parse_multiple(reader, Disc, cls))
        
        # Joints parsing - parse count and each joint
        joints = []
        joints_count = reader.read_uint8()
        for _ in range(joints_count):
            joint = Joint.parse(reader, cls)
            joints.append(joint)
        stadium.set_joints(joints)
        
        # Spawn points - red team
        red_spawn_count = reader.read_uint8()
        red_spawns = []
        for _ in range(red_spawn_count):
            x = reader.read_double_be()
            y = reader.read_double_be()
            red_spawns.append((x, y))
        
        # Spawn points - blue team
        blue_spawn_count = reader.read_uint8()
        blue_spawns = []
        for _ in range(blue_spawn_count):
            x = reader.read_double_be()
            y = reader.read_double_be()
            blue_spawns.append((x, y))

        return stadium

    @staticmethod
    def parse_multiple(reader, cls_type, stadium_cls):
        items = []
        num = reader.read_uint8()
        for _ in range(num):
            items.append(cls_type.parse(reader, stadium_cls))
        return items

    @classmethod
    def parse_mask(cls, val: int) -> List[str]:
        if val == -1:
            return ["all"]
        masks = []
        for key in sorted(cls.MASKS.keys(), reverse=True):
            if val & key:
                masks.append(cls.MASKS[key])
        return masks

    @classmethod
    def parse_team(cls, team: int) -> str:
        return cls.TEAMS[team] if team < len(cls.TEAMS) else cls.TEAMS[0]

    def json_serialize(self) -> Dict[str, Any]:
        info = {"name": self.name, "custom": self.custom}
        if self.is_custom():
            info.update(
                {
                    "bg": self.background,
                    "playerPhysics": self.player_physics,
                    "ballPhysics": self.ball_physics,
                    "vertexes": self.vertexes,
                    "segments": self.segments,
                    "goals": self.goals,
                    "discs": self.discs,
                    "joints": self.joints,
                }
            )
        return info

    # Setters and Getters
    def set_name(self, name: str):
        self.name = str(name)
        return self

    def get_name(self) -> Optional[str]:
        return self.name

    def set_custom(self, custom: bool):
        self.custom = bool(custom)
        return self

    def is_custom(self) -> bool:
        return self.custom

    def set_width(self, width: float):
        self.width = float(width)
        return self

    def get_width(self) -> Optional[float]:
        return self.width

    def set_height(self, height: float):
        self.height = float(height)
        return self

    def get_height(self) -> Optional[float]:
        return self.height

    def set_background(self, background):
        self.background = background
        return self

    def get_background(self):
        return self.background

    def set_spawn_distance(self, spawn_distance: float):
        self.spawn_distance = float(spawn_distance)
        return self

    def get_spawn_distance(self) -> Optional[float]:
        return self.spawn_distance

    def set_player_physics(self, physics):
        self.player_physics = physics
        return self

    def get_player_physics(self):
        return self.player_physics

    def set_ball_physics(self, ball_physics):
        self.ball_physics = ball_physics
        return self

    def get_ball_physics(self):
        return self.ball_physics

    def set_vertexes(self, vertexes: List[Any]):
        self.vertexes = vertexes
        return self

    def get_vertexes(self) -> List[Any]:
        return self.vertexes

    def set_segments(self, segments: List[Any]):
        self.segments = segments
        return self

    def get_segments(self) -> List[Any]:
        return self.segments

    def set_planes(self, planes: List[Any]):
        self.planes = planes
        return self

    def get_planes(self) -> List[Any]:
        return self.planes

    def set_goals(self, goals: List[Any]):
        self.goals = goals
        return self

    def get_goals(self) -> List[Any]:
        return self.goals

    def set_discs(self, discs: List[Any]):
        self.discs = discs
        return self

    def get_discs(self) -> List[Any]:
        return self.discs

    def set_joints(self, joints: List[Any]):
        self.joints = joints
        return self

    def get_joints(self) -> List[Any]:
        return self.joints
