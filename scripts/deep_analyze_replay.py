#!/usr/bin/env python3
"""
Deep analysis script for replay files to debug player parsing.
"""

import sys
import zlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from haxmetrics.binary_reader import BinaryReader


def analyze_replay_structure(replay_path: str):
    """Analyze replay structure in detail."""
    print(f"\n{'='*80}")
    print(f"Deep Analysis: {replay_path}")
    print(f"{'='*80}\n")
    
    with open(replay_path, "rb") as f:
        data = f.read()
    
    reader = BinaryReader(data)
    
    # Header
    magic = reader.read_fixed_string(4)
    version = reader.read_uint32_be()
    duration = reader.read_uint32_be()
    
    print(f"Header:")
    print(f"  Magic: {magic}")
    print(f"  Version: {version}")
    print(f"  Duration: {duration} frames")
    
    # Decompress body
    compressed = reader.get_input_string()
    decompressed = zlib.decompress(compressed, wbits=-15)
    print(f"\nDecompressed: {len(decompressed)} bytes")
    
    reader = BinaryReader(decompressed)
    
    # Messages
    msg_count = reader.read_uint16_be()
    print(f"\nMessages: {msg_count}")
    
    for i in range(msg_count):
        delta = reader.read_varint()
        msg_type = reader.read_byte()
        print(f"  Message {i}: delta={delta}, type={msg_type}")
    
    print(f"\nPosition after messages: {reader.position}")
    
    # Room state
    print(f"\n--- Room State ---")
    name = reader.read_string()
    print(f"Room name: '{name}'")
    
    teams_locked = reader.read_byte()
    print(f"Teams locked: {teams_locked}")
    
    score_limit = reader.read_uint32_be()
    time_limit = reader.read_uint32_be()
    print(f"Limits: score={score_limit}, time={time_limit}")
    
    kick_burst = reader.read_uint16_be()
    kick_rate = reader.read_byte()
    kick_timeout = reader.read_byte()
    print(f"Kick: burst={kick_burst}, rate={kick_rate}, timeout={kick_timeout}")
    
    # Stadium
    stadium_type = reader.read_byte()
    print(f"\nStadium type: 0x{stadium_type:02X} ({stadium_type})")
    
    if stadium_type == 0xFF:
        stadium_name = reader.read_string()
        print(f"Custom stadium: '{stadium_name}'")
        
        # Skip stadium data to get to game_active byte
        # We need to parse the stadium structure
        bg_type = reader.read_byte()
        bg_width = reader.read_double_be()
        bg_height = reader.read_double_be()
        max_view_width = reader.read_double_be()
        max_view_height = reader.read_double_be()
        spawn_distance = reader.read_double_be()
        
        # Player physics
        p_bcoef = reader.read_double_be()
        p_accel = reader.read_double_be()
        p_kick = reader.read_double_be()
        
        # Additional fields
        max_view_override = reader.read_nullable_int32()
        camera_follow = reader.read_uint8()
        can_be_stored = reader.read_uint8()
        full_reset = reader.read_uint8()
        
        # Arrays
        vertex_count = reader.read_byte()
        print(f"  Vertices: {vertex_count}")
        # Skip vertices (each is 32 bytes)
        for _ in range(vertex_count):
            reader.read_bytes(32)
        
        segment_count = reader.read_byte()
        print(f"  Segments: {segment_count}")
        # Skip segments (variable size, need to parse)
        for _ in range(segment_count):
            # v0, v1
            reader.read_byte()
            reader.read_byte()
            # bcoef, cmask
            reader.read_double_be()
            reader.read_double_be()
            # color (nullable)
            color_present = reader.read_byte()
            if color_present:
                reader.read_int32()
            # vis, curve_flag
            reader.read_byte()
            curve_flag = reader.read_byte()
            if curve_flag:
                reader.read_double_be()
        
        # Planes
        plane_count = reader.read_byte()
        print(f"  Planes: {plane_count}")
        for _ in range(plane_count):
            reader.read_bytes(40)  # 5 doubles
        
        # Goals
        goal_count = reader.read_byte()
        print(f"  Goals: {goal_count}")
        for _ in range(goal_count):
            reader.read_bytes(33)  # 4 doubles + 1 byte
        
        # Discs
        disc_count = reader.read_byte()
        print(f"  Discs: {disc_count}")
        for _ in range(disc_count):
            # x, y, radius, bcoef, invMass, damping
            reader.read_bytes(48)
            # color (nullable)
            color_present = reader.read_byte()
            if color_present:
                reader.read_int32()
            # cMask, cGroup
            reader.read_bytes(16)
        
        # Joints
        joint_count = reader.read_byte()
        print(f"  Joints: {joint_count}")
        for _ in range(joint_count):
            reader.read_byte()  # d0
            reader.read_byte()  # d1
            # length (nullable)
            length_present = reader.read_byte()
            if length_present:
                reader.read_double_be()
            # color (nullable)
            color_present = reader.read_byte()
            if color_present:
                reader.read_int32()
            # strength (nullable)
            strength_present = reader.read_byte()
            if strength_present:
                reader.read_double_be()
    
    print(f"\nPosition after stadium: {reader.position}")
    
    # Game active
    game_active = reader.read_byte()
    print(f"\nGame active: {game_active}")
    
    if game_active:
        print("  (Parsing game state...)")
        # Skip game state for now
        frame = reader.read_uint32_be()
        score_red = reader.read_byte()
        score_blue = reader.read_byte()
        match_time = reader.read_double_be()
        print(f"  Frame: {frame}, Score: {score_red}-{score_blue}, Time: {match_time}")
        
        # Has pause
        has_pause = reader.read_byte()
        if has_pause:
            reader.read_double_be()
        
        # Has kickoff
        has_kickoff = reader.read_byte()
        if has_kickoff:
            reader.read_byte()
        
        kickoff_taken = reader.read_byte()
        
        # Has rules timer
        has_rules = reader.read_byte()
        if has_rules:
            reader.read_double_be()
        
        # Ball position
        ball_x = reader.read_double_be()
        ball_y = reader.read_double_be()
        
        # Discs
        disc_count = reader.read_byte()
        print(f"  Discs in game: {disc_count}")
        for _ in range(disc_count):
            reader.read_bytes(32)  # x, y, vx, vy
    
    print(f"Position after game state: {reader.position}")
    
    # Players
    player_count = reader.read_byte()
    print(f"\nPlayer count: {player_count}")
    print(f"Position at player count: {reader.position}")
    
    # Show next 100 bytes as hex
    print(f"\nNext 100 bytes (hex):")
    next_bytes = decompressed[reader.position:reader.position+100]
    for i in range(0, min(100, len(next_bytes)), 16):
        hex_str = ' '.join(f'{b:02x}' for b in next_bytes[i:i+16])
        ascii_str = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in next_bytes[i:i+16])
        print(f"  {reader.position+i:04x}: {hex_str:<48}  {ascii_str}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python deep_analyze_replay.py <replay_file>")
        sys.exit(1)
    
    analyze_replay_structure(sys.argv[1])
