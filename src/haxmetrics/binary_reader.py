# haxmetrics/utils/binary_reader.py

import struct
from typing import Optional, Union, Tuple


class BinaryReader:
    def __init__(self, data):
        self.data = data
        self.position = 0
        self.length = len(data)
        self.little_endian = True

    def read_byte(self) -> int:
        if self.position >= self.length:
            raise EOFError("Fin de datos")

        result = self.data[self.position]
        self.position += 1
        return result

    def read_bool(self) -> bool:
        return self.read_byte() != 0

    def read_fixed_string(self, length: int) -> str:
        if self.position + length > self.length:
            raise EOFError(f"No hay suficientes bytes para leer {length} bytes")

        result = self.data[self.position : self.position + length].decode("utf-8")
        self.position += length
        return result

    def read_uint16(self) -> int:
        if self.position + 2 > self.length:
            raise EOFError("No hay suficientes bytes para leer uint16")

        result = struct.unpack(
            "<H" if self.little_endian else ">H",
            self.data[self.position : self.position + 2],
        )[0]
        self.position += 2
        return result

    def read_int32(self) -> int:
        if self.position + 4 > self.length:
            raise EOFError("No hay suficientes bytes para leer int32")

        result = struct.unpack(
            "<i" if self.little_endian else ">i",
            self.data[self.position : self.position + 4],
        )[0]
        self.position += 4
        return result

    def read_uint32(self) -> int:
        if self.position + 4 > self.length:
            raise EOFError("No hay suficientes bytes para leer uint32")

        result = struct.unpack(
            "<I" if self.little_endian else ">I",
            self.data[self.position : self.position + 4],
        )[0]
        self.position += 4
        return result

    def read_float64(self) -> float:
        if self.position + 8 > self.length:
            raise EOFError("No hay suficientes bytes para leer float64")

        result = struct.unpack(
            "<d" if self.little_endian else ">d",
            self.data[self.position : self.position + 8],
        )[0]
        self.position += 8
        return result

    def read_string(self) -> Optional[str]:
        length = self.read_varint()
        if length == 0:
            return None
        length -= 1

        if self.position + length > self.length:
            raise EOFError("No hay suficientes bytes para leer string")

        result = self.data[self.position : self.position + length].decode("utf-8")
        self.position += length
        return result

    def read_varint(self) -> int:
        result = 0
        shift = 0

        while True:
            byte = self.read_byte()
            result |= (byte & 0x7F) << shift
            if not (byte & 0x80):
                break
            shift += 7

            if shift > 35:
                raise ValueError("VarInt demasiado grande, posible corrupción de datos")

        return result

    def read_remaining(self) -> bytes:
        result = self.data[self.position :]
        self.position = self.length
        return result

    def read_bytes(self, length: int) -> bytes:
        if self.position + length > self.length:
            raise EOFError(f"No hay suficientes bytes para leer {length} bytes")

        result = self.data[self.position : self.position + length]
        self.position += length
        return result

    def read_nullable_int32(self) -> Optional[int]:
        if self.read_bool():
            return self.read_int32()
        return None

    def read_nullable_string(self) -> Optional[str]:
        if self.read_bool():
            return self.read_string()
        return None

    def peek_byte(self) -> int:
        if self.position >= self.length:
            raise EOFError("Fin de datos")

        return self.data[self.position]

    def peek_bytes(self, count: int) -> bytes:
        end = min(self.position + count, self.length)
        return self.data[self.position : end]

    def skip(self, count: int) -> None:
        self.position = min(self.position + count, self.length)

    def get_position(self) -> int:
        return self.position

    def set_position(self, position: int) -> None:
        if position < 0 or position > self.length:
            raise ValueError("Posición fuera de rango")

        self.position = position

    def reset(self) -> None:
        self.position = 0

    def eof(self) -> bool:
        return self.position >= self.length

    def read_position(self) -> Tuple[float, float]:
        x = self.read_float64()
        y = self.read_float64()
        return (x, y)

    def read_player_id(self) -> int:
        return self.read_int32()

    def read_team_id(self) -> int:
        return self.read_byte()

    # Compatibility methods for HaxBall original scripts
    def read_uint8(self) -> int:
        """Alias for read_byte() for compatibility with original scripts"""
        return self.read_byte()

    def read_uint32_be(self) -> int:
        """Read uint32 in big-endian format (for HaxBall compatibility)"""
        if self.position + 4 > self.length:
            raise EOFError("No hay suficientes bytes para leer uint32")

        result = struct.unpack(">I", self.data[self.position : self.position + 4])[0]
        self.position += 4
        return result

    def read_uint16_be(self) -> int:
        """Read uint16 in big-endian format (for HaxBall compatibility)"""
        if self.position + 2 > self.length:
            raise EOFError("No hay suficientes bytes para leer uint16")

        result = struct.unpack(">H", self.data[self.position : self.position + 2])[0]
        self.position += 2
        return result

    def read_string_auto(self) -> Optional[str]:
        """Alias for read_string() for compatibility with original scripts"""
        return self.read_string()

    def read_double(self) -> float:
        """Alias for read_float64() for compatibility with original scripts"""
        return self.read_float64()

    def read_double_be(self) -> float:
        """Read double in big-endian format (for HaxBall stadium data)"""
        if self.position + 8 > self.length:
            raise EOFError("No hay suficientes bytes para leer float64")

        result = struct.unpack(">d", self.data[self.position : self.position + 8])[0]
        self.position += 8
        return result

    def read_float_le(self) -> float:
        """Read 32-bit float in little-endian format (for HaxBall action data)"""
        if self.position + 4 > self.length:
            raise EOFError("No hay suficientes bytes para leer float32")

        result = struct.unpack("<f", self.data[self.position : self.position + 4])[0]
        self.position += 4
        return result

    def get_input_string(self) -> bytes:
        """Alias for read_remaining() for compatibility"""
        return self.read_remaining()
