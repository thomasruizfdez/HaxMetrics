from ..action import Action


class PlayerJoined(Action):
    """
    Action index 5 (Na in original JS)
    Player joins room
    xa(): int Z (player_id), string name, string uj (country), string Zb (avatar)
    """
    def __init__(self):
        super().__init__()
        self.type = "PlayerJoined"
        self.player_id = None
        self.name = None
        self.country = None
        self.avatar = None

    @classmethod
    def parse(cls, reader):
        obj = cls()
        obj.player_id = reader.read_int32()  # N() - int32
        obj.name = reader.read_nullable_string()  # Ab() - nullable string
        obj.country = reader.read_nullable_string()  # Ab() - nullable string  
        obj.avatar = reader.read_nullable_string()  # Ab() - nullable string
        return obj

    def get_data(self):
        return {
            "player_id": self.player_id,
            "name": self.name,
            "country": self.country,
            "avatar": self.avatar,
        }
