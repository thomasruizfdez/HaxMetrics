from ..action import Action


class ChangeTeamsLock(Action):
    def __init__(self):
        super().__init__()
        self.teams_locked = None

    @classmethod
    def parse(cls, reader):
        obj = cls()
        obj.teams_locked = reader.read_uint8()
        return obj

    def get_data(self):
        return {"teams_locked": self.teams_locked}
