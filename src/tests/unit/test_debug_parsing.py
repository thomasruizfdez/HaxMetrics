"""
Debug tests for GameState and TeamColors parsing.

These tests are designed to help identify parsing issues by:
1. Enabling comprehensive logging in BinaryReader
2. Tracking parsing progress with DebugParser
3. Generating JSON output showing parsed data up to failure point
4. Providing hex dumps around failure points

Run these tests with:
    python -m pytest src/tests/unit/test_debug_parsing.py -v -s
"""

import logging
import zlib
from pathlib import Path

import pytest

from haxmetrics.binary_reader import BinaryReader
from haxmetrics.debug_utils import DebugParser, hex_dump
from haxmetrics.models.game_state import GameState, parse_game_state
from haxmetrics.models.header import Header
from haxmetrics.models.messages import Messages
from haxmetrics.models.player import Player
from haxmetrics.models.room import RoomBasic
from haxmetrics.models.stadium import parse_stadium
from haxmetrics.models.team_color import TeamColor

# Configure logging to show all debug messages
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s: %(message)s'
)

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"


class TestDebugGameStateParsing:
    """Debug tests for GameState parsing issues"""
    
    def test_debug_game_no_active(self, tmp_path):
        """Debug parsing when game_active = 0 (should work)"""
        fixture_path = FIXTURES_DIR / "game_state" / "game_no_active.hbr2"
        debug = DebugParser()
        
        with open(fixture_path, "rb") as f:
            data = f.read()
            reader = BinaryReader(data, enable_logging=False)  # Disable for less noise
            
            try:
                # Parse Header
                debug.start_section("Header", reader.position)
                header = Header.parse(reader)
                debug.log_field("signature", header.magic)
                debug.log_field("version", header.version)
                debug.log_field("duration", header.duration)
                debug.end_section(reader.position)
                
                # Decompress
                debug.start_section("Decompression", reader.position)
                compressed_data = reader.read_remaining()
                decompressed = zlib.decompress(compressed_data, wbits=-15)
                debug.log_field("compressed_size", len(compressed_data))
                debug.log_field("decompressed_size", len(decompressed))
                debug.end_section(reader.position)
                
                reader = BinaryReader(decompressed, enable_logging=False)
                
                # Parse Messages
                debug.start_section("Messages", reader.position)
                messages = Messages.parse(reader)
                debug.log_field("message_count", len(messages))
                debug.end_section(reader.position)
                
                # Parse RoomBasic
                debug.start_section("RoomBasic", reader.position)
                room_basic = RoomBasic.parse(reader)
                debug.log_field("name", room_basic.name)
                debug.log_field("locked", room_basic.locked)
                debug.log_field("score_limit", room_basic.score_limit)
                debug.log_field("time_limit", room_basic.time_limit)
                debug.end_section(reader.position)
                
                # Parse Stadium
                debug.start_section("Stadium", reader.position)
                stadium = parse_stadium(reader)
                debug.log_field("stadium_parsed", True)
                debug.end_section(reader.position)
                
                # Parse GameState
                debug.start_section("GameState", reader.position)
                game_state = parse_game_state(reader)
                debug.log_field("game_active", 0 if game_state is None else 1)
                if game_state:
                    debug.log_field("frame", game_state.frame)
                    debug.log_field("score_red", game_state.score_red)
                    debug.log_field("score_blue", game_state.score_blue)
                    debug.log_field("disc_count", len(game_state.discs))
                debug.end_section(reader.position)
                
            except Exception as e:
                debug.end_section(reader.position, error=str(e))
                print(f"\nParsing failed: {e}")
                print(f"Bytes remaining: {reader.bytes_remaining}")
            
            # Save debug output
            output_file = tmp_path / "debug_game_no_active.json"
            debug.save_to_file(str(output_file))
            
            print(f"\n=== Debug output saved to: {output_file} ===")
            print(debug.to_json())
            
            # Should succeed
            assert not debug.to_dict()["has_errors"], "Parsing should succeed for game_no_active"
    
    def test_debug_game_active_and_playing(self, tmp_path):
        """Debug parsing when game_active = 1 (this is where we check for issues)"""
        fixture_path = FIXTURES_DIR / "game_state" / "game_active_and_playing.hbr2"
        debug = DebugParser()
        
        with open(fixture_path, "rb") as f:
            data = f.read()
            reader = BinaryReader(data, enable_logging=True)  # Enable logging for detailed info
            
            try:
                # Parse Header
                debug.start_section("Header", reader.position)
                header = Header.parse(reader)
                debug.log_field("signature", header.magic)
                debug.log_field("version", header.version)
                debug.log_field("duration", header.duration)
                debug.end_section(reader.position)
                
                # Decompress
                debug.start_section("Decompression", reader.position)
                compressed_data = reader.read_remaining()
                decompressed = zlib.decompress(compressed_data, wbits=-15)
                debug.log_field("compressed_size", len(compressed_data))
                debug.log_field("decompressed_size", len(decompressed))
                debug.end_section(reader.position)
                
                reader = BinaryReader(decompressed, enable_logging=True)
                
                # Parse Messages
                debug.start_section("Messages", reader.position)
                messages = Messages.parse(reader)
                debug.log_field("message_count", len(messages))
                debug.end_section(reader.position)
                
                # Parse RoomBasic
                debug.start_section("RoomBasic", reader.position)
                room_basic = RoomBasic.parse(reader)
                debug.log_field("name", room_basic.name)
                debug.log_field("locked", room_basic.locked)
                debug.log_field("score_limit", room_basic.score_limit)
                debug.log_field("time_limit", room_basic.time_limit)
                debug.end_section(reader.position)
                
                # Parse Stadium
                debug.start_section("Stadium", reader.position)
                stadium = parse_stadium(reader)
                debug.log_field("stadium_parsed", True)
                debug.end_section(reader.position)
                
                # Parse GameState
                debug.start_section("GameState", reader.position)
                offset_before_game = reader.position
                game_state = parse_game_state(reader)
                debug.log_field("game_active", 0 if game_state is None else 1)
                if game_state:
                    debug.log_field("frame", game_state.frame)
                    debug.log_field("score_red", game_state.score_red)
                    debug.log_field("score_blue", game_state.score_blue)
                    debug.log_field("disc_count", len(game_state.discs))
                    for i, disc in enumerate(game_state.discs):
                        debug.log_field(f"disc_{i}_x", disc.x)
                        debug.log_field(f"disc_{i}_y", disc.y)
                        debug.log_field(f"disc_{i}_vx", disc.vx)
                        debug.log_field(f"disc_{i}_vy", disc.vy)
                debug.end_section(reader.position)
                
                # Parse Players
                debug.start_section("Players", reader.position)
                player_count = reader.read_byte()
                debug.log_field("player_count", player_count)
                for i in range(player_count):
                    try:
                        player = Player.parse(reader)
                        debug.log_field(f"player_{i}_id", player.player_id)
                    except Exception as e:
                        debug.log_field(f"player_{i}_error", str(e))
                        raise
                debug.end_section(reader.position)
                
                # Parse TeamColors
                debug.start_section("TeamColors", reader.position)
                team_colors = {
                    "red": TeamColor.parse(reader),
                    "blue": TeamColor.parse(reader)
                }
                debug.log_field("red_angle", team_colors["red"].get_angle())
                debug.log_field("red_text_color", team_colors["red"].get_text_color())
                debug.log_field("blue_angle", team_colors["blue"].get_angle())
                debug.log_field("blue_text_color", team_colors["blue"].get_text_color())
                debug.end_section(reader.position)
                
            except Exception as e:
                debug.end_section(reader.position, error=str(e))
                print(f"\nParsing failed at offset {reader.position}: {e}")
                print(f"Bytes remaining: {reader.bytes_remaining}")
                
                # Print hex dump around failure point
                if reader.position < len(decompressed):
                    print(f"\n=== Hex dump around failure ===")
                    print(hex_dump(decompressed, reader.position, context=32))
            
            # Save debug output
            output_file = tmp_path / "debug_game_active_and_playing.json"
            debug.save_to_file(str(output_file))
            
            print(f"\n=== Debug output saved to: {output_file} ===")
            print(debug.to_json())
            
            # Should succeed - if not, we'll see detailed output
            if debug.to_dict()["has_errors"]:
                print("\n⚠️  Parsing encountered errors - check the JSON output above")
    
    def test_debug_red_winning_1_0(self, tmp_path):
        """Debug parsing of red_winning_1_0 fixture"""
        fixture_path = FIXTURES_DIR / "game_state" / "red_winning_1_0.hbr2"
        debug = DebugParser()
        
        with open(fixture_path, "rb") as f:
            data = f.read()
            reader = BinaryReader(data, enable_logging=True)
            
            try:
                # Parse Header
                debug.start_section("Header", reader.position)
                header = Header.parse(reader)
                debug.end_section(reader.position)
                
                # Decompress
                compressed_data = reader.read_remaining()
                decompressed = zlib.decompress(compressed_data, wbits=-15)
                reader = BinaryReader(decompressed, enable_logging=True)
                
                # Parse Messages
                debug.start_section("Messages", reader.position)
                messages = Messages.parse(reader)
                debug.end_section(reader.position)
                
                # Parse RoomBasic
                debug.start_section("RoomBasic", reader.position)
                room_basic = RoomBasic.parse(reader)
                debug.end_section(reader.position)
                
                # Parse Stadium
                debug.start_section("Stadium", reader.position)
                stadium = parse_stadium(reader)
                debug.end_section(reader.position)
                
                # Parse GameState
                debug.start_section("GameState", reader.position)
                game_state = parse_game_state(reader)
                if game_state:
                    debug.log_field("score_red", game_state.score_red)
                    debug.log_field("score_blue", game_state.score_blue)
                    debug.log_field("winner", game_state.winner)
                debug.end_section(reader.position)
                
            except Exception as e:
                debug.end_section(reader.position, error=str(e))
            
            output_file = tmp_path / "debug_red_winning_1_0.json"
            debug.save_to_file(str(output_file))
            print(f"\n=== Debug output saved to: {output_file} ===")


class TestDebugTeamColorsParsing:
    """Debug tests for TeamColors parsing issues"""
    
    def test_debug_no_team_colors(self, tmp_path):
        """Debug parsing with default team colors"""
        fixture_path = FIXTURES_DIR / "team-colors" / "no_team_colors.hbr2"
        debug = DebugParser()
        
        with open(fixture_path, "rb") as f:
            data = f.read()
            reader = BinaryReader(data, enable_logging=True)
            
            try:
                # Parse Header
                debug.start_section("Header", reader.position)
                header = Header.parse(reader)
                debug.end_section(reader.position)
                
                # Decompress
                compressed_data = reader.read_remaining()
                decompressed = zlib.decompress(compressed_data, wbits=-15)
                reader = BinaryReader(decompressed, enable_logging=True)
                
                # Parse Messages
                debug.start_section("Messages", reader.position)
                messages = Messages.parse(reader)
                debug.end_section(reader.position)
                
                # Parse RoomBasic
                debug.start_section("RoomBasic", reader.position)
                room_basic = RoomBasic.parse(reader)
                debug.end_section(reader.position)
                
                # Parse Stadium
                debug.start_section("Stadium", reader.position)
                stadium = parse_stadium(reader)
                debug.end_section(reader.position)
                
                # Parse GameState
                debug.start_section("GameState", reader.position)
                game_state = parse_game_state(reader)
                debug.end_section(reader.position)
                
                # Parse Players
                debug.start_section("Players", reader.position)
                player_count = reader.read_byte()
                debug.log_field("player_count", player_count)
                for i in range(player_count):
                    player = Player.parse(reader)
                debug.end_section(reader.position)
                
                # Parse TeamColors
                debug.start_section("TeamColors_Red", reader.position)
                red_color = TeamColor.parse(reader)
                debug.log_field("angle", red_color.get_angle())
                debug.log_field("text_color", red_color.get_text_color())
                debug.log_field("stripe_count", len(red_color.get_stripes()))
                debug.end_section(reader.position)
                
                debug.start_section("TeamColors_Blue", reader.position)
                blue_color = TeamColor.parse(reader)
                debug.log_field("angle", blue_color.get_angle())
                debug.log_field("text_color", blue_color.get_text_color())
                debug.log_field("stripe_count", len(blue_color.get_stripes()))
                debug.end_section(reader.position)
                
            except Exception as e:
                debug.end_section(reader.position, error=str(e))
                print(f"\nParsing failed at offset {reader.position}: {e}")
                if reader.position < len(decompressed):
                    print(hex_dump(decompressed, reader.position))
            
            output_file = tmp_path / "debug_no_team_colors.json"
            debug.save_to_file(str(output_file))
            print(f"\n=== Debug output saved to: {output_file} ===")
    
    def test_debug_both_teams_custom_colors(self, tmp_path):
        """Debug parsing with custom team colors"""
        fixture_path = FIXTURES_DIR / "team-colors" / "both_teams_custom_colors.hbr2"
        debug = DebugParser()
        
        with open(fixture_path, "rb") as f:
            data = f.read()
            reader = BinaryReader(data, enable_logging=True)
            
            try:
                # Parse Header
                debug.start_section("Header", reader.position)
                header = Header.parse(reader)
                debug.end_section(reader.position)
                
                # Decompress
                compressed_data = reader.read_remaining()
                decompressed = zlib.decompress(compressed_data, wbits=-15)
                reader = BinaryReader(decompressed, enable_logging=True)
                
                # Parse Messages
                debug.start_section("Messages", reader.position)
                messages = Messages.parse(reader)
                debug.end_section(reader.position)
                
                # Parse RoomBasic
                debug.start_section("RoomBasic", reader.position)
                room_basic = RoomBasic.parse(reader)
                debug.end_section(reader.position)
                
                # Parse Stadium
                debug.start_section("Stadium", reader.position)
                stadium = parse_stadium(reader)
                debug.end_section(reader.position)
                
                # Parse GameState
                debug.start_section("GameState", reader.position)
                game_state = parse_game_state(reader)
                debug.end_section(reader.position)
                
                # Parse Players
                debug.start_section("Players", reader.position)
                player_count = reader.read_byte()
                debug.log_field("player_count", player_count)
                for i in range(player_count):
                    player = Player.parse(reader)
                debug.end_section(reader.position)
                
                # Parse TeamColors
                debug.start_section("TeamColors_Red", reader.position)
                red_color = TeamColor.parse(reader)
                debug.log_field("angle", red_color.get_angle())
                debug.log_field("text_color", red_color.get_text_color())
                debug.log_field("stripes", red_color.get_stripes())
                debug.end_section(reader.position)
                
                debug.start_section("TeamColors_Blue", reader.position)
                blue_color = TeamColor.parse(reader)
                debug.log_field("angle", blue_color.get_angle())
                debug.log_field("text_color", blue_color.get_text_color())
                debug.log_field("stripes", blue_color.get_stripes())
                debug.end_section(reader.position)
                
            except Exception as e:
                debug.end_section(reader.position, error=str(e))
                print(f"\nParsing failed at offset {reader.position}: {e}")
                if reader.position < len(decompressed):
                    print(hex_dump(decompressed, reader.position))
            
            output_file = tmp_path / "debug_both_teams_custom_colors.json"
            debug.save_to_file(str(output_file))
            print(f"\n=== Debug output saved to: {output_file} ===")
            print(debug.to_json())


class TestHexDumpUtility:
    """Test hex dump utility"""
    
    def test_hex_dump_basic(self):
        """Test hex_dump function"""
        data = b"Hello, World! This is a test."
        output = hex_dump(data, 7, context=16)
        
        assert "Hex dump" in output
        assert "failure at 7" in output
        print(f"\n{output}")
    
    def test_hex_dump_at_start(self):
        """Test hex_dump at start of data"""
        data = b"Test data"
        output = hex_dump(data, 0, context=8)
        
        assert "0000" in output
        print(f"\n{output}")
    
    def test_hex_dump_at_end(self):
        """Test hex_dump at end of data"""
        data = b"Test data"
        output = hex_dump(data, len(data) - 1, context=8)
        
        print(f"\n{output}")
