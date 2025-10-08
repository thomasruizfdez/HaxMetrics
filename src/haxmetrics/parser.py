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
        self.header = self.reader.read_string(4)
        self.version = self.reader.read_uint32_be()
        self.frames = self.reader.read_uint32_be()

        if self.header != "HBR2":
            raise Exception("Not a valid haxball replay!")

        self.replay = {
            "version": self.version,
            "frames": self.frames,
            "room_info": None,
            "discs": [],
            "players": [],
            "team_colors": {},
            "actions": [],
        }

    def parse(self):
        # 1. Descomprime el bloque principal
        decompressed_data = zlib.decompress(self.reader.get_input_string(), wbits=-15)
        print(f"First 500 bytes: {decompressed_data[:500]}")
        reader = BinaryReader(decompressed_data)

        # 2. Room info
        self.replay["room_info"] = Room.parse(reader, self.version)

        # 3. Discs (si corresponde)
        if self.replay["room_info"].is_playing():
            self.replay["discs"] = self.parse_discs(reader)

        # 4. Players
        self.replay["players"] = self.parse_players(reader)

        # 5. Team colors (si versión >= 12)
        if self.version >= 12:
            self.replay["team_colors"] = self.parse_team_colors(reader)

        # 6. Actions
        self.replay["actions"] = self.parse_actions(reader)

        return self.replay

    def parse_discs(self, reader):
        discs = []
        num = reader.read_uint32_be()
        for _ in range(num):
            discs.append(Disc.parse(reader))
        return discs

    def parse_players(self, reader):
        players = []
        num = reader.read_uint32_be()
        for _ in range(num):
            players.append(Player.parse(reader, self.version))
        return players

    def parse_team_colors(self, reader):
        return {"red": TeamColor.parse(reader), "blue": TeamColor.parse(reader)}

    def parse_actions(self, reader):
        actions = []
        frame = 0
        while not reader.eof():
            new_frame = reader.read_uint8()
            if new_frame:
                frame += reader.read_uint32_be()
            sender = reader.read_uint32_be()
            type_ = reader.read_uint8()
            if type_ >= len(self.ACTION_TYPES):
                raise Exception(f"Action type {type_} invalid")
            cls = self.ACTION_TYPES[type_]
            action = cls.parse(reader)
            action.set_frame(frame).set_sender(sender)
            actions.append(action)
        return actions
