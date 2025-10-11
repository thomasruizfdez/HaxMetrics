from ..action import Action


class DiscUpdate(Action):
    """
    Action index 23 (Hb in original JS)
    Disc/physics update with nullable fields
    xa(): int Ke (disc_id), bool sn (is_player_disc), 
          10 nullable floats in Ma array (x, y, vx, vy, ax, ay, radius, bcoeff, invMass, damping),
          3 nullable ints in Yc array (color, cMask, cGroup)
    """
    def __init__(self):
        super().__init__()
        self.type = "DiscUpdate"
        self.disc_id = None
        self.is_player_disc = False
        self.ma = [None] * 10  # Float array
        self.yc = [None] * 3   # Int array

    @classmethod
    def parse(cls, reader):
        obj = cls()
        obj.disc_id = reader.read_int32()  # N() - int32
        obj.is_player_disc = reader.read_byte() != 0  # F() - byte as bool
        flags = reader.read_uint16()  # Sb() - uint16 flags
        
        # Parse Ma array (10 nullable floats)
        bit = 1
        for i in range(10):
            if (flags & bit) != 0:
                obj.ma[i] = reader.read_float_le()  # Ci() - float32
            bit <<= 1
        
        # Parse Yc array (3 nullable ints)
        for i in range(3):
            if (flags & bit) != 0:
                obj.yc[i] = reader.read_int32()  # N() - int32
            bit <<= 1
        
        return obj

    def get_data(self):
        return {
            "disc_id": self.disc_id,
            "is_player_disc": self.is_player_disc,
            "ma": obj.ma,
            "yc": self.yc,
        }
