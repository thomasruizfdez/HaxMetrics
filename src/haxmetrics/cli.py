"""``haxmetrics`` command-line interface.

``haxmetrics analyze <replay>.hbr2`` orchestrates the pipeline transparently:
Node extractor (node-haxball -> Parquet) -> Python analytics -> stats.json.
"""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
from pathlib import Path

import click

from haxmetrics.analytics import compute_stats


def _extractor_path() -> str:
    override = os.environ.get("HAXMETRICS_EXTRACTOR")
    if override:
        return override
    # src/haxmetrics/cli.py -> repo root is parents[2]
    return str(Path(__file__).resolve().parents[2] / "scripts" / "extract_replay.js")


@click.group()
def main() -> None:
    """HaxMetrics: Haxball replay analytics."""


@main.command()
@click.argument("replay", type=click.Path(exists=True, dir_okay=False))
@click.option("-o", "--output", type=click.Path(dir_okay=False),
              help="Write stats JSON to this file instead of stdout.")
def analyze(replay: str, output: str | None) -> None:
    """Analyze REPLAY (.hbr2) and emit score + duration as JSON."""
    with tempfile.TemporaryDirectory(prefix="haxmetrics-") as tmp:
        proc = subprocess.run(
            ["node", _extractor_path(), replay, tmp],
            capture_output=True, text=True,
        )
        if proc.returncode != 0:
            raise click.ClickException(
                f"extractor failed: {proc.stderr.strip() or proc.stdout.strip()}"
            )

        stats = compute_stats(tmp)

    result = {
        "replay": Path(replay).name,
        "score": {"red": stats.red, "blue": stats.blue},
        "duration": {
            "frames": stats.duration_frames,
            "seconds": stats.duration_seconds,
        },
        "score_invariant_ok": stats.score_invariant_ok,
    }
    payload = json.dumps(result, indent=2)
    if output:
        Path(output).write_text(payload, encoding="utf-8")
    else:
        click.echo(payload)


if __name__ == "__main__":
    main()
