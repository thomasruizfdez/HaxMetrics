"""
Team Colors Parser for HBR2 Replays

This module handles team colors parsing following game-min.js structure.

Structure (per team color) from ta.ma(a) method (line 8508+):
- angle (byte): Text angle
- text_color (uint32_be): Text color in ARGB format
- stripe_count (byte): Number of stripes (max 3)
- stripes[] (uint32_be): Array of stripe colors in ARGB format
"""

from dataclasses import dataclass
from typing import Dict, List

from haxmetrics.binary_reader import BinaryReader


@dataclass(frozen=True)
class TeamColor:
    """
    Represents colors for one team.
    
    Size: 6 bytes + (stripe_count * 4 bytes)
    
    Attributes:
        angle (int): Text angle (byte, 0-255)
        text_color (int): Text color (ARGB uint32)
        stripes (List[int]): Stripe colors (ARGB uint32 array)
    """
    angle: int                # byte (not int16)
    text_color: int           # uint32_be (ARGB)
    stripes: List[int]        # uint32_be[] (ARGB)
    
    @classmethod
    def parse(cls, reader: BinaryReader) -> 'TeamColor':
        """
        Parse team color from binary reader following game-min.js ta.ma(a).
        
        Args:
            reader: BinaryReader positioned at team color data
            
        Returns:
            TeamColor: Parsed team color instance
        """
        # Parse following exact order from game-min.js line 8508+
        angle = reader.read_byte()  # this.sd = a.F()
        text_color = reader.read_uint32_be()  # this.pd = a.N()
        stripe_count = reader.read_byte()  # let b = a.F()
        
        # Validate stripe count (game-min.js: if (3 < b) throw v.C("too many"))
        if stripe_count > 3:
            raise ValueError(f"Too many stripes: {stripe_count} (max 3)")
        
        # Parse stripes array
        stripes = [reader.read_uint32_be() for _ in range(stripe_count)]
        
        return cls(
            angle=angle,
            text_color=text_color,
            stripes=stripes
        )
    
    @property
    def text_color_hex(self) -> str:
        """Get text color as hex string (e.g., '#FFFFFFFF')"""
        return f"#{self.text_color:08X}"
    
    @property
    def text_color_rgba(self) -> tuple:
        """Get text color as (R, G, B, A) tuple"""
        a = (self.text_color >> 24) & 0xFF
        r = (self.text_color >> 16) & 0xFF
        g = (self.text_color >> 8) & 0xFF
        b = self.text_color & 0xFF
        return (r, g, b, a)
    
    @property
    def stripes_hex(self) -> List[str]:
        """Get stripe colors as hex strings"""
        return [f"#{color:08X}" for color in self.stripes]
    
    @property
    def has_stripes(self) -> bool:
        """Check if team has stripes"""
        return len(self.stripes) > 0
    
    def to_dict(self) -> Dict:
        """Convert to dictionary representation"""
        return {
            "angle": self.angle,
            "text_color": self.text_color,
            "text_color_hex": self.text_color_hex,
            "text_color_rgba": self.text_color_rgba,
            "stripes": self.stripes,
            "stripes_hex": self.stripes_hex,
            "has_stripes": self.has_stripes
        }


@dataclass(frozen=True)
class TeamColors:
    """
    Represents colors for both teams.
    
    Total size: 12 bytes + stripes (when no stripes)
    
    Attributes:
        red (TeamColor): Red team colors
        blue (TeamColor): Blue team colors
    """
    red: TeamColor
    blue: TeamColor
    
    @classmethod
    def parse(cls, reader: BinaryReader) -> 'TeamColors':
        """
        Parse team colors for both teams.
        
        Order: Red team first, then Blue team
        From game-min.js: this.mb[1].ma(a); this.mb[2].ma(a);
        
        Args:
            reader: BinaryReader positioned at team colors data
            
        Returns:
            TeamColors: Parsed team colors instance
        """
        red = TeamColor.parse(reader)
        blue = TeamColor.parse(reader)
        
        return cls(red=red, blue=blue)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary representation"""
        return {
            "red": self.red.to_dict(),
            "blue": self.blue.to_dict()
        }
