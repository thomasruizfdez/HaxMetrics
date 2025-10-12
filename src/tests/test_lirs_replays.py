#!/usr/bin/env python3
import sys
sys.path.insert(0, '/home/runner/work/HaxMetrics/HaxMetrics/src')
import os
from haxmetrics.parser import Parser

lirs_dir = "/home/runner/work/HaxMetrics/HaxMetrics/src/replays/LIRS"
replay_files = sorted([f for f in os.listdir(lirs_dir) if f.endswith('.hbr2')])

print("=" * 80)
print("HaxBall LIRS Replay Parser Test Results")
print("=" * 80)
print()

total = len(replay_files)
success = 0

for replay_file in replay_files:
    filepath = os.path.join(lirs_dir, replay_file)
    try:
        with open(filepath, 'rb') as f:
            data = f.read()
        parser = Parser(data)
        replay = parser.parse()
        
        # Extract key info
        version = replay['version']
        duration = replay['duration']
        room_name = replay['room_info'].name if replay['room_info'] else "N/A"
        stadium_name = replay['room_info'].stadium.name if replay['room_info'] and replay['room_info'].stadium else "N/A"
        messages = len(replay['messages'])
        players = len(replay['players'])
        actions = len(replay['actions'])
        
        print(f"✓ {replay_file}")
        print(f"  Version: {version}, Duration: {duration} frames")
        print(f"  Room: {room_name}")
        print(f"  Stadium: {stadium_name}")
        print(f"  Messages: {messages}, Players: {players}, Actions: {actions}")
        print()
        
        success += 1
    except Exception as e:
        print(f"✗ {replay_file}")
        print(f"  Error: {str(e)}")
        print()

print("=" * 80)
print(f"Results: {success}/{total} replays parsed successfully ({100*success//total}%)")
print("=" * 80)

if success == total:
    print("\n✓ ALL LIRS REPLAYS PARSE SUCCESSFULLY!")
    print("\nNote: Action parsing is partial (5 actions per replay).")
    print("Further investigation needed for full action parsing.")
else:
    print(f"\n✗ {total - success} replay(s) failed to parse")

sys.exit(0 if success == total else 1)
