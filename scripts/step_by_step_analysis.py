#!/usr/bin/env python3
"""
Análisis paso a paso de la decodificación del replay, comparando con game-min.js.
"""

import sys
import zlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from haxmetrics.binary_reader import BinaryReader


def show_bytes(data, start, count, label=""):
    """Muestra bytes en formato hex."""
    if label:
        print(f"\n{label}:")
    for i in range(start, min(start + count, len(data)), 16):
        hex_str = ' '.join(f'{b:02x}' for b in data[i:i+16])
        ascii_str = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in data[i:i+16])
        print(f"  {i:04x}: {hex_str:<48}  {ascii_str}")


def analyze_step_by_step(replay_path: str):
    """Análisis paso a paso del replay."""
    
    print("="*80)
    print("ANÁLISIS PASO A PASO DE REPLAY")
    print("="*80)
    
    with open(replay_path, "rb") as f:
        data = f.read()
    
    reader = BinaryReader(data)
    
    # ========== HEADER ==========
    print("\n" + "="*80)
    print("1. HEADER (12 bytes sin comprimir)")
    print("="*80)
    
    magic = reader.read_fixed_string(4)
    version = reader.read_uint32_be()
    duration = reader.read_uint32_be()
    
    print(f"Magic: '{magic}' ✓")
    print(f"Version: {version} ✓")
    print(f"Duration: {duration} frames ({duration/60:.1f}s) ✓")
    print(f"Position after header: {reader.position}")
    
    # ========== DECOMPRESS ==========
    print("\n" + "="*80)
    print("2. BODY (comprimido con zlib)")
    print("="*80)
    
    compressed = reader.get_input_string()
    decompressed = zlib.decompress(compressed, wbits=-15)
    
    print(f"Compressed size: {len(compressed)} bytes")
    print(f"Decompressed size: {len(decompressed)} bytes")
    print(f"Compression ratio: {len(decompressed)/len(compressed):.2f}x")
    
    reader = BinaryReader(decompressed)
    
    # ========== MESSAGES ==========
    print("\n" + "="*80)
    print("3. MESSAGES")
    print("="*80)
    print(f"Position: {reader.position}")
    
    msg_count = reader.read_uint16_be()
    print(f"Message count: {msg_count}")
    
    for i in range(msg_count):
        pos_before = reader.position
        delta = reader.read_varint()
        msg_type = reader.read_byte()
        print(f"  Message {i}: delta={delta}, type={msg_type} (consumed {reader.position - pos_before} bytes)")
    
    print(f"Position after messages: {reader.position}")
    
    # ========== ROOM STATE ==========
    print("\n" + "="*80)
    print("4. ROOM STATE")
    print("="*80)
    
    # Room name
    pos_before = reader.position
    room_name = reader.read_string()
    print(f"4.1. Room name: '{room_name}' (consumed {reader.position - pos_before} bytes)")
    
    # Teams locked
    pos_before = reader.position
    teams_locked = reader.read_byte()
    print(f"4.2. Teams locked: {teams_locked} (consumed {reader.position - pos_before} bytes)")
    
    # Score limit
    pos_before = reader.position
    score_limit = reader.read_uint32_be()
    print(f"4.3. Score limit: {score_limit} (consumed {reader.position - pos_before} bytes)")
    
    # Time limit
    pos_before = reader.position
    time_limit = reader.read_uint32_be()
    print(f"4.4. Time limit: {time_limit} (consumed {reader.position - pos_before} bytes)")
    
    # Kick settings
    pos_before = reader.position
    kick_burst = reader.read_uint16_be()
    kick_rate = reader.read_byte()
    kick_timeout = reader.read_byte()
    print(f"4.5. Kick: burst={kick_burst}, rate={kick_rate}, timeout={kick_timeout} (consumed {reader.position - pos_before} bytes)")
    
    # Stadium
    print(f"\n4.6. STADIUM (position: {reader.position})")
    pos_before = reader.position
    stadium_type = reader.read_byte()
    print(f"  Stadium type: 0x{stadium_type:02x} ({stadium_type})")
    
    if stadium_type == 0:
        print(f"  -> Predefined stadium (Classic)")
    elif stadium_type == 0xFF:
        print(f"  -> Custom stadium")
        # Parse custom stadium name
        stadium_name = reader.read_string()
        print(f"  Stadium name: '{stadium_name}'")
        # Skip rest of stadium parsing for now
    
    print(f"  Stadium consumed {reader.position - pos_before} bytes")
    print(f"  Position after stadium: {reader.position}")
    
    # Game active
    print(f"\n4.7. GAME ACTIVE (position: {reader.position})")
    pos_before = reader.position
    game_active = reader.read_byte()
    print(f"  Game active: {game_active} ({'YES' if game_active else 'NO'})")
    print(f"  Consumed {reader.position - pos_before} bytes")
    
    if game_active:
        print(f"\n4.8. GAME STATE (position: {reader.position})")
        game_start_pos = reader.position
        
        # Según game-min.js: Y.ma() llama primero a this.va.ma(a)
        # que es Sa.ma() que parsea los discos
        
        print(f"  4.8.1. DISC COUNT")
        pos_before = reader.position
        disc_count = reader.read_byte()
        print(f"    Disc count: {disc_count}")
        print(f"    Consumed {reader.position - pos_before} bytes")
        print(f"    Position: {reader.position}")
        
        # Parse each disc
        print(f"\n  4.8.2. DISCS (parsing {disc_count} discs)")
        for i in range(disc_count):
            disc_start = reader.position
            print(f"    Disc {i} (starts at position {disc_start}):")
            
            # According to qa.ma():
            # b.x = a.w(); b.y = a.w(); (position)
            x = reader.read_double_be()
            y = reader.read_double_be()
            print(f"      Position: ({x:.2f}, {y:.2f})")
            
            # b.x = a.w(); b.y = a.w(); (velocity)
            vx = reader.read_double_be()
            vy = reader.read_double_be()
            print(f"      Velocity: ({vx:.2f}, {vy:.2f})")
            
            # b.x = a.w(); b.y = a.w(); (ra)
            ra_x = reader.read_double_be()
            ra_y = reader.read_double_be()
            print(f"      Ra: ({ra_x:.2f}, {ra_y:.2f})")
            
            # this.V = a.w(); (radius)
            radius = reader.read_double_be()
            print(f"      Radius: {radius:.2f}")
            
            # this.o = a.w(); (bcoef)
            bcoef = reader.read_double_be()
            print(f"      Bcoef: {bcoef:.2f}")
            
            # this.ca = a.w(); (inv_mass)
            inv_mass = reader.read_double_be()
            print(f"      Inv mass: {inv_mass:.2f}")
            
            # this.Ea = a.w(); (damping)
            damping = reader.read_double_be()
            print(f"      Damping: {damping:.4f}")
            
            # this.S = a.jb(); (color - uint32 NOT nullable)
            color = reader.read_uint32_be()
            print(f"      Color: 0x{color:08x}")
            
            # this.i = a.N(); this.B = a.N(); (collision masks)
            c_mask = reader.read_int32()
            c_group = reader.read_int32()
            print(f"      Collision: mask={c_mask}, group={c_group}")
            
            disc_end = reader.position
            print(f"      Disc {i} consumed {disc_end - disc_start} bytes")
        
        print(f"\n  4.8.3. GAME FIELDS (position: {reader.position})")
        
        # Según Y.ma() después de this.va.ma(a):
        # this.yc = a.N();
        yc = reader.read_int32()
        print(f"    yc: {yc}")
        
        # this.Cb = a.N();
        cb = reader.read_int32()
        print(f"    Cb: {cb}")
        
        # this.Tb = a.N();
        tb = reader.read_int32()
        print(f"    Tb (score_red): {tb}")
        
        # this.Ob = a.N();
        ob = reader.read_int32()
        print(f"    Ob (score_blue): {ob}")
        
        # this.Nc = a.w();
        nc = reader.read_double_be()
        print(f"    Nc (match_time): {nc:.2f}")
        
        # this.Ta = a.N();
        ta = reader.read_int32()
        print(f"    Ta: {ta}")
        
        # a = a.zf(); (signed byte)
        ke = reader.read_byte()
        ke_signed = ke if ke < 128 else ke - 256
        print(f"    ke: {ke_signed}")
        
        game_end_pos = reader.position
        print(f"\n  Game state consumed {game_end_pos - game_start_pos} bytes")
        print(f"  Position after game state: {reader.position}")
    
    # ========== PLAYERS ==========
    print("\n" + "="*80)
    print("5. PLAYERS")
    print("="*80)
    print(f"Position: {reader.position}")
    
    player_count = reader.read_byte()
    print(f"Player count: {player_count}")
    
    show_bytes(decompressed, reader.position, 80, "Next 80 bytes")
    
    for i in range(player_count):
        print(f"\n  Player {i} (starts at position {reader.position}):")
        player_start = reader.position
        
        # Según ua.xa(a, b):
        # this.fb = 0 != a.F();
        admin = reader.read_byte() != 0
        print(f"    Admin: {admin}")
        
        # this.Nb = a.N();
        # ¡IMPORTANTE! Verificar si es big-endian o little-endian
        print(f"    Next 4 bytes (player_id): {' '.join(f'{decompressed[reader.position+j]:02x}' for j in range(4))}")
        # Probar primero con big-endian
        player_id = reader.read_uint32_be()
        print(f"    Player ID (big-endian): {player_id}")
        
        # this.Zb = a.Ab();
        avatar = reader.read_string()
        print(f"    Avatar: '{avatar}'")
        
        # this.Sd = a.Ab();
        unknown_str = reader.read_string()
        print(f"    Unknown str: '{unknown_str}'")
        
        # this.Td = 0 != a.F();
        unknown_flag = reader.read_byte() != 0
        print(f"    Unknown flag: {unknown_flag}")
        
        # this.country = a.Ab();
        country = reader.read_string()
        print(f"    Country: '{country}'")
        
        # this.gh = a.N();
        unknown_int = reader.read_int32()
        print(f"    Unknown int: {unknown_int}")
        
        # this.D = a.Ab();
        name = reader.read_string()
        print(f"    Name: '{name}'")
        
        # this.W = a.N();
        input_state = reader.read_int32()
        print(f"    Input state: {input_state}")
        
        # this.Z = a.Bb(); - int16
        unknown_int16 = reader.read_int16()
        print(f"    Unknown int16: {unknown_int16}")
        
        # this.Yb = 0 != a.F();
        kicking = reader.read_byte() != 0
        print(f"    Kicking: {kicking}")
        
        # this.Bc = a.Di(); - int16
        unknown_int16_2 = reader.read_int16()
        print(f"    Unknown int16_2: {unknown_int16_2}")
        
        # this.Zc = a.F();
        unknown_byte = reader.read_byte()
        print(f"    Unknown byte: {unknown_byte}")
        
        # let c = a.zf(); - signed byte (team)
        team_byte = reader.read_byte()
        team_signed = team_byte if team_byte < 128 else team_byte - 256
        print(f"    Team: {team_signed}")
        
        # a = a.Di(); - int16 (disc_id)
        disc_id = reader.read_int16()
        print(f"    Disc ID: {disc_id}")
        
        player_end = reader.position
        print(f"    Player {i} consumed {player_end - player_start} bytes")
    
    print(f"\nPosition after players: {reader.position}")
    
    # ========== TEAM COLORS ==========
    print("\n" + "="*80)
    print("6. TEAM COLORS")
    print("="*80)
    print(f"Position: {reader.position}")
    print(f"Remaining bytes: {len(decompressed) - reader.position}")
    
    show_bytes(decompressed, reader.position, 80, "Next 80 bytes")
    
    # this.mb[1].ma(a); - red team
    # According to ta.ma() in game-min.js:
    # this.sd = a.F(); - angle is a BYTE
    # this.pd = a.N(); - text color is uint32_be
    # let b = a.F(); - num stripes is a BYTE
    # this.hb.push(a.N()); - each stripe is uint32_be
    print("\n  Red team:")
    angle = reader.read_byte()  # FIX: Changed from read_uint32_be()
    print(f"    Angle: {angle}")
    text_color = reader.read_uint32_be()
    print(f"    Text color: 0x{text_color:08x}")
    num_stripes = reader.read_byte()
    print(f"    Num stripes: {num_stripes}")
    if num_stripes > 3:
        print(f"    WARNING: Invalid num_stripes {num_stripes} (max 3)")
        num_stripes = 0
    for j in range(num_stripes):
        stripe_color = reader.read_uint32_be()
        print(f"      Stripe {j}: 0x{stripe_color:08x}")
    
    # this.mb[2].ma(a); - blue team
    print("\n  Blue team:")
    angle = reader.read_byte()  # FIX: Changed from read_uint32_be()
    print(f"    Angle: {angle}")
    text_color = reader.read_uint32_be()
    print(f"    Text color: 0x{text_color:08x}")
    num_stripes = reader.read_byte()
    print(f"    Num stripes: {num_stripes}")
    if num_stripes > 3:
        print(f"    WARNING: Invalid num_stripes {num_stripes} (max 3)")
        num_stripes = 0
    for j in range(num_stripes):
        stripe_color = reader.read_uint32_be()
        print(f"      Stripe {j}: 0x{stripe_color:08x}")
    
    print(f"\nPosition after team colors: {reader.position}")
    
    # ========== ACTIONS ==========
    print("\n" + "="*80)
    print("7. ACTIONS")
    print("="*80)
    print(f"Position: {reader.position}")
    print(f"Remaining bytes: {len(decompressed) - reader.position}")
    
    show_bytes(decompressed, reader.position, min(80, len(decompressed) - reader.position), "Next bytes")
    
    print("\n" + "="*80)
    print("ANÁLISIS COMPLETADO")
    print("="*80)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python step_by_step_analysis.py <replay_file>")
        sys.exit(1)
    
    analyze_step_by_step(sys.argv[1])
