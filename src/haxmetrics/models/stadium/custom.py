"""
Custom Stadium class for HaxBall HBR2 replay parsing.

Custom stadiums (type 255) contain full stadium definitions with:
- Basic configuration
- Component arrays (vertices, segments, planes, goals, discs, joints)
- Player physics
"""

from dataclasses import dataclass
from typing import Dict, List

from .base import Stadium
from .components import (
    Goal,
    Joint,
    Plane,
    PlayerPhysics,
    Segment,
    StadiumDisc,
    Vertex,
)


@dataclass(frozen=True)
class CustomStadium(Stadium):
    """
    Custom stadium (type 255).
    
    Contains complete stadium definition with all components.
    Parsing order follows the original stadium.py implementation.
    
    Attributes:
        name: Stadium name
        bg_type: Background type (0=none, 1=grass, 2=hockey)
        bg_width: Background width (float)
        bg_height: Background height (float)
        bg_kick_off_radius: Kick-off circle radius (float)
        bg_corner_radius: Corner arc radius (float)
        bg_goal_line: Goal line distance (float)
        bg_color: Background color (uint32)
        max_view_width: Maximum viewport width
        max_view_height: Maximum viewport height
        spawn_distance: Distance for player spawning
        camera_follow: Camera follow mode
        can_be_stored: Whether stadium can be stored
        kick_off_reset: Reset mode (0=partial, 1=full)
        vertices: List of vertices
        segments: List of segments
        planes: List of planes
        goals: List of goals
        discs: List of discs
        joints: List of joints
        player_physics: Player physics parameters
    """
    
    # Basic configuration
    name: str
    bg_type: int
    bg_width: float
    bg_height: float
    bg_kick_off_radius: float
    bg_corner_radius: float
    bg_goal_line: float
    bg_color: int
    max_view_width: float
    max_view_height: float
    spawn_distance: float
    camera_follow: int
    can_be_stored: bool
    kick_off_reset: bool
    
    # Component arrays
    vertices: List[Vertex]
    segments: List[Segment]
    planes: List[Plane]
    goals: List[Goal]
    discs: List[StadiumDisc]
    joints: List[Joint]
    
    # Player physics
    player_physics: PlayerPhysics
    
    @classmethod
    def parse(cls, reader) -> "CustomStadium":
        """
        Parse custom stadium from binary reader.
        
        Parsing order follows game-min.js class q.ws(a):
        1. Stadium name
        2. Background (type + 5 floats + color = 48 bytes)
        3. Max view width/height (16 bytes)
        4. Spawn distance (8 bytes)
        5. Player physics (92 bytes - 12 fields)
        6. Additional fields (nullable_int32 + 3 bytes)
        7. Component arrays (6 arrays with counts)
        8. Spawn points (red + blue teams)
        
        Args:
            reader: BinaryReader instance
            
        Returns:
            CustomStadium: Parsed custom stadium
        """
        # 1. Stadium name
        name = reader.read_string()
        if name is None:
            name = ""
        
        # 2. Background (48 bytes total)
        bg_type = reader.read_uint32_be()  # 4 bytes
        bg_width = reader.read_double_be()  # 8 bytes
        bg_height = reader.read_double_be()  # 8 bytes
        bg_kick_off_radius = reader.read_double_be()  # 8 bytes
        bg_corner_radius = reader.read_double_be()  # 8 bytes
        bg_goal_line = reader.read_double_be()  # 8 bytes
        bg_color = reader.read_uint32_be()  # 4 bytes
        
        # 3. Max view dimensions (16 bytes)
        max_view_width = reader.read_double_be()
        max_view_height = reader.read_double_be()
        
        # 4. Spawn distance (8 bytes)
        spawn_distance = reader.read_double_be()
        
        # 5. Player physics (92 bytes - 12 fields from game-min.js)
        player_physics = PlayerPhysics.parse(reader)
        
        # 6. Additional fields
        max_view_width_override = reader.read_nullable_int32()  # 1 or 5 bytes
        camera_follow = reader.read_byte()  # 1 byte
        can_be_stored = reader.read_byte() != 0  # 1 byte
        kick_off_reset = reader.read_byte() != 0  # 1 byte
        
        # NOTE: There's an extra 0x00 byte here in the actual data that's not in game-min.js
        # This might be a version difference or undocumented field
        _ = reader.read_byte()  # Skip 1 byte
        
        # 7. Component arrays (each starts with count byte)
        # Vertices (32 bytes each with c_mask/c_group as uint32)
        vertex_count = reader.read_byte()
        vertices = [Vertex.parse(reader) for _ in range(vertex_count)]
        
        # Segments (variable size with flags system)
        segment_count = reader.read_byte()
        segments = [Segment.parse(reader) for _ in range(segment_count)]
        
        # Planes
        plane_count = reader.read_byte()
        planes = [Plane.parse(reader) for _ in range(plane_count)]
        
        # Goals
        goal_count = reader.read_byte()
        goals = [Goal.parse(reader) for _ in range(goal_count)]
        
        # Discs
        disc_count = reader.read_byte()
        discs = [StadiumDisc.parse(reader) for _ in range(disc_count)]
        
        # Joints
        joint_count = reader.read_byte()
        joints = [Joint.parse(reader) for _ in range(joint_count)]
        
        # 8. Spawn points (after component arrays, not before)
        # Red team spawn points
        red_spawn_count = reader.read_byte()
        for _ in range(red_spawn_count):
            _ = reader.read_double_be()  # x
            _ = reader.read_double_be()  # y
        
        # Blue team spawn points
        blue_spawn_count = reader.read_byte()
        for _ in range(blue_spawn_count):
            _ = reader.read_double_be()  # x
            _ = reader.read_double_be()  # y
        
        return cls(
            name=name,
            bg_type=bg_type,
            bg_width=bg_width,
            bg_height=bg_height,
            bg_kick_off_radius=bg_kick_off_radius,
            bg_corner_radius=bg_corner_radius,
            bg_goal_line=bg_goal_line,
            bg_color=bg_color,
            max_view_width=max_view_width,
            max_view_height=max_view_height,
            spawn_distance=spawn_distance,
            camera_follow=camera_follow,
            can_be_stored=can_be_stored,
            kick_off_reset=kick_off_reset,
            vertices=vertices,
            segments=segments,
            planes=planes,
            goals=goals,
            discs=discs,
            joints=joints,
            player_physics=player_physics
        )
    
    def to_dict(self) -> Dict:
        """
        Convert to dictionary representation.
        
        Returns:
            Dict: Dictionary with full stadium data
        """
        bg_type_name = "none"
        if self.bg_type == 1:
            bg_type_name = "grass"
        elif self.bg_type == 2:
            bg_type_name = "hockey"
            
        return {
            "custom": True,
            "name": self.name,
            "background": {
                "type": bg_type_name,
                "width": self.bg_width,
                "height": self.bg_height,
                "kickOffRadius": self.bg_kick_off_radius,
                "cornerRadius": self.bg_corner_radius,
                "goalLine": self.bg_goal_line,
                "color": f"{self.bg_color:08x}"
            },
            "maxViewWidth": self.max_view_width,
            "maxViewHeight": self.max_view_height,
            "spawnDistance": self.spawn_distance,
            "cameraFollow": self.camera_follow,
            "canBeStored": self.can_be_stored,
            "kickOffReset": self.kick_off_reset,
            "vertexes": [v.to_dict() for v in self.vertices],
            "segments": [s.to_dict() for s in self.segments],
            "planes": [p.to_dict() for p in self.planes],
            "goals": [g.to_dict() for g in self.goals],
            "discs": [d.to_dict() for d in self.discs],
            "joints": [j.to_dict() for j in self.joints],
            "playerPhysics": self.player_physics.to_dict()
        }
