from __future__ import annotations
import io, struct
from dataclasses import dataclass
from typing import Iterator, List, Tuple, Optional

MAGIC = b"HBR2"


@dataclass
class Block:
    offset: int  # offset del inicio del bloque (lenBE)
    length_be: int  # longitud leída (BE) del header del bloque
    type: int  # byte de tipo
    payload_off: int  # offset del payload
    payload: bytes  # bytes crudos (NO descomprimidos)


@dataclass
class HBR2File:
    version: int
    duration: int
    blocks: List[Block]


def read_u32_be(b: bytes, off: int) -> int:
    return struct.unpack(">I", b[off : off + 4])[0]


def read_u16_be(b: bytes, off: int) -> int:
    return struct.unpack(">H", b[off : off + 2])[0]


def read_hbr2_raw(path: str) -> HBR2File:
    with open(path, "rb") as f:
        data = f.read()

    if data[:4] != MAGIC:
        raise ValueError("Not an HBR2 file")
    version = read_u32_be(data, 4)
    duration = read_u32_be(data, 8)

    # Escaneamos bloques: [u16 BE len][u8 type][payload...]
    blocks: List[Block] = []
    i = 12
    n = len(data)
    while i + 3 <= n:
        # Heurística: candidato a bloque si (i+3) apunta a payload y no nos salimos
        length_be = read_u16_be(data, i)
        typ = data[i + 2]
        payload_off = i + 3
        # No confiamos a ciegas en length_be para saltar; sólo almacenamos el bloque
        # y avanzamos buscando el siguiente patrón conservadormente.
        # Para que el bucle no se quede en un sitio, avanzamos 1 y seguimos buscando.
        # Si quieres un escaneo más estricto, añade validaciones por tipo.
        blocks.append(
            Block(
                i,
                length_be,
                typ,
                payload_off,
                data[payload_off : min(n, payload_off + max(length_be, 0))],
            )
        )
        i += 1

    return HBR2File(version=version, duration=duration, blocks=blocks)
