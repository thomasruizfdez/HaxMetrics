from typing import Optional, Any, Dict


class Player:
    def __init__(self):
        self.id: Optional[int] = None
        self.name: Optional[str] = None
        self.admin: Optional[bool] = None
        self.team: Optional[str] = None
        self.number: Optional[int] = None
        self.avatar: Optional[str] = None
        self.input: Optional[int] = None
        self.kicking: Optional[bool] = None
        self.desynced: Optional[bool] = None
        self.country: Optional[str] = None
        self.handicap: Optional[int] = None
        self.disc_id: Optional[int] = None

    @classmethod
    def parse(cls, reader, version: int):
        """
        Parse player from binary data according to HaxBall's ua.xa(a, b) method.
        Based on game-min.js class ua, method xa().
        
        IMPORTANT: HaxBall uses BIG-ENDIAN by default in the binary reader!
        """
        player = cls()
        
        # this.fb = 0 != a.F(); - admin flag
        player.set_admin(reader.read_byte() != 0)
        
        # this.Nb = a.N(); - player ID (big-endian int32)
        player.set_id(reader.read_uint32_be())
        
        # this.Zb = a.Ab(); - avatar string
        player.set_avatar(reader.read_string())
        
        # this.Sd = a.Ab(); - unknown string (maybe secondary ID or session?)
        unknown_str = reader.read_string()
        
        # this.Td = 0 != a.F(); - unknown bool flag
        unknown_flag = reader.read_byte() != 0
        
        # this.country = a.Ab(); - country string
        player.set_country(reader.read_string())
        
        # this.gh = a.N(); - unknown int32 (big-endian)
        unknown_int = reader.read_uint32_be()
        
        # this.D = a.Ab(); - player name
        player.set_name(reader.read_string())
        
        # this.W = a.N(); - unknown int32 (input state?) (big-endian)
        player.set_input(reader.read_uint32_be())
        
        # this.Z = a.Bb(); - unknown int16 (big-endian)
        unknown_int16 = reader.read_uint16_be()
        
        # this.Yb = 0 != a.F(); - kicking flag
        player.set_kicking(reader.read_byte() != 0)
        
        # this.Bc = a.Di(); - unknown int16 (Di() uses endianness, so big-endian)
        unknown_int16_2 = reader.read_int16_be()
        
        # this.Zc = a.F(); - unknown byte
        unknown_byte = reader.read_byte()
        
        # let c = a.zf(); - team (signed byte)
        # this.fa = 1 == c ? u.ia : 2 == c ? u.Da : u.Oa;
        team_byte = reader.read_byte()
        team_signed = team_byte if team_byte < 128 else team_byte - 256
        if team_signed == 1:
            player.set_team("Red")
        elif team_signed == 2:
            player.set_team("Blue")
        else:
            player.set_team("Spectators")
        
        # a = a.Di(); - disc ID (int16, big-endian)
        # this.I = 0 > a ? null : b[a];
        disc_id = reader.read_int16_be()
        player.set_disc_id(disc_id if disc_id >= 0 else None)
        
        return player

    def json_serialize(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "admin": self.admin,
            "team": self.team,
            "number": self.number,
            "avatar": self.avatar,
            "input": self.input,
            "kicking": self.kicking,
            "desynced": self.desynced,
            "country": self.country,
            "handicap": self.handicap,
            "discId": self.disc_id,
        }

    def set_id(self, id_: int):
        self.id = int(id_)
        return self

    def get_id(self) -> Optional[int]:
        return self.id

    def set_name(self, name: str):
        self.name = str(name) if name is not None else None
        return self

    def get_name(self) -> Optional[str]:
        return self.name

    def set_admin(self, state: int):
        self.admin = bool(state)
        return self

    def is_admin(self) -> Optional[bool]:
        return self.admin

    def set_team(self, team: str):
        self.team = team
        return self

    def get_team(self) -> Optional[str]:
        return self.team

    def set_number(self, number: int):
        self.number = int(number)
        return self

    def get_number(self) -> Optional[int]:
        return self.number

    def set_avatar(self, avatar: str):
        self.avatar = str(avatar)
        return self

    def get_avatar(self) -> Optional[str]:
        return self.avatar

    def set_input(self, input_: int):
        self.input = int(input_)
        return self

    def get_input(self) -> Optional[int]:
        return self.input

    def set_kicking(self, state: int):
        self.kicking = bool(state)
        return self

    def is_kicking(self) -> Optional[bool]:
        return self.kicking

    def set_desynced(self, state: int):
        self.desynced = bool(state)
        return self

    def is_desynced(self) -> Optional[bool]:
        return self.desynced

    def set_country(self, country: str):
        self.country = str(country)
        return self

    def get_country(self) -> Optional[str]:
        return self.country

    def set_handicap(self, handicap: int):
        self.handicap = int(handicap)
        return self

    def get_handicap(self) -> Optional[int]:
        return self.handicap

    def set_disc_id(self, disc_id: int):
        self.disc_id = int(disc_id)
        return self

    def get_disc_id(self) -> Optional[int]:
        return self.disc_id
