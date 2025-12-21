#!/usr/bin/env python3
"""
Analyze replay patterns from HBR2 files.

This script extracts and analyzes patterns from HaxBall replay files:
- Action type distribution
- Stadium information
- Player statistics
- Message patterns
- Frame timing
"""

import sys
import os
from pathlib import Path
from collections import Counter

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from haxmetrics.parser import Parser


def analyze_replay(replay_path: str) -> dict:
    """Analyze a single replay file and extract patterns."""
    print(f"\n{'='*80}")
    print(f"Analyzing: {replay_path}")
    print(f"{'='*80}\n")
    
    with open(replay_path, "rb") as f:
        data = f.read()
    
    parser = Parser(data)
    replay = parser.parse()
    
    # Basic metadata
    result = {
        "file": os.path.basename(replay_path),
        "version": replay["version"],
        "duration_frames": replay["duration"],
        "duration_seconds": replay["duration"] / 60.0,
        "messages": [],
        "room": {},
        "players": [],
        "actions": [],
        "statistics": {}
    }
    
    # Messages analysis
    messages = replay.get("messages", [])
    result["messages"] = {
        "count": len(messages),
        "types": Counter([msg.get("type", "unknown") for msg in messages])
    }
    
    # Room info
    if replay["room_info"]:
        room = replay["room_info"]
        result["room"] = {
            "name": room.name,
            "teams_locked": getattr(room, "teams_locked", None) or getattr(room, "locked", None),
            "score_limit": room.score_limit,
            "time_limit": room.time_limit,
            "game_active": room.in_progress if hasattr(room, "in_progress") else False,
            "stadium": {
                "type": room.stadium.type if room.stadium else None,
                "name": room.stadium.name if room.stadium else None,
                "custom": room.stadium.custom if room.stadium else False
            }
        }
    
    # Players analysis
    players = replay.get("players", [])
    result["players"] = {
        "count": len(players),
        "teams": Counter([p.team for p in players if hasattr(p, "team")])
    }
    
    # Actions analysis
    actions = replay.get("actions", [])
    result["actions"] = {
        "count": len(actions),
        "types": Counter([type(a).__name__ for a in actions])
    }
    
    # Statistics
    result["statistics"] = {
        "actions_per_second": len(actions) / (replay["duration"] / 60.0) if replay["duration"] > 0 else 0,
        "messages_per_minute": len(messages) / (replay["duration"] / 3600.0) if replay["duration"] > 0 else 0
    }
    
    return result


def print_analysis(result: dict):
    """Pretty print analysis results."""
    print(f"\n📊 Replay Analysis: {result['file']}")
    print(f"{'='*80}")
    
    print(f"\n📝 Metadata:")
    print(f"  Version: {result['version']}")
    print(f"  Duration: {result['duration_frames']} frames ({result['duration_seconds']:.1f}s)")
    
    print(f"\n📨 Messages:")
    print(f"  Count: {result['messages']['count']}")
    if result['messages']['types']:
        print(f"  Types: {dict(result['messages']['types'])}")
    
    print(f"\n🏟️  Room:")
    for key, value in result['room'].items():
        if key == 'stadium':
            print(f"  Stadium:")
            print(f"    Type: {value['type']}")
            print(f"    Name: {value['name']}")
            print(f"    Custom: {value['custom']}")
        else:
            print(f"  {key}: {value}")
    
    print(f"\n👥 Players:")
    print(f"  Count: {result['players']['count']}")
    if result['players']['teams']:
        print(f"  Teams: {dict(result['players']['teams'])}")
    
    print(f"\n🎮 Actions:")
    print(f"  Count: {result['actions']['count']}")
    if result['actions']['types']:
        print(f"  Types:")
        for action_type, count in sorted(result['actions']['types'].items(), key=lambda x: -x[1]):
            percentage = (count / result['actions']['count'] * 100) if result['actions']['count'] > 0 else 0
            print(f"    {action_type}: {count} ({percentage:.1f}%)")
    
    print(f"\n📈 Statistics:")
    print(f"  Actions/second: {result['statistics']['actions_per_second']:.2f}")
    print(f"  Messages/minute: {result['statistics']['messages_per_minute']:.2f}")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python analyze_replay_patterns.py <replay_file> [replay_file2 ...]")
        print("\nExample:")
        print("  python analyze_replay_patterns.py src/replays/LIRS/*.hbr2")
        sys.exit(1)
    
    results = []
    for replay_path in sys.argv[1:]:
        try:
            result = analyze_replay(replay_path)
            print_analysis(result)
            results.append(result)
        except Exception as e:
            print(f"❌ Error analyzing {replay_path}: {e}")
            import traceback
            traceback.print_exc()
    
    # Summary
    if len(results) > 1:
        print(f"\n{'='*80}")
        print(f"📊 Summary of {len(results)} replays")
        print(f"{'='*80}")
        
        total_actions = sum(r['actions']['count'] for r in results)
        total_duration = sum(r['duration_frames'] for r in results)
        
        print(f"Total actions: {total_actions}")
        print(f"Total duration: {total_duration} frames ({total_duration / 60.0:.1f}s)")
        print(f"Average actions/replay: {total_actions / len(results):.0f}")


if __name__ == "__main__":
    main()
