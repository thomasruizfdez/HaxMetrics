"""Analytics layer: read the extractor's Parquet output and compute stats.

Importable as a library (``from haxmetrics.analytics import compute_stats``) and
used by the ``haxmetrics analyze`` CLI.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pyarrow.parquet as pq

EXPECTED_COLUMNS: dict[str, frozenset[str]] = {
    "meta": frozenset({"total_frames", "duration_ms", "recorded_red", "recorded_blue"}),
    "events": frozenset({"kind", "scoring_team", "player_id"}),
    "players": frozenset({"player_id", "name", "team_id"}),
    "frames": frozenset({"object_id", "team"}),
}

SIMULATION_HZ: int = 60


def _active_frames(frames_rows: list) -> dict[int, int]:
    counts: dict[int, int] = {}
    for row in frames_rows:
        pid = row.get("object_id")
        if pid is not None and row.get("team") in (1, 2):
            counts[pid] = counts.get(pid, 0) + 1
    return counts


def _check_columns(table, name: str) -> None:
    missing = EXPECTED_COLUMNS[name] - set(table.schema.names)
    if missing:
        raise ValueError(
            f"Parquet table '{name}' is missing expected columns: {sorted(missing)}"
        )


@dataclass(frozen=True)
class PlayerStats:
    player_id: int
    name: str
    team_id: int
    frames_played: int
    seconds_played: float


@dataclass(frozen=True)
class GoalStats:
    frame_no: int
    scoring_team: int
    conceding_team: int
    scorer_id: int | None
    minute: float


@dataclass(frozen=True)
class RosterChange:
    frame_no: int
    player_id: int
    kind: str
    minute: float


@dataclass(frozen=True)
class Stats:
    red: int
    blue: int
    duration_frames: int
    duration_seconds: float
    score_invariant_ok: bool
    players: tuple[PlayerStats, ...] = ()
    goals: tuple[GoalStats, ...] = ()
    roster_changes: tuple[RosterChange, ...] = ()


def _minute(frame_no: int) -> float:
    return round(frame_no / SIMULATION_HZ / 60, 2)


def _extract_goals(events: list[dict]) -> tuple[GoalStats, ...]:
    goals = []
    for e in events:
        if e["kind"] != "goal":
            continue
        scoring_team = int(e["scoring_team"])
        scorer_id = e.get("player_id")
        goals.append(
            GoalStats(
                frame_no=int(e["frame_no"]),
                scoring_team=scoring_team,
                conceding_team=3 - scoring_team,
                scorer_id=int(scorer_id) if scorer_id is not None else None,
                minute=_minute(int(e["frame_no"])),
            )
        )
    return tuple(goals)


def _extract_roster_changes(events: list[dict]) -> tuple[RosterChange, ...]:
    changes = []
    for e in events:
        if e["kind"] not in ("join", "leave"):
            continue
        changes.append(
            RosterChange(
                frame_no=int(e["frame_no"]),
                player_id=int(e["player_id"]),
                kind=e["kind"],
                minute=_minute(int(e["frame_no"])),
            )
        )
    return tuple(changes)


def _group_roster_by_team(players: tuple[PlayerStats, ...]) -> dict[str, list[dict]]:
    team_key = {1: "red", 2: "blue"}
    roster: dict[str, list[dict]] = {"red": [], "blue": [], "spec": []}
    for p in players:
        roster[team_key.get(p.team_id, "spec")].append({"id": p.player_id, "name": p.name})
    return roster


def stats_to_dict(replay_name: str, stats: Stats) -> dict:
    return {
        "replay": replay_name,
        "score": {"red": stats.red, "blue": stats.blue},
        "duration": {
            "frames": stats.duration_frames,
            "seconds": stats.duration_seconds,
        },
        "score_invariant_ok": stats.score_invariant_ok,
        "players": [
            {
                "id": p.player_id,
                "name": p.name,
                "team": p.team_id,
                "frames_played": p.frames_played,
                "seconds_played": p.seconds_played,
            }
            for p in stats.players
        ],
        "goals": [
            {
                "frame_no": g.frame_no,
                "minute": g.minute,
                "scoring_team": g.scoring_team,
                "conceding_team": g.conceding_team,
                "scorer_id": g.scorer_id,
            }
            for g in stats.goals
        ],
        "roster": _group_roster_by_team(stats.players),
        "roster_changes": [
            {
                "frame_no": rc.frame_no,
                "minute": rc.minute,
                "player_id": rc.player_id,
                "kind": rc.kind,
            }
            for rc in stats.roster_changes
        ],
    }


def compute_stats(parquet_dir: str | Path) -> Stats:
    parquet_dir = Path(parquet_dir)

    meta_table = pq.read_table(parquet_dir / "meta.parquet")
    _check_columns(meta_table, "meta")
    meta = meta_table.to_pylist()[0]

    events_table = pq.read_table(parquet_dir / "events.parquet")
    _check_columns(events_table, "events")
    events = events_table.to_pylist()

    recorded_red = int(meta["recorded_red"])
    recorded_blue = int(meta["recorded_blue"])

    goal_stats = _extract_goals(events)
    roster_changes = _extract_roster_changes(events)
    reconstructed_red = sum(1 for g in goal_stats if g.scoring_team == 1)
    reconstructed_blue = sum(1 for g in goal_stats if g.scoring_team == 2)

    players_table = pq.read_table(parquet_dir / "players.parquet")
    _check_columns(players_table, "players")
    players_rows = players_table.to_pylist()

    frames_table = pq.read_table(parquet_dir / "frames.parquet")
    _check_columns(frames_table, "frames")
    frames_rows = frames_table.to_pylist()

    frames_by_player = _active_frames(frames_rows)

    players = tuple(
        PlayerStats(
            player_id=int(p["player_id"]),
            name=str(p["name"]),
            team_id=int(p["team_id"]),
            frames_played=frames_by_player.get(int(p["player_id"]), 0),
            seconds_played=round(frames_by_player.get(int(p["player_id"]), 0) / SIMULATION_HZ, 4),
        )
        for p in players_rows
    )

    return Stats(
        red=recorded_red,
        blue=recorded_blue,
        duration_frames=int(meta["total_frames"]),
        duration_seconds=round(float(meta["duration_ms"]) / 1000, 4),
        score_invariant_ok=(
            reconstructed_red == recorded_red
            and reconstructed_blue == recorded_blue
        ),
        players=players,
        goals=goal_stats,
        roster_changes=roster_changes,
    )
