from ..action import Action


class PlayerInput(Action):
    """
    Action index 3 (La in original JS)
    Player input (movement, kick)
    xa(): uint32 input
    """
    def __init__(self):
        super().__init__()
        self.type = "PlayerInput"
        self.input = None

    @classmethod
    def parse(cls, reader):
        obj = cls()
        obj.input = reader.read_uint32()  # jb() - uint32
        return obj

    def get_data(self):
        return {"input": self.input}
