"""Analytics layer: read the extractor's Parquet output and compute stats.

Importable as a library (``from haxmetrics.analytics import compute_stats``) and
used by the ``haxmetrics analyze`` CLI.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pyarrow.parquet as pq


@dataclass(frozen=True)
class Stats:
    red: int
    blue: int
    duration_frames: int
    duration_seconds: float
    score_invariant_ok: bool


def compute_stats(parquet_dir: str | Path) -> Stats:
    parquet_dir = Path(parquet_dir)
    meta = pq.read_table(parquet_dir / "meta.parquet").to_pylist()[0]
    events = pq.read_table(parquet_dir / "events.parquet").to_pylist()

    recorded_red = int(meta["recorded_red"])
    recorded_blue = int(meta["recorded_blue"])

    goals = [e for e in events if e["kind"] == "goal"]
    reconstructed_red = sum(1 for e in goals if e["scoring_team"] == 1)
    reconstructed_blue = sum(1 for e in goals if e["scoring_team"] == 2)

    return Stats(
        red=recorded_red,
        blue=recorded_blue,
        duration_frames=int(meta["total_frames"]),
        duration_seconds=round(float(meta["duration_ms"]) / 1000, 4),
        score_invariant_ok=(
            reconstructed_red == recorded_red
            and reconstructed_blue == recorded_blue
        ),
    )
