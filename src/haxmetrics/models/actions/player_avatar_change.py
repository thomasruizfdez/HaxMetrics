from ..action import Action


class PlayerAvatarChange(Action):
    def __init__(self):
        super().__init__()
        self.player_id = None
        self.avatar = None

    @classmethod
    def parse(cls, reader):
        obj = cls()
        obj.player_id = reader.read_uint32_be()
        obj.avatar = reader.read_string_auto()
        return obj

    def get_data(self):
        return {"player_id": self.player_id, "avatar": self.avatar}
