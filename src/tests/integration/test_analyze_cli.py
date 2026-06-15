"""End-to-end tracer bullet: haxmetrics analyze <replay>.hbr2 -> stats.json.

Runs the real Node extractor (node-haxball -> Parquet) and the Python analytics
through the CLI on a real replay fixture.
"""

import json
from pathlib import Path

import pytest
from click.testing import CliRunner

from haxmetrics.cli import main

# A short, ASYMMETRIC replay (26 445 frames, final 0-1) so the test actually
# exercises the team-mapping direction; a symmetric score would pass regardless.
REPLAY = (
    Path(__file__).resolve().parents[1]
    / "fixtures" / "actions" / "HBReplay-2026-01-09-22h17m.hbr2"
)


@pytest.mark.integration
def test_analyze_produces_stats_json_with_score_and_duration(tmp_path):
    out = tmp_path / "stats.json"

    result = CliRunner().invoke(main, ["analyze", str(REPLAY), "-o", str(out)])

    assert result.exit_code == 0, result.output
    data = json.loads(out.read_text())

    assert data["duration"]["frames"] == 26445
    assert data["duration"]["seconds"] > 0
    # Score reconstructed from goal events must equal the simulated score.
    assert data["score_invariant_ok"] is True
    # Exactly one goal scored during this replay, by blue (asymmetric).
    assert data["score"] == {"red": 0, "blue": 1}


@pytest.mark.integration
def test_analyze_invalid_replay_exits_nonzero_with_clear_error(tmp_path):
    bad = tmp_path / "garbage.hbr2"
    bad.write_bytes(b"not a real replay file")

    result = CliRunner().invoke(main, ["analyze", str(bad)])

    assert result.exit_code != 0
    assert "extractor failed" in result.output
