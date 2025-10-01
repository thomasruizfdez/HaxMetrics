# src/haxmetrics/io/decoder.py
from __future__ import annotations
import io
import json
import struct
from typing import Iterator, Dict, Any, List, Tuple, Optional

# Extras opcionales
try:
    import zstandard as _zstd  # pip install zstandard
except Exception:
    _zstd = None

try:
    import lz4.frame as _lz4  # pip install lz4
except Exception:
    _lz4 = None

try:
    import msgpack  # pip install msgpack
except Exception:
    msgpack = None

try:
    import cbor2  # pip install cbor2
except Exception:
    cbor2 = None


class DecodeError(RuntimeError):
    pass


class PayloadDecoder:
    """
    Decodifica el payload crudo hacia una secuencia de ticks (dict por tick).
    Estrategia:
      A) Intentar JSON/NDJSON plano
      B) Intentar descompresión total (zlib/gzip/lz4/zstd) y repetir A
      C) Intentar zlib *concatenado* (varios streams seguidos) y repetir A sobre el concatenado
      D) Intentar 'length-prefixed framing' (uint32_le len + blob) sobre:
         - payload crudo
         - payload descomprimido
         Con cada blob intentar: JSON/NDJSON/MsgPack/CBOR (y blob descomprimido) → ticks.
      E) Intentar MsgPack/CBOR directos (total)
    """

    # ---------- API principal ----------
    def decode_ticks(self, payload: bytes) -> Iterator[Dict[str, Any]]:
        # A) directo
        for it in (self._as_json_ticks(payload), self._as_ndjson_ticks(payload)):
            try:
                return self._prime(it)
            except DecodeError:
                pass

        # B) descomprimir TODO y reintentar A
        for decomp in self._maybe_decompress_all(payload):
            for it in (self._as_json_ticks(decomp), self._as_ndjson_ticks(decomp)):
                try:
                    return self._prime(it)
                except DecodeError:
                    pass

            # E parcial: MsgPack/CBOR sobre total descomprimido
            for it in (self._as_msgpack_ticks(decomp), self._as_cbor_ticks(decomp)):
                try:
                    return self._prime(it)
                except DecodeError:
                    pass

            # D) framing length-prefixed dentro del descomprimido
            it = self._as_length_prefixed_ticks(decomp)
            if it is not None:
                return self._prime(it)

        # C) zlib concatenado (varios streams pegados)
        concat = self._zlib_concatenated(payload)
        if concat:
            for it in (self._as_json_ticks(concat), self._as_ndjson_ticks(concat)):
                try:
                    return self._prime(it)
                except DecodeError:
                    pass

        # D) framing length-prefixed sobre el payload crudo
        it = self._as_length_prefixed_ticks(payload)
        if it is not None:
            return self._prime(it)

        # E) MsgPack / CBOR directos
        for it in (self._as_msgpack_ticks(payload), self._as_cbor_ticks(payload)):
            try:
                return self._prime(it)
            except DecodeError:
                pass

        raise DecodeError(
            "No se pudo decodificar el payload a ticks (ninguna ruta coincidió)."
        )

    # ---------- Parsers “planos” ----------
    @staticmethod
    def _as_json_ticks(data: bytes) -> Iterator[Dict[str, Any]]:
        try:
            obj = json.loads(data.decode("utf-8"))
        except Exception as e:
            raise DecodeError(f"JSON inválido: {e}")

        if isinstance(obj, dict) and "ticks" in obj:
            ticks = obj["ticks"]
            if not isinstance(ticks, list):
                raise DecodeError("JSON: 'ticks' no es lista.")
            for t in ticks:
                if not isinstance(t, dict):
                    raise DecodeError("JSON: cada tick debe ser dict.")
                yield t
            return

        if isinstance(obj, list):
            for t in obj:
                if not isinstance(t, dict):
                    raise DecodeError("JSON array: cada elemento debe ser dict.")
                yield t
            return

        # Permitimos “stream con prefacio”: buscar primer '{'
        i = data.find(b"{")
        if i > 0:
            return PayloadDecoder._as_json_ticks(data[i:])  # reintenta
        raise DecodeError("JSON: estructura desconocida (esperaba 'ticks' o lista).")

    @staticmethod
    def _as_ndjson_ticks(data: bytes) -> Iterator[Dict[str, Any]]:
        buf = io.BytesIO(data)
        any_line = False
        while True:
            line = buf.readline()
            if not line:
                break
            s = line.strip()
            if not s:
                continue
            any_line = True
            try:
                obj = json.loads(s.decode("utf-8"))
            except Exception as e:
                raise DecodeError(f"NDJSON: línea inválida: {e}")
            if not isinstance(obj, dict):
                raise DecodeError("NDJSON: cada línea debe ser dict.")
            yield obj
        if not any_line:
            raise DecodeError("NDJSON: payload vacío o sin líneas.")

    # ---------- Descompresión ----------
    @staticmethod
    def _maybe_decompress_all(payload: bytes) -> Iterator[bytes]:
        """Genera posibles descompresiones completas del payload."""
        import zlib, gzip

        # zlib con distintos wbits
        for wb in (zlib.MAX_WBITS, -zlib.MAX_WBITS, 15, -15):
            try:
                yield zlib.decompress(payload, wb)
            except Exception:
                pass

        # gzip
        try:
            yield gzip.decompress(payload)
        except Exception:
            pass

        # lz4 frame
        if _lz4 is not None:
            try:
                yield _lz4.decompress(payload)
            except Exception:
                pass

        # zstd
        if _zstd is not None:
            try:
                dctx = _zstd.ZstdDecompressor()
                yield dctx.decompress(payload)
            except Exception:
                pass

    @staticmethod
    def _zlib_concatenated(payload: bytes) -> Optional[bytes]:
        """
        Intenta leer *varios* streams zlib concatenados.
        Devuelve la concatenación de los descomprimidos si al menos uno funciona.
        """
        import zlib

        out = bytearray()
        data = memoryview(payload)
        any_ok = False

        # probamos con dos configuraciones típicas: zlib (wbits=MAX_WBITS) y raw (wbits=-MAX_WBITS)
        for wbits in (zlib.MAX_WBITS, -zlib.MAX_WBITS):
            out.clear()
            mv = data
            ok = False
            try:
                while mv:
                    d = zlib.decompressobj(wbits)
                    chunk = d.decompress(mv)
                    out += chunk
                    mv = d.unused_data
                    if not chunk and not mv:
                        break
                    ok = True
                if ok:
                    any_ok = True
                    return bytes(out)
            except Exception:
                continue
        return bytes(out) if any_ok else None

    # ---------- Framing: length-prefixed ----------
    def _as_length_prefixed_ticks(
        self, data: bytes
    ) -> Optional[Iterator[Dict[str, Any]]]:
        """
        Intenta interpretar 'data' como una secuencia de:
            [uint32_le length][blob] [uint32_le length][blob] ...
        - length válido: 1 .. 64 MiB (para evitar falsos positivos).
        - Tolerancia: si queda un residuo < 4 bytes al final, lo ignora.
        Para cada blob:
          - prueba JSON/NDJSON
          - si falla, intenta descomprimir el blob y vuelve a probar
          - si aún falla, intenta msgpack/cbor
        Si al menos un blob produce dicts, devolvemos un generador concatenado.
        """
        blobs = self._split_length_prefixed(data)
        if not blobs:
            return None

        def per_blob_ticks() -> Iterator[Dict[str, Any]]:
            decoded_any = False
            for blob in blobs:
                # 1) plano
                for it in (
                    self._try_iter(self._as_json_ticks, blob),
                    self._try_iter(self._as_ndjson_ticks, blob),
                    self._try_iter(self._as_msgpack_ticks, blob),
                    self._try_iter(self._as_cbor_ticks, blob),
                ):
                    if it is not None:
                        decoded_any = True
                        for x in it:
                            yield x
                        continue

                # 2) blob descomprimido
                for decomp in self._maybe_decompress_all(blob):
                    for it in (
                        self._try_iter(self._as_json_ticks, decomp),
                        self._try_iter(self._as_ndjson_ticks, decomp),
                        self._try_iter(self._as_msgpack_ticks, decomp),
                        self._try_iter(self._as_cbor_ticks, decomp),
                    ):
                        if it is not None:
                            decoded_any = True
                            for x in it:
                                yield x
                            continue
            if not decoded_any:
                raise DecodeError("length-prefixed: ningún blob decodificó a ticks.")

        try:
            # “priming” para validar
            return self._prime(per_blob_ticks())
        except DecodeError:
            return None

    @staticmethod
    def _split_length_prefixed(data: bytes) -> List[bytes]:
        blobs: List[bytes] = []
        i = 0
        n = len(data)
        MAX_LEN = 64 * 1024 * 1024
        while i + 4 <= n:
            (length,) = struct.unpack_from("<I", data, i)
            i += 4
            if length <= 0 or length > MAX_LEN or i + length > n:
                # tolerancia: si esto parece falso positivo, abortamos
                return []
            blobs.append(data[i : i + length])
            i += length
        # toleramos residuo < 4 bytes
        return blobs if blobs else []

    # ---------- Binarios estructurados ----------
    @staticmethod
    def _as_msgpack_ticks(data: bytes) -> Iterator[Dict[str, Any]]:
        if msgpack is None:
            raise DecodeError("MessagePack no disponible (instala 'msgpack').")
        try:
            unpacker = msgpack.Unpacker(io.BytesIO(data), raw=False)
            any_item = False
            for obj in unpacker:
                any_item = True
                if not isinstance(obj, dict):
                    raise DecodeError("MessagePack: cada tick debe ser dict.")
                yield obj
            if not any_item:
                raise DecodeError("MessagePack: stream vacío.")
        except Exception as e:
            raise DecodeError(f"MessagePack: fallo al decodificar: {e}")

    @staticmethod
    def _as_cbor_ticks(data: bytes) -> Iterator[Dict[str, Any]]:
        if cbor2 is None:
            raise DecodeError("CBOR no disponible (instala 'cbor2').")
        try:
            bio = io.BytesIO(data)
            items = []
            while True:
                try:
                    obj = cbor2.load(bio)
                except EOFError:
                    break
                items.append(obj)
            if not items:
                one = cbor2.loads(data)
                if isinstance(one, list):
                    items = one
            if not items:
                raise DecodeError("CBOR: no se encontraron elementos.")
            for obj in items:
                if not isinstance(obj, dict):
                    raise DecodeError("CBOR: cada tick debe ser dict.")
                yield obj
        except Exception as e:
            raise DecodeError(f"CBOR: fallo al decodificar: {e}")

    # ---------- utils ----------
    @staticmethod
    def _prime(it: Iterator[Dict[str, Any]]) -> Iterator[Dict[str, Any]]:
        try:
            first = next(it)
        except StopIteration:
            raise DecodeError("Stream de ticks vacío.")
        except Exception as e:
            raise DecodeError(f"Iterador de ticks inválido: {e}")

        def _gen():
            yield first
            for x in it:
                yield x

        return _gen()

    @staticmethod
    def _try_iter(fn, data: bytes) -> Optional[Iterator[Dict[str, Any]]]:
        try:
            return fn(data)
        except DecodeError:
            return None
