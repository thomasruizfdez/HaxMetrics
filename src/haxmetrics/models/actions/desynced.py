from ..action import Action


class Desynced(Action):
    def __init__(self):
        super().__init__()
        self.player_id = None

    @classmethod
    def parse(cls, reader):
        obj = cls()
        obj.player_id = reader.read_uint32_be()
        return obj

    def get_data(self):
        return {"player_id": self.player_id}
