from typing import Any, Dict, List, Optional


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
        self.name: Optional[str] = None
        self.custom: bool = False
        self.width: Optional[float] = None
        self.height: Optional[float] = None
        self.spawn_distance: Optional[float] = None
        self.background = None
        self.player_physics = None
        self.ball_physics = None
        self.vertexes: List[Any] = []
        self.segments: List[Any] = []
        self.planes: List[Any] = []
        self.goals: List[Any] = []
        self.discs: List[Any] = []

    @classmethod
    def parse(cls, reader):
        stadium = cls()
        type_ = reader.read_uint8()
        if type_ < len(cls.STADIUMS):
            stadium.set_name(cls.STADIUMS[type_])
            return stadium
        stadium.set_custom(True)
        stadium.set_name(reader.read_string_auto())
        stadium.set_background(None)  # Background.parse(reader) to be implemented
        stadium.set_width(reader.read_double_be())
        stadium.set_height(reader.read_double_be())
        stadium.set_spawn_distance(reader.read_double_be())
        stadium.set_vertexes(
            cls.parse_multiple(reader, "Vertex")
        )  # Replace with actual Vertex class
        stadium.set_segments(
            cls.parse_multiple(reader, "Segment")
        )  # Replace with actual Segment class
        stadium.set_planes(
            cls.parse_multiple(reader, "Plane")
        )  # Replace with actual Plane class
        stadium.set_goals(
            cls.parse_multiple(reader, "Goal")
        )  # Replace with actual Goal class
        stadium.set_discs(
            cls.parse_multiple(reader, "Disc")
        )  # Replace with actual Disc class
        stadium.set_player_physics(
            None
        )  # PlayerPhysics.parse(reader) to be implemented
        stadium.set_ball_physics(None)  # BallPhysics.parse(reader) to be implemented
        return stadium

    @staticmethod
    def parse_multiple(reader, type_name):
        items = []
        num = reader.read_uint8()
        # Replace with actual parse call for each class, e.g. Vertex.parse(reader)
        for _ in range(num):
            items.append(None)  # Placeholder: type_name + '.parse(reader)'
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
