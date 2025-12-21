"""
Tests unitarios para Header parsing.

Fixtures usadas:
- src/tests/fixtures/basic/basic.hbr2
"""

from pathlib import Path

import pytest

from haxmetrics.binary_reader import BinaryReader
from haxmetrics.models.header import Header

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"
BASIC_REPLAY = FIXTURES_DIR / "basic" / "basic.hbr2"


def test_parse_valid_header_basic_replay():
    """Debe parsear header correctamente de replay real."""
    with open(BASIC_REPLAY, "rb") as f:
        reader = BinaryReader(f.read())
        header = Header.parse(reader)

        assert header.magic == "HBR2"
        assert header.version == 3
        assert header.duration >= 0
        assert reader.position == 12  # Header size


def test_parse_header_magic_field():
    """Debe extraer magic 'HBR2' correctamente."""
    data = b"HBR2" + b"\x00\x00\x00\x03" + b"\x00\x00\x00\x64"
    reader = BinaryReader(data)
    header = Header.parse(reader)

    assert header.magic == "HBR2"


def test_parse_header_version_field():
    """Debe extraer version correctamente (big-endian)."""
    data = b"HBR2" + b"\x00\x00\x00\x05" + b"\x00\x00\x00\x64"
    reader = BinaryReader(data)
    header = Header.parse(reader)

    assert header.version == 5


def test_parse_header_duration_field():
    """Debe extraer duration correctamente."""
    data = b"HBR2" + b"\x00\x00\x00\x03" + b"\x00\x00\x04\xb0"  # 1200 frames
    reader = BinaryReader(data)
    header = Header.parse(reader)

    assert header.duration == 1200


def test_parse_invalid_magic_raises_error():
    """Debe lanzar ValueError si magic != 'HBR2'."""
    data = b"FAKE" + b"\x00\x00\x00\x03" + b"\x00\x00\x00\x64"
    reader = BinaryReader(data)

    with pytest.raises(ValueError, match="Invalid HBR2 magic"):
        Header.parse(reader)


def test_header_to_dict():
    """Debe serializar a dict correctamente."""
    header = Header(magic="HBR2", version=3, duration=600)
    result = header.to_dict()

    assert result["magic"] == "HBR2"
    assert result["version"] == 3
    assert result["duration"] == 600
    assert result["duration_seconds"] == 10.0


def test_header_duration_seconds_property():
    """Debe calcular duration_seconds correctamente."""
    header = Header(magic="HBR2", version=3, duration=3600)

    assert header.duration_seconds == 60.0  # 3600 frames / 60 fps


def test_header_immutability():
    """Debe ser inmutable (frozen dataclass)."""
    header = Header(magic="HBR2", version=3, duration=100)

    with pytest.raises(AttributeError):
        header.duration = 200


def test_header_equality():
    """Debe comparar instancias correctamente."""
    h1 = Header(magic="HBR2", version=3, duration=100)
    h2 = Header(magic="HBR2", version=3, duration=100)
    h3 = Header(magic="HBR2", version=3, duration=200)

    assert h1 == h2
    assert h1 != h3


def test_header_string_representation():
    """Debe tener __str__ legible."""
    header = Header(magic="HBR2", version=3, duration=120)
    result = str(header)

    assert "HBR2" in result
    assert "3" in result
    assert "120" in result


def test_header_validation_negative_version():
    """Debe rechazar version negativa."""
    with pytest.raises(ValueError, match="Version must be non-negative"):
        Header(magic="HBR2", version=-1, duration=100)


def test_header_validation_negative_duration():
    """Debe rechazar duration negativa."""
    with pytest.raises(ValueError, match="Duration must be non-negative"):
        Header(magic="HBR2", version=3, duration=-100)
