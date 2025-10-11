from ..action import Action


class PlayerLeft(Action):
    """
    Action index 6 (ma in original JS)
    Player leaves/kicked
    xa(): int Z (player_id), string qd (reason), bool ah (kicked flag)
    """
    def __init__(self):
        super().__init__()
        self.type = "PlayerLeft"
        self.player_id = None
        self.reason = None
        self.kicked = False

    @classmethod
    def parse(cls, reader):
        obj = cls()
        obj.player_id = reader.read_int32()  # N() - int32
        obj.reason = reader.read_nullable_string()  # Ab() - nullable string
        if obj.reason and len(obj.reason) > 100:
            raise ValueError("string too long")
        obj.kicked = reader.read_byte() != 0  # F() - byte as bool
        return obj

    def get_data(self):
        return {
            "player_id": self.player_id,
            "reason": self.reason,
            "kicked": self.kicked,
        }
