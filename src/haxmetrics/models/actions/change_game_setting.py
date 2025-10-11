from ..action import Action


class ChangeGameSetting(Action):
    """
    Action index 10 (va in original JS)
    Game settings change
    xa(): int Gj (setting type), int newValue
    """
    def __init__(self):
        super().__init__()
        self.type = "ChangeGameSetting"
        self.setting = None
        self.value = None

    @classmethod
    def parse(cls, reader):
        obj = cls()
        obj.setting = reader.read_int32()  # N() - int32
        obj.value = reader.read_int32()  # N() - int32
        return obj

    def get_data(self):
        return {"setting": self.setting, "value": self.value}
