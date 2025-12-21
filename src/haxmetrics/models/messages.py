"""
HBR2 Replay Messages Parser

Responsabilidad: Parsear y gestionar los mensajes del replay.
Los mensajes están en la sección comprimida del replay.

Formato:
    - Varint: Número de mensajes
    - Para cada mensaje:
        - Varint: Frame en que ocurre
        - String: Texto del mensaje (varint length + UTF-8)
"""

from dataclasses import dataclass
from typing import Dict, Iterator, List

from haxmetrics.binary_reader import BinaryReader


@dataclass(frozen=True)
class Message:
    """
    Representa un mensaje individual del replay.

    Atributos:
        frame (int): Frame en que se envió el mensaje
        text (str): Contenido del mensaje
    """

    frame: int
    text: str

    def to_dict(self) -> Dict[str, any]:
        """Serializa el mensaje a diccionario."""
        return {"frame": self.frame, "text": self.text}


class Messages:
    """
    Gestiona la colección de mensajes del replay.

    Proporciona acceso tipo lista y métodos de utilidad.
    """

    def __init__(self, messages: List[Message]):
        """
        Inicializa la colección de mensajes.

        Args:
            messages: Lista de mensajes (se ordena por frame)
        """
        self._messages = sorted(messages, key=lambda m: m.frame)

    @classmethod
    def parse(cls, reader: BinaryReader) -> "Messages":
        """
        Parsea los mensajes desde un BinaryReader.

        IMPORTANTE: El reader debe estar posicionado en la sección
        descomprimida del replay, justo después del header.

        Args:
            reader: BinaryReader con datos descomprimidos

        Returns:
            Messages: Instancia con los mensajes parseados

        Ejemplo:
            >>> # Después de descomprimir
            >>> messages = Messages.parse(decompressed_reader)
            >>> print(len(messages))
            5
        """
        messages_count = reader.read_varint()

        messages = []
        for _ in range(messages_count):
            frame = reader.read_varint()
            text = reader.read_string()
            messages.append(Message(frame=frame, text=text))

        return cls(messages)

    def to_dict(self) -> Dict[str, any]:
        """
        Serializa la colección a diccionario.

        Returns:
            dict: Con 'count' y 'messages'
        """
        return {
            "count": len(self._messages),
            "messages": [msg.to_dict() for msg in self._messages],
        }

    def __len__(self) -> int:
        """Retorna el número de mensajes."""
        return len(self._messages)

    def __iter__(self) -> Iterator[Message]:
        """Permite iteración sobre los mensajes."""
        return iter(self._messages)

    def __getitem__(self, index: int) -> Message:
        """Permite acceso por índice."""
        return self._messages[index]

    def __str__(self) -> str:
        """Representación legible."""
        return f"Messages(count={len(self._messages)})"
