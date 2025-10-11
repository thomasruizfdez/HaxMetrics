from ..action import Action


class ChatMessage(Action):
    """
    Action index 4 (Ya in original JS)
    Chat message from player
    xa(): string $c (max 140)
    """
    def __init__(self):
        super().__init__()
        self.type = "ChatMessage"
        self.message = None

    @classmethod
    def parse(cls, reader):
        obj = cls()
        obj.message = reader.read_string()  # kc() - length-prefixed string
        if obj.message and len(obj.message) > 140:
            raise ValueError("message too long")
        return obj

    def get_data(self):
        return {"message": self.message}
