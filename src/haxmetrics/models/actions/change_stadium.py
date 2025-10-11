from ..action import Action
import zlib


class ChangeStadium(Action):
    """
    Action index 2 (cb in original JS)
    Stadium change - loads stadium from compressed bytes
    xa(): bytes dh (stadium data, length-prefixed)
    """
    def __init__(self):
        super().__init__()
        self.type = "ChangeStadium"
        self.stadium = None

    @classmethod
    def parse(cls, reader):
        obj = cls()
        # Read length as varint, then read that many bytes
        length = reader.read_varint()  # Bb()
        obj.stadium = reader.read_bytes(length)  # bm()
        return obj

    def get_data(self):
        return {"stadium_data_size": len(self.stadium) if self.stadium else 0}
