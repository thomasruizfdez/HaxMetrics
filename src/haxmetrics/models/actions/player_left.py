from ..action import Action


class PlayerLeft(Action):
    def __init__(self):
        super().__init__()
        self.player_id = None
        self.reason = None

    @classmethod
    def parse(cls, reader):
        obj = cls()
        obj.player_id = reader.read_uint32_be()
        obj.reason = reader.read_uint8()
        return obj

    def get_data(self):
        return {"player_id": self.player_id, "reason": self.reason}
