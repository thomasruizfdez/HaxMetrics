from ..action import Action


class LogicUpdate(Action):
    def __init__(self):
        super().__init__()
        self.frame = None

    @classmethod
    def parse(cls, reader):
        obj = cls()
        obj.frame = reader.read_uint32_be()
        return obj

    def get_data(self):
        return {"frame": self.frame}
