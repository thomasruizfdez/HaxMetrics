from ..action import Action


class ChangeStadium(Action):
    def __init__(self):
        super().__init__()
        self.stadium = None

    @classmethod
    def parse(cls, reader):
        obj = cls()
        obj.stadium = reader.read_string_auto()
        return obj

    def get_data(self):
        return {"stadium": self.stadium}
