from ..action import Action


class AvatarChange(Action):
    """
    Action index 18 (Qa in original JS)
    Avatar change
    xa(): nullable string ac (max 2 chars)
    """
    def __init__(self):
        super().__init__()
        self.type = "AvatarChange"
        self.avatar = None

    @classmethod
    def parse(cls, reader):
        obj = cls()
        obj.avatar = reader.read_nullable_string()  # Ab() - nullable string
        if obj.avatar and len(obj.avatar) > 2:
            obj.avatar = obj.avatar[:2]  # Truncate to 2 chars
        return obj

    def get_data(self):
        return {"avatar": self.avatar}
