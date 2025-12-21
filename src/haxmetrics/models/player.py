"""
Player Parser for HBR2 Replays

This module handles player parsing following game-min.js structure.

Structure (per player) from ua.xa(a, b) method (line 6889-6907):
- admin (byte→bool): Admin flag
- player_id (uint32_be): Player ID
- avatar (string): Avatar string
- unknown_str (string): Unknown string field
- flag (byte→bool): Has country flag
- country (string): Country code
- unknown_int (uint32_be): Unknown integer
- name (string): Player name
- input_state (uint32_be): Input state
- unknown_int16 (uint16_be): Unknown short
- kicking (byte→bool): Is kicking
- unknown_int16_2 (int16_be): Unknown short 2
- unknown_byte (byte): Unknown byte
- team (signed_byte): Team (-1 to 2, where 0=spec, 1=red, 2=blue)
- disc_id (int16_be): Disc ID (-1 if no disc)
"""

from dataclasses import dataclass
from typing import Dict, List, Optional

from haxmetrics.binary_reader import BinaryReader


@dataclass(frozen=True)
class Player:
    """
    Represents a player in the room.
    
    Attributes:
        admin (bool): Whether player is admin
        player_id (int): Unique player ID
        avatar (str): Avatar string
        unknown_str (str): Unknown string field
        flag (bool): Has country flag
        country (str): Country code
        unknown_int (int): Unknown integer
        name (str): Player name
        input_state (int): Input state
        unknown_int16 (int): Unknown short
        kicking (bool): Is kicking
        unknown_int16_2 (int): Unknown short 2
        unknown_byte (int): Unknown byte
        team (int): Team assignment (0=spectator, 1=red, 2=blue)
        disc_id (int): Associated disc ID (-1 if player has no disc)
    """
    admin: bool
    player_id: int
    avatar: str
    unknown_str: str
    flag: bool
    country: str
    unknown_int: int
    name: str
    input_state: int
    unknown_int16: int
    kicking: bool
    unknown_int16_2: int
    unknown_byte: int
    team: int
    disc_id: int
    
    @classmethod
    def parse(cls, reader: BinaryReader) -> 'Player':
        """
        Parse a player from binary reader following game-min.js ua.xa(a, b).
        
        Args:
            reader: BinaryReader positioned at player data
            
        Returns:
            Player: Parsed player instance
        """
        # Parse following exact order from game-min.js line 6889-6907
        admin = reader.read_byte() != 0  # this.fb = 0 != a.F()
        player_id = reader.read_uint32_be()  # this.Nb = a.N()
        avatar = reader.read_string() or ""  # this.Zb = a.Ab()
        unknown_str = reader.read_string() or ""  # this.Sd = a.Ab()
        flag = reader.read_byte() != 0  # this.Td = 0 != a.F()
        country = reader.read_string() or ""  # this.country = a.Ab()
        unknown_int = reader.read_uint32_be()  # this.gh = a.N()
        name = reader.read_string() or ""  # this.D = a.Ab()
        input_state = reader.read_uint32_be()  # this.W = a.N()
        unknown_int16 = reader.read_uint16_be()  # this.Z = a.Bb()
        kicking = reader.read_byte() != 0  # this.Yb = 0 != a.F()
        unknown_int16_2 = reader.read_int16_be()  # this.Bc = a.Di()
        unknown_byte = reader.read_byte()  # this.Zc = a.F()
        team_byte = reader.read_byte()  # let c = a.zf() - but we use F() for signed byte
        # Convert team: 1=red, 2=blue, 0=spectator (game-min.js: 1 == c ? u.ia : 2 == c ? u.Da : u.Oa)
        # Note: In original it's zf() which is signed byte, but values are 0, 1, 2
        team = team_byte if team_byte in [0, 1, 2] else 0
        disc_id = reader.read_int16_be()  # a = a.Di()
        
        return cls(
            admin=admin,
            player_id=player_id,
            avatar=avatar,
            unknown_str=unknown_str,
            flag=flag,
            country=country,
            unknown_int=unknown_int,
            name=name,
            input_state=input_state,
            unknown_int16=unknown_int16,
            kicking=kicking,
            unknown_int16_2=unknown_int16_2,
            unknown_byte=unknown_byte,
            team=team,
            disc_id=disc_id
        )
    
    @property
    def is_spectator(self) -> bool:
        """Check if player is spectator"""
        return self.team == 0
    
    @property
    def is_red(self) -> bool:
        """Check if player is on red team"""
        return self.team == 1
    
    @property
    def is_blue(self) -> bool:
        """Check if player is on blue team"""
        return self.team == 2
    
    @property
    def team_name(self) -> str:
        """Get human-readable team name"""
        return {
            0: "spectators",
            1: "red",
            2: "blue"
        }.get(self.team, "unknown")
    
    @property
    def has_disc(self) -> bool:
        """Check if player has an associated disc"""
        return self.disc_id != -1
    
    def to_dict(self) -> Dict:
        """Convert to dictionary representation"""
        return {
            "player_id": self.player_id,
            "name": self.name,
            "team": self.team,
            "team_name": self.team_name,
            "admin": self.admin,
            "disc_id": self.disc_id,
            "has_disc": self.has_disc,
            "is_spectator": self.is_spectator,
            "is_red": self.is_red,
            "is_blue": self.is_blue,
            "avatar": self.avatar,
            "country": self.country,
            "flag": self.flag,
            "kicking": self.kicking,
            "input_state": self.input_state
        }


@dataclass(frozen=True)
class Players:
    """
    Collection of players in the room.
    
    Attributes:
        players (List[Player]): List of all players
    """
    players: List[Player]
    
    @classmethod
    def parse(cls, reader: BinaryReader) -> 'Players':
        """
        Parse players array from binary reader.
        
        Args:
            reader: BinaryReader positioned at player_count
            
        Returns:
            Players: Parsed players collection
        """
        count = reader.read_byte()
        players = [Player.parse(reader) for _ in range(count)]
        return cls(players=players)
    
    def __len__(self) -> int:
        """Get number of players"""
        return len(self.players)
    
    def __iter__(self):
        """Iterate over players"""
        return iter(self.players)
    
    def __getitem__(self, index: int) -> Player:
        """Get player by index"""
        return self.players[index]
    
    @property
    def spectators(self) -> List[Player]:
        """Get all spectators"""
        return [p for p in self.players if p.is_spectator]
    
    @property
    def red_team(self) -> List[Player]:
        """Get all red team players"""
        return [p for p in self.players if p.is_red]
    
    @property
    def blue_team(self) -> List[Player]:
        """Get all blue team players"""
        return [p for p in self.players if p.is_blue]
    
    @property
    def admins(self) -> List[Player]:
        """Get all admin players"""
        return [p for p in self.players if p.admin]
    
    def to_dict(self) -> Dict:
        """Convert to dictionary representation"""
        return {
            "count": len(self.players),
            "players": [p.to_dict() for p in self.players],
            "spectators_count": len(self.spectators),
            "red_team_count": len(self.red_team),
            "blue_team_count": len(self.blue_team),
            "admins_count": len(self.admins)
        }
