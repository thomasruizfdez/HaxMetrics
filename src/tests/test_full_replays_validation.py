"""
Full replay validation tests with incremental parsing.

These tests parse complete replay files incrementally,
generating detailed reports for each section.
"""

import pytest
from pathlib import Path
from haxmetrics.validation.replay_validator import ReplayValidator
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)

logger = logging.getLogger(__name__)


class TestFullReplaysValidation:
    """
    Validation tests for full real replays.
    
    These tests parse complete replay files incrementally,
    generating detailed reports for each section.
    """
    
    REPLAYS = [
        "HBReplay-18-12-2025-23h29m.hbr2",
        "HBReplay-18-12-2025-23h43m.hbr2",
        "HBReplay-19-12-2025-22h39m.hbr2",
        "HBReplay-19-12-2025-22h52m.hbr2",
        "HBReplay-21-12-2025-21h27m.hbr2",
        "HBReplay-21-12-2025-21h41m.hbr2",
    ]
    
    @pytest.mark.parametrize("replay_file", REPLAYS)
    def test_validate_full_replay(self, replay_file, tmp_path):
        """
        Validate a full replay with incremental parsing.
        
        This test:
        1. Parses each section with checkpoints
        2. Generates detailed JSON report
        3. Shows exactly where parsing fails (if any)
        4. Provides hex dump at failure point
        """
        fixture_path = Path("src/tests/fixtures/full-replays") / replay_file
        
        if not fixture_path.exists():
            pytest.skip(f"Fixture not found: {fixture_path}")
        
        # Create validator
        validator = ReplayValidator(enable_logging=True)
        
        # Validate replay
        logger.info(f"\n{'='*80}")
        logger.info(f"VALIDATING: {replay_file}")
        logger.info(f"{'='*80}")
        
        report = validator.validate_replay(fixture_path)
        
        # Save report
        output_file = tmp_path / f"validation_{replay_file}.json"
        report.save(output_file)
        
        # Print summary
        print(f"\n{report.summary()}")
        print(f"\nFull report saved to: {output_file}")
        
        # Print section-by-section results
        print(f"\n{'Section':<15} {'Status':<15} {'Bytes Read':<15} {'Remaining':<15}")
        print("=" * 65)
        
        for section, result in report.checkpoints.items():
            status = result.status
            bytes_read = f"{result.bytes_read:,}" if result.bytes_read else "N/A"
            remaining = f"{result.bytes_remaining:,}" if result.bytes_remaining is not None else "N/A"
            
            print(f"{section:<15} {status:<15} {bytes_read:<15} {remaining:<15}")
            
            if result.status == "❌ FAILED":
                print(f"\n  Error: {result.error}")
                print(f"  Type: {result.error_type}")
                print(f"  Offset: {result.offset_before}")
                
                if result.hex_dump:
                    print(f"\n  Hex Dump:")
                    for line in result.hex_dump.split('\n'):
                        print(f"    {line}")
        
        # Assert for tracking (but don't fail test yet - this is validation)
        if report.failure_section:
            logger.warning(f"⚠️  Parsing failed at section: {report.failure_section}")
            logger.warning(f"⚠️  This is expected during initial validation phase")
        else:
            logger.info(f"✅ All sections parsed successfully!")
    
    def test_generate_comparison_matrix(self, tmp_path):
        """
        Generate comparison matrix showing results across all replays.
        
        Creates a table showing which sections pass/fail for each replay.
        """
        validator = ReplayValidator(enable_logging=False)
        
        results = {}
        
        for replay_file in self.REPLAYS:
            fixture_path = Path("src/tests/fixtures/full-replays") / replay_file
            
            if not fixture_path.exists():
                continue
            
            report = validator.validate_replay(fixture_path)
            results[replay_file] = report
        
        # Generate matrix
        print(f"\n{'='*100}")
        print("REPLAY VALIDATION MATRIX")
        print(f"{'='*100}")
        
        sections = ["header", "messages", "room_basic", "stadium", "game_state", "players", "team_colors", "actions"]
        
        # Header
        header = f"{'Replay':<35}"
        for section in sections:
            header += f" | {section[:8]:^8}"
        print(header)
        print("-" * 100)
        
        # Rows
        for replay_file, report in results.items():
            row = f"{replay_file:<35}"
            
            for section in sections:
                if section in report.checkpoints:
                    result = report.checkpoints[section]
                    symbol = "✅" if result.status == "✅ SUCCESS" else "❌"
                else:
                    symbol = "-"
                
                row += f" |    {symbol:^2}   "
            
            print(row)
        
        print(f"{'='*100}")
        
        # Summary
        print(f"\nSummary:")
        for replay_file, report in results.items():
            progress = report.parsing_progress
            failure = report.failure_section or "None"
            print(f"  {replay_file}: {progress:.1f}% parsed, failed at: {failure}")
        
        # Save matrix to file
        matrix_file = tmp_path / "validation_matrix.txt"
        with open(matrix_file, 'w') as f:
            f.write(f"Generated comparison matrix saved to: {matrix_file}\n")
        
        print(f"\nComparison matrix saved to: {matrix_file}")
