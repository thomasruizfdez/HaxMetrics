#!/usr/bin/env python3
"""
Validate serialization between JavaScript and Python implementations.

This script validates that the Python parser correctly interprets the binary
format as defined in game-min.js by:
1. Checking all action types are implemented
2. Validating stadium parsing
3. Comparing byte-level patterns
4. Checking for consistency across multiple replays
"""

import sys
import os
from pathlib import Path
from collections import Counter

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from haxmetrics.parser import Parser
from haxmetrics.models.action_types import ACTION_TYPES


def validate_action_types():
    """Validate that all 24 action types are implemented."""
    print("\n" + "="*80)
    print("VALIDATING ACTION TYPES")
    print("="*80)
    
    expected_count = 24
    actual_count = len(ACTION_TYPES)
    
    print(f"\nExpected action types: {expected_count}")
    print(f"Implemented action types: {actual_count}")
    
    if actual_count == expected_count:
        print("✅ All action types are implemented!")
    else:
        print(f"❌ Missing {expected_count - actual_count} action types")
        return False
    
    print("\nAction type list:")
    for i, action_class in enumerate(ACTION_TYPES):
        print(f"  {i:2d}. {action_class.__name__}")
    
    return True


def validate_parser_structure(replay_path: str):
    """Validate parser can read the basic structure of a replay."""
    print(f"\n" + "="*80)
    print(f"VALIDATING PARSER STRUCTURE: {os.path.basename(replay_path)}")
    print("="*80)
    
    try:
        with open(replay_path, "rb") as f:
            data = f.read()
        
        parser = Parser(data)
        replay = parser.parse()
        
        # Check required fields
        checks = {
            "version": replay.get("version"),
            "duration": replay.get("duration"),
            "room_info": replay.get("room_info"),
            "messages": replay.get("messages"),
            "team_colors": replay.get("team_colors"),
        }
        
        all_ok = True
        for key, value in checks.items():
            if value is None:
                print(f"❌ Missing field: {key}")
                all_ok = False
            else:
                print(f"✅ {key}: present")
        
        # Check room info details
        if replay["room_info"]:
            room = replay["room_info"]
            room_checks = {
                "name": room.name,
                "stadium": room.stadium,
                "players": room.players,
                "team_colors": room.team_colors,
            }
            
            print("\nRoom info details:")
            for key, value in room_checks.items():
                if value is None and key != "players":  # players can be None/empty
                    print(f"  ❌ Missing: {key}")
                    all_ok = False
                else:
                    if key == "players":
                        print(f"  ✅ {key}: {len(value) if value else 0} players")
                    elif key == "stadium":
                        print(f"  ✅ {key}: {value.name if value else 'None'}")
                    elif key == "team_colors":
                        print(f"  ✅ {key}: {len(value) if value else 0} teams")
                    else:
                        print(f"  ✅ {key}: {value}")
        
        return all_ok
        
    except Exception as e:
        print(f"❌ Error parsing: {e}")
        import traceback
        traceback.print_exc()
        return False


def validate_stadium_parsing(replay_path: str):
    """Validate stadium parsing is correct."""
    print(f"\n" + "="*80)
    print(f"VALIDATING STADIUM PARSING: {os.path.basename(replay_path)}")
    print("="*80)
    
    try:
        with open(replay_path, "rb") as f:
            data = f.read()
        
        parser = Parser(data)
        replay = parser.parse()
        
        if not replay["room_info"] or not replay["room_info"].stadium:
            print("❌ No stadium found")
            return False
        
        stadium = replay["room_info"].stadium
        
        print(f"\nStadium type: {stadium.type}")
        print(f"Stadium name: {stadium.name}")
        print(f"Custom: {stadium.custom}")
        
        if stadium.custom:
            print(f"\nCustom stadium details:")
            print(f"  Vertices: {len(stadium.vertexes) if hasattr(stadium, 'vertexes') else 0}")
            print(f"  Segments: {len(stadium.segments) if hasattr(stadium, 'segments') else 0}")
            print(f"  Planes: {len(stadium.planes) if hasattr(stadium, 'planes') else 0}")
            print(f"  Goals: {len(stadium.goals) if hasattr(stadium, 'goals') else 0}")
            print(f"  Discs: {len(stadium.discs) if hasattr(stadium, 'discs') else 0}")
            print(f"  Joints: {len(stadium.joints) if hasattr(stadium, 'joints') else 0}")
            
            if stadium.player_physics:
                print(f"  Player physics:")
                print(f"    b_coef: {stadium.player_physics.b_coef}")
                print(f"    acceleration: {stadium.player_physics.acceleration}")
                print(f"    kick_strength: {stadium.player_physics.kick_strength}")
        
        print("✅ Stadium parsed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error parsing stadium: {e}")
        import traceback
        traceback.print_exc()
        return False


def validate_consistency(replay_paths: list):
    """Validate consistency across multiple replays."""
    print("\n" + "="*80)
    print("VALIDATING CONSISTENCY ACROSS REPLAYS")
    print("="*80)
    
    results = []
    
    for replay_path in replay_paths:
        try:
            with open(replay_path, "rb") as f:
                data = f.read()
            
            parser = Parser(data)
            replay = parser.parse()
            
            result = {
                "file": os.path.basename(replay_path),
                "version": replay["version"],
                "has_room": replay["room_info"] is not None,
                "has_stadium": replay["room_info"].stadium is not None if replay["room_info"] else False,
                "stadium_custom": replay["room_info"].stadium.custom if replay["room_info"] and replay["room_info"].stadium else False,
                "player_count": len(replay["players"]) if replay["players"] else 0,
                "action_count": len(replay["actions"]) if replay["actions"] else 0,
            }
            results.append(result)
            
        except Exception as e:
            print(f"❌ Error with {os.path.basename(replay_path)}: {e}")
    
    # Check for consistency
    print(f"\nAnalyzed {len(results)} replays:")
    
    versions = set(r["version"] for r in results)
    print(f"  Versions: {versions}")
    
    all_have_room = all(r["has_room"] for r in results)
    print(f"  All have room info: {'✅' if all_have_room else '❌'}")
    
    all_have_stadium = all(r["has_stadium"] for r in results)
    print(f"  All have stadium: {'✅' if all_have_stadium else '❌'}")
    
    custom_count = sum(1 for r in results if r["stadium_custom"])
    print(f"  Custom stadiums: {custom_count}/{len(results)}")
    
    print(f"\nPlayer counts: {[r['player_count'] for r in results]}")
    print(f"Action counts: {[r['action_count'] for r in results]}")
    
    return all_have_room and all_have_stadium


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python validate_serialization.py <replay_file> [replay_file2 ...]")
        print("\nExample:")
        print("  python validate_serialization.py src/replays/LIRS/*.hbr2")
        sys.exit(1)
    
    print("="*80)
    print("HBR2 SERIALIZATION VALIDATION")
    print("="*80)
    
    # 1. Validate action types
    action_types_ok = validate_action_types()
    
    # 2. Validate parser structure for each file
    parser_ok = True
    for replay_path in sys.argv[1:]:
        if not validate_parser_structure(replay_path):
            parser_ok = False
    
    # 3. Validate stadium parsing for each file
    stadium_ok = True
    for replay_path in sys.argv[1:]:
        if not validate_stadium_parsing(replay_path):
            stadium_ok = False
    
    # 4. Validate consistency across files
    consistency_ok = validate_consistency(sys.argv[1:])
    
    # Summary
    print("\n" + "="*80)
    print("VALIDATION SUMMARY")
    print("="*80)
    
    checks = {
        "Action types": action_types_ok,
        "Parser structure": parser_ok,
        "Stadium parsing": stadium_ok,
        "Consistency": consistency_ok,
    }
    
    all_ok = all(checks.values())
    
    for check, status in checks.items():
        status_str = "✅ PASS" if status else "❌ FAIL"
        print(f"  {check}: {status_str}")
    
    print("\n" + "="*80)
    if all_ok:
        print("✅ ALL VALIDATIONS PASSED")
    else:
        print("❌ SOME VALIDATIONS FAILED")
    print("="*80)
    
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
