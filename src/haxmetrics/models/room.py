"""
HBR2 Room State Parser

This module contains parsers for room state information from HaxBall replays.
"""

from dataclasses import dataclass
from typing import Any, Dict

from haxmetrics.binary_reader import BinaryReader
from haxmetrics.models.game import Game
from haxmetrics.models.stadium.stadium import Stadium


@dataclass(frozen=True)
class RoomBasic:
    """
    Representa los campos básicos de configuración de una sala de HaxBall.

    Esta clase contiene solo los campos de configuración inicial,
    sin incluir stadium, game state, players ni team colors.

    Atributos:
        name (str): Nombre de la sala
        locked (bool): Si la sala está cerrada (True) o abierta (False)
        score_limit (int): Límite de puntuación (0 = sin límite)
        time_limit (int): Límite de tiempo en minutos (0 = sin límite)
        unknown_int16 (int): Campo desconocido (me en game-min.js)
        rules_type (int): Tipo de reglas (0 = default)
        unknown_byte (int): Campo desconocido (Gd en game-min.js)
    """

    name: str
    locked: bool
    score_limit: int
    time_limit: int
    unknown_int16: int
    rules_type: int
    unknown_byte: int

    def __post_init__(self):
        """Valida los datos de room basic."""
        if self.score_limit < 0:
            raise ValueError(
                f"Score limit must be non-negative, got {self.score_limit}"
            )

        if self.time_limit < 0:
            raise ValueError(
                f"Time limit must be non-negative, got {self.time_limit}"
            )

    @classmethod
    def parse(cls, reader: BinaryReader) -> "RoomBasic":
        """
        Parsea los campos básicos de room desde un BinaryReader.

        IMPORTANTE: El reader debe estar posicionado en la sección
        descomprimida del replay, justo después de Messages.

        Orden de parsing (según game-min.js línea 293-303):
        1. name: Ab() - read_string
        2. locked: F() - read_byte → bool (0=false, !0=true)
        3. score_limit: N() - read_uint32_be
        4. time_limit: N() - read_uint32_be
        5. unknown_int16: Di() - read_int16_be
        6. rules_type: F() - read_byte
        7. unknown_byte: F() - read_byte

        Args:
            reader: BinaryReader con datos descomprimidos

        Returns:
            RoomBasic: Instancia con los campos básicos parseados

        Ejemplo:
            >>> # Después de parsear messages
            >>> room_basic = RoomBasic.parse(reader)
            >>> print(room_basic.name)
            'My HaxBall Room'
        """
        # 1. Name (string)
        name = reader.read_string()
        if name is None:
            name = ""  # Tratar null como string vacío

        # 2. Locked (bool from byte)
        locked_byte = reader.read_byte()
        locked = locked_byte != 0

        # 3. Score limit (uint32_be)
        score_limit = reader.read_uint32_be()

        # 4. Time limit (uint32_be)
        time_limit = reader.read_uint32_be()

        # 5. Unknown int16 (int16_be)
        unknown_int16 = reader.read_int16_be()

        # 6. Rules type (byte)
        rules_type = reader.read_byte()

        # 7. Unknown byte (byte)
        unknown_byte = reader.read_byte()

        return cls(
            name=name,
            locked=locked,
            score_limit=score_limit,
            time_limit=time_limit,
            unknown_int16=unknown_int16,
            rules_type=rules_type,
            unknown_byte=unknown_byte,
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Serializa room basic a un diccionario.

        Returns:
            dict: Representación serializable
        """
        return {
            "name": self.name,
            "locked": self.locked,
            "score_limit": self.score_limit,
            "time_limit": self.time_limit,
            "unknown_int16": self.unknown_int16,
            "rules_type": self.rules_type,
            "unknown_byte": self.unknown_byte,
        }

    def __str__(self) -> str:
        """Representación legible de room basic."""
        lock_status = "🔒 Locked" if self.locked else "🔓 Open"
        limits = []
        if self.score_limit > 0:
            limits.append(f"Score: {self.score_limit}")
        if self.time_limit > 0:
            limits.append(f"Time: {self.time_limit}min")

        limits_str = f" ({', '.join(limits)})" if limits else ""

        return f"Room(name='{self.name}', {lock_status}{limits_str})"


class Room:
    def __init__(self, version: int):
        self.version = version

        self.kick_timeout = 2
        self.kick_rate_limit = 0
        self.kick_rate_limit_burst = 1

        self.score_limit = None
        self.time_limit = None

        self.teams_locked = None
        self.team_colors = None

        self.name = None

        self.game = None
        self.in_progress = False

        self.players = None
        self.stadium = None

    @classmethod
    def parse(cls, reader, version):
        """
        Parse room info from binary data according to HaxBall original scripts.
        The structure follows the ma(a) method from the original code.
        This includes players and team colors as they're part of the state.
        """
        room = cls(version)

        # 1. Room name (string with varint length)
        room.set_name(reader.read_string())

        # 2. Teams locked (1 byte)
        room.set_locked(reader.read_byte())

        # 3. Score limit (4 bytes, big-endian)
        room.set_score_limit(reader.read_uint32_be())

        # 4. Time limit (4 bytes, big-endian)
        room.set_time_limit(reader.read_uint32_be())

        # 5. Kick rate limit burst (2 bytes, big-endian)
        room.kick_rate_limit_burst = reader.read_uint16_be()

        # 6. Kick rate limit (1 byte)
        room.kick_rate_limit = reader.read_byte()

        # 7. Kick timeout (1 byte)
        room.kick_timeout = reader.read_byte()

        # 8. Stadium
        room.set_stadium(Stadium.parse(reader))

        # 9. Game active flag (1 byte)
        game_active = reader.read_byte() != 0

        # 10. If game is active, parse game state (including discs)
        if game_active:
            room.set_in_progress(True)
            room.game = Game.parse(reader, room)
            print(f"Game is active - parsed game state at frame {room.game.frame}")
        else:
            room.set_in_progress(False)

        # 11. Parse players (count + player data)
        # According to original script ma() method, players are part of the state
        from haxmetrics.models.player import Player

        room.players = []
        player_count = reader.read_byte()
        print(f"Player count: {player_count}")
        for i in range(player_count):
            try:
                player = Player.parse(reader, version)
                room.players.append(player)
            except Exception as e:
                print(f"Warning: Failed to parse player {i+1}/{player_count}: {e}")
                break

        # 12. Parse team colors (red and blue)
        # According to original script ma() method: this.mb[1].ma(a); this.mb[2].ma(a)
        from haxmetrics.models.team_color import TeamColor

        room.team_colors = {
            "red": TeamColor.parse(reader),
            "blue": TeamColor.parse(reader),
        }

        return room

    def json_serialize(self) -> Dict[str, Any]:
        return {
            "frame": self.frame,
            "name": self.name,
            "locked": bool(self.locked),
            "scoreLimit": self.score_limit,
            "timeLimit": self.time_limit,
            "rulesTimer": self.rules_timer,
            "kickOffTaken": bool(self.kick_off_taken),
            "kickOffTeam": self.kick_off_team,
            "ball": {"x": self.ball_x, "y": self.ball_y},
            "score": {"red": self.score_red, "blue": self.score_blue},
            "matchTime": self.match_time,
            "pauseTimer": self.pause_timer,
            "stadium": self.stadium,  # Should be serialized if implemented
            "inProgress": bool(self.in_progress),
        }

    # Setters and Getters
    def set_frame(self, frame):
        self.frame = int(frame)
        return self

    def get_frame(self):
        return self.frame

    def set_name(self, name):
        self.name = str(name)
        return self

    def get_name(self):
        return self.name

    def set_locked(self, status):
        self.locked = bool(status)
        return self

    def get_locked(self):
        return self.locked

    def set_score_limit(self, limit):
        self.score_limit = int(limit)
        return self

    def get_score_limit(self):
        return self.score_limit

    def set_time_limit(self, limit):
        self.time_limit = int(limit)
        return self

    def get_time_limit(self):
        return self.time_limit

    def set_rules_timer(self, rules_timer):
        self.rules_timer = int(rules_timer)
        return self

    def get_rules_timer(self):
        return self.rules_timer

    def set_kick_off_taken(self, state):
        self.kick_off_taken = bool(state)
        return self

    def get_kick_off_taken(self):
        return self.kick_off_taken

    def set_kick_off_team(self, team):
        self.kick_off_team = str(team)
        return self

    def get_kick_off_team(self):
        return self.kick_off_team

    def set_ball_x(self, pos):
        self.ball_x = float(pos)
        return self

    def get_ball_x(self):
        return self.ball_x

    def set_ball_y(self, pos):
        self.ball_y = float(pos)
        return self

    def get_ball_y(self):
        return self.ball_y

    def set_score_red(self, score):
        self.score_red = int(score)
        return self

    def get_score_red(self):
        return self.score_red

    def set_score_blue(self, score):
        self.score_blue = int(score)
        return self

    def get_score_blue(self):
        return self.score_blue

    def set_match_time(self, timer):
        self.match_time = float(timer)
        return self

    def get_match_time(self):
        return self.match_time

    def set_pause_timer(self, timer):
        # version 8 special handling could be implemented here
        self.pause_timer = bool(timer) if self.version == 8 else int(timer)
        return self

    def get_pause_timer(self):
        return self.pause_timer

    def set_stadium(self, stadium):
        self.stadium = stadium
        return self

    def get_stadium(self):
        return self.stadium

    def set_in_progress(self, state):
        self.in_progress = bool(state)
        return self

    def get_in_progress(self):
        return self.in_progress

    def is_playing(self):
        return bool(self.in_progress)
