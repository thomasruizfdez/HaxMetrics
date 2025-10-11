from ..action import Action


class ChangePaused(Action):
    """
    Action index 9 (Za in original JS)
    Pause toggle
    xa(): bool Pf (paused state)
    """
    def __init__(self):
        super().__init__()
        self.type = "ChangePaused"
        self.paused = None

    @classmethod
    def parse(cls, reader):
        obj = cls()
        obj.paused = reader.read_uint8()
        return obj

    def get_data(self):
        return {"paused": self.paused}
