# haxmetrics/models/replay_messages.py

import struct
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass


@dataclass
class ReplayMessage:
    """Representa un mensaje dentro del replay de HaxBall"""

    index: int
    delta_time: int
    type: int
    data: Any = None


class MessageType:
    """
    Constantes para los tipos de mensajes en replays de HaxBall
    basados en el código fuente original
    """

    ANNOUNCEMENT = 0  # Mensaje de anuncio del sistema
    CHAT = 1  # Mensaje de chat de jugador
    GOAL = 2  # Gol anotado
    TEAM_GOAL = 3  # Gol de equipo
    GAME_START = 4  # Inicio del juego
    GAME_STOP = 5  # Fin del juego
    PLAYER_JOIN = 6  # Jugador se une
    PLAYER_LEAVE = 7  # Jugador se va
    PLAYER_TEAM_CHANGE = 8  # Cambio de equipo
    PAUSE = 9  # Juego pausado
    UNPAUSE = 10  # Juego reanudado
    ADMIN_CHANGE = 11  # Cambio de admin
    STADIUM_CHANGE = 12  # Cambio de estadio
    KICK = 13  # Jugador expulsado
    POSITION_CHANGE = 14  # Cambio de posición

    @staticmethod
    def get_name(type_id: int) -> str:
        """Devuelve el nombre del tipo de mensaje"""
        types = {
            0: "ANNOUNCEMENT",
            1: "CHAT",
            2: "GOAL",
            3: "TEAM_GOAL",
            4: "GAME_START",
            5: "GAME_STOP",
            6: "PLAYER_JOIN",
            7: "PLAYER_LEAVE",
            8: "PLAYER_TEAM_CHANGE",
            9: "PAUSE",
            10: "UNPAUSE",
            11: "ADMIN_CHANGE",
            12: "STADIUM_CHANGE",
            13: "KICK",
            14: "POSITION_CHANGE",
        }
        return types.get(type_id, f"UNKNOWN_{type_id}")


class ReplayMessages:
    """
    Clase para parsear y representar los mensajes al inicio de un replay HaxBall
    después de la cabecera y la descompresión.
    """

    def __init__(self):
        self.count: int = 0
        self.messages: List[ReplayMessage] = []
        self.end_position: int = 0  # Posición después del último mensaje

    def __len__(self) -> int:
        """Return the number of messages for len() support"""
        return len(self.messages)

    def __iter__(self):
        """Make the class iterable"""
        return iter(self.messages)

    def __getitem__(self, index):
        """Allow indexing"""
        return self.messages[index]

    @classmethod
    def parse(cls, data) -> "ReplayMessages":
        """
        Parsea los mensajes desde datos binarios descomprimidos.

        Args:
            data: Objeto DataReader posicionado al comienzo de la sección de mensajes

        Returns:
            ReplayMessages: Objeto con los mensajes parseados
        """
        messages = cls()

        # 1. Leer contador de mensajes (2 bytes big-endian)
        messages.count = data.read_uint16_be()

        # 2. Leer cada mensaje
        for i in range(messages.count):
            # Leer delta tiempo (VarInt)
            delta_time = data.read_varint()

            # Leer tipo de mensaje
            msg_type = data.read_uint8()

            # Leer datos adicionales según el tipo
            msg_data = cls._parse_message_data(data, msg_type)

            # Crear y añadir el mensaje
            message = ReplayMessage(
                index=i, delta_time=delta_time, type=msg_type, data=msg_data
            )
            messages.messages.append(message)

        # Guardar la posición actual para saber dónde termina la sección de mensajes
        messages.end_position = data.position

        print(f"Parsed {messages.count} messages")
        print(f"End position after messages: {messages.end_position}")
        print(f"Message details:")
        for msg in messages.messages:
            print(f" - Message {msg.index}: {MessageType.get_name(msg.type)}")

        return messages

    @staticmethod
    def _parse_message_data(data, msg_type) -> Dict[str, Any]:
        """
        Parse message metadata. In HaxBall replays, messages only store the type
        and timestamp - the actual data (player names, text, etc.) is reconstructed
        from the actions during playback.
        
        Args:
            data: Objeto DataReader posicionado justo después del tipo de mensaje
            msg_type: Tipo de mensaje

        Returns:
            Dict: Empty dict or minimal metadata for the message type
        """
        # Messages in replays don't store their full data, only the type
        # The data is reconstructed from actions during playback
        return {"type": msg_type}
