from ..action import Action


class PlayerAvatarSet(Action):
    """
    Action index 22 (Gb in original JS)
    Player avatar set
    xa(): nullable string ac (max 2 chars), int Ke (player_id)
    """
    def __init__(self):
        super().__init__()
        self.type = "PlayerAvatarSet"
        self.avatar = None
        self.player_id = None

    @classmethod
    def parse(cls, reader):
        obj = cls()
        obj.avatar = reader.read_nullable_string()  # Ab() - nullable string
        if obj.avatar and len(obj.avatar) > 2:
            obj.avatar = obj.avatar[:2]  # Truncate to 2 chars
        obj.player_id = reader.read_int32()  # N() - int32
        return obj

    def get_data(self):
        return {"avatar": self.avatar, "player_id": self.player_id}
