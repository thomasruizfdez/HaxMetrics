"""Joint class for stadium parsing"""


class Joint:
    """
    Joint (ob class in original JS)
    Connects two discs with distance constraints
    """
    def __init__(self):
        self.disc1_index = 0
        self.disc2_index = 0
        self.min_distance = 100.0
        self.max_distance = 100.0
        self.stiffness = float('inf')
        self.color = 0

    @classmethod
    def parse(cls, reader, stadium_cls):
        joint = cls()
        joint.disc1_index = reader.read_uint8()  # F() - byte
        joint.disc2_index = reader.read_uint8()  # F() - byte
        joint.min_distance = reader.read_double_be()  # w() - double
        joint.max_distance = reader.read_double_be()  # w() - double
        joint.stiffness = reader.read_double_be()  # w() - double
        joint.color = reader.read_int32()  # N() - int32
        return joint

    def json_serialize(self):
        return {
            "disc1": self.disc1_index,
            "disc2": self.disc2_index,
            "min_distance": self.min_distance,
            "max_distance": self.max_distance,
            "stiffness": self.stiffness,
            "color": self.color,
        }
