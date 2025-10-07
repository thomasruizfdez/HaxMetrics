from ..action import Action


class ChangeColors(Action):
    def __init__(self):
        super().__init__()
        self.team = None
        self.colors = None

    @classmethod
    def parse(cls, reader):
        obj = cls()
        obj.team = reader.read_uint8()
        obj.colors = reader.read_string_auto()
        return obj

    def get_data(self):
        return {"team": self.team, "colors": self.colors}
