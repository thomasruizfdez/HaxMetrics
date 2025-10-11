from ..action import Action


class BroadcastPings(Action):
    """
    Action index 17 (Ma in original JS)
    Pings update - array of player pings
    xa(): array of pings (varint count, then each ping as varint)
    """
    def __init__(self):
        super().__init__()
        self.type = "BroadcastPings"
        self.pings = []

    @classmethod
    def parse(cls, reader):
        obj = cls()
        count = reader.read_varint()  # Bb() - varint count
        for _ in range(count):
            ping = reader.read_varint()  # Bb() - varint ping value
            obj.pings.append(ping)
        return obj

    def get_data(self):
        return {"pings": self.pings}
