from ..action import Action


class Message(Action):
    """
    Action index 0 (Eb in original JS)
    Message/notification with color and style
    xa(): string $c (max 1000), int color, byte style, byte Jn
    """
    def __init__(self):
        super().__init__()
        self.type = "Message"
        self.message = None
        self.color = None
        self.style = None
        self.flag = None  # Jn in original

    @classmethod
    def parse(cls, reader):
        obj = cls()
        obj.message = reader.read_string()  # kc() - length-prefixed string
        if obj.message and len(obj.message) > 1000:
            raise ValueError("message too long")
        obj.color = reader.read_int32()  # N() - int32
        obj.style = reader.read_byte()  # F() - byte
        obj.flag = reader.read_byte()  # F() - byte
        return obj

    def get_data(self):
        return {
            "message": self.message,
            "color": self.color,
            "style": self.style,
            "flag": self.flag,
        }
