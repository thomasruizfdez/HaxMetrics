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
        Parse player from binary data according to HaxBall original scripts.
        Uses read_int32() for IDs, read_string() for strings, read_byte() for bytes.
        """
        player = cls()
        player.set_id(reader.read_int32())
        player.set_name(reader.read_string())
        player.set_admin(reader.read_byte())
        team_val = reader.read_byte()
        # Stadium.parse_team emulated below, replace with Stadium.parse_team if available
        if hasattr(reader, "stadium") and hasattr(reader.stadium, "parse_team"):
            player.set_team(reader.stadium.parse_team(team_val))
        else:
            from .stadium.stadium import Stadium

            player.set_team(Stadium.parse_team(team_val))
        player.set_number(reader.read_byte())
        player.set_avatar(reader.read_string())
        player.set_input(reader.read_int32())
        player.set_kicking(reader.read_byte())
        player.set_desynced(reader.read_byte())
        player.set_country(reader.read_string())
        if version >= 11:
            player.set_handicap(reader.read_uint16())
        player.set_disc_id(reader.read_int32())
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
        self.name = str(name)
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
