from ..action import Action
import zlib


class StadiumUpdate(Action):
    """
    Action index 11 (Ea in original JS)
    Stadium data update (compressed)
    xa(): compressed bytes (inflateRaw), then Stadium.parse()
    """
    def __init__(self):
        super().__init__()
        self.type = "StadiumUpdate"
        self.stadium_data = None

    @classmethod
    def parse(cls, reader):
        obj = cls()
        # Read length using varint, then read compressed bytes
        length = reader.read_varint()  # Bb()
        compressed_data = reader.read_bytes(length)  # sb()
        # Decompress using inflateRaw (same as zlib with negative wbits)
        try:
            obj.stadium_data = zlib.decompress(compressed_data, wbits=-15)
        except Exception as e:
            obj.stadium_data = compressed_data  # Store raw if decompression fails
        return obj

    def get_data(self):
        return {
            "stadium_data_size": len(self.stadium_data) if self.stadium_data else 0
        }
