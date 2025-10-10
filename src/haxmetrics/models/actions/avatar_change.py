from ..action import Action


class AvatarChange(Action):
    """Action 18 (Qa): Avatar change without player ID (sender is implicit)"""
    def __init__(self):
        super().__init__()
        self.avatar = None

    @classmethod
    def parse(cls, reader):
        obj = cls()
        obj.avatar = reader.read_string_auto()
        if obj.avatar is not None and len(obj.avatar) > 2:
            obj.avatar = obj.avatar[:2]  # Limit to 2 characters as in original
        return obj

    def get_data(self):
        return {"avatar": self.avatar}
