# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Personal preferences

For my personal AI preferences in this repo, read `Personal.md` when relevant.

In particular, when investigating the codebase or planning changes, follow the CodeGraph exploration rules from `Personal.md`.

## Workflow

Use this flow for non-trivial work:

1. Investigate before implementing.
2. Use Plan Mode before multi-file or architectural changes.
3. Wait for explicit approval before implementation.
4. Implement with TDD when behavior changes.
5. Run the narrowest relevant verification command.
6. Review the final diff in a fresh context.

## Engineering principles

- Prefer clean, simple, maintainable code.
- Avoid speculative abstractions.
- Avoid unrelated refactors.
- Show test/build/lint evidence before saying a task is done.

## Commands

### Python

```bash
# Install in editable mode
pip install -e ".[dev]"

# Run all tests
python -m pytest src/tests -v

# Run a single test file
python -m pytest src/tests/unit/test_actions.py -v

# Run a single test by name
python -m pytest src/tests/unit/test_actions.py::test_name -v

# Type checking
mypy src/haxmetrics

# Formatting
black src/haxmetrics
isort src/haxmetrics
flake8 src/haxmetrics
```

### Node.js (Decoders)

```bash
npm install

# Decode a replay to JSON (recommended)
npm run decode:v2 -- <file.hbr2> [output.json]

# Full decoder V1 (original Haxball implementation)
npm run decode:full -- <file.hbr2> [output.json]

# Basic metadata-only decoder
npm run decode -- <file.hbr2> [output.json]

# Debug: list internal classes in replay-min.js
npm run debug:replay
```

## Architecture

HaxMetrics parses Haxball `.hbr2` binary replay files. There are two parallel implementations:

- **Python parser** (`src/haxmetrics/`) — modular, typed, test-driven; primary development target
- **Node.js decoders** (`decode_hbr2*.js`) — leverage the official Haxball JS runtime (`node-haxball`) to extract complete JSON; V2 is recommended

### HBR2 Format (sequential sections)

```
Header (12 bytes, raw)          → magic "HBR2", version, duration
zlib-compressed body (wbits=-15)
  Messages                      → chat messages with frame timestamps
  RoomBasic                     → room name, locks, score/time limits
  Stadium                       → predefined (types 0–9) or custom (type 0xFF) map geometry
  GameState                     → ball/disc positions, scores
  Players                       → player list with physics discs
  TeamColors                    → team color customization
  Actions                       → timestamped gameplay events (24 types, see below)
```

The full byte-by-byte spec is in `docs/HBR2_PARSING_GUIDE.md`.

### Python Parser Layer Stack

```
src/haxmetrics/
├── binary_reader.py     # Low-level: read_byte, read_varint, read_string, etc. (big-endian)
├── models/
│   ├── header.py        # Header dataclass — first 12 bytes before decompression
│   ├── messages.py      # Messages collection — first section after decompression
│   ├── room.py          # RoomBasic — second section
│   ├── stadium/         # Stadium hierarchy — predefined and custom map geometry
│   ├── game.py          # GameState — disc positions and scores
│   ├── player.py        # Player dataclass with embedded disc physics
│   ├── team_color.py    # TeamColors
│   └── actions/         # Actions — 24 types parsed via factory function
├── parser.py            # ⚠️ Legacy Parser class — deprecated, removal in v2.0.0
└── cli.py               # Click CLI entry point (haxmetrics command)
```

### Key Patterns

**All models are frozen dataclasses** validated in `__post_init__`. Each exposes a `parse(reader: BinaryReader)` classmethod and a `to_dict()` method.

**Collection classes** (`Messages`, `Actions`) wrap a list with `__len__`, `__iter__`, `__getitem__`, and domain-specific filter methods.

**Actions use a factory**: `parse_action(header, reader)` dispatches to the correct subclass based on `header.action_type` (0–23). `ActionHeader` carries `frame_delta`, `sender`, and `action_type`; absolute frame numbers are computed by the `Actions` collection.

**BinaryReader** accepts `enable_logging=True` to emit read traces — useful when debugging parser failures at a specific byte offset. The `hex_dump()` utility and `DebugParser` in `src/haxmetrics/debug/` assist with section-level tracing.

### Adding a New Action Type

1. Create `src/haxmetrics/models/actions/type_N.py` with a frozen dataclass that extends `Action` and implements `parse(header, reader)` + `to_dict()`.
2. Register it in the factory in `src/haxmetrics/models/actions/__init__.py`.
3. Add unit tests in `src/tests/unit/test_actions.py` and integration tests in `src/tests/integration/test_actions_with_fixtures.py` using `.hbr2` fixtures from `src/tests/fixtures/actions/`.

### Endianness

`BinaryReader` defaults to **big-endian**. The HBR2 format uses big-endian throughout except for the zlib stream itself.

## Agent skills

### Issue tracker

Issues live in GitHub Issues for `thomasruizfdez/HaxMetrics`. See `docs/agents/issue-tracker.md`.

### Triage labels

Using default canonical label names (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`). See `docs/agents/triage-labels.md`.

### Domain docs

Single-context layout — `CONTEXT.md` + `docs/adr/` at the repo root (neither exists yet; proceed silently). See `docs/agents/domain.md`.
