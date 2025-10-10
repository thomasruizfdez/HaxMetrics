from ..action import Action


class KickRateLimit(Action):
    """Action 21 (Pa): Kick rate limit settings"""
    def __init__(self):
        super().__init__()
        self.min = None
        self.rate = None
        self.burst = None

    @classmethod
    def parse(cls, reader):
        obj = cls()
        obj.min = reader.read_uint32_be()
        obj.rate = reader.read_uint32_be()
        obj.burst = reader.read_uint32_be()
        return obj

    def get_data(self):
        return {
            "min": self.min,
            "rate": self.rate,
            "burst": self.burst
        }
