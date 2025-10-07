from models.action import Action


class ChangePaused(Action):
    def __init__(self):
        super().__init__()
        self.paused = None

    @classmethod
    def parse(cls, reader):
        obj = cls()
        obj.paused = reader.read_uint8()
        return obj

    def get_data(self):
        return {"paused": self.paused}
