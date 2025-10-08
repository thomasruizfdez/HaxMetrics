import struct


class BinaryReader:
    def read_string_auto_be(self):
        length = self.read_uint16_be()
        if length > 0:
            return self.read_string(length)
        return ""

    def get_input_string(self):
        """
        Devuelve los datos binarios restantes desde el offset actual.
        """
        return self.data[self.offset :]

    def __init__(self, data: bytes):
        self.data = data
        self.offset = 0

    def read_bytes(self, n):
        val = self.data[self.offset : self.offset + n]
        self.offset += n
        return val

    def read_uint8(self):
        val = self.data[self.offset]
        self.offset += 1
        return val

    def read_uint16(self):
        # Lee 2 bytes como unsigned short (big-endian)
        val = struct.unpack(">H", self.read_bytes(2))[0]
        return val

    def read_uint32_be(self):
        val = struct.unpack(">I", self.data[self.offset : self.offset + 4])[0]
        self.offset += 4
        return val

    def read_string(self, length, decode_utf8=True):
        raw = self.data[self.offset : self.offset + length]
        self.offset += length
        if decode_utf8:
            try:
                return raw.decode("utf-8")
            except UnicodeDecodeError:
                # Si no se puede decodificar, devuelve los bytes
                return raw
        else:
            return raw

    def eof(self):
        return self.offset >= len(self.data)

    def read_double(self):
        # Lee 8 bytes como double big-endian
        raw = self.read_bytes(8)
        double = struct.unpack(">d", raw)[0]
        return double if not (double != double) else 0  # is_nan check

    def read_string_auto(self):
        length = self.read_uint8()
        return self.read_string(length - 1) if length > 0 else ""
