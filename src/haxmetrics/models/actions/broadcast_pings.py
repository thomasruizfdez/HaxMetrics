from models.action import Action


class BroadcastPings(Action):
    def __init__(self):
        super().__init__()
        self.pings = None

    @classmethod
    def parse(cls, reader):
        obj = cls()
        obj.pings = []
        count = reader.read_uint8()
        for _ in range(count):
            obj.pings.append(reader.read_uint32_be())
        return obj

    def get_data(self):
        return {"pings": self.pings}
