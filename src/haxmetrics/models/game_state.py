"""
GameState Parser for HBR2 Replays

This module handles conditional game state parsing following the HBR2 specification.
Game state is only present when game_active flag is set to 1.

Structure:
- GameDisc: Individual disc (ball or player disc) with position and velocity
- GameState: Complete game state including scores, time, ball position, and all discs
- parse_game_state(): Helper function for conditional parsing
"""

from dataclasses import dataclass
from typing import Dict, List, Optional

from haxmetrics.binary_reader import BinaryReader


@dataclass(frozen=True)
class GameDisc:
    """
    Represents a disc in the game state (ball or player disc).
    
    Size: 92 bytes per disc (following game-min.js qa.ma() structure)
    
    Attributes:
        x (float): X position
        y (float): Y position
        vx (float): X velocity (G.x in game-min.js)
        vy (float): Y velocity (G.y in game-min.js)
        ra_x (float): ra.x value
        ra_y (float): ra.y value
        radius (float): V - radius
        bounce_coef (float): o - bounce coefficient
        inv_mass (float): ca - inverse mass
        damping (float): Ea - damping
        color (int): S - color (uint32)
        c_mask (int): i - collision mask (uint32_be)
        c_group (int): B - collision group (uint32_be)
    """
    x: float
    y: float
    vx: float
    vy: float
    ra_x: float
    ra_y: float
    radius: float
    bounce_coef: float
    inv_mass: float
    damping: float
    color: int
    c_mask: int
    c_group: int
    
    @classmethod
    def parse(cls, reader: BinaryReader) -> 'GameDisc':
        """
        Parse a game disc from binary reader following game-min.js qa.ma() structure.
        
        Args:
            reader: BinaryReader positioned at disc data
            
        Returns:
            GameDisc: Parsed disc instance
        """
        # Position (a.x, a.y)
        x = reader.read_float64_be()
        y = reader.read_float64_be()
        
        # Velocity (G.x, G.y)
        vx = reader.read_float64_be()
        vy = reader.read_float64_be()
        
        # ra (ra.x, ra.y)
        ra_x = reader.read_float64_be()
        ra_y = reader.read_float64_be()
        
        # Physics properties
        radius = reader.read_float64_be()  # V
        bounce_coef = reader.read_float64_be()  # o
        inv_mass = reader.read_float64_be()  # ca
        damping = reader.read_float64_be()  # Ea
        
        # Color (uint32 with endianness from Ua flag)
        # Since we're in decompressed stream, should be uint32 with BinaryReader's default endianness
        # But game-min.js uses getUint32 with this.Ua, which in decompressed mode is big-endian
        color = reader.read_uint32_be()  # S = a.jb()
        
        # Collision properties (uint32_be)
        c_mask = reader.read_uint32_be()  # i = a.N()
        c_group = reader.read_uint32_be()  # B = a.N()
        
        return cls(
            x=x,
            y=y,
            vx=vx,
            vy=vy,
            ra_x=ra_x,
            ra_y=ra_y,
            radius=radius,
            bounce_coef=bounce_coef,
            inv_mass=inv_mass,
            damping=damping,
            color=color,
            c_mask=c_mask,
            c_group=c_group
        )
    
    def to_dict(self) -> Dict:
        """Convert to dictionary representation"""
        return {
            "x": self.x,
            "y": self.y,
            "vx": self.vx,
            "vy": self.vy,
            "ra_x": self.ra_x,
            "ra_y": self.ra_y,
            "radius": self.radius,
            "bounce_coef": self.bounce_coef,
            "inv_mass": self.inv_mass,
            "damping": self.damping,
            "color": self.color,
            "c_mask": self.c_mask,
            "c_group": self.c_group
        }


@dataclass(frozen=True)
class GameState:
    """
    Represents the state of an active game.
    
    This class contains the current game state including scores, time,
    and all disc states. Parsing follows game-min.js Y.ma() structure.
    
    Attributes:
        discs (List[GameDisc]): List of all discs (ball + players) - parsed FIRST
        frame (int): Current frame number (yc in game-min.js)
        field_cb (int): Unknown field (Cb in game-min.js) 
        score_red (int): Red team score (Tb in game-min.js)
        score_blue (int): Blue team score (Ob in game-min.js)
        match_time (float): Time elapsed in seconds (Nc in game-min.js)
        time_limit_or_pause (int): Time limit or pause timer (Ta in game-min.js)
        kickoff_team (Optional[int]): Team for kickoff (1=red, 2=blue, None=no kickoff)
    """
    # Discs are parsed FIRST
    discs: List[GameDisc]
    
    # Game state fields (parsed after discs)
    frame: int
    field_cb: int  # Unknown purpose
    score_red: int
    score_blue: int
    match_time: float
    time_limit_or_pause: int  # Unknown if this is time_limit or pause_timer
    kickoff_team: Optional[int]  # 1=red, 2=blue, None=no team
    
    # Legacy compatibility fields (computed from discs)
    @property
    def ball_x(self) -> float:
        """Get ball X position from first disc (if exists)"""
        return self.discs[0].x if self.discs else 0.0
    
    @property
    def ball_y(self) -> float:
        """Get ball Y position from first disc (if exists)"""
        return self.discs[0].y if self.discs else 0.0
    
    @property
    def pause_timer(self) -> Optional[float]:
        """
        Get pause timer value.
        Returns time_limit_or_pause as float if paused, None otherwise.
        """
        return float(self.time_limit_or_pause) if self.is_paused else None
    
    @property
    def kickoff_taken(self) -> bool:
        """Placeholder for kickoff taken (mapping TBD)"""
        return False
    
    @property
    def rules_timer(self) -> Optional[float]:
        """Placeholder for rules timer (mapping TBD)"""
        return None
    
    @property
    def is_paused(self) -> bool:
        """Check if game is paused (Ta > 0 likely means pause timer is active)"""
        return self.time_limit_or_pause > 0
    
    @property
    def has_kickoff(self) -> bool:
        """Check if there's a kickoff state"""
        return self.kickoff_team is not None
    
    @property
    def has_rules_timer(self) -> bool:
        """Placeholder for rules timer (mapping TBD)"""
        return False
    
    @property
    def winner(self) -> Optional[str]:
        """
        Get current winner based on scores.
        
        Returns:
            "red" if red is winning, "blue" if blue is winning, "tie" if tied, None if 0-0
        """
        if self.score_red == 0 and self.score_blue == 0:
            return None
        elif self.score_red > self.score_blue:
            return "red"
        elif self.score_blue > self.score_red:
            return "blue"
        else:
            return "tie"
    
    def to_dict(self) -> Dict:
        """Convert to dictionary representation"""
        return {
            "frame": self.frame,
            "field_cb": self.field_cb,
            "score_red": self.score_red,
            "score_blue": self.score_blue,
            "match_time": self.match_time,
            "time_limit_or_pause": self.time_limit_or_pause,
            "kickoff_team": self.kickoff_team,
            # Computed/legacy properties
            "pause_timer": self.pause_timer,
            "kickoff_taken": self.kickoff_taken,
            "rules_timer": self.rules_timer,
            "ball_x": self.ball_x,
            "ball_y": self.ball_y,
            "discs": [disc.to_dict() for disc in self.discs],
            "is_paused": self.is_paused,
            "has_kickoff": self.has_kickoff,
            "has_rules_timer": self.has_rules_timer,
            "winner": self.winner
        }
    
    @classmethod
    def parse(cls, reader: BinaryReader) -> 'GameState':
        """
        Parse game state from binary reader following game-min.js Y.ma() structure.
        
        IMPORTANT: This method should only be called when game_active=1.
        The parsing order follows game-min.js exactly:
        1. FIRST: Parse discs (this.va.ma(a))
        2. THEN: Parse game state fields
        
        Args:
            reader: BinaryReader positioned at game state data
            
        Returns:
            GameState: Parsed game state instance
        """
        # 1. Parse discs FIRST (this.va.ma(a))
        disc_count = reader.read_byte()
        discs = [GameDisc.parse(reader) for _ in range(disc_count)]
        
        # 2. Parse game state fields (following Y.ma())
        frame = reader.read_uint32_be()  # this.yc = a.N()
        field_cb = reader.read_uint32_be()  # this.Cb = a.N()
        score_red = reader.read_uint32_be()  # this.Tb = a.N()
        score_blue = reader.read_uint32_be()  # this.Ob = a.N()
        match_time = reader.read_float64_be()  # this.Nc = a.w()
        time_limit_or_pause = reader.read_uint32_be()  # this.Ta = a.N()
        kickoff_team_byte = reader.read_byte()  # a = a.zf()
        
        # Map kickoff team: 1 = red, 2 = blue, 0 = no team
        kickoff_team = kickoff_team_byte if kickoff_team_byte in [1, 2] else None
        
        return cls(
            discs=discs,
            frame=frame,
            field_cb=field_cb,
            score_red=score_red,
            score_blue=score_blue,
            match_time=match_time,
            time_limit_or_pause=time_limit_or_pause,
            kickoff_team=kickoff_team
        )
    
    @property
    def winner(self) -> Optional[str]:
        """
        Get current winner.
        
        Returns:
            "red" if red is winning, "blue" if blue is winning, "tie" if tied, None if 0-0
        """
        if self.score_red == 0 and self.score_blue == 0:
            return None
        elif self.score_red > self.score_blue:
            return "red"
        elif self.score_blue > self.score_red:
            return "blue"
        else:
            return "tie"


def parse_game_state(reader: BinaryReader) -> Optional[GameState]:
    """
    Parse game state section conditionally.
    
    This function handles the conditional logic:
    - If game_active=0: returns None, no bytes read
    - If game_active=1: parses full GameState
    
    Args:
        reader: BinaryReader positioned at game_active flag
        
    Returns:
        GameState if game is active, None otherwise
    """
    game_active = reader.read_byte()
    
    if game_active == 0:
        return None
    else:
        return GameState.parse(reader)
