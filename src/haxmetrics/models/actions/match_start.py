from models.action import Action


class MatchStart(Action):
    def __init__(self):
        super().__init__()

    @classmethod
    def parse(cls, reader):
        return cls()

    def get_data(self):
        return {}
