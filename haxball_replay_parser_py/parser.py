from haxball_replay_parser_py.models.room import Room
from haxball_replay_parser_py.models.player import Player
from haxball_replay_parser_py.models.team_color import TeamColor
from haxball_replay_parser_py.models.action import Action  # y tus subclases específicas
from binary_reader import BinaryReader

# from models.stadium.disc import Disc  # si tienes el modelo

import zlib


class Parser:
    ACTION_TYPES = [
        # Añade aquí tus clases Action específicas en el mismo orden que PHP
        # PlayerJoined, PlayerLeft, ChatMessage, etc.
    ]

    def __init__(self, replay_data: bytes):
        self.reader = BinaryReader(replay_data)
        self.version = self.reader.read_uint32_be()
        self.header = self.reader.read_string(4)
        self.frames = self.reader.read_uint32_be()

        if self.header != "HBRP":
            raise Exception("Not a valid haxball replay!")
        if self.version < 7:
            raise Exception("Replay must be at least version 7")

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
        decompressed_data = zlib.decompress(self.reader.get_input_string())
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
            # discs.append(Disc.parse(reader))  # Si tienes el modelo Disc
            discs.append(None)  # Placeholder
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
