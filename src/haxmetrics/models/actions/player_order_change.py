from ..action import Action


class PlayerOrderChange(Action):
    """
    Action index 20 (Fb in original JS)
    Player order change - reorders player list
    xa(): bool An (append/prepend flag), byte count, then count player_ids
    """
    def __init__(self):
        super().__init__()
        self.type = "PlayerOrderChange"
        self.append_mode = False
        self.player_ids = []

    @classmethod
    def parse(cls, reader):
        obj = cls()
        obj.append_mode = reader.read_byte() != 0  # F() - byte as bool
        count = reader.read_byte()  # F() - byte count
        for _ in range(count):
            player_id = reader.read_int32()  # N() - int32
            obj.player_ids.append(player_id)
        return obj

    def get_data(self):
        return {"append_mode": self.append_mode, "player_ids": self.player_ids}
