"""Invariant harness over the 14-replay corpus.

Runs ``haxmetrics analyze`` once per replay (module-scoped fixture) and asserts
structural invariants across all of them. Also maintains golden JSON files for
extractor/analytics regression detection.

Golden files live in ``src/tests/fixtures/golden/``. Regenerate with::

    UPDATE_GOLDEN=1 python -m pytest src/tests/integration/test_invariants.py::test_golden_output -v
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest

CORPUS_DIR = Path(__file__).resolve().parents[1] / "fixtures" / "actions"
GOLDEN_DIR = Path(__file__).resolve().parents[1] / "fixtures" / "golden"
CACHE_DIR = Path(__file__).resolve().parents[1] / "fixtures" / ".corpus_cache"

CORPUS_NAMES = sorted(f.name for f in CORPUS_DIR.glob("HBReplay-*.hbr2"))

# subprocess is thread-safe (unlike CliRunner, which patches sys.stdout globally)
_CLI = [sys.executable, "-m", "haxmetrics.cli"]


def _load_or_extract(name: str) -> tuple[str, dict]:
    replay_path = CORPUS_DIR / name
    h = hashlib.sha256(replay_path.read_bytes()).hexdigest()[:16]
    cache_file = CACHE_DIR / f"{h}.json"
    if cache_file.exists():
        return name, json.loads(cache_file.read_text(encoding="utf-8"))
    proc = subprocess.run(
        [*_CLI, "analyze", str(replay_path)],
        capture_output=True, text=True,
    )
    assert proc.returncode == 0, f"analyze failed for {name}: {proc.stderr}"
    data = json.loads(proc.stdout)
    cache_file.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return name, data


@pytest.fixture(scope="session")
def corpus_results():
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=4) as pool:
        return dict(pool.map(_load_or_extract, CORPUS_NAMES))


@pytest.mark.integration
@pytest.mark.parametrize("replay_name", CORPUS_NAMES)
def test_duration_invariant(replay_name, corpus_results):
    d = corpus_results[replay_name]["duration"]
    assert d["frames"] > 0
    assert d["seconds"] > 0


@pytest.mark.integration
@pytest.mark.parametrize("replay_name", CORPUS_NAMES)
def test_players_invariant(replay_name, corpus_results):
    players = corpus_results[replay_name]["players"]
    assert len(players) > 0
    for p in players:
        assert p["seconds_played"] >= 0


@pytest.mark.integration
@pytest.mark.parametrize("replay_name", CORPUS_NAMES)
def test_score_invariant_ok(replay_name, corpus_results):
    assert corpus_results[replay_name]["score_invariant_ok"] is True


@pytest.mark.integration
@pytest.mark.slow
@pytest.mark.parametrize("replay_name", CORPUS_NAMES)
def test_golden_output(replay_name, corpus_results):
    data = corpus_results[replay_name]
    golden_path = GOLDEN_DIR / (Path(replay_name).stem + ".json")
    actual = json.dumps(data, indent=2)

    if os.getenv("UPDATE_GOLDEN") == "1":
        GOLDEN_DIR.mkdir(parents=True, exist_ok=True)
        golden_path.write_text(actual, encoding="utf-8")
        return

    assert golden_path.exists(), (
        f"Golden missing: {golden_path.name}. "
        "Run UPDATE_GOLDEN=1 pytest src/tests/integration/test_invariants.py::test_golden_output to create."
    )
    assert data == json.loads(golden_path.read_text(encoding="utf-8"))
