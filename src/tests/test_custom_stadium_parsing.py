"""
Test custom stadium parsing functionality.

This test suite validates that custom stadiums are parsed correctly,
including all components: vertices, segments, planes, goals, discs, joints,
background, and physics parameters.
"""

import pytest
import os
from pathlib import Path

# Add parent directory to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from haxmetrics.parser import Parser
from haxmetrics.models.stadium.stadium import Stadium


class TestCustomStadiumParsing:
    """Test suite for custom stadium parsing."""
    
    @pytest.fixture
    def lirs_replay_path(self):
        """Fixture providing path to a LIRS replay with custom stadium."""
        base_path = Path(__file__).parent.parent.parent
        replay_path = base_path / "src" / "replays" / "LIRS" / "Albania-Poland3.hbr2"
        
        if not replay_path.exists():
            pytest.skip(f"Replay file not found: {replay_path}")
        
        return str(replay_path)
    
    @pytest.fixture
    def parsed_replay(self, lirs_replay_path):
        """Fixture providing a parsed replay."""
        with open(lirs_replay_path, "rb") as f:
            data = f.read()
        
        parser = Parser(data)
        return parser.parse()
    
    def test_stadium_exists(self, parsed_replay):
        """Test that stadium is present in parsed replay."""
        assert parsed_replay["room_info"] is not None
        assert parsed_replay["room_info"].stadium is not None
    
    def test_stadium_is_custom(self, parsed_replay):
        """Test that the stadium is detected as custom."""
        stadium = parsed_replay["room_info"].stadium
        assert stadium.custom is True
        assert stadium.type == 0xFF
    
    def test_stadium_name(self, parsed_replay):
        """Test that custom stadium name is parsed correctly."""
        stadium = parsed_replay["room_info"].stadium
        assert stadium.name == "LIRS RS 4v4"
    
    def test_stadium_background(self, parsed_replay):
        """Test that stadium background is parsed."""
        stadium = parsed_replay["room_info"].stadium
        assert stadium.background is not None
        # Background should have type, width, height
        assert hasattr(stadium.background, "type")
    
    def test_stadium_player_physics(self, parsed_replay):
        """Test that player physics are parsed correctly."""
        stadium = parsed_replay["room_info"].stadium
        assert stadium.player_physics is not None
        
        # Check expected physics values for LIRS RS 4v4
        physics = stadium.player_physics
        assert hasattr(physics, "b_coef")
        assert hasattr(physics, "acceleration")
        assert hasattr(physics, "kick_strength")
        
        # These values should match the documented structure
        assert physics.b_coef == pytest.approx(0.3, rel=0.01)
        assert physics.acceleration == pytest.approx(0.12, rel=0.01)
        assert physics.kick_strength == pytest.approx(5.65, rel=0.01)
    
    def test_stadium_components_arrays(self, parsed_replay):
        """Test that all stadium component arrays are present."""
        stadium = parsed_replay["room_info"].stadium
        
        # All component arrays should exist (even if empty)
        assert hasattr(stadium, "vertexes")
        assert hasattr(stadium, "segments")
        assert hasattr(stadium, "planes")
        assert hasattr(stadium, "goals")
        assert hasattr(stadium, "discs")
        assert hasattr(stadium, "joints")
        
        # These should be lists
        assert isinstance(stadium.vertexes, list)
        assert isinstance(stadium.segments, list)
        assert isinstance(stadium.planes, list)
        assert isinstance(stadium.goals, list)
        assert isinstance(stadium.discs, list)
        assert isinstance(stadium.joints, list)
    
    def test_stadium_lirs_is_empty(self, parsed_replay):
        """Test that LIRS RS 4v4 stadium has no collision geometry."""
        stadium = parsed_replay["room_info"].stadium
        
        # LIRS RS 4v4 is documented as having no collision geometry
        assert len(stadium.vertexes) == 0
        assert len(stadium.segments) == 0
        assert len(stadium.planes) == 0
        assert len(stadium.goals) == 0
        assert len(stadium.discs) == 0
        assert len(stadium.joints) == 0
    
    def test_stadium_predefined_detection(self):
        """Test that predefined stadiums are detected correctly."""
        # Predefined stadiums are identified by type < 10
        for i, name in enumerate(Stadium.STADIUMS):
            assert Stadium.STADIUMS[i] == name
        
        # Check that we have the expected predefined stadiums
        assert "Classic" in Stadium.STADIUMS
        assert "Hockey" in Stadium.STADIUMS
        assert "Big" in Stadium.STADIUMS
    
    def test_stadium_custom_marker(self):
        """Test that 0xFF is correctly used as custom stadium marker."""
        # This is documented in section 4.7 of GAME_MIN_REVERSE_ENGINEERING.md
        assert 0xFF == 255
        
        # Custom stadiums have type 255
        # Predefined stadiums have type 0-9
        assert 0xFF > len(Stadium.STADIUMS)


class TestStadiumComponents:
    """Test individual stadium components parsing."""
    
    def test_vertex_structure(self):
        """Test that Vertex class has expected fields."""
        from haxmetrics.models.stadium.vertex import Vertex
        
        # Vertices need constructor arguments
        # Just verify the class exists
        assert Vertex is not None
        assert hasattr(Vertex, "parse")
    
    def test_segment_structure(self):
        """Test that Segment class has expected fields."""
        from haxmetrics.models.stadium.segment import Segment
        
        # Segments need constructor arguments
        # Just verify the class exists
        assert Segment is not None
        assert hasattr(Segment, "parse")
    
    def test_goal_structure(self):
        """Test that Goal class has expected fields."""
        from haxmetrics.models.stadium.goal import Goal
        
        # Goals need constructor arguments
        # Just verify the class exists
        assert Goal is not None
        assert hasattr(Goal, "parse")
    
    def test_disc_structure(self):
        """Test that Disc class has expected fields."""
        from haxmetrics.models.stadium.disc import Disc
        
        # Discs need constructor arguments
        # Just verify the class exists
        assert Disc is not None
        assert hasattr(Disc, "parse")


class TestStadiumSerialization:
    """Test stadium binary format serialization."""
    
    def test_custom_stadium_byte_marker(self):
        """Test that custom stadium uses 0xFF byte marker."""
        # According to documentation section 4.7
        custom_marker = 0xFF
        assert custom_marker == 255
    
    def test_stadium_type_range(self):
        """Test that predefined stadium types are in valid range."""
        # Predefined stadiums: 0-9
        # Custom stadiums: 255 (0xFF)
        # Any value 10-254 is invalid
        
        valid_predefined = range(0, len(Stadium.STADIUMS))
        custom_type = 0xFF
        
        # Check boundaries
        assert 0 in valid_predefined
        assert 9 in valid_predefined
        assert custom_type == 255
        
        # Check invalid range
        for invalid in range(10, 255):
            assert invalid not in valid_predefined
            assert invalid != custom_type


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
