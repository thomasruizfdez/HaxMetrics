# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- New modular parser architecture following HBR2 format specification
- `Header` class for header parsing (PR #1)
- `Messages` class for messages parsing (PR #1)
- `RoomBasic` class for room basic fields (PR #2)
- Comprehensive documentation in `docs/HBR2_PARSING_GUIDE.md`
- Reverse engineering documentation in `docs/GAME_MIN_REVERSE_ENGINEERING.md`
- BinaryReader with full HBR2 format support and JavaScript equivalents
- Type hints throughout the codebase
- Comprehensive unit tests for new parser components

### Deprecated
- `Parser` class in `parser.py` - Use new modular parser (removal in v2.0.0)
  - Replace with: `Header.parse()`, `Messages.parse()`, `RoomBasic.parse()`, etc.
- `ReplayMessages` class in `replay_messages.py` - Replaced by `Messages` (removal in v2.0.0)
  - Replace with: `haxmetrics.models.messages.Messages`

### Changed
- All comments and docstrings translated from Spanish to English
- Binary reader methods aligned with HBR2 guide naming conventions
- Error messages standardized to English
- Improved documentation with JavaScript method equivalents

### Fixed
- Consistent big-endian/little-endian byte order handling
- Better error messages for binary parsing failures

## [1.0.0] - TBD

### Added
- Complete HBR2 parsing guide documentation
- Initial parser implementation with support for:
  - Header parsing (magic, version, duration)
  - Messages parsing (game events timeline)
  - Room basic information (name, locked status, score/time limits)
  - Player data parsing
  - Team colors parsing
  - Actions parsing
  - Stadium data structures

[Unreleased]: https://github.com/thomasruizfdez/HaxMetrics/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/thomasruizfdez/HaxMetrics/releases/tag/v1.0.0
