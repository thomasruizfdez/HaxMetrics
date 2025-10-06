import struct


class BinaryReader:
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

    def read_uint16_be(self):
        val = struct.unpack(">H", self.data[self.offset : self.offset + 2])[0]
        self.offset += 2
        return val

    def read_uint32_be(self):
        val = struct.unpack(">I", self.data[self.offset : self.offset + 4])[0]
        self.offset += 4
        return val

    def read_string(self, length):
        val = self.data[self.offset : self.offset + length].decode("utf-8")
        self.offset += length
        return val

    def eof(self):
        return self.offset >= len(self.data)
