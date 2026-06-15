import pytest

from haxmetrics.binary_reader import BinaryReader


def test_binary_reader_warns_on_instantiation():
    with pytest.warns(DeprecationWarning, match="deprecated"):
        BinaryReader(b"\x00")
