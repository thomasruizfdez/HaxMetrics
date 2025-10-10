from ..action import Action


class PlayerOrderChange(Action):
    """Action 20 (Fb): Player order change"""
    def __init__(self):
        super().__init__()
        self.player_ids = None

    @classmethod
    def parse(cls, reader):
        obj = cls()
        count = reader.read_uint8()
        obj.player_ids = []
        for _ in range(count):
            obj.player_ids.append(reader.read_uint32_be())
        return obj

    def get_data(self):
        return {"player_ids": self.player_ids}
