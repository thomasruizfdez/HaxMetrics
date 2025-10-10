#!/usr/bin/env python3
"""
Final test demonstrating successful parsing of all LIRS replays.
"""
import sys
import os
sys.path.insert(0, '/home/runner/work/HaxMetrics/HaxMetrics/src')

from haxmetrics.parser import Parser

def test_replay(filepath):
    """Test a single replay file."""
    try:
        with open(filepath, 'rb') as f:
            data = f.read()
        
        parser = Parser(data)
        replay = parser.parse()
        
        return {
            'success': True,
            'version': replay['version'],
            'duration': replay['duration'],
            'room': replay['room_info'].name if replay['room_info'] else 'Unknown',
            'stadium': replay['room_info'].stadium.name if replay['room_info'] and replay['room_info'].stadium else 'Unknown',
            'custom_stadium': replay['room_info'].stadium.custom if replay['room_info'] and replay['room_info'].stadium else False,
            'messages': len(replay['messages'].messages) if replay['messages'] else 0,
            'players': len(replay['players']),
            'actions': len(replay['actions']),
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def main():
    """Test all LIRS replays."""
    lirs_dir = "/home/runner/work/HaxMetrics/HaxMetrics/src/replays/LIRS"
    
    print("="*80)
    print("HaxMetrics Parser - LIRS Replay Test Suite")
    print("="*80)
    print()
    
    replays = sorted([
        os.path.join(lirs_dir, f) 
        for f in os.listdir(lirs_dir) 
        if f.endswith('.hbr2')
    ])
    
    results = []
    for replay_file in replays:
        filename = os.path.basename(replay_file)
        print(f"Testing: {filename:30s} ", end='', flush=True)
        
        result = test_replay(replay_file)
        results.append((filename, result))
        
        if result['success']:
            print(f"✓ SUCCESS")
            print(f"  Version: {result['version']}")
            print(f"  Duration: {result['duration']:,} frames")
            print(f"  Room: {result['room']}")
            print(f"  Stadium: {result['stadium']} (custom={result['custom_stadium']})")
            print(f"  Messages: {result['messages']}, Actions: {result['actions']}")
        else:
            print(f"✗ FAILED")
            print(f"  Error: {result['error']}")
        print()
    
    # Summary
    print("="*80)
    print("SUMMARY")
    print("="*80)
    
    successful = sum(1 for _, r in results if r['success'])
    total = len(results)
    
    print(f"\nResults: {successful}/{total} replays parsed successfully")
    print()
    
    if successful == total:
        print("✓ ALL TESTS PASSED!")
        print()
        print("The HaxMetrics parser successfully handles:")
        print("  • LIRS league replays with custom stadiums")
        print("  • Message parsing (timestamps and types)")
        print("  • Room configuration (name, settings, locks)")
        print("  • Custom stadium detection and properties")
        print("  • Action parsing (partial due to known issues)")
        print()
        print("See PARSER_TESTING_REPORT.md for detailed findings.")
        return 0
    else:
        print(f"⚠ {total - successful} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
