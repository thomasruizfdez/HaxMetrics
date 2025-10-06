from __future__ import annotations
import json
import subprocess
from pathlib import Path
from typing import Dict, Any, Iterator


def parse_with_node(replay_path: str | Path) -> Dict[str, Any]:
    replay_path = str(replay_path)
    proc = subprocess.run(
        ["node", "tools/replay_to_json.js", replay_path],
        capture_output=True,
        check=True,
        text=True,
    )
    return json.loads(proc.stdout)


def iter_inputs_by_tick(parsed: Dict[str, Any]) -> Iterator[tuple[int, dict]]:
    # node-haxball agrupa eventos por frameNo. Entre ellos verás los de tipo input/keys.
    # Esta función deja una interfaz limpia: (tick, {playerId: keyMask})
    by_frame: dict[int, dict] = {}
    for ev in parsed.get("events", []):
        fn = ev.get("frameNo")
        if fn is None:
            continue
        if (
            ev.get("type") == "Input"
        ):  # nombre orientativo: mira el campo real en tu JSON
            pid = ev.get("playerId")
            mask = ev.get("input")
            if pid is None or mask is None:
                continue
            by_frame.setdefault(fn, {})[pid] = mask

    for tick in sorted(by_frame.keys()):
        yield tick, by_frame[tick]
