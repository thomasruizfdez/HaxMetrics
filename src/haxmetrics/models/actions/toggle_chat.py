from ..action import Action


class ToggleChat(Action):
    """
    Action index 1 (Ha in original JS)
    Toggle chat indicator
    xa(): byte Hj
    """
    def __init__(self):
        super().__init__()
        self.type = "ToggleChat"
        self.flag = None

    @classmethod
    def parse(cls, reader):
        obj = cls()
        obj.flag = reader.read_byte()  # F() - byte
        return obj

    def get_data(self):
        return {"flag": self.flag}
