from ..action import Action


class PlayerAvatarSet(Action):
    """Action 22 (Gb): Set avatar for specific player (includes player ID)"""
    def __init__(self):
        super().__init__()
        self.avatar = None
        self.player_id = None

    @classmethod
    def parse(cls, reader):
        obj = cls()
        obj.avatar = reader.read_string_auto()
        obj.player_id = reader.read_uint32_be()
        if obj.avatar is not None and len(obj.avatar) > 2:
            obj.avatar = obj.avatar[:2]  # Limit to 2 characters as in original
        return obj

    def get_data(self):
        return {
            "avatar": self.avatar,
            "player_id": self.player_id
        }
