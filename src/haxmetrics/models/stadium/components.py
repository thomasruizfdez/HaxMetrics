"""
Stadium component classes for HaxBall HBR2 replay parsing.

These classes represent the building blocks of custom stadiums:
- Vertex: Points in 2D space (24 bytes)
- Segment: Lines connecting vertices (36 bytes)
- Plane: Collision planes (40 bytes)
- Goal: Goal lines (33 bytes)
- StadiumDisc: Physical discs (92 bytes)
- Joint: Connections between discs (28 bytes)
- PlayerPhysics: Player movement physics (64 bytes)
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Vertex:
    """
    Stadium vertex (32 bytes).
    
    Represents a point in 2D space used by segments.
    From game-min.js class G.ma(a):
    - x, y, bcoef as float64
    - c_mask, c_group as uint32 (NOT float64)
    
    Attributes:
        x: X coordinate
        y: Y coordinate
        b_coef: Bounce coefficient
        c_mask: Collision mask (uint32)
        c_group: Collision group (uint32)
    """
    
    x: float
    y: float
    b_coef: float
    c_mask: int
    c_group: int
    
    @classmethod
    def parse(cls, reader) -> "Vertex":
        """
        Parse vertex from binary reader.
        
        Structure (32 bytes total):
        - x: float64_be (8 bytes)
        - y: float64_be (8 bytes)
        - b_coef: float64_be (8 bytes)
        - c_mask: uint32_be (4 bytes)
        - c_group: uint32_be (4 bytes)
        
        Args:
            reader: BinaryReader instance
            
        Returns:
            Vertex: Parsed vertex
        """
        return cls(
            x=reader.read_double_be(),
            y=reader.read_double_be(),
            b_coef=reader.read_double_be(),
            c_mask=reader.read_uint32_be(),
            c_group=reader.read_uint32_be()
        )
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            "x": self.x,
            "y": self.y,
            "bCoef": self.b_coef,
            "cMask": self.c_mask,
            "cGroup": self.c_group
        }


@dataclass(frozen=True)
class Segment:
    """
    Stadium segment (variable size 19-39 bytes).
    
    Represents a line between two vertices with physics properties.
    From game-min.js class I.ma(a, b): uses flags byte for optional fields.
    
    Attributes:
        v0: Index of first vertex
        v1: Index of second vertex
        bias: Bias value (optional, default 0)
        curve: Curve value (optional, default infinity)
        color: ARGB color value (optional, default 0)
        visible: Whether segment is visible
        b_coef: Bounce coefficient
        c_mask: Collision mask (uint32)
        c_group: Collision group (uint32)
    """
    
    v0: int
    v1: int
    bias: float
    curve: float
    color: int
    visible: bool
    b_coef: float
    c_mask: int
    c_group: int
    
    @classmethod
    def parse(cls, reader) -> "Segment":
        """
        Parse segment from binary reader.
        
        Structure (variable size):
        - flags: byte (1 byte) - bit flags for optional fields
        - v0: byte (1 byte) - vertex 0 index
        - v1: byte (1 byte) - vertex 1 index
        - bias: float64_be (8 bytes) - only if flags & 1
        - curve: float64_be (8 bytes) - only if flags & 2
        - color: uint32_be (4 bytes) - only if flags & 4
        - visible: boolean from flags & 8
        - b_coef: float64_be (8 bytes)
        - c_mask: uint32_be (4 bytes)
        - c_group: uint32_be (4 bytes)
        
        Min size: 1 + 1 + 1 + 8 + 4 + 4 = 19 bytes
        Max size: 1 + 1 + 1 + 8 + 8 + 4 + 8 + 4 + 4 = 39 bytes
        
        Args:
            reader: BinaryReader instance
            
        Returns:
            Segment: Parsed segment
        """
        flags = reader.read_byte()
        v0 = reader.read_byte()
        v1 = reader.read_byte()
        
        # Optional fields based on flags
        bias = reader.read_double_be() if (flags & 1) != 0 else 0.0
        curve = reader.read_double_be() if (flags & 2) != 0 else float('inf')
        color = reader.read_uint32_be() if (flags & 4) != 0 else 0
        visible = (flags & 8) != 0
        
        # Required fields
        b_coef = reader.read_double_be()
        c_mask = reader.read_uint32_be()
        c_group = reader.read_uint32_be()
        
        return cls(
            v0=v0,
            v1=v1,
            bias=bias,
            curve=curve,
            color=color,
            visible=visible,
            b_coef=b_coef,
            c_mask=c_mask,
            c_group=c_group
        )
    
    def to_dict(self):
        """Convert to dictionary."""
        result = {
            "v0": self.v0,
            "v1": self.v1,
            "bCoef": self.b_coef,
            "cMask": self.c_mask,
            "cGroup": self.c_group
        }
        
        # Only include optional fields if they have non-default values
        if self.bias != 0.0:
            result["bias"] = self.bias
        if self.curve != float('inf'):
            result["curve"] = self.curve
        if self.color != 0:
            result["color"] = self.color
        if self.visible:
            result["vis"] = self.visible
            
        return result


@dataclass(frozen=True)
class Plane:
    """
    Stadium plane (40 bytes).
    
    Represents a collision plane with normal and distance.
    
    Attributes:
        normal_x: Normal vector X component
        normal_y: Normal vector Y component
        dist: Distance from origin
        b_coef: Bounce coefficient
        c_mask: Collision mask
        c_group: Collision group
    """
    
    normal_x: float
    normal_y: float
    dist: float
    b_coef: float
    c_mask: int
    c_group: int
    
    @classmethod
    def parse(cls, reader) -> "Plane":
        """
        Parse plane from binary reader.
        
        Structure (40 bytes):
        - normal_x: float64_be (8 bytes)
        - normal_y: float64_be (8 bytes)
        - dist: float64_be (8 bytes)
        - b_coef: float64_be (8 bytes)
        - c_mask: uint32_be (4 bytes)
        - c_group: uint32_be (4 bytes)
        
        Args:
            reader: BinaryReader instance
            
        Returns:
            Plane: Parsed plane
        """
        return cls(
            normal_x=reader.read_double_be(),
            normal_y=reader.read_double_be(),
            dist=reader.read_double_be(),
            b_coef=reader.read_double_be(),
            c_mask=reader.read_uint32_be(),
            c_group=reader.read_uint32_be()
        )
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            "normal": [self.normal_x, self.normal_y],
            "dist": self.dist,
            "bCoef": self.b_coef,
            "cMask": self.c_mask,
            "cGroup": self.c_group
        }


@dataclass(frozen=True)
class Goal:
    """
    Stadium goal (33 bytes).
    
    Represents a goal line with two points and team assignment.
    
    Attributes:
        p0_x: Point 0 X coordinate
        p0_y: Point 0 Y coordinate
        p1_x: Point 1 X coordinate
        p1_y: Point 1 Y coordinate
        team: Team ID (1=red, 2=blue)
    """
    
    p0_x: float
    p0_y: float
    p1_x: float
    p1_y: float
    team: int
    
    @classmethod
    def parse(cls, reader) -> "Goal":
        """
        Parse goal from binary reader.
        
        Structure (33 bytes):
        - p0_x: float64_be (8 bytes)
        - p0_y: float64_be (8 bytes)
        - p1_x: float64_be (8 bytes)
        - p1_y: float64_be (8 bytes)
        - team: byte (1 byte) - 1=red, 2=blue
        
        Args:
            reader: BinaryReader instance
            
        Returns:
            Goal: Parsed goal
        """
        return cls(
            p0_x=reader.read_double_be(),
            p0_y=reader.read_double_be(),
            p1_x=reader.read_double_be(),
            p1_y=reader.read_double_be(),
            team=reader.read_byte()
        )
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            "p0": [self.p0_x, self.p0_y],
            "p1": [self.p1_x, self.p1_y],
            "team": self.team
        }


@dataclass(frozen=True)
class StadiumDisc:
    """
    Stadium disc (92 bytes).
    
    Represents a physical disc object (ball, player disc, etc.).
    
    Attributes:
        pos_x: Position X
        pos_y: Position Y
        speed_x: Speed X
        speed_y: Speed Y
        gravity_x: Gravity X
        gravity_y: Gravity Y
        radius: Disc radius
        b_coef: Bounce coefficient
        inv_mass: Inverse mass
        damping: Damping coefficient
        color: ARGB color value
        c_mask: Collision mask
        c_group: Collision group
    """
    
    pos_x: float
    pos_y: float
    speed_x: float
    speed_y: float
    gravity_x: float
    gravity_y: float
    radius: float
    b_coef: float
    inv_mass: float
    damping: float
    color: int
    c_mask: int
    c_group: int
    
    @classmethod
    def parse(cls, reader) -> "StadiumDisc":
        """
        Parse disc from binary reader.
        
        Structure (92 bytes):
        - pos_x: float64_be (8 bytes)
        - pos_y: float64_be (8 bytes)
        - speed_x: float64_be (8 bytes)
        - speed_y: float64_be (8 bytes)
        - gravity_x: float64_be (8 bytes)
        - gravity_y: float64_be (8 bytes)
        - radius: float64_be (8 bytes)
        - b_coef: float64_be (8 bytes)
        - inv_mass: float64_be (8 bytes)
        - damping: float64_be (8 bytes)
        - color: uint32_be (4 bytes)
        - c_mask: uint32_be (4 bytes)
        - c_group: uint32_be (4 bytes)
        
        Args:
            reader: BinaryReader instance
            
        Returns:
            StadiumDisc: Parsed disc
        """
        return cls(
            pos_x=reader.read_double_be(),
            pos_y=reader.read_double_be(),
            speed_x=reader.read_double_be(),
            speed_y=reader.read_double_be(),
            gravity_x=reader.read_double_be(),
            gravity_y=reader.read_double_be(),
            radius=reader.read_double_be(),
            b_coef=reader.read_double_be(),
            inv_mass=reader.read_double_be(),
            damping=reader.read_double_be(),
            color=reader.read_uint32_be(),
            c_mask=reader.read_uint32_be(),
            c_group=reader.read_uint32_be()
        )
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            "pos": {"x": self.pos_x, "y": self.pos_y},
            "speed": {"x": self.speed_x, "y": self.speed_y},
            "gravity": {"x": self.gravity_x, "y": self.gravity_y},
            "radius": self.radius,
            "bCoef": self.b_coef,
            "invMass": self.inv_mass,
            "damping": self.damping,
            "color": f"{self.color:08x}",
            "cMask": self.c_mask,
            "cGroup": self.c_group
        }


@dataclass(frozen=True)
class Joint:
    """
    Stadium joint (28 bytes).
    
    Represents a connection between two discs with distance constraints.
    
    Attributes:
        d0: Index of disc 0
        d1: Index of disc 1
        strength: Joint strength (stiffness)
        length: Joint length
        color: ARGB color value (optional)
    """
    
    d0: int
    d1: int
    strength: float
    length: float
    color: Optional[int] = None
    
    @classmethod
    def parse(cls, reader) -> "Joint":
        """
        Parse joint from binary reader.
        
        Structure (28 bytes):
        - d0: byte (1 byte) - disc 0 index
        - d1: byte (1 byte) - disc 1 index
        - strength: float64_be (8 bytes)
        - length: float64_be (8 bytes)
        - color: uint32_be (4 bytes) - ARGB color
        
        Args:
            reader: BinaryReader instance
            
        Returns:
            Joint: Parsed joint
        """
        d0 = reader.read_byte()
        d1 = reader.read_byte()
        strength = reader.read_double_be()
        length = reader.read_double_be()
        color = reader.read_uint32_be()
        
        return cls(
            d0=d0,
            d1=d1,
            strength=strength,
            length=length,
            color=color
        )
    
    def to_dict(self):
        """Convert to dictionary."""
        result = {
            "d0": self.d0,
            "d1": self.d1,
            "strength": self.strength,
            "length": self.length
        }
        if self.color is not None:
            result["color"] = f"{self.color:08x}"
        return result


@dataclass(frozen=True)
class PlayerPhysics:
    """
    Player physics parameters (92 bytes).
    
    Defines default physics for players in the stadium.
    From game-min.js class Ub.ma(a): 12 fields total.
    
    Attributes:
        b_coef: Bounce coefficient
        inv_mass: Inverse mass
        damping: Damping coefficient
        acceleration: Normal acceleration
        kick_acceleration: Acceleration when kicking
        kick_damping: Damping when kicking
        kick_strength: Kick strength
        gravity_x: Gravity X component
        gravity_y: Gravity Y component
        c_group: Collision group (uint32)
        radius: Player disc radius
        inv_mass_2: Second inverse mass value
    """
    
    b_coef: float
    inv_mass: float
    damping: float
    acceleration: float
    kick_acceleration: float
    kick_damping: float
    kick_strength: float
    gravity_x: float
    gravity_y: float
    c_group: int
    radius: float
    inv_mass_2: float
    
    @classmethod
    def parse(cls, reader) -> "PlayerPhysics":
        """
        Parse player physics from binary reader.
        
        Structure (92 bytes total):
        - b_coef: float64_be (8 bytes)
        - inv_mass: float64_be (8 bytes)
        - damping: float64_be (8 bytes)
        - acceleration: float64_be (8 bytes)
        - kick_acceleration: float64_be (8 bytes)
        - kick_damping: float64_be (8 bytes)
        - kick_strength: float64_be (8 bytes)
        - gravity_x: float64_be (8 bytes)
        - gravity_y: float64_be (8 bytes)
        - c_group: uint32_be (4 bytes)
        - radius: float64_be (8 bytes)
        - inv_mass_2: float64_be (8 bytes)
        
        Total: 11*8 + 4 = 92 bytes
        
        Args:
            reader: BinaryReader instance
            
        Returns:
            PlayerPhysics: Parsed player physics
        """
        return cls(
            b_coef=reader.read_double_be(),
            inv_mass=reader.read_double_be(),
            damping=reader.read_double_be(),
            acceleration=reader.read_double_be(),
            kick_acceleration=reader.read_double_be(),
            kick_damping=reader.read_double_be(),
            kick_strength=reader.read_double_be(),
            gravity_x=reader.read_double_be(),
            gravity_y=reader.read_double_be(),
            c_group=reader.read_uint32_be(),
            radius=reader.read_double_be(),
            inv_mass_2=reader.read_double_be()
        )
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            "bCoef": self.b_coef,
            "invMass": self.inv_mass,
            "damping": self.damping,
            "acceleration": self.acceleration,
            "kickingAcceleration": self.kick_acceleration,
            "kickingDamping": self.kick_damping,
            "kickStrength": self.kick_strength,
            "gravity": [self.gravity_x, self.gravity_y],
            "cGroup": self.c_group,
            "radius": self.radius
        }
