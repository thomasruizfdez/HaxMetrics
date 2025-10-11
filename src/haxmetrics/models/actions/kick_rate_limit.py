from ..action import Action


class KickRateLimit(Action):
    """
    Action index 21 (Pa in original JS)
    Kick rate limit
    xa(): int min, int rate, int sj (burst)
    """
    def __init__(self):
        super().__init__()
        self.type = "KickRateLimit"
        self.min = None
        self.rate = None
        self.burst = None

    @classmethod
    def parse(cls, reader):
        obj = cls()
        obj.min = reader.read_int32()  # N() - int32
        obj.rate = reader.read_int32()  # N() - int32
        obj.burst = reader.read_int32()  # N() - int32
        return obj

    def get_data(self):
        return {"min": self.min, "rate": self.rate, "burst": self.burst}
