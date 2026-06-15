"""Unit tests for the Python analytics layer (reads Parquet -> Stats)."""

import pyarrow as pa
import pyarrow.parquet as pq

from haxmetrics.analytics import compute_stats


def _write_fixture(parquet_dir, *, scoring_teams, **meta_overrides):
    """Write the minimal meta+events Parquet contract the extractor produces.

    ``scoring_teams`` is the per-goal scoring team (1=red, 2=blue) used to
    reconstruct the score; ``meta_overrides`` set the recorded score etc.
    """
    meta = {
        "total_frames": 22247,
        "duration_ms": 370783.3,
        "recorded_red": 2,
        "recorded_blue": 3,
        "score_limit": 0,
        "time_limit": 0,
        "stadium_name": "Test Stadium",
        "num_players": 8,
    }
    meta.update(meta_overrides)
    pq.write_table(
        pa.table({k: [v] for k, v in meta.items()}),
        str(parquet_dir / "meta.parquet"),
    )

    events = {
        "frame_no": [1000 * (i + 1) for i in range(len(scoring_teams))],
        "kind": ["goal"] * len(scoring_teams),
        "team_id": [3 - t for t in scoring_teams],  # raw marker (conceding team)
        "scoring_team": list(scoring_teams),
    }
    pq.write_table(pa.table(events), str(parquet_dir / "events.parquet"))


def test_compute_stats_reads_score_and_duration(tmp_path):
    _write_fixture(tmp_path, scoring_teams=[1, 1, 2, 2, 2])

    stats = compute_stats(tmp_path)

    assert stats.red == 2
    assert stats.blue == 3
    assert stats.duration_frames == 22247
    assert stats.duration_seconds == 370.7833


def test_score_invariant_ok_when_reconstructed_matches_recorded(tmp_path):
    # recorded 2-3 and events reconstruct to red=2, blue=3 -> invariant holds
    _write_fixture(tmp_path, scoring_teams=[1, 1, 2, 2, 2])

    stats = compute_stats(tmp_path)

    assert stats.score_invariant_ok is True


def test_score_invariant_fails_when_reconstructed_mismatches_recorded(tmp_path):
    # recorded says 2-3 but events only reconstruct red=1, blue=3 -> mismatch
    _write_fixture(tmp_path, scoring_teams=[1, 2, 2, 2], recorded_red=2, recorded_blue=3)

    stats = compute_stats(tmp_path)

    assert stats.score_invariant_ok is False
