# Actions Parser Implementation Summary

## Overview
Implemented a complete actions parser for HaxBall HBR2 replay files following SOLID principles and the HBR2 Parsing Guide (Section 7).

## Implementation Details

### Architecture

#### 1. Core Classes
- **ActionType** (`action_type.py`): IntEnum with all 24 action types (0-23)
- **ActionHeader** (`action_header.py`): Immutable dataclass for universal action header (frame_delta, sender, action_type)
- **Action** (`base.py`): Abstract base class that all action types inherit from
- **Actions** (`actions_collection.py`): Collection class with helper methods
- **parse_action()**: Factory function that creates the appropriate action type based on header

#### 2. Action Types (24 total)
All action types are immutable dataclasses (`frozen=True`) that:
- Inherit from `Action` base class
- Implement `parse(header, reader)` class method
- Implement `to_dict()` instance method
- Provide convenient properties where appropriate

**Implemented Actions:**
- Type 0: MessageAction - System messages with color/style
- Type 1: ToggleChatAction - Toggle chat on/off
- Type 2: ChangeStadiumAction - Change stadium/map
- Type 3: PlayerInput - Player keyboard input with bitfield properties
- Type 4: ChatMessageAction - Player chat messages
- Type 5: PlayerJoinedAction - Player joins room
- Type 6: PlayerLeftAction - Player leaves room
- Type 7: MatchStartAction - Match starts
- Type 8: MatchStoppedAction - Match stops
- Type 9: ChangePausedAction - Pause/unpause game
- Type 10: ChangeGameSettingAction - Change settings (score/time limits)
- Type 11: StadiumUpdateAction - Update stadium (⚠️ synthetic test)
- Type 12: PlayerTeamChangeAction - Player changes team
- Type 13: ChangeTeamsLockAction - Lock/unlock teams
- Type 14: PlayerAdminChangeAction - Change admin status
- Type 15: AutoTeamBalanceAction - Toggle auto balance
- Type 16: DesyncedAction - Desync notification (⚠️ synthetic test)
- Type 17: BroadcastPingsAction - Player ping updates
- Type 18: AvatarChangeAction - Change player avatar
- Type 19: TeamColorsChangeAction - Change team colors
- Type 20: PlayerOrderChangeAction - Reorder players (⚠️ synthetic test)
- Type 21: KickRateLimitAction - Set kick rate limits (⚠️ synthetic test)
- Type 22: PlayerAvatarSetAction - Admin sets player avatar (⚠️ synthetic test)
- Type 23: DiscUpdateAction - Disc/ball position updates

### Key Features

#### PlayerInput Bitfield Properties
PlayerInput action provides convenient boolean properties:
- `is_left`: Check if left key is pressed
- `is_right`: Check if right key is pressed
- `is_up`: Check if up key is pressed
- `is_down`: Check if down key is pressed
- `is_kick`: Check if kick key is pressed

#### Actions Collection Methods
The `Actions` class provides:
- `__len__()`: Get count of actions
- `__iter__()`: Iterate over actions
- `__getitem__()`: Access actions by index
- `filter_by_type(action_type)`: Filter actions by type
- `filter_by_sender(sender)`: Filter actions by sender
- `get_absolute_frames()`: Calculate absolute frame numbers from frame deltas
- `to_dict()`: Serialize to dictionary

### Parsing Specifications

All parsing follows the HBR2 Parsing Guide exactly:
- Frame deltas use **varint** encoding (1-5 bytes)
- Sender IDs are **uint16_be** (2 bytes, big-endian)
- Action types are **byte** (1 byte, 0-23)
- Strings use **varint-prefixed UTF-8** encoding
- Multi-byte integers use **big-endian** byte order
- Signed bytes use `read_signed_byte()` for team IDs

### BinaryReader Enhancements

Added two methods to `BinaryReader`:
- `read_signed_byte()`: Read signed byte (-128 to 127) for team IDs
- `is_eof()`: Alias for `eof()` for consistency

## Testing

### Test Coverage
Created comprehensive test suite (`test_actions.py`) with **32 tests**:

1. **ActionType enum** (1 test)
   - Verify all 24 action types have correct values

2. **ActionHeader parsing** (4 tests)
   - Parse header correctly
   - Handle varint frame_delta
   - Parse uint16_be sender
   - Serialize to dict

3. **Individual action types** (15 tests)
   - MessageAction fields and to_dict()
   - ToggleChatAction
   - PlayerInput with all bitfield properties
   - Match start/stopped (no additional data)
   - DesyncedAction (synthetic)
   - PlayerTeamChangeAction
   - StadiumUpdateAction (synthetic)
   - PlayerOrderChangeAction (synthetic)
   - KickRateLimitAction (synthetic)
   - PlayerAvatarSetAction (synthetic)

4. **Actions collection** (6 tests)
   - Length, iteration, indexing
   - Filter by type
   - Filter by sender
   - Calculate absolute frames

5. **Factory function** (2 tests)
   - Creates correct action type
   - Handles invalid types

### Test Results
✅ All 32 tests pass successfully
✅ No existing tests broken

### Synthetic Tests
5 action types are tested synthetically (no real fixtures available):
- Type 11: StadiumUpdate
- Type 16: Desynced
- Type 20: PlayerOrderChange
- Type 21: KickRateLimit
- Type 22: PlayerAvatarSet

These types are rare in real games but are fully implemented according to spec.

## Code Quality

### SOLID Principles
- **Single Responsibility**: Each action type has one responsibility
- **Open/Closed**: Easy to add new action types by extending Action
- **Liskov Substitution**: All actions can be used interchangeably through Action interface
- **Interface Segregation**: Action interface is minimal (parse + to_dict)
- **Dependency Inversion**: Depends on abstractions (Action) not concrete types

### Other Quality Metrics
- ✅ Immutable dataclasses (`frozen=True`)
- ✅ Type hints throughout
- ✅ Comprehensive docstrings
- ✅ English comments
- ✅ Follows HBR2 spec exactly
- ✅ No breaking changes to existing code

## Usage Example

See `examples/parse_actions_example.py` for a complete example of:
- Parsing actions from binary data
- Iterating over actions
- Filtering by type and sender
- Calculating absolute frames
- Using PlayerInput bitfield properties

## Files Changed

### New Files
- `src/haxmetrics/models/actions/action_type.py`
- `src/haxmetrics/models/actions/action_header.py`
- `src/haxmetrics/models/actions/base.py`
- `src/haxmetrics/models/actions/actions_collection.py`
- `src/haxmetrics/models/actions/__init__.py`
- `src/tests/unit/test_actions.py`
- `examples/parse_actions_example.py`

### Modified Files
- `src/haxmetrics/binary_reader.py` - Added read_signed_byte() and is_eof()
- All 24 action type files updated to follow new architecture

## Next Steps

1. ✅ Core architecture implemented
2. ✅ All 24 action types implemented
3. ✅ Comprehensive test suite created
4. ⏳ Code review requested
5. ⏳ Security scan (CodeQL)
6. ⏳ Integration with full replay parser

## Notes

- All parsing follows HBR2_PARSING_GUIDE.md Section 7
- 5 action types have synthetic tests (rare in real games)
- PlayerInput includes convenient bitfield properties
- Actions collection provides filtering and frame calculation
- No breaking changes to existing code
- All tests pass (32/32)
