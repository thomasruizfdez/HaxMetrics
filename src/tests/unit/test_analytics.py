"""Unit tests for the Python analytics layer (reads Parquet -> Stats)."""

import pytest
import pyarrow as pa
import pyarrow.parquet as pq

from haxmetrics.analytics import EXPECTED_COLUMNS, Stats, PlayerStats, compute_stats, stats_to_dict


def _write_fixture(
    parquet_dir,
    *,
    scoring_teams,
    scorer_ids=None,  # [player_id | None, ...] aligned with scoring_teams
    players=(),      # [(player_id, name, team_id), ...]
    player_frames=(), # [(frame_no, object_id, team), ...] — active-game player rows
    extra_events=(),  # [(frame_no, kind, player_id, team_id), ...] join/leave/team_change
    **meta_overrides,
):
    """Write the full Parquet contract the extractor produces.

    ``scoring_teams`` — per-goal scoring team (1=red, 2=blue).
    ``scorer_ids``    — per-goal scorer player_id, or None if unresolved; defaults
                         to all-None (matches the extractor's best-effort behavior).
    ``players``       — rows for players.parquet; empty list = no players.
    ``player_frames`` — (frame_no, object_id, team) rows added to frames.parquet
                        as object_kind='player' rows; empty = no frames.
    ``extra_events``  — non-goal event rows (join/leave/team_change).
    ``meta_overrides``— override meta fields.
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
    assert EXPECTED_COLUMNS["meta"].issubset(meta.keys())
    pq.write_table(
        pa.table({k: [v] for k, v in meta.items()}),
        str(parquet_dir / "meta.parquet"),
    )

    if scorer_ids is None:
        scorer_ids = [None] * len(scoring_teams)
    assert len(scorer_ids) == len(scoring_teams)

    frame_nos = [1000 * (i + 1) for i in range(len(scoring_teams))]
    kinds = ["goal"] * len(scoring_teams)
    team_ids = [3 - t for t in scoring_teams]
    scoring_team_col = list(scoring_teams)
    player_id_col = list(scorer_ids)

    for frame_no, kind, player_id, team_id in extra_events:
        frame_nos.append(frame_no)
        kinds.append(kind)
        team_ids.append(team_id)
        scoring_team_col.append(None)
        player_id_col.append(player_id)

    events = {
        "frame_no": pa.array(frame_nos, type=pa.int64()),
        "kind": pa.array(kinds, type=pa.string()),
        "team_id": pa.array(team_ids, type=pa.int32()),
        "scoring_team": pa.array(scoring_team_col, type=pa.int32()),
        "player_id": pa.array(player_id_col, type=pa.int32()),
    }
    assert EXPECTED_COLUMNS["events"].issubset(events.keys())
    pq.write_table(pa.table(events), str(parquet_dir / "events.parquet"))

    players_dict = {
        "player_id": pa.array([p[0] for p in players], type=pa.int32()),
        "name": pa.array([p[1] for p in players], type=pa.string()),
        "team_id": pa.array([p[2] for p in players], type=pa.int32()),
    }
    assert EXPECTED_COLUMNS["players"].issubset(players_dict.keys())
    pq.write_table(pa.table(players_dict), str(parquet_dir / "players.parquet"))

    frames_dict = {
        "frame_no": pa.array([f[0] for f in player_frames], type=pa.int64()),
        "object_kind": pa.array(["player"] * len(player_frames), type=pa.string()),
        "object_id": pa.array([f[1] for f in player_frames], type=pa.int32()),
        "team": pa.array([f[2] for f in player_frames], type=pa.int32()),
    }
    assert EXPECTED_COLUMNS["frames"].issubset(frames_dict.keys())
    pq.write_table(pa.table(frames_dict), str(parquet_dir / "frames.parquet"))


def test_stats_to_dict_score_and_duration():
    stats = Stats(red=2, blue=3, duration_frames=22247, duration_seconds=370.7833, score_invariant_ok=True)
    result = stats_to_dict("match.hbr2", stats)
    assert result["replay"] == "match.hbr2"
    assert result["score"] == {"red": 2, "blue": 3}
    assert result["duration"] == {"frames": 22247, "seconds": 370.7833}
    assert result["score_invariant_ok"] is True
    assert result["players"] == []


def test_stats_to_dict_player_fields_are_renamed():
    player = PlayerStats(player_id=7, name="Alice", team_id=1, frames_played=120, seconds_played=2.0)
    stats = Stats(red=1, blue=0, duration_frames=100, duration_seconds=1.6667, score_invariant_ok=True, players=(player,))
    result = stats_to_dict("x.hbr2", stats)
    p = result["players"][0]
    assert p["id"] == 7
    assert p["name"] == "Alice"
    assert p["team"] == 1
    assert p["frames_played"] == 120
    assert p["seconds_played"] == 2.0


def test_compute_stats_includes_players(tmp_path):
    _write_fixture(
        tmp_path,
        scoring_teams=[2],
        players=[(1, "Alice", 1), (2, "Bob", 2)],
    )

    stats = compute_stats(tmp_path)

    ids = {p.player_id for p in stats.players}
    assert ids == {1, 2}
    alice = next(p for p in stats.players if p.player_id == 1)
    assert alice.name == "Alice"
    assert alice.team_id == 1


def test_player_frames_played_counts_active_game_frames(tmp_path):
    # Alice played 3 frames (team=1), Bob played 2 frames (team=2)
    _write_fixture(
        tmp_path,
        scoring_teams=[],
        recorded_red=0, recorded_blue=0,
        players=[(1, "Alice", 1), (2, "Bob", 2)],
        player_frames=[
            (10, 1, 1), (20, 1, 1), (30, 1, 1),  # Alice, 3 frames
            (10, 2, 2), (20, 2, 2),                 # Bob, 2 frames
        ],
    )

    stats = compute_stats(tmp_path)

    alice = next(p for p in stats.players if p.player_id == 1)
    bob = next(p for p in stats.players if p.player_id == 2)
    assert alice.frames_played == 3
    assert bob.frames_played == 2


def test_player_seconds_played_is_frames_over_60(tmp_path):
    _write_fixture(
        tmp_path,
        scoring_teams=[],
        recorded_red=0, recorded_blue=0,
        players=[(1, "Alice", 1)],
        player_frames=[(f, 1, 1) for f in range(120)],  # 120 frames = 2.0s
    )

    stats = compute_stats(tmp_path)

    alice = next(p for p in stats.players if p.player_id == 1)
    assert alice.seconds_played == 2.0


def test_spectator_has_zero_frames_played(tmp_path):
    _write_fixture(
        tmp_path,
        scoring_teams=[],
        recorded_red=0, recorded_blue=0,
        players=[(99, "Lurker", 0)],
        player_frames=[],
    )

    stats = compute_stats(tmp_path)

    lurker = stats.players[0]
    assert lurker.frames_played == 0
    assert lurker.seconds_played == 0.0


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


def test_compute_stats_raises_on_missing_column(tmp_path):
    # meta.parquet is missing 'total_frames' — validation must catch this
    pq.write_table(
        pa.table({"duration_ms": [370783.3], "recorded_red": [2], "recorded_blue": [3]}),
        str(tmp_path / "meta.parquet"),
    )
    with pytest.raises(ValueError, match="total_frames"):
        compute_stats(tmp_path)


def test_goals_include_scorer_and_minute(tmp_path):
    _write_fixture(tmp_path, scoring_teams=[2], scorer_ids=[5], players=[(5, "Alice", 2)])

    stats = compute_stats(tmp_path)

    assert len(stats.goals) == 1
    goal = stats.goals[0]
    assert goal.frame_no == 1000
    assert goal.scoring_team == 2
    assert goal.conceding_team == 1
    assert goal.scorer_id == 5
    assert goal.minute == round(1000 / 60 / 60, 2)


def test_goals_scorer_id_null_when_unresolved(tmp_path):
    _write_fixture(tmp_path, scoring_teams=[1], scorer_ids=[None])

    stats = compute_stats(tmp_path)

    assert stats.goals[0].scorer_id is None
    result = stats_to_dict("x.hbr2", stats)
    assert result["goals"][0]["scorer_id"] is None


def test_roster_grouped_by_team(tmp_path):
    _write_fixture(
        tmp_path,
        scoring_teams=[],
        recorded_red=0, recorded_blue=0,
        players=[(1, "Alice", 1), (2, "Bob", 2), (3, "Spec", 0)],
    )

    stats = compute_stats(tmp_path)
    result = stats_to_dict("x.hbr2", stats)

    assert result["roster"] == {
        "red": [{"id": 1, "name": "Alice"}],
        "blue": [{"id": 2, "name": "Bob"}],
        "spec": [{"id": 3, "name": "Spec"}],
    }


def test_roster_changes_from_join_leave_events(tmp_path):
    _write_fixture(
        tmp_path,
        scoring_teams=[],
        recorded_red=0, recorded_blue=0,
        players=[(7, "Charlie", 1)],
        extra_events=[(500, "join", 7, None), (900, "leave", 7, None)],
    )

    stats = compute_stats(tmp_path)

    assert len(stats.roster_changes) == 2
    joined, left = stats.roster_changes
    assert joined.kind == "join" and joined.player_id == 7 and joined.frame_no == 500
    assert left.kind == "leave" and left.player_id == 7 and left.frame_no == 900


def test_compute_stats_raises_on_missing_events_player_id_column(tmp_path):
    pq.write_table(
        pa.table({k: [v] for k, v in {
            "total_frames": 22247, "duration_ms": 370783.3,
            "recorded_red": 2, "recorded_blue": 3,
        }.items()}),
        str(tmp_path / "meta.parquet"),
    )
    pq.write_table(
        pa.table({
            "frame_no": pa.array([1000], type=pa.int64()),
            "kind": pa.array(["goal"], type=pa.string()),
            "team_id": pa.array([1], type=pa.int32()),
            "scoring_team": pa.array([2], type=pa.int32()),
        }),
        str(tmp_path / "events.parquet"),
    )
    with pytest.raises(ValueError, match="player_id"):
        compute_stats(tmp_path)
