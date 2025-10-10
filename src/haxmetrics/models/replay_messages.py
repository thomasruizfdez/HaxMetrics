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
        Parsea los datos adicionales de un mensaje según su tipo de manera determinista.
        Basado en el análisis del código fuente de HaxBall.

        Args:
            data: Objeto DataReader posicionado justo después del tipo de mensaje
            msg_type: Tipo de mensaje

        Returns:
            Dict: Datos parseados específicos para el tipo de mensaje
        """
        if msg_type == MessageType.ANNOUNCEMENT:
            # Mensaje del sistema
            return {
                "text": data.read_string(),
                "color": data.read_int32(),
                "style": data.read_uint8(),
                "sound": data.read_uint8(),
            }

        elif msg_type == MessageType.CHAT:
            # Mensaje de chat
            return {"player_id": data.read_int32(), "message": data.read_string()}

        elif msg_type == MessageType.GOAL:
            # Gol anotado
            return {
                "player_id": data.read_int32(),
                "team": data.read_uint8(),  # 1 = rojo, 2 = azul
            }

        elif msg_type == MessageType.TEAM_GOAL:
            # Gol de equipo
            return {"team": data.read_uint8()}  # 1 = rojo, 2 = azul

        elif msg_type == MessageType.GAME_START:
            # Inicio del juego
            return {"admin_id": data.read_int32() if data.read_uint8() != 0 else None}

        elif msg_type == MessageType.GAME_STOP:
            # Fin del juego
            return {"admin_id": data.read_int32() if data.read_uint8() != 0 else None}

        elif msg_type == MessageType.PLAYER_JOIN:
            # Jugador se une
            return {
                "player_id": data.read_int32(),
                "name": data.read_string(),
                "country": data.read_string(),
                "avatar": data.read_string(),
            }

        elif msg_type == MessageType.PLAYER_LEAVE:
            # Jugador se va
            return {
                "player_id": data.read_int32(),
                "reason": data.read_string(),
                "banned": data.read_uint8() != 0,
                "admin_id": data.read_int32() if data.read_uint8() != 0 else None,
            }

        elif msg_type == MessageType.PLAYER_TEAM_CHANGE:
            # Cambio de equipo
            return {
                "player_id": data.read_int32(),
                "team": data.read_uint8(),  # 0 = espectador, 1 = rojo, 2 = azul
                "admin_id": data.read_int32() if data.read_uint8() != 0 else None,
            }

        elif msg_type == MessageType.PAUSE:
            # Juego pausado
            return {
                "admin_id": data.read_int32() if data.read_uint8() != 0 else None,
                "is_paused": data.read_uint8() != 0,
                "by_game": data.read_uint8() != 0,
            }

        elif msg_type == MessageType.UNPAUSE:
            # Juego reanudado
            return {"admin_id": data.read_int32() if data.read_uint8() != 0 else None}

        elif msg_type == MessageType.ADMIN_CHANGE:
            # Cambio de admin
            return {
                "player_id": data.read_int32(),
                "is_admin": data.read_uint8() != 0,
                "by_player_id": data.read_int32() if data.read_uint8() != 0 else None,
            }

        elif msg_type == MessageType.STADIUM_CHANGE:
            # Cambio de estadio
            stadium_bytes = data.read_bytes(data.read_int32())  # Leer bytes del estadio
            return {
                "admin_id": data.read_int32() if data.read_uint8() != 0 else None,
                "stadium_bytes": stadium_bytes,
            }

        elif msg_type == MessageType.KICK:
            # Jugador expulsado
            return {
                "player_id": data.read_int32(),
                "reason": data.read_string() if data.read_uint8() != 0 else None,
                "banned": data.read_uint8() != 0,
                "admin_id": data.read_int32() if data.read_uint8() != 0 else None,
            }

        elif msg_type == MessageType.POSITION_CHANGE:
            # Cambio de posición
            return {
                "player_id": data.read_int32(),
                "position": data.read_int32(),
                "admin_id": data.read_int32() if data.read_uint8() != 0 else None,
            }

        else:
            # Tipo desconocido
            # Nota: Podríamos intentar leer algunos bytes genéricos o simplemente no avanzar
            return {"unknown_type": msg_type}
