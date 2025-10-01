# src/haxmetrics/io/probes.py
from __future__ import annotations
import io
import os
import json
import math
import binascii
from typing import Optional, Iterator, Dict, Any, Tuple

try:
    import click  # CLI opcional
except Exception:
    click = None

from .hbr2_reader import HBR2Reader, HBR2ReaderError
from .decoder import PayloadDecoder, DecodeError

# ---- util de bytes/estadísticas -------------------------------------------------

PRINTABLE = set(range(32, 127)) | {9, 10, 13}  # tab, \n, \r + ASCII visibles


def hex_head(b: bytes, n: int = 64) -> str:
    h = binascii.hexlify(b[:n]).decode("ascii")
    spaced = " ".join(h[i : i + 2] for i in range(0, len(h), 2))
    if len(b) > n:
        spaced += " ..."
    return spaced


def ratio_printable(b: bytes, sample: int = 4096) -> float:
    s = b[:sample]
    if not s:
        return 0.0
    return sum(1 for x in s if x in PRINTABLE) / len(s)


def entropy_estimate(b: bytes, sample: int = 16384) -> float:
    s = b[:sample]
    if not s:
        return 0.0
    from collections import Counter

    c = Counter(s)
    N = len(s)
    ent = 0.0
    for v in c.values():
        p = v / N
        ent -= p * math.log2(p)
    return ent  # bits/byte (máx 8.0)


def detect_compression_sig(b: bytes) -> Optional[str]:
    if len(b) < 4:
        return None
    if b.startswith(b"\x1f\x8b\x08"):
        return "gzip"
    if b[0] == 0x78:
        return "zlib-like"
    if b.startswith(b"\x04\x22\x4d\x18"):
        return "lz4-frame"
    if b.startswith(b"\x28\xb5\x2f\xfd"):
        return "zstd"
    return None


# ---- intento de decodificación, reportando qué ruta ha funcionado ---------------


def try_decode_with_label(payload: bytes) -> Tuple[str, Iterator[Dict[str, Any]]]:
    """
    Intenta las rutas del PayloadDecoder pero devolviendo una *etiqueta* que diga
    qué camino funcionó. Si falla, levanta DecodeError.
    """
    dec = PayloadDecoder()

    # 1) sin compresión
    for label, fn in (("json", dec._as_json_ticks), ("ndjson", dec._as_ndjson_ticks)):
        try:
            it = dec._prime(fn(payload))
            return label, it
        except Exception:
            pass

    # 2) con descompresión (probando varias)
    for decomp in dec._maybe_decompress(payload):
        # re-intentar JSON/NDJSON
        for label, fn in (
            ("z*+json", dec._as_json_ticks),
            ("z*+ndjson", dec._as_ndjson_ticks),
        ):
            try:
                it = dec._prime(fn(decomp))
                return label, it
            except Exception:
                pass
        # binarios
        for label, fn in (
            ("z*+msgpack", dec._as_msgpack_ticks),
            ("z*+cbor", dec._as_cbor_ticks),
        ):
            try:
                it = dec._prime(fn(decomp))
                return label, it
            except Exception:
                pass

    # 3) binarios sin descompresión previa
    for label, fn in (("msgpack", dec._as_msgpack_ticks), ("cbor", dec._as_cbor_ticks)):
        try:
            it = dec._prime(fn(payload))
            return label, it
        except Exception:
            pass

    raise DecodeError("No decoder matched")


# ---- CLI principal --------------------------------------------------------------


def probe_file(
    path: str, dump_dir: Optional[str] = None, preview_ticks: int = 5
) -> Dict[str, Any]:
    version, header_bytes, payload = HBR2Reader(path).read_raw()

    header_json = None
    if header_bytes:
        # intentar JSON directo o JSON embebido buscando primera '{'
        try:
            header_json = json.loads(header_bytes.decode("utf-8"))
        except Exception:
            j = header_bytes.find(b"{")
            if j >= 0:
                try:
                    header_json = json.loads(header_bytes[j:].decode("utf-8"))
                except Exception:
                    header_json = None

    report: Dict[str, Any] = {
        "file": path,
        "version": version,
        "size_bytes": os.path.getsize(path),
        "header_len": len(header_bytes),
        "header_head_hex": hex_head(header_bytes or b"", 64),
        "header_json_keys": (
            list(header_json.keys()) if isinstance(header_json, dict) else None
        ),
        "payload_len": len(payload),
        "payload_head_hex": hex_head(payload, 64),
        "payload_printable_ratio": round(ratio_printable(payload), 3),
        "payload_entropy_bits_per_byte": round(entropy_estimate(payload), 3),
        "compression_signature": detect_compression_sig(payload),
        "decoder_route": None,
        "preview_ticks": [],
    }

    if dump_dir:
        os.makedirs(dump_dir, exist_ok=True)
        raw_out = os.path.join(dump_dir, os.path.basename(path) + ".payload.bin")
        with open(raw_out, "wb") as w:
            w.write(payload)
        report["payload_dump"] = raw_out
        if header_bytes:
            h_out = os.path.join(dump_dir, os.path.basename(path) + ".header.bin")
            with open(h_out, "wb") as w:
                w.write(header_bytes)
            report["header_dump"] = h_out

    try:
        route, it = try_decode_with_label(payload)
        report["decoder_route"] = route
        preview = []
        for i, t in enumerate(it):
            if i >= preview_ticks:
                break
            sample = {"keys": list(t.keys())}
            for k in ("inputs", "playing", "state"):
                if k in t:
                    v = t[k]
                    if k == "state" and isinstance(v, dict):
                        sample["state_keys"] = list(v.keys())
                        b = v.get("ball")
                        if isinstance(b, dict):
                            sample["ball"] = {
                                kk: b.get(kk) for kk in ("x", "y", "vx", "vy")
                            }
                    elif k == "inputs" and isinstance(v, dict):
                        some = list(v.items())[:3]
                        sample["inputs_sample"] = {pid: vv for pid, vv in some}
                    else:
                        sample[k] = v
            preview.append(sample)
        report["preview_ticks"] = preview
    except DecodeError as e:
        report["decoder_error"] = str(e)

    return report


# ---- CLI con Click -------------------------------------------------------------


def _echo_json(obj: Dict[str, Any]):
    print(json.dumps(obj, indent=2, ensure_ascii=False))


def main_cli():
    if click is None:
        raise RuntimeError("Instala 'click' para usar la CLI: pip install click")

    @click.command("probe")
    @click.argument("replays", nargs=-1, type=click.Path(exists=True, dir_okay=False))
    @click.option(
        "--dump-dir",
        type=click.Path(file_okay=False, dir_okay=True),
        default=None,
        help="Directorio donde volcar payloads crudos (.payload.bin)",
    )
    @click.option(
        "--preview", type=int, default=5, help="Nº de ticks de previsualización"
    )
    def _cmd(replays, dump_dir, preview):
        if not replays:
            raise click.ClickException("Debes pasar al menos un archivo .hbr2")
        out = []
        for p in replays:
            try:
                rep = probe_file(p, dump_dir=dump_dir, preview_ticks=preview)
            except HBR2ReaderError as e:
                rep = {"file": p, "error": f"Reader: {e}"}
            out.append(rep)
        _echo_json(out if len(out) > 1 else out[0])

    _cmd()


if __name__ == "__main__":
    main_cli()
