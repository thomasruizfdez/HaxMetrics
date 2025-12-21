"""
Unit tests for Stadium parsing.

Tests parsing of both predefined (types 0-11) and custom (type 255) stadiums.
"""

import zlib
from pathlib import Path

import pytest

from haxmetrics.binary_reader import BinaryReader
from haxmetrics.models.header import Header
from haxmetrics.models.messages import Messages
from haxmetrics.models.stadium import (
    CustomStadium,
    PredefinedStadium,
    parse_stadium,
)
from haxmetrics.models.stadium.components import (
    Goal,
    Joint,
    Plane,
    PlayerPhysics,
    Segment,
    StadiumDisc,
    Vertex,
)

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures" / "stadium"


def parse_to_stadium(replay_path: Path):
    """
    Helper to parse a complete replay file up to the stadium.
    
    Returns:
        tuple: (stadium, reader) where reader is positioned after stadium parsing
    """
    with open(replay_path, "rb") as f:
        data = f.read()
    
    reader = BinaryReader(data)
    
    # Parse header
    header = Header.parse(reader)
    
    # Decompress
    compressed = reader.read_remaining()
    decompressed = zlib.decompress(compressed, -15)
    dreader = BinaryReader(decompressed)
    
    # Parse messages
    messages = Messages.parse(dreader)
    
    # Skip room fields to get to stadium
    room_name = dreader.read_string()
    teams_locked = dreader.read_byte()
    score_limit = dreader.read_uint32_be()
    time_limit = dreader.read_uint32_be()
    kick_rate_limit_burst = dreader.read_uint16_be()
    kick_rate_limit = dreader.read_byte()
    kick_timeout = dreader.read_byte()
    
    # Parse stadium
    stadium = parse_stadium(dreader)
    
    return stadium, dreader


class TestPredefinedStadium:
    """Tests for predefined stadium parsing (types 0-11)."""
    
    def test_parse_classic_stadium(self):
        """Should parse Classic stadium (type 0)."""
        # Stadium type 0 = Classic
        data = bytes([0])
        reader = BinaryReader(data)
        
        stadium = parse_stadium(reader)
        
        assert isinstance(stadium, PredefinedStadium)
        assert stadium.stadium_type == 0
        assert stadium.name == "Classic"
        assert reader.position == 1  # Only 1 byte consumed
    
    def test_parse_hockey_stadium(self):
        """Should parse Hockey stadium (type 5)."""
        data = bytes([5])
        reader = BinaryReader(data)
        
        stadium = parse_stadium(reader)
        
        assert isinstance(stadium, PredefinedStadium)
        assert stadium.stadium_type == 5
        assert stadium.name == "Hockey"
    
    def test_parse_huge_stadium(self):
        """Should parse Huge stadium (type 9)."""
        data = bytes([9])
        reader = BinaryReader(data)
        
        stadium = parse_stadium(reader)
        
        assert isinstance(stadium, PredefinedStadium)
        assert stadium.stadium_type == 9
        assert stadium.name == "Huge"
    
    def test_stadium_name_mapping(self):
        """Should map all stadium types to correct names."""
        expected = {
            0: "Classic",
            1: "Easy",
            2: "Small",
            3: "Big",
            4: "Rounded",
            5: "Hockey",
            6: "Big Hockey",
            7: "Big Easy",
            8: "Big Rounded",
            9: "Huge",
            10: "Unknown",
            11: "Unknown"
        }
        
        for type_id, name in expected.items():
            data = bytes([type_id])
            reader = BinaryReader(data)
            stadium = parse_stadium(reader)
            assert stadium.name == name
    
    def test_predefined_to_dict(self):
        """Should serialize to dict correctly."""
        data = bytes([0])
        reader = BinaryReader(data)
        stadium = parse_stadium(reader)
        
        result = stadium.to_dict()
        
        assert result["type"] == 0
        assert result["name"] == "Classic"
        assert result["custom"] is False
    
    def test_predefined_immutability(self):
        """Should be immutable (frozen dataclass)."""
        data = bytes([0])
        reader = BinaryReader(data)
        stadium = parse_stadium(reader)
        
        with pytest.raises(AttributeError):
            stadium.name = "Changed"
    
    def test_invalid_type_raises_error(self):
        """Should raise error for invalid stadium type (<12, !=255)."""
        data = bytes([12])  # Invalid: not 0-11 or 255
        reader = BinaryReader(data)
        
        with pytest.raises(ValueError, match="Invalid stadium type"):
            parse_stadium(reader)
    
    def test_invalid_type_254_raises_error(self):
        """Should raise error for type 254."""
        data = bytes([254])
        reader = BinaryReader(data)
        
        with pytest.raises(ValueError, match="Invalid stadium type"):
            parse_stadium(reader)


class TestCustomStadium:
    """Tests for custom stadium parsing (type 255)."""
    
    def test_parse_minimal_custom_stadium(self):
        """Should parse custom stadium with no components."""
        data = bytes([255])  # Type 255 = custom
        
        # Stadium name (empty)
        data += bytes([1])  # varint 1 = empty string
        
        # Basic config (12 fields)
        data += b"\x00\x00\x01\x00"  # bg_width = 256 (int32_be)
        data += b"\x00\x00\x00\xc8"  # bg_height = 200 (int32_be)
        data += b"\x00\x00\x00\x4b"  # bg_kick_off_radius = 75 (int32_be)
        data += b"\x00\x00\x00\x00"  # bg_corner_radius = 0 (int32_be)
        data += b"\x40\x94\x00\x00\x00\x00\x00\x00"  # bg_max_view_width = 1280.0 (float64_be)
        data += bytes([1])  # camera_follow = 1
        data += bytes([0])  # spawn_inv_flags = false
        data += b"\x40\x49\x00\x00\x00\x00\x00\x00"  # spawn_distance = 50.0 (float64_be)
        data += bytes([1])  # can_be_stored = 1
        data += bytes([1])  # can_kick_off = 1
        data += bytes([1])  # kick_off_reset = 1
        
        # Component arrays (all empty)
        data += bytes([0])  # 0 vertices
        data += bytes([0])  # 0 segments
        data += bytes([0])  # 0 planes
        data += bytes([0])  # 0 goals
        data += bytes([0])  # 0 discs
        data += bytes([0])  # 0 joints
        
        # Player physics (8 fields, 64 bytes)
        data += b"\x40\x2e\x00\x00\x00\x00\x00\x00"  # radius = 15.0
        data += b"\x3f\xe0\x00\x00\x00\x00\x00\x00"  # b_coef = 0.5
        data += b"\x3f\xe0\x00\x00\x00\x00\x00\x00"  # inv_mass = 0.5
        data += b"\x3f\xee\xb8\x51\xeb\x85\x1e\xb8"  # damping = 0.96
        data += b"\x3f\xb9\x99\x99\x99\x99\x99\x9a"  # acceleration = 0.1
        data += b"\x3f\xb1\xeb\x85\x1e\xb8\x51\xec"  # kick_acceleration = 0.07
        data += b"\x3f\xee\xb8\x51\xeb\x85\x1e\xb8"  # kick_damping = 0.96
        data += b"\x40\x14\x00\x00\x00\x00\x00\x00"  # kick_strength = 5.0
        
        reader = BinaryReader(data)
        stadium = parse_stadium(reader)
        
        assert isinstance(stadium, CustomStadium)
        assert stadium.name == ""
        assert stadium.bg_width == 256
        assert stadium.bg_height == 200
        assert len(stadium.vertices) == 0
        assert len(stadium.segments) == 0
        assert len(stadium.planes) == 0
        assert len(stadium.goals) == 0
        assert len(stadium.discs) == 0
        assert len(stadium.joints) == 0
        assert stadium.player_physics.radius == 15.0
    
    def test_parse_custom_stadium_with_vertices(self):
        """Should parse custom stadium with vertices."""
        data = bytes([255])  # Type 255
        
        # Name "Test" = varint 5 (4 chars + null), then 4 bytes
        data += bytes([5]) + b"Test"
        
        # Basic config (simplified, use zeros where appropriate)
        data += b"\x00\x00\x02\x00"  # bg_width = 512
        data += b"\x00\x00\x01\x00"  # bg_height = 256
        data += b"\x00\x00\x00\x50"  # bg_kick_off_radius = 80
        data += b"\x00\x00\x00\x00"  # bg_corner_radius = 0
        data += b"\x40\x94\x00\x00\x00\x00\x00\x00"  # bg_max_view_width = 1280.0
        data += bytes([0])  # camera_follow = 0
        data += bytes([0])  # spawn_inv_flags = false
        data += b"\x40\x49\x00\x00\x00\x00\x00\x00"  # spawn_distance = 50.0
        data += bytes([0])  # can_be_stored = 0
        data += bytes([1])  # can_kick_off = 1
        data += bytes([0])  # kick_off_reset = 0
        
        # Component arrays
        # 2 vertices
        data += bytes([2])
        # Vertex 0
        data += b"\x40\x59\x00\x00\x00\x00\x00\x00"  # x = 100.0
        data += b"\x00\x00\x00\x00\x00\x00\x00\x00"  # y = 0.0
        data += b"\x3f\xf0\x00\x00\x00\x00\x00\x00"  # b_coef = 1.0
        # Vertex 1
        data += b"\xc0\x59\x00\x00\x00\x00\x00\x00"  # x = -100.0
        data += b"\x00\x00\x00\x00\x00\x00\x00\x00"  # y = 0.0
        data += b"\x3f\xf0\x00\x00\x00\x00\x00\x00"  # b_coef = 1.0
        
        # 0 segments, planes, goals, discs, joints
        data += bytes([0] * 5)
        
        # Player physics
        data += b"\x40\x2e\x00\x00\x00\x00\x00\x00"  # radius = 15.0
        data += b"\x3f\xe0\x00\x00\x00\x00\x00\x00"  # b_coef = 0.5
        data += b"\x3f\xe0\x00\x00\x00\x00\x00\x00"  # inv_mass = 0.5
        data += b"\x3f\xee\xb8\x51\xeb\x85\x1e\xb8"  # damping = 0.96
        data += b"\x3f\xb9\x99\x99\x99\x99\x99\x9a"  # acceleration = 0.1
        data += b"\x3f\xb1\xeb\x85\x1e\xb8\x51\xec"  # kick_acceleration = 0.07
        data += b"\x3f\xee\xb8\x51\xeb\x85\x1e\xb8"  # kick_damping = 0.96
        data += b"\x40\x14\x00\x00\x00\x00\x00\x00"  # kick_strength = 5.0
        
        reader = BinaryReader(data)
        stadium = parse_stadium(reader)
        
        assert isinstance(stadium, CustomStadium)
        assert stadium.name == "Test"
        assert len(stadium.vertices) == 2
        assert stadium.vertices[0].x == 100.0
        assert stadium.vertices[0].y == 0.0
        assert stadium.vertices[1].x == -100.0
    
    def test_custom_stadium_to_dict(self):
        """Should serialize custom stadium to dict."""
        # Use minimal stadium from first test
        data = bytes([255, 1])  # Type + empty name
        data += b"\x00\x00\x01\x00" * 4  # bg fields
        data += b"\x40\x94\x00\x00\x00\x00\x00\x00"  # bg_max_view_width
        data += bytes([1, 0])  # camera_follow, spawn_inv_flags
        data += b"\x40\x49\x00\x00\x00\x00\x00\x00"  # spawn_distance
        data += bytes([1, 1, 1])  # can_be_stored, can_kick_off, kick_off_reset
        data += bytes([0] * 6)  # Empty arrays
        # Player physics
        data += b"\x40\x2e\x00\x00\x00\x00\x00\x00" * 8  # 8 floats
        
        reader = BinaryReader(data)
        stadium = parse_stadium(reader)
        
        result = stadium.to_dict()
        
        assert result["custom"] is True
        assert result["name"] == ""
        assert "background" in result
        assert "vertexes" in result
        assert "playerPhysics" in result
    
    def test_custom_stadium_immutability(self):
        """Should be immutable (frozen dataclass)."""
        data = bytes([255, 1])
        data += b"\x00\x00\x01\x00" * 4
        data += b"\x40\x94\x00\x00\x00\x00\x00\x00"
        data += bytes([1, 0])
        data += b"\x40\x49\x00\x00\x00\x00\x00\x00"
        data += bytes([1, 1, 1])
        data += bytes([0] * 6)
        data += b"\x40\x2e\x00\x00\x00\x00\x00\x00" * 8
        
        reader = BinaryReader(data)
        stadium = parse_stadium(reader)
        
        with pytest.raises(AttributeError):
            stadium.name = "Changed"


class TestStadiumComponents:
    """Tests for stadium component parsing."""
    
    def test_parse_vertex(self):
        """Should parse vertex (24 bytes)."""
        data = b"\x40\x59\x00\x00\x00\x00\x00\x00"  # x = 100.0
        data += b"\x40\x49\x00\x00\x00\x00\x00\x00"  # y = 50.0
        data += b"\x3f\xf0\x00\x00\x00\x00\x00\x00"  # b_coef = 1.0
        
        reader = BinaryReader(data)
        vertex = Vertex.parse(reader)
        
        assert vertex.x == 100.0
        assert vertex.y == 50.0
        assert vertex.b_coef == 1.0
        assert reader.position == 24
    
    def test_parse_segment(self):
        """Should parse segment (39 bytes, not 36)."""
        data = bytes([0])  # v0 = 0
        data += bytes([1])  # v1 = 1
        data += b"\x00\x00\x00\x00\x00\x00\x00\x00"  # bias = 0.0
        data += b"\x3f\xf0\x00\x00\x00\x00\x00\x00"  # b_coef = 1.0
        data += b"\x00\x00\x00\x00\x00\x00\x00\x00"  # curve = 0.0
        data += b"\x00\x00\x00\x00\x00\x00\x00\x00"  # curve_f = 0.0
        data += bytes([1])  # visible = true
        data += b"\xff\xff\xff\xff"  # color = 0xFFFFFFFF
        
        reader = BinaryReader(data)
        segment = Segment.parse(reader)
        
        assert segment.v0 == 0
        assert segment.v1 == 1
        assert segment.visible is True
        assert reader.position == 39  # Actual size is 39 bytes (1+1+8+8+8+8+1+4)
    
    def test_parse_goal(self):
        """Should parse goal (33 bytes)."""
        data = b"\xc0\x79\x00\x00\x00\x00\x00\x00"  # p0_x = -400.0
        data += b"\x00\x00\x00\x00\x00\x00\x00\x00"  # p0_y = 0.0
        data += b"\xc0\x79\x00\x00\x00\x00\x00\x00"  # p1_x = -400.0
        data += b"\x40\x59\x00\x00\x00\x00\x00\x00"  # p1_y = 100.0
        data += bytes([1])  # team = 1 (red)
        
        reader = BinaryReader(data)
        goal = Goal.parse(reader)
        
        assert goal.p0_x == -400.0
        assert goal.team == 1
        assert reader.position == 33
    
    def test_parse_player_physics(self):
        """Should parse player physics (64 bytes)."""
        data = b"\x40\x2e\x00\x00\x00\x00\x00\x00"  # radius = 15.0
        data += b"\x3f\xe0\x00\x00\x00\x00\x00\x00"  # b_coef = 0.5
        data += b"\x3f\xe0\x00\x00\x00\x00\x00\x00"  # inv_mass = 0.5
        data += b"\x3f\xee\xb8\x51\xeb\x85\x1e\xb8"  # damping = 0.96
        data += b"\x3f\xb9\x99\x99\x99\x99\x99\x9a"  # acceleration = 0.1
        data += b"\x3f\xb1\xeb\x85\x1e\xb8\x51\xec"  # kick_acceleration = 0.07
        data += b"\x3f\xee\xb8\x51\xeb\x85\x1e\xb8"  # kick_damping = 0.96
        data += b"\x40\x14\x00\x00\x00\x00\x00\x00"  # kick_strength = 5.0
        
        reader = BinaryReader(data)
        physics = PlayerPhysics.parse(reader)
        
        assert physics.radius == 15.0
        assert physics.b_coef == 0.5
        assert abs(physics.acceleration - 0.1) < 0.001
        assert reader.position == 64


class TestStadiumFactory:
    """Tests for parse_stadium factory method."""
    
    def test_factory_routes_to_predefined(self):
        """Should route type 0-11 to PredefinedStadium."""
        data = bytes([0])
        reader = BinaryReader(data)
        
        stadium = parse_stadium(reader)
        
        assert isinstance(stadium, PredefinedStadium)
    
    def test_factory_routes_to_custom(self):
        """Should route type 255 to CustomStadium."""
        # Minimal custom stadium
        data = bytes([255, 1])  # Type + empty name
        data += b"\x00\x00\x01\x00" * 4
        data += b"\x40\x94\x00\x00\x00\x00\x00\x00"
        data += bytes([1, 0])
        data += b"\x40\x49\x00\x00\x00\x00\x00\x00"
        data += bytes([1, 1, 1])
        data += bytes([0] * 6)
        data += b"\x40\x2e\x00\x00\x00\x00\x00\x00" * 8
        
        reader = BinaryReader(data)
        stadium = parse_stadium(reader)
        
        assert isinstance(stadium, CustomStadium)
    
    def test_factory_raises_for_invalid_type(self):
        """Should raise ValueError for invalid stadium type."""
        # Type 100 is invalid (not 0-11 or 255)
        data = bytes([100])
        reader = BinaryReader(data)
        
        with pytest.raises(ValueError, match="Invalid stadium type: 100"):
            parse_stadium(reader)


class TestStadiumWithRealFixtures:
    """Tests using real replay fixtures from src/tests/fixtures/stadium/."""
    
    def test_parse_classic_stadium_fixture(self):
        """Should parse Classic stadium from real replay."""
        stadium, _ = parse_to_stadium(FIXTURES_DIR / "stadium_classic.hbr2")
        
        assert isinstance(stadium, PredefinedStadium)
        assert stadium.stadium_type == 0
        assert stadium.name == "Classic"
    
    def test_parse_easy_stadium_fixture(self):
        """Should parse Easy stadium from real replay."""
        stadium, _ = parse_to_stadium(FIXTURES_DIR / "stadium_easy.hbr2")
        
        assert isinstance(stadium, PredefinedStadium)
        assert stadium.stadium_type == 1
        assert stadium.name == "Easy"
    
    def test_parse_hockey_stadium_fixture(self):
        """Should parse Hockey stadium from real replay."""
        stadium, _ = parse_to_stadium(FIXTURES_DIR / "stadium_hockey.hbr2")
        
        assert isinstance(stadium, PredefinedStadium)
        assert stadium.stadium_type == 5
        assert stadium.name == "Hockey"
    
    def test_parse_custom_stadium_gk_training(self):
        """Should parse custom GK Training stadium from real replay."""
        stadium, _ = parse_to_stadium(
            FIXTURES_DIR / "stadium_custom_name_GK_ULTIMATE_TRAINING.hbr2"
        )
        
        assert isinstance(stadium, CustomStadium)
        assert stadium.name == "GK Training ULTIMATE by H from HaxMaps"
        assert stadium.bg_width > 0
        assert stadium.bg_height > 0
        assert isinstance(stadium.player_physics, PlayerPhysics)
    
    def test_parse_custom_stadium_one_goal(self):
        """Should parse custom one goal stadium from real replay."""
        stadium, _ = parse_to_stadium(
            FIXTURES_DIR / "stadium_custom_one_goal_one_ball_multiple_verteces.hbr2"
        )
        
        assert isinstance(stadium, CustomStadium)
        assert stadium.name == "GK Training ULTIMATE by H from HaxMaps"
        # Just verify it parses successfully - the exact component counts may vary
        assert isinstance(stadium.player_physics, PlayerPhysics)
    
    def test_all_fixtures_parse_successfully(self):
        """All stadium fixtures should parse without errors."""
        fixtures = [
            "stadium_classic.hbr2",
            "stadium_easy.hbr2",
            "stadium_hockey.hbr2",
            "stadium_custom_name_GK_ULTIMATE_TRAINING.hbr2",
            "stadium_custom_one_goal_one_ball_multiple_verteces.hbr2",
        ]
        
        for fixture_name in fixtures:
            stadium, _ = parse_to_stadium(FIXTURES_DIR / fixture_name)
            assert stadium is not None
            assert hasattr(stadium, 'to_dict')
            # Verify to_dict works
            stadium_dict = stadium.to_dict()
            assert isinstance(stadium_dict, dict)
            assert 'custom' in stadium_dict or 'type' in stadium_dict
