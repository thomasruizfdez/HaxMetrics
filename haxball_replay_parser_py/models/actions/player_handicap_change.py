from models.action import Action


class PlayerHandicapChange(Action):
    def __init__(self):
        super().__init__()
        self.player_id = None
        self.handicap = None

    @classmethod
    def parse(cls, reader):
        obj = cls()
        obj.player_id = reader.read_uint32_be()
        obj.handicap = reader.read_uint8()
        return obj

    def get_data(self):
        return {"player_id": self.player_id, "handicap": self.handicap}
