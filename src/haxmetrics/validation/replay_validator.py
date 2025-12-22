"""
Replay validator with incremental parsing checkpoints.

This module provides validation tools for parsing HBR2 replay files
with detailed tracking at each parsing section.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Any
import json
import logging

logger = logging.getLogger(__name__)


@dataclass
class CheckpointResult:
    """Result of parsing a single section"""
    section: str
    status: str  # "✅ SUCCESS" or "❌ FAILED"
    offset_before: int
    offset_after: Optional[int] = None
    bytes_read: Optional[int] = None
    bytes_remaining: Optional[int] = None
    data: Optional[Dict] = None
    error: Optional[str] = None
    error_type: Optional[str] = None
    hex_dump: Optional[str] = None


@dataclass
class ValidationReport:
    """Complete validation report for a replay"""
    filepath: str
    file_size: int
    checkpoints: Dict[str, CheckpointResult]
    debug_log: Optional[Dict] = None
    
    @property
    def sections_parsed(self) -> int:
        """Count successfully parsed sections"""
        return sum(1 for r in self.checkpoints.values() if r.status == "✅ SUCCESS")
    
    @property
    def sections_failed(self) -> int:
        """Count failed sections"""
        return sum(1 for r in self.checkpoints.values() if r.status == "❌ FAILED")
    
    @property
    def failure_section(self) -> Optional[str]:
        """Get first section that failed"""
        for section, result in self.checkpoints.items():
            if result.status == "❌ FAILED":
                return section
        return None
    
    @property
    def parsing_progress(self) -> float:
        """Get parsing progress percentage"""
        total = len(self.checkpoints)
        if total == 0:
            return 0.0
        return (self.sections_parsed / total) * 100
    
    def summary(self) -> str:
        """Generate summary string"""
        lines = []
        lines.append(f"File: {Path(self.filepath).name}")
        lines.append(f"Size: {self.file_size:,} bytes")
        lines.append(f"Progress: {self.parsing_progress:.1f}% ({self.sections_parsed}/{len(self.checkpoints)} sections)")
        
        if self.failure_section:
            lines.append(f"Failed at: {self.failure_section}")
            failure = self.checkpoints[self.failure_section]
            lines.append(f"Error: {failure.error}")
            lines.append(f"Offset: {failure.offset_before}")
        else:
            lines.append("Status: ✅ ALL SECTIONS PARSED SUCCESSFULLY")
        
        return "\n".join(lines)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "filepath": self.filepath,
            "file_size": self.file_size,
            "checkpoints": {
                section: {
                    "status": result.status,
                    "offset_before": result.offset_before,
                    "offset_after": result.offset_after,
                    "bytes_read": result.bytes_read,
                    "bytes_remaining": result.bytes_remaining,
                    "data": result.data,
                    "error": result.error,
                    "error_type": result.error_type,
                    "hex_dump": result.hex_dump
                }
                for section, result in self.checkpoints.items()
            },
            "summary": {
                "sections_parsed": self.sections_parsed,
                "sections_failed": self.sections_failed,
                "failure_section": self.failure_section,
                "parsing_progress": f"{self.parsing_progress:.1f}%"
            }
        }
    
    def to_json(self, indent: int = 2) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), indent=indent)
    
    def save(self, filepath: Path):
        """Save report to JSON file"""
        with open(filepath, 'w') as f:
            f.write(self.to_json())


class ReplayValidator:
    """
    Validates replay parsing with incremental checkpoints.
    
    Parses each section of a replay file and tracks results.
    If parsing fails, provides detailed error information including
    hex dump around failure point.
    """
    
    def __init__(self, enable_logging: bool = True):
        self.enable_logging = enable_logging
    
    def validate_replay(self, filepath: Path) -> ValidationReport:
        """
        Validate a replay file with incremental parsing.
        
        Args:
            filepath: Path to .hbr2 replay file
            
        Returns:
            ValidationReport with detailed results for each section
        """
        # Read file
        with open(filepath, 'rb') as f:
            data = f.read()
        
        file_size = len(data)
        logger.info(f"Validating replay: {filepath.name} ({file_size:,} bytes)")
        
        # Create reader with logging
        from haxmetrics.binary_reader import BinaryReader
        reader = BinaryReader(data, enable_logging=self.enable_logging)
        
        # Create debug parser
        from haxmetrics.debug_utils import DebugParser
        debug = DebugParser()
        
        # Define checkpoints (sections to parse)
        checkpoints = {
            "header": self._parse_header,
            "messages": self._parse_messages,
            "room_basic": self._parse_room_basic,
            "stadium": self._parse_stadium,
            "game_state": self._parse_game_state,
            "players": self._parse_players,
            "team_colors": self._parse_team_colors,
            "actions": self._parse_actions
        }
        
        results = {}
        
        # Parse each section with checkpoint
        for section_name, parser_func in checkpoints.items():
            offset_before = reader.position
            
            logger.info(f"Parsing section: {section_name} (offset={offset_before})")
            
            try:
                debug.start_section(section_name, offset_before)
                
                # Parse section
                result = parser_func(reader, debug)
                
                offset_after = reader.position
                bytes_read = offset_after - offset_before
                bytes_remaining = reader.bytes_remaining
                
                debug.end_section(offset_after)
                
                # Store success result
                results[section_name] = CheckpointResult(
                    section=section_name,
                    status="✅ SUCCESS",
                    offset_before=offset_before,
                    offset_after=offset_after,
                    bytes_read=bytes_read,
                    bytes_remaining=bytes_remaining,
                    data=result.to_dict() if hasattr(result, 'to_dict') else result
                )
                
                logger.info(f"  ✅ Success: {bytes_read} bytes read, {bytes_remaining} remaining")
                
            except Exception as e:
                offset_failure = reader.position
                bytes_remaining = reader.bytes_remaining
                
                debug.end_section(offset_failure, error=str(e))
                
                # Generate hex dump around failure
                from haxmetrics.utils.hex_dump import hex_dump
                dump = hex_dump(data, offset_failure, context=64)
                
                # Store failure result
                results[section_name] = CheckpointResult(
                    section=section_name,
                    status="❌ FAILED",
                    offset_before=offset_before,
                    offset_after=offset_failure,
                    bytes_remaining=bytes_remaining,
                    error=str(e),
                    error_type=type(e).__name__,
                    hex_dump=dump
                )
                
                logger.error(f"  ❌ Failed: {e}")
                logger.error(f"  Offset: {offset_failure}, Remaining: {bytes_remaining}")
                
                # Stop at first failure
                break
        
        return ValidationReport(
            filepath=str(filepath),
            file_size=file_size,
            checkpoints=results,
            debug_log=debug.to_dict()
        )
    
    def _parse_header(self, reader, debug):
        """Parse header section"""
        from haxmetrics.models.header import Header
        
        header = Header.parse(reader)
        
        debug.log_field("signature", header.magic)
        debug.log_field("version", header.version)
        debug.log_field("duration", header.duration)
        
        return header
    
    def _parse_messages(self, reader, debug):
        """Parse messages section"""
        # Decompress first
        import zlib
        
        # Store the compressed size for tracking
        compressed_size = reader.bytes_remaining
        compressed = reader.read_remaining()  # This advances position to end
        decompressed = zlib.decompress(compressed, wbits=-15)
        
        # Create new reader for decompressed data
        from haxmetrics.binary_reader import BinaryReader
        reader_decompressed = BinaryReader(decompressed, enable_logging=self.enable_logging)
        
        from haxmetrics.models.messages import Messages
        messages = Messages.parse(reader_decompressed)
        
        # Update main reader to use decompressed data for subsequent sections
        reader.data = decompressed
        reader.position = reader_decompressed.position
        reader.length = len(decompressed)
        
        debug.log_field("count", len(messages))
        debug.log_field("compressed_size", compressed_size)
        debug.log_field("decompressed_size", len(decompressed))
        
        return messages
    
    def _parse_room_basic(self, reader, debug):
        """Parse room basic section"""
        from haxmetrics.models.room import RoomBasic
        
        room = RoomBasic.parse(reader)
        
        debug.log_field("name", room.name)
        debug.log_field("locked", room.locked)
        debug.log_field("score_limit", room.score_limit)
        debug.log_field("time_limit", room.time_limit)
        
        return room
    
    def _parse_stadium(self, reader, debug):
        """Parse stadium section"""
        from haxmetrics.models.stadium import parse_stadium
        
        stadium = parse_stadium(reader)
        
        debug.log_field("type", stadium.stadium_type if hasattr(stadium, 'stadium_type') else 255)
        
        if hasattr(stadium, 'name'):
            debug.log_field("name", stadium.name)
        
        if hasattr(stadium, 'vertices'):
            debug.log_field("vertices_count", len(stadium.vertices))
            debug.log_field("segments_count", len(stadium.segments))
            debug.log_field("planes_count", len(stadium.planes))
            debug.log_field("goals_count", len(stadium.goals))
            debug.log_field("discs_count", len(stadium.discs))
            debug.log_field("joints_count", len(stadium.joints))
        
        return stadium
    
    def _parse_game_state(self, reader, debug):
        """Parse game state section"""
        from haxmetrics.models.game_state import parse_game_state
        
        game_state = parse_game_state(reader)
        
        if game_state is None:
            debug.log_field("game_active", False)
        else:
            debug.log_field("game_active", True)
            debug.log_field("frame", game_state.frame)
            debug.log_field("score_red", game_state.score_red)
            debug.log_field("score_blue", game_state.score_blue)
            debug.log_field("disc_count", len(game_state.discs))
        
        return game_state
    
    def _parse_players(self, reader, debug):
        """Parse players section"""
        from haxmetrics.models.player import Player
        
        # Players count (byte)
        player_count = reader.read_byte()
        debug.log_field("count", player_count)
        
        players = []
        for _ in range(player_count):
            player = Player.parse(reader)
            players.append(player)
        
        # Return a simple container
        class Players:
            def __init__(self, players):
                self.players = players
            
            def __len__(self):
                return len(self.players)
            
            def to_dict(self):
                return {
                    "count": len(self.players),
                    "players": [p.__dict__ for p in self.players]
                }
        
        return Players(players)
    
    def _parse_team_colors(self, reader, debug):
        """Parse team colors section"""
        from haxmetrics.models.team_colors import TeamColors
        
        team_colors = TeamColors.parse(reader)
        
        debug.log_field("red_angle", team_colors.red.angle)
        debug.log_field("red_stripes_count", len(team_colors.red.stripes))
        debug.log_field("blue_angle", team_colors.blue.angle)
        debug.log_field("blue_stripes_count", len(team_colors.blue.stripes))
        
        return team_colors
    
    def _parse_actions(self, reader, debug):
        """Parse actions section"""
        from haxmetrics.models.actions.actions_collection import Actions
        
        actions = Actions.parse(reader)
        
        debug.log_field("count", len(actions))
        
        return actions
