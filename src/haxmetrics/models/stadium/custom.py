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
    Parsing order MUST match game-min.js class q.ma() exactly.
    
    Attributes:
        name: Stadium name
        bg_width: Background width
        bg_height: Background height
        bg_kick_off_radius: Kick-off circle radius
        bg_corner_radius: Corner arc radius
        bg_max_view_width: Maximum viewport width
        camera_follow: Camera follow mode (0=none, 1=player)
        spawn_inv_flags: Spawn inversion flags
        spawn_distance: Distance for player spawning
        can_be_stored: Whether stadium can be stored
        can_kick_off: Whether kick-off is allowed
        kick_off_reset: Reset mode (0=partial, 1=full)
        vertices: List of vertices
        segments: List of segments
        planes: List of planes
        goals: List of goals
        discs: List of discs
        joints: List of joints
        player_physics: Player physics parameters
    """
    
    # Basic configuration (12 fields)
    name: str
    bg_width: int
    bg_height: int
    bg_kick_off_radius: int
    bg_corner_radius: int
    bg_max_view_width: float
    camera_follow: int
    spawn_inv_flags: bool
    spawn_distance: float
    can_be_stored: int
    can_kick_off: int
    kick_off_reset: int
    
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
        
        CRITICAL: Parsing order MUST match game-min.js class q.ma() exactly:
        1. Basic configuration (12 fields)
        2. Component arrays (6 arrays: vertices, segments, planes, goals, discs, joints)
        3. Player physics (8 fields)
        
        Args:
            reader: BinaryReader instance
            
        Returns:
            CustomStadium: Parsed custom stadium
        """
        # 1. Basic configuration (12 fields)
        name = reader.read_string()
        if name is None:
            name = ""
        
        bg_width = reader.read_int32_be()
        bg_height = reader.read_int32_be()
        bg_kick_off_radius = reader.read_int32_be()
        bg_corner_radius = reader.read_int32_be()
        bg_max_view_width = reader.read_double_be()
        camera_follow = reader.read_byte()
        spawn_inv_flags = bool(reader.read_byte())
        spawn_distance = reader.read_double_be()
        can_be_stored = reader.read_byte()
        can_kick_off = reader.read_byte()
        kick_off_reset = reader.read_byte()
        
        # 2. Component arrays (each starts with count byte)
        # 2.1 Vertices
        vertex_count = reader.read_byte()
        vertices = [Vertex.parse(reader) for _ in range(vertex_count)]
        
        # 2.2 Segments
        segment_count = reader.read_byte()
        segments = [Segment.parse(reader) for _ in range(segment_count)]
        
        # 2.3 Planes
        plane_count = reader.read_byte()
        planes = [Plane.parse(reader) for _ in range(plane_count)]
        
        # 2.4 Goals
        goal_count = reader.read_byte()
        goals = [Goal.parse(reader) for _ in range(goal_count)]
        
        # 2.5 Discs
        disc_count = reader.read_byte()
        discs = [StadiumDisc.parse(reader) for _ in range(disc_count)]
        
        # 2.6 Joints
        joint_count = reader.read_byte()
        joints = [Joint.parse(reader) for _ in range(joint_count)]
        
        # 3. Player physics (8 fields, 64 bytes)
        player_physics = PlayerPhysics.parse(reader)
        
        return cls(
            name=name,
            bg_width=bg_width,
            bg_height=bg_height,
            bg_kick_off_radius=bg_kick_off_radius,
            bg_corner_radius=bg_corner_radius,
            bg_max_view_width=bg_max_view_width,
            camera_follow=camera_follow,
            spawn_inv_flags=spawn_inv_flags,
            spawn_distance=spawn_distance,
            can_be_stored=can_be_stored,
            can_kick_off=can_kick_off,
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
        return {
            "custom": True,
            "name": self.name,
            "background": {
                "width": self.bg_width,
                "height": self.bg_height,
                "kickOffRadius": self.bg_kick_off_radius,
                "cornerRadius": self.bg_corner_radius,
                "maxViewWidth": self.bg_max_view_width
            },
            "cameraFollow": self.camera_follow,
            "spawnInvFlags": self.spawn_inv_flags,
            "spawnDistance": self.spawn_distance,
            "canBeStored": self.can_be_stored,
            "canKickOff": self.can_kick_off,
            "kickOffReset": self.kick_off_reset,
            "vertexes": [v.to_dict() for v in self.vertices],
            "segments": [s.to_dict() for s in self.segments],
            "planes": [p.to_dict() for p in self.planes],
            "goals": [g.to_dict() for g in self.goals],
            "discs": [d.to_dict() for d in self.discs],
            "joints": [j.to_dict() for j in self.joints],
            "playerPhysics": self.player_physics.to_dict()
        }
