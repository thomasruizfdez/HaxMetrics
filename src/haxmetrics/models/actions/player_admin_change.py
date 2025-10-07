from models.action import Action


class PlayerAdminChange(Action):
    def __init__(self):
        super().__init__()
        self.player_id = None
        self.is_admin = None

    @classmethod
    def parse(cls, reader):
        obj = cls()
        obj.player_id = reader.read_uint32_be()
        obj.is_admin = reader.read_uint8()
        return obj

    def get_data(self):
        return {"player_id": self.player_id, "is_admin": self.is_admin}
