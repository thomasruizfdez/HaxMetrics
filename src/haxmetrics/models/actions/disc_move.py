from models.action import Action


class DiscMove(Action):
    def __init__(self):
        super().__init__()
        self.disc_id = None
        self.x = None
        self.y = None
        self.xspeed = None
        self.yspeed = None
        self.radius = None

    @classmethod
    def parse(cls, reader):
        obj = cls()
        obj.disc_id = reader.read_uint8()
        obj.x = reader.read_float_le()
        obj.y = reader.read_float_le()
        obj.xspeed = reader.read_float_le()
        obj.yspeed = reader.read_float_le()
        obj.radius = reader.read_float_le()
        return obj

    def get_data(self):
        return {
            "disc_id": self.disc_id,
            "x": self.x,
            "y": self.y,
            "xspeed": self.xspeed,
            "yspeed": self.yspeed,
            "radius": self.radius,
        }
