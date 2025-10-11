from ..action import Action


class PlayerAdminChange(Action):
    """
    Action index 14 (Ga in original JS)
    Admin change
    xa(): int Ud (player_id), bool jh (is_admin)
    """
    def __init__(self):
        super().__init__()
        self.type = "PlayerAdminChange"
        self.player_id = None
        self.is_admin = None

    @classmethod
    def parse(cls, reader):
        obj = cls()
        obj.player_id = reader.read_int32()  # N() - int32
        obj.is_admin = reader.read_uint8()  # F() - byte
        return obj

    def get_data(self):
        return {"player_id": self.player_id, "is_admin": self.is_admin}
