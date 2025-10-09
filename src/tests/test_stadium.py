"""
Tests for Stadium parsing functionality.
"""
import sys
sys.path.insert(0, 'src')

from haxmetrics.binary_reader import BinaryReader
from haxmetrics.models.stadium.stadium import Stadium
from haxmetrics.models.stadium.background import Background
from haxmetrics.models.stadium.vertex import Vertex
import zlib


def test_predefined_stadium():
    """Test parsing a predefined stadium."""
    # Create a simple byte stream with a predefined stadium (type 0 = Classic)
    data = bytearray([0])  # Stadium type 0
    reader = BinaryReader(bytes(data))
    
    stadium = Stadium.parse(reader)
    
    assert stadium is not None
    assert stadium.name == "Classic"
    assert stadium.custom == False
    print("✓ Predefined stadium test passed")


def test_custom_stadium_basic():
    """Test parsing a basic custom stadium."""
    # Stadium type 255 + name + background + fields
    data = bytearray()
    data.append(255)  # Custom stadium type
    
    # Stadium name (varint length + string)
    name = "Test Stadium"
    name_bytes = name.encode('utf-8')
    # Varint encoding for length
    length = len(name_bytes) + 1  # +1 for null terminator encoding
    data.append(length)
    data.extend(name_bytes)
    
    # Background (uint32_be type + 5 doubles_be + uint32_be color)
    data.extend((0).to_bytes(4, 'big'))  # type = 0 (none)
    data.extend(int.from_bytes(struct.pack('>d', 200.0), 'big').to_bytes(8, 'big'))  # width
    data.extend(int.from_bytes(struct.pack('>d', 150.0), 'big').to_bytes(8, 'big'))  # height
    data.extend(int.from_bytes(struct.pack('>d', 50.0), 'big').to_bytes(8, 'big'))   # kick_off
    data.extend(int.from_bytes(struct.pack('>d', 0.0), 'big').to_bytes(8, 'big'))    # corner
    data.extend(int.from_bytes(struct.pack('>d', 0.0), 'big').to_bytes(8, 'big'))    # goal_line
    data.extend((0).to_bytes(4, 'big'))  # color
    
    # Max view width, height
    data.extend(int.from_bytes(struct.pack('>d', 250.0), 'big').to_bytes(8, 'big'))
    data.extend(int.from_bytes(struct.pack('>d', 200.0), 'big').to_bytes(8, 'big'))
    
    # Spawn distance
    data.extend(int.from_bytes(struct.pack('>d', 150.0), 'big').to_bytes(8, 'big'))
    
    # Player physics (7 doubles)
    for val in [0.5, 0.5, 0.96, 0.1, 0.07, 0.96, 5.0]:
        data.extend(int.from_bytes(struct.pack('>d', val), 'big').to_bytes(8, 'big'))
    
    # Nullable int32 (max view width override)
    data.append(0)  # False = no value
    
    # Camera follow, can store, full reset
    data.extend([0, 1, 0])
    
    # Element counts (vertices, segments, planes, goals, discs, joints)
    data.extend([0, 0, 0, 0, 0, 0])
    
    # Spawn points (red count=0, blue count=0)
    data.extend([0, 0])
    
    reader = BinaryReader(bytes(data))
    stadium = Stadium.parse(reader)
    
    assert stadium is not None
    assert stadium.name == "Test Stadium"
    assert stadium.custom == True
    assert stadium.background is not None
    assert stadium.background.width == 200.0
    assert stadium.background.height == 150.0
    print("✓ Custom stadium basic test passed")


def test_stadium_with_replay():
    """Test parsing stadium from actual replay file."""
    try:
        with open('src/replays/prueba_custom.hbr2', 'rb') as f:
            data = f.read()
        
        reader = BinaryReader(data)
        header = reader.read_fixed_string(4)
        version = reader.read_uint32_be()
        duration = reader.read_uint32_be()
        
        # Decompress
        decompressed = zlib.decompress(reader.read_remaining(), wbits=-15)
        reader = BinaryReader(decompressed)
        
        # Skip to stadium
        msg_count = reader.read_uint16()
        room_name = reader.read_string()
        reader.skip(1 + 4 + 4 + 2 + 1 + 1)  # room fields
        
        # Parse stadium
        stadium = Stadium.parse(reader)
        
        assert stadium is not None
        assert stadium.custom == True
        assert stadium.name == "GK Training ULTIMATE by H from HaxMaps"
        assert stadium.background is not None
        assert stadium.background.type == "grass"
        assert stadium.background.width == 250.0
        assert stadium.background.height == 170.0
        assert stadium.player_physics is not None
        print("✓ Stadium with replay test passed")
        print(f"  Stadium: {stadium.name}")
        print(f"  Background: {stadium.background.type} {stadium.background.width}x{stadium.background.height}")
        print(f"  Player Physics: bCoef={stadium.player_physics.b_coef}")
        
    except FileNotFoundError:
        print("⚠ Replay file not found, skipping test")


if __name__ == "__main__":
    import struct
    
    print("Running Stadium tests...")
    print()
    
    test_predefined_stadium()
    test_custom_stadium_basic()
    test_stadium_with_replay()
    
    print()
    print("All Stadium tests passed! ✓")
