# haxmetrics/utils/binary_reader.py

import struct
from typing import Optional, Tuple, Union


class BinaryReader:
    """
    Binary data reader following HaxBall HBR2 format specification.

    All multi-byte integers use BIG-ENDIAN byte order unless specified.
    Corresponds to JavaScript class `J` in game-min.js.

    See: docs/HBR2_PARSING_GUIDE.md Section 3
    """

    def __init__(self, data):
        self.data = data
        self.position = 0
        self.length = len(data)
        self.little_endian = True

    def read_byte(self) -> int:
        """
        Read 1 unsigned byte (0-255).

        Corresponds to: F() in game-min.js

        Returns:
            int: Unsigned byte value
        """
        if self.position >= self.length:
            raise EOFError("End of data")

        result = self.data[self.position]
        self.position += 1
        return result

    def read_bool(self) -> bool:
        """Read a boolean value (0 = False, non-zero = True)."""
        return self.read_byte() != 0

    def read_fixed_string(self, length: int) -> str:
        """
        Read a fixed-length string (no varint prefix).

        Used for header magic "HBR2".

        Args:
            length: Number of bytes to read

        Returns:
            str: Decoded UTF-8 string
        """
        if self.position + length > self.length:
            raise EOFError(f"Not enough bytes to read {length} bytes")

        result = self.data[self.position : self.position + length].decode("utf-8")
        self.position += length
        return result

    def read_uint16(self) -> int:
        """
        Read 2-byte unsigned integer (little-endian by default).

        Returns:
            int: Unsigned 16-bit integer value
        """
        if self.position + 2 > self.length:
            raise EOFError("Not enough bytes to read uint16")

        result = struct.unpack(
            "<H" if self.little_endian else ">H",
            self.data[self.position : self.position + 2],
        )[0]
        self.position += 2
        return result

    def read_int32(self) -> int:
        """
        Read 4-byte signed integer (little-endian by default).

        Corresponds to: Sb() in game-min.js (when little-endian)

        Returns:
            int: Signed 32-bit integer value
        """
        if self.position + 4 > self.length:
            raise EOFError("Not enough bytes to read int32")

        result = struct.unpack(
            "<i" if self.little_endian else ">i",
            self.data[self.position : self.position + 4],
        )[0]
        self.position += 4
        return result

    def read_uint32(self) -> int:
        """
        Read 4-byte unsigned integer (little-endian by default).

        Returns:
            int: Unsigned 32-bit integer value
        """
        if self.position + 4 > self.length:
            raise EOFError("Not enough bytes to read uint32")

        result = struct.unpack(
            "<I" if self.little_endian else ">I",
            self.data[self.position : self.position + 4],
        )[0]
        self.position += 4
        return result

    def read_float64(self) -> float:
        """
        Read 8-byte double-precision float (little-endian by default).

        Corresponds to: w() in game-min.js (when little-endian)

        Returns:
            float: 64-bit floating point value
        """
        if self.position + 8 > self.length:
            raise EOFError("Not enough bytes to read float64")

        result = struct.unpack(
            "<d" if self.little_endian else ">d",
            self.data[self.position : self.position + 8],
        )[0]
        self.position += 8
        return result

    def read_string(self) -> Optional[str]:
        """
        Read a variable-length string with varint prefix.

        Corresponds to: Ab()/kc() in game-min.js

        Returns:
            Optional[str]: Decoded string or None if length is 0
        """
        length = self.read_varint()
        if length == 0:
            return None
        length -= 1

        if self.position + length > self.length:
            raise EOFError("Not enough bytes to read string")

        # Try UTF-8 decoding with error handling for corrupted/invalid strings
        try:
            result = self.data[self.position : self.position + length].decode("utf-8")
        except UnicodeDecodeError:
            # Fall back to latin-1 which accepts all byte values
            result = self.data[self.position : self.position + length].decode("latin-1")

        self.position += length
        return result

    def read_varint(self) -> int:
        """
        Read a variable-length integer (LEB128 encoding).

        Corresponds to: Cg() in game-min.js

        Returns:
            int: Decoded variable-length integer
        """
        result = 0
        shift = 0

        while True:
            byte = self.read_byte()
            result |= (byte & 0x7F) << shift
            if not (byte & 0x80):
                break
            shift += 7

            if shift > 35:
                raise ValueError("VarInt too large, possible data corruption")

        return result

    def read_remaining(self) -> bytes:
        """
        Read all remaining bytes from current position to end.

        Returns:
            bytes: Remaining data
        """
        result = self.data[self.position :]
        self.position = self.length
        return result

    def get_remaining_bytes(self) -> bytes:
        """Alias for read_remaining() for compatibility"""
        return self.read_remaining()

    def read_bytes(self, length: int) -> bytes:
        """
        Read a specific number of bytes.

        Args:
            length: Number of bytes to read

        Returns:
            bytes: Read data
        """
        if self.position + length > self.length:
            raise EOFError(f"Not enough bytes to read {length} bytes")

        result = self.data[self.position : self.position + length]
        self.position += length
        return result

    def read_nullable_int32(self) -> Optional[int]:
        """Read an optional int32 (bool flag + int32 if present)."""
        if self.read_bool():
            return self.read_int32()
        return None

    def read_nullable_string(self) -> Optional[str]:
        """Read an optional string (bool flag + string if present)."""
        if self.read_bool():
            return self.read_string()
        return None

    def peek_byte(self) -> int:
        """
        Peek at the next byte without advancing position.

        Returns:
            int: Next byte value
        """
        if self.position >= self.length:
            raise EOFError("End of data")

        return self.data[self.position]

    def peek_bytes(self, count: int) -> bytes:
        """
        Peek at multiple bytes without advancing position.

        Args:
            count: Number of bytes to peek

        Returns:
            bytes: Peeked data (may be less than count if at end)
        """
        end = min(self.position + count, self.length)
        return self.data[self.position : end]

    def skip(self, count: int) -> None:
        """Skip forward by a number of bytes."""
        self.position = min(self.position + count, self.length)

    def get_position(self) -> int:
        """Get current read position."""
        return self.position

    def set_position(self, position: int) -> None:
        """
        Set the read position.

        Args:
            position: New position to set

        Raises:
            ValueError: If position is out of range
        """
        if position < 0 or position > self.length:
            raise ValueError("Position out of range")

        self.position = position

    def reset(self) -> None:
        """Reset position to the beginning."""
        self.position = 0

    def eof(self) -> bool:
        """Check if at end of data."""
        return self.position >= self.length

    def read_position(self) -> Tuple[float, float]:
        """Read a 2D position (x, y) as two float64 values."""
        x = self.read_float64()
        y = self.read_float64()
        return (x, y)

    def read_player_id(self) -> int:
        """Read a player ID (int32)."""
        return self.read_int32()

    def read_team_id(self) -> int:
        """Read a team ID (byte)."""
        return self.read_byte()

    # Compatibility methods for HaxBall original scripts
    def read_uint8(self) -> int:
        """
        Alias for read_byte() for compatibility with original scripts.

        Corresponds to: F() in game-min.js
        """
        return self.read_byte()

    def read_uint32_be(self) -> int:
        """
        Read uint32 in big-endian format (for HaxBall compatibility).

        Corresponds to: N() in game-min.js

        Returns:
            int: Unsigned 32-bit integer (big-endian)
        """
        if self.position + 4 > self.length:
            raise EOFError("Not enough bytes to read uint32")

        result = struct.unpack(">I", self.data[self.position : self.position + 4])[0]
        self.position += 4
        return result

    def read_uint16_be(self) -> int:
        """
        Read uint16 in big-endian format (for HaxBall compatibility).

        Corresponds to: Bb() in game-min.js

        Returns:
            int: Unsigned 16-bit integer (big-endian)
        """
        if self.position + 2 > self.length:
            raise EOFError("Not enough bytes to read uint16")

        result = struct.unpack(">H", self.data[self.position : self.position + 2])[0]
        self.position += 2
        return result

    def read_int16_be(self) -> int:
        """
        Read int16 in big-endian format (for HaxBall compatibility).

        Corresponds to: Di() in game-min.js

        Returns:
            int: Signed 16-bit integer (big-endian)
        """
        if self.position + 2 > self.length:
            raise EOFError("Not enough bytes to read int16")

        result = struct.unpack(">h", self.data[self.position : self.position + 2])[0]
        self.position += 2
        return result

    def read_string_auto(self) -> Optional[str]:
        """Alias for read_string() for compatibility with original scripts."""
        return self.read_string()

    def read_double(self) -> float:
        """Alias for read_float64() for compatibility with original scripts."""
        return self.read_float64()

    def read_double_be(self) -> float:
        """
        Read double in big-endian format (for HaxBall stadium data).

        Corresponds to: w() in game-min.js (big-endian mode)

        Returns:
            float: 64-bit floating point value (big-endian)
        """
        if self.position + 8 > self.length:
            raise EOFError("Not enough bytes to read float64")

        result = struct.unpack(">d", self.data[self.position : self.position + 8])[0]
        self.position += 8
        return result

    def read_float_le(self) -> float:
        """
        Read 32-bit float in little-endian format (for HaxBall action data).

        Returns:
            float: 32-bit floating point value (little-endian)
        """
        if self.position + 4 > self.length:
            raise EOFError("Not enough bytes to read float32")

        result = struct.unpack("<f", self.data[self.position : self.position + 4])[0]
        self.position += 4
        return result

    def get_input_string(self) -> bytes:
        """Alias for read_remaining() for compatibility"""
        return self.read_remaining()
