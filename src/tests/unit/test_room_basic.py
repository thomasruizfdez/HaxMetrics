"""
Tests unitarios para RoomBasic parsing.

Fixtures usadas:
- src/tests/fixtures/basic/basic.hbr2
- src/tests/fixtures/room/ (si existen)
"""

import zlib
from pathlib import Path

import pytest

from haxmetrics.binary_reader import BinaryReader
from haxmetrics.models.header import Header
from haxmetrics.models.messages import Messages
from haxmetrics.models.room import RoomBasic

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"
BASIC_REPLAY = FIXTURES_DIR / "basic" / "basic.hbr2"


def get_room_reader(replay_path: Path) -> BinaryReader:
    """
    Helper: Lee replay, skip header, descomprime, skip messages,
    retorna reader posicionado en room state.
    """
    with open(replay_path, "rb") as f:
        data = f.read()

    reader = BinaryReader(data)

    # Skip header (12 bytes)
    Header.parse(reader)

    # Descomprimir
    compressed = reader.get_remaining_bytes()
    decompressed = zlib.decompress(compressed, wbits=-15)
    reader = BinaryReader(decompressed)

    # Skip messages
    Messages.parse(reader)

    return reader


def test_parse_room_basic_from_basic_replay():
    """Debe parsear room basic correctamente de replay real."""
    reader = get_room_reader(BASIC_REPLAY)
    room = RoomBasic.parse(reader)

    # Verificar que se parsearon todos los campos
    assert isinstance(room.name, str)
    assert isinstance(room.locked, bool)
    assert isinstance(room.score_limit, int)
    assert isinstance(room.time_limit, int)
    assert isinstance(room.unknown_int16, int)
    assert isinstance(room.rules_type, int)
    assert isinstance(room.unknown_byte, int)

    # Verificar valores razonables
    assert room.score_limit >= 0
    assert room.time_limit >= 0


def test_parse_room_name_field():
    """Debe extraer nombre de sala correctamente."""
    # Crear datos sintéticos
    # String "Test Room" = varint(10) + "Test Room" (9 bytes)
    data = bytes([10]) + b"Test Room"
    # Locked = 0
    data += bytes([0])
    # Score limit = 3 (uint32_be)
    data += b"\x00\x00\x00\x03"
    # Time limit = 5 (uint32_be)
    data += b"\x00\x00\x00\x05"
    # Unknown int16 = 0
    data += b"\x00\x00"
    # Rules type = 0
    data += bytes([0])
    # Unknown byte = 0
    data += bytes([0])

    reader = BinaryReader(data)
    room = RoomBasic.parse(reader)

    assert room.name == "Test Room"


def test_parse_room_locked_field_true():
    """Debe detectar sala cerrada (locked=true)."""
    # Name = "" (varint 1, solo null terminator)
    data = bytes([1])
    # Locked = 1 (true)
    data += bytes([1])
    # Resto de campos en 0
    data += b"\x00" * 14

    reader = BinaryReader(data)
    room = RoomBasic.parse(reader)

    assert room.locked is True


def test_parse_room_locked_field_false():
    """Debe detectar sala abierta (locked=false)."""
    # Name = ""
    data = bytes([1])
    # Locked = 0 (false)
    data += bytes([0])
    # Resto de campos en 0
    data += b"\x00" * 14

    reader = BinaryReader(data)
    room = RoomBasic.parse(reader)

    assert room.locked is False


def test_parse_room_score_limit_field():
    """Debe parsear score limit correctamente (big-endian)."""
    # Name = ""
    data = bytes([1])
    # Locked = 0
    data += bytes([0])
    # Score limit = 10 (uint32_be: 0x0000000A)
    data += b"\x00\x00\x00\x0a"
    # Time limit = 0
    data += b"\x00\x00\x00\x00"
    # Resto en 0
    data += b"\x00" * 4

    reader = BinaryReader(data)
    room = RoomBasic.parse(reader)

    assert room.score_limit == 10


def test_parse_room_time_limit_field():
    """Debe parsear time limit correctamente (big-endian)."""
    # Name = ""
    data = bytes([1])
    # Locked = 0
    data += bytes([0])
    # Score limit = 0
    data += b"\x00\x00\x00\x00"
    # Time limit = 15 (uint32_be: 0x0000000F)
    data += b"\x00\x00\x00\x0f"
    # Resto en 0
    data += b"\x00" * 4

    reader = BinaryReader(data)
    room = RoomBasic.parse(reader)

    assert room.time_limit == 15


def test_parse_room_unknown_fields():
    """Debe parsear campos desconocidos correctamente."""
    # Name = ""
    data = bytes([1])
    # Locked = 0
    data += bytes([0])
    # Limits = 0
    data += b"\x00" * 8
    # Unknown int16 = -1 (int16_be: 0xFFFF)
    data += b"\xff\xff"
    # Rules type = 2
    data += bytes([2])
    # Unknown byte = 5
    data += bytes([5])

    reader = BinaryReader(data)
    room = RoomBasic.parse(reader)

    assert room.unknown_int16 == -1
    assert room.rules_type == 2
    assert room.unknown_byte == 5


def test_room_basic_to_dict():
    """Debe serializar a dict correctamente."""
    room = RoomBasic(
        name="Test",
        locked=True,
        score_limit=5,
        time_limit=10,
        unknown_int16=0,
        rules_type=0,
        unknown_byte=0,
    )

    result = room.to_dict()

    assert result["name"] == "Test"
    assert result["locked"] is True
    assert result["score_limit"] == 5
    assert result["time_limit"] == 10


def test_room_basic_immutability():
    """Debe ser inmutable (frozen dataclass)."""
    room = RoomBasic(
        name="Test",
        locked=False,
        score_limit=0,
        time_limit=0,
        unknown_int16=0,
        rules_type=0,
        unknown_byte=0,
    )

    with pytest.raises(AttributeError):
        room.name = "Changed"


def test_room_basic_string_representation():
    """Debe tener __str__ legible."""
    room = RoomBasic(
        name="My Room",
        locked=True,
        score_limit=3,
        time_limit=5,
        unknown_int16=0,
        rules_type=0,
        unknown_byte=0,
    )

    result = str(room)

    assert "My Room" in result
    assert "🔒" in result or "Locked" in result
    assert "3" in result
    assert "5" in result


def test_room_name_empty_string():
    """Debe manejar nombre vacío correctamente."""
    # Name = "" (varint 1)
    data = bytes([1])
    # Resto de campos en 0
    data += bytes([0])
    data += b"\x00" * 14

    reader = BinaryReader(data)
    room = RoomBasic.parse(reader)

    assert room.name == ""


def test_room_limits_zero_values():
    """Debe aceptar límites en 0 (sin límites)."""
    room = RoomBasic(
        name="No Limits",
        locked=False,
        score_limit=0,
        time_limit=0,
        unknown_int16=0,
        rules_type=0,
        unknown_byte=0,
    )

    assert room.score_limit == 0
    assert room.time_limit == 0


def test_room_negative_limits_raise_error():
    """Debe rechazar límites negativos."""
    with pytest.raises(ValueError, match="Score limit must be non-negative"):
        RoomBasic(
            name="Bad",
            locked=False,
            score_limit=-1,
            time_limit=0,
            unknown_int16=0,
            rules_type=0,
            unknown_byte=0,
        )


def test_room_negative_time_limit_raise_error():
    """Debe rechazar time limit negativo."""
    with pytest.raises(ValueError, match="Time limit must be non-negative"):
        RoomBasic(
            name="Bad",
            locked=False,
            score_limit=0,
            time_limit=-1,
            unknown_int16=0,
            rules_type=0,
            unknown_byte=0,
        )


def test_room_basic_equality():
    """Debe comparar instancias correctamente."""
    room1 = RoomBasic(
        name="Test",
        locked=False,
        score_limit=5,
        time_limit=10,
        unknown_int16=0,
        rules_type=0,
        unknown_byte=0,
    )
    room2 = RoomBasic(
        name="Test",
        locked=False,
        score_limit=5,
        time_limit=10,
        unknown_int16=0,
        rules_type=0,
        unknown_byte=0,
    )
    room3 = RoomBasic(
        name="Different",
        locked=False,
        score_limit=5,
        time_limit=10,
        unknown_int16=0,
        rules_type=0,
        unknown_byte=0,
    )

    assert room1 == room2
    assert room1 != room3
