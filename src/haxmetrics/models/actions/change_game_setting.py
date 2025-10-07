from ..action import Action


class ChangeGameSetting(Action):
    def __init__(self):
        super().__init__()
        self.setting = None
        self.value = None

    @classmethod
    def parse(cls, reader):
        obj = cls()
        obj.setting = reader.read_string_auto()
        obj.value = reader.read_string_auto()
        return obj

    def get_data(self):
        return {"setting": self.setting, "value": self.value}
