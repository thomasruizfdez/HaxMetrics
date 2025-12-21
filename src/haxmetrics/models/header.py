"""
HBR2 Replay Header Parser

Responsabilidad: Parsear y almacenar los primeros 12 bytes del archivo HBR2.
Formato:
    - Bytes 0-3: Magic "HBR2" (0x48 0x42 0x52 0x32)
    - Bytes 4-7: Version (uint32_be)
    - Bytes 8-11: Duration in frames (uint32_be)
"""

from dataclasses import dataclass
from typing import Dict

from haxmetrics.binary_reader import BinaryReader


@dataclass(frozen=True)
class Header:
    """
    Representa el header de un archivo HBR2.

    Atributos:
        magic (str): Signature del archivo ("HBR2")
        version (int): Versión del formato (típicamente 3)
        duration (int): Duración del replay en frames
    """

    magic: str
    version: int
    duration: int

    def __post_init__(self):
        """Valida los datos del header."""
        if self.magic != "HBR2":
            raise ValueError(f"Invalid HBR2 magic: expected 'HBR2', got '{self.magic}'")

        if self.version < 0:
            raise ValueError(f"Version must be non-negative, got {self.version}")

        if self.duration < 0:
            raise ValueError(f"Duration must be non-negative, got {self.duration}")

    @classmethod
    def parse(cls, reader: BinaryReader) -> "Header":
        """
        Parsea el header desde un BinaryReader.

        Args:
            reader: BinaryReader posicionado al inicio del archivo

        Returns:
            Header: Instancia con los datos parseados

        Raises:
            ValueError: Si el magic no es "HBR2"

        Ejemplo:
            >>> with open('replay.hbr2', 'rb') as f:
            ...     reader = BinaryReader(f.read())
            ...     header = Header.parse(reader)
            ...     print(header.version)
            3
        """
        magic = reader.read_fixed_string(4)
        version = reader.read_uint32_be()
        duration = reader.read_uint32_be()

        return cls(magic=magic, version=version, duration=duration)

    @property
    def duration_seconds(self) -> float:
        """
        Calcula la duración en segundos.

        HaxBall usa 60 frames por segundo.

        Returns:
            float: Duración en segundos
        """
        return self.duration / 60.0

    def to_dict(self) -> Dict[str, any]:
        """
        Serializa el header a un diccionario.

        Returns:
            dict: Representación serializable
        """
        return {
            "magic": self.magic,
            "version": self.version,
            "duration": self.duration,
            "duration_seconds": self.duration_seconds,
        }

    def __str__(self) -> str:
        """Representación legible del header."""
        return (
            f"Header(magic={self.magic}, version={self.version}, "
            f"duration={self.duration} frames / {self.duration_seconds:.1f}s)"
        )
