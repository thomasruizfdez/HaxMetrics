from __future__ import annotations
import io
from dataclasses import dataclass
from typing import Iterator, Tuple, Optional


class BitReader:
    """
    Lector de bits eficiente sobre bytes ya descomprimidos.
    """

    __slots__ = ("_buf", "_pos", "_bitbuf", "_bitcnt")

    def __init__(self, data: bytes):
        self._buf = data
        self._pos = 0
        self._bitbuf = 0
        self._bitcnt = 0

    def _fill(self, nbits: int) -> None:
        while self._bitcnt < nbits:
            if self._pos >= len(self._buf):
                raise EOFError("BitReader: EOF")
            self._bitbuf |= self._buf[self._pos] << self._bitcnt
            self._pos += 1
            self._bitcnt += 8

    def read_bits(self, nbits: int) -> int:
        if nbits == 0:
            return 0
        self._fill(nbits)
        val = self._bitbuf & ((1 << nbits) - 1)
        self._bitbuf >>= nbits
        self._bitcnt -= nbits
        return val

    def align_byte(self) -> None:
        self._bitbuf = 0
        self._bitcnt = 0

    def read_bytes(self, n: int) -> bytes:
        self.align_byte()
        if self._pos + n > len(self._buf):
            raise EOFError("BitReader: EOF on read_bytes")
        b = self._buf[self._pos : self._pos + n]
        self._pos += n
        return b

    def tell(self) -> int:
        return self._pos


def read_uvarint_le(b: io.BytesIO) -> int:
    """
    LEB128 (unsigned) sobre stream byte-alineado.
    """
    x = 0
    s = 0
    while True:
        c = b.read(1)
        if not c:
            raise EOFError("uvarint: EOF")
        c = c[0]
        x |= (c & 0x7F) << s
        if (c & 0x80) == 0:
            break
        s += 7
        if s > 63:
            raise ValueError("uvarint: too large")
    return x


@dataclass
class RawToken:
    kind: str
    args: tuple
    at: int  # offset


def iter_raw_tokens(inflated: bytes) -> Iterator[RawToken]:
    """
    Dumper de alto nivel, NO asume aún el significado semántico.
    Sirve para reverse-engineering estable: saca una secuencia reproducible
    (varints, tags de 1 byte, longitudes + blobs).
    """
    bio = io.BytesIO(inflated)
    while True:
        at = bio.tell()
        b = bio.read(1)
        if not b:
            return
        tag = b[0]

        # Heurística:
        # - tags < 0x20 suelen ser controles/flags
        # - 0x20..0x7E podría venir como ASCII (chat, nicks) y lo tratamos como 'str' con longitud previa
        # - muchísimos campos vienen como varint (tick delta, playerId, etc.)
        if tag in (0x00, 0x01, 0x02, 0x03, 0x10, 0x11, 0x12):
            # interpretamos: tag + uno o más uvarint
            n_args = 1
            if tag in (0x02, 0x03):
                n_args = 2
            args = tuple(read_uvarint_le(bio) for _ in range(n_args))
            yield RawToken(kind=f"tag{tag:02X}", args=args, at=at)
        elif 0x20 <= tag <= 0x7E:
            # Probable string/ASCII blob → leemos una varint como longitud y luego bytes
            strlen = read_uvarint_le(bio)
            s = bio.read(strlen)
            try:
                sval = s.decode("utf-8")
                yield RawToken(kind=f"str[{tag:02X}]", args=(sval,), at=at)
            except UnicodeDecodeError:
                yield RawToken(kind=f"blob[{tag:02X}]", args=(s,), at=at)
        else:
            # fallback genérico: una varint y opcionalmente un byte-blob corto
            v = read_uvarint_le(bio)
            # Si después hay un “blob” pequeño (p.e. máscara de teclas) suele venir como 1 byte.
            peek = bio.read(1)
            if peek:
                yield RawToken(kind=f"tag{tag:02X}", args=(v, peek[0]), at=at)
            else:
                yield RawToken(kind=f"tag{tag:02X}", args=(v,), at=at)


# --------- futuras funciones de alto nivel ---------
# Aquí mapearemos los RawToken a eventos semánticos:
# - TickAdvance (delta)
# - PlayerInput (playerId, keyMask)
# - ChatMessage (playerId, text)
# - Goal/ScoreUpdate, Stadium, Teams, etc.
#
# Una vez identifiquemos la gramática comparando contra HRA, construiremos:
#
# def decode_inputs_by_tick(inflated: bytes) -> Iterator[TickFrame]:
#     ...
#
# …donde TickFrame lleve tick_index y un dict {playerId: key_mask}
