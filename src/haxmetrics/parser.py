from haxmetrics.models.replay_messages import ReplayMessages
from haxmetrics.models.room import Room
from haxmetrics.models.player import Player
from haxmetrics.models.team_color import TeamColor
from haxmetrics.models.action import Action
from haxmetrics.models.action_types import ACTION_TYPES
from haxmetrics.models.stadium.disc import Disc
from haxmetrics.binary_reader import BinaryReader
import zlib


class Parser:
    ACTION_TYPES = ACTION_TYPES

    def __init__(self, replay_data: bytes):
        self.reader = BinaryReader(replay_data)

        # Header fields are big-endian according to HaxBall format
        self.header = self.reader.read_fixed_string(4)
        self.version = self.reader.read_uint32_be()
        self.duration = self.reader.read_uint32_be()

        if self.header != "HBR2":
            raise Exception("Not a valid haxball replay!")

        self.replay = {
            "version": self.version,
            "duration": self.duration,
            "room_info": None,
            "messages": [],
            "discs": [],
            "players": [],
            "team_colors": {},
            "actions": [],
        }

    def parse(self):
        """
        Parse the replay file according to HaxBall original scripts structure.
        Order: messages -> room -> discs (if game active) -> players -> team colors -> actions
        """
        # 1. Descomprime el bloque principal
        decompressed_data = zlib.decompress(self.reader.get_input_string(), wbits=-15)
        print(f"First 500 bytes: {decompressed_data[:500].hex()}")
        reader = BinaryReader(decompressed_data)

        # 2. Parse messages (must be done before room)
        self.replay["messages"] = ReplayMessages.parse(reader)

        # 3. Parse room info
        self.replay["room_info"] = Room.parse(reader, self.version)

        # 4. Parse discs (only if game is active/playing)
        if self.replay["room_info"].is_playing():
            self.replay["discs"] = self.parse_discs(reader)
            print(f"Parsed {len(self.replay['discs'])} discs")

        # 5. Parse players (count is read as a byte)
        self.replay["players"] = self.parse_players(reader)
        print(f"Parsed {len(self.replay['players'])} players")
        print(f"Position after players: {reader.position}")

        # 6. Parse team colors (always parsed - these are defaults even with 0 players)
        self.replay["team_colors"] = self.parse_team_colors(reader)
        print(f"Position after team colors: {reader.position}")

        # 7. Parse actions
        self.replay["actions"] = self.parse_actions(reader)

        return self.replay

    def parse_discs(self, reader):
        """Parse discs from the replay. Count is a single byte (F() in original)."""
        discs = []
        num = reader.read_byte()
        for _ in range(num):
            discs.append(Disc.parse(reader))
        return discs

    def parse_players(self, reader):
        """
        Parse players from the replay. Count is a single byte (F() in original).
        
        Note: Player structure appears to differ between replay types.
        Some replays may have simplified player data or different field ordering.
        """
        players = []
        num = reader.read_byte()
        for i in range(num):
            try:
                players.append(Player.parse(reader, self.version))
            except Exception as e:
                print(f"Warning: Failed to parse player {i+1}/{num}: {e}")
                # Player parsing failed - this may indicate a structural difference
                # in how players are stored for certain replay types
                break
        return players

    def parse_team_colors(self, reader):
        """
        Parse team colors. May fail if prior parsing (players) consumed incorrect bytes.
        """
        try:
            return {"red": TeamColor.parse(reader), "blue": TeamColor.parse(reader)}
        except Exception as e:
            print(f"Warning: Failed to parse team colors: {e}")
            print(f"  This often indicates issues with prior parsing steps")
            # Return default team colors
            return {"red": None, "blue": None}

    def parse_actions(self, reader):
        """
        Parse actions from the replay according to HaxBall original scripts.
        Actions use big-endian for frame and sender IDs.
        """
        actions = []
        frame = 0
        print(f"Starting action parsing at position: {reader.position}")
        
        while not reader.eof():
            try:
                new_frame = reader.read_byte()
                if new_frame:
                    frame += reader.read_uint32_be()
                sender = reader.read_uint32_be()
                type_ = reader.read_byte()
                if type_ >= len(self.ACTION_TYPES):
                    print(f"Invalid action type {type_} at position {reader.position - 1}")
                    print(f"Remaining bytes: {reader.peek_bytes(20).hex()}")
                    # Stop parsing actions - likely means we're at wrong position
                    break
                cls = self.ACTION_TYPES[type_]
                action = cls.parse(reader)
                action.set_frame(frame).set_sender(sender)
                actions.append(action)
            except Exception as e:
                print(f"Warning: Failed to parse action at position {reader.position}: {e}")
                break
                
        return actions
