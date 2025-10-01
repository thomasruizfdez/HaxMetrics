from __future__ import annotations
import struct
from typing import Tuple


class HBR2ReaderError(RuntimeError):
    pass


class HBR2Reader:
    """
    Lector de bajo nivel de archivos .hbr2:
      - Valida cabecera 'HBR2'
      - Extrae versión (uint32 LE)
      - Expone header_bytes (si existiera) y payload_bytes crudo

    Nota: El formato 'HBR2' que has compartido parece comenzar por:
        0x00: 'H' 'B' 'R' '2'
        0x04: uint32_le version  (hemos visto 3)
        0x08: ... (metadata binaria propietaria hasta el inicio del payload)
    Como el tamaño del bloque de metadatos no es fijo, este lector aplica:
      1) Valida magic y lee version.
      2) Busca un posible inicio de payload por firmas conocidas (gzip/zlib/lz4/zstd).
      3) Si no encuentra firmas inequívocas, entrega el payload desde offset=8 (tras magic+version).
         Eso permite que el decoder decida cómo interpretarlo (o intente varias estrategias).
    """

    MAGIC = b"HBR2"

    def __init__(self, path: str):
        self.path = path

    def read_raw(self) -> tuple[int, bytes, bytes]:
        with open(self.path, "rb") as f:
            data = f.read()

        if len(data) < 8:
            raise HBR2ReaderError("Archivo demasiado corto para ser HBR2.")
        if data[:4] != self.MAGIC:
            raise HBR2ReaderError("Magic 'HBR2' no encontrado al inicio del archivo.")

        # ← Nuevo: detectar versión leyendo BE y LE y escoger la plausible
        ver_be, ver_le = self._read_version_be_or_le(data[4:8])
        version = None
        for v in (ver_le, ver_be):
            if 0 < v < 100:  # rango razonable para versiones
                version = v
                break
        if version is None:
            # si ninguna cuadra, muestra ambas para diagnóstico
            raise HBR2ReaderError(f"Versión HBR2 sospechosa: BE={ver_be} LE={ver_le}")

        # Buscar inicio de payload por firmas conocidas a partir de offset 8
        start = self._find_payload_start(data, min_off=8)
        if start is None:
            # Fallback: asumir que el payload empieza tras magic+version
            header_bytes = b""
            payload_bytes = data[8:]
        else:
            header_bytes = data[8:start]
            payload_bytes = data[start:]
        return version, header_bytes, payload_bytes

    @staticmethod
    def _read_version_be_or_le(b4: bytes) -> tuple[int, int]:
        """Devuelve (version_be, version_le) interpretando los 4 bytes en ambos endianness."""
        if len(b4) != 4:
            return (0, 0)
        ver_be = struct.unpack(">I", b4)[0]
        ver_le = struct.unpack("<I", b4)[0]
        return ver_be, ver_le

    @staticmethod
    def _find_payload_start(b: bytes, min_off: int = 8) -> int | None:
        candidates = []

        def _find(sig: bytes):
            i = b.find(sig, min_off)
            if i >= 0:
                candidates.append(i)

        _find(b"\x1f\x8b\x08")  # gzip
        for flg in (b"\x01", b"\x5e", b"\x9c", b"\xda", b"\xa9", b"\x99"):
            _find(b"\x78" + flg)  # zlib variants
        _find(b"\x04\x22\x4d\x18")  # lz4 frame
        _find(b"\x28\xb5\x2f\xfd")  # zstd
        # Por si el payload arranca directamente en JSON/NDJSON
        j = b.find(b"{", min_off)
        if j >= 0:
            candidates.append(j)
        if not candidates:
            return None
        return min(candidates)
