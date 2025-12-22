"""
Unit tests for Actions parsing.

Tests all 24 action types following HBR2 Parsing Guide section 7.

Fixtures used:
- src/tests/fixtures/actions/*.hbr2
"""

from pathlib import Path
import struct

import pytest

from haxmetrics.binary_reader import BinaryReader
from haxmetrics.models.actions import (
    ActionType,
    ActionHeader,
    Action,
    Actions,
    parse_action,
    MessageAction,
    ToggleChatAction,
    ChangeStadiumAction,
    PlayerInput,
    ChatMessageAction,
    PlayerJoinedAction,
    PlayerLeftAction,
    MatchStartAction,
    MatchStoppedAction,
    ChangePausedAction,
    ChangeGameSettingAction,
    StadiumUpdateAction,
    PlayerTeamChangeAction,
    ChangeTeamsLockAction,
    PlayerAdminChangeAction,
    AutoTeamBalanceAction,
    DesyncedAction,
    BroadcastPingsAction,
    AvatarChangeAction,
    TeamColorsChangeAction,
    PlayerOrderChangeAction,
    KickRateLimitAction,
    PlayerAvatarSetAction,
    DiscUpdateAction,
)

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures" / "actions"


class TestActionType:
    """Test ActionType enum."""
    
    def test_action_type_values(self):
        """Should have all 24 action types with correct values."""
        assert ActionType.MESSAGE == 0
        assert ActionType.TOGGLE_CHAT == 1
        assert ActionType.CHANGE_STADIUM == 2
        assert ActionType.PLAYER_INPUT == 3
        assert ActionType.CHAT_MESSAGE == 4
        assert ActionType.PLAYER_JOINED == 5
        assert ActionType.PLAYER_LEFT == 6
        assert ActionType.MATCH_START == 7
        assert ActionType.MATCH_STOPPED == 8
        assert ActionType.CHANGE_PAUSED == 9
        assert ActionType.CHANGE_GAME_SETTING == 10
        assert ActionType.STADIUM_UPDATE == 11
        assert ActionType.PLAYER_TEAM_CHANGE == 12
        assert ActionType.CHANGE_TEAMS_LOCK == 13
        assert ActionType.PLAYER_ADMIN_CHANGE == 14
        assert ActionType.AUTO_TEAM_BALANCE == 15
        assert ActionType.DESYNCED == 16
        assert ActionType.BROADCAST_PINGS == 17
        assert ActionType.AVATAR_CHANGE == 18
        assert ActionType.TEAM_COLORS_CHANGE == 19
        assert ActionType.PLAYER_ORDER_CHANGE == 20
        assert ActionType.KICK_RATE_LIMIT == 21
        assert ActionType.PLAYER_AVATAR_SET == 22
        assert ActionType.DISC_UPDATE == 23


class TestActionHeader:
    """Test ActionHeader parsing."""
    
    def test_parse_action_header(self):
        """Should parse action header correctly."""
        # frame_delta=10 (varint), sender=5 (uint16_be), type=3 (byte)
        data = bytes([10, 0, 5, 3])
        reader = BinaryReader(data)
        
        header = ActionHeader.parse(reader)
        
        assert header.frame_delta == 10
        assert header.sender == 5
        assert header.action_type == ActionType.PLAYER_INPUT
    
    def test_action_header_frame_delta_varint(self):
        """Should handle varint frame_delta correctly."""
        # frame_delta=300 as varint (0xAC 0x02), sender=0, type=0
        data = bytes([0xAC, 0x02, 0, 0, 0])
        reader = BinaryReader(data)
        
        header = ActionHeader.parse(reader)
        
        assert header.frame_delta == 300
        assert header.sender == 0
        assert header.action_type == ActionType.MESSAGE
    
    def test_action_header_sender_uint16_be(self):
        """Should parse sender as uint16_be."""
        # frame_delta=1, sender=0x0105 (big-endian = 261), type=0
        data = bytes([1, 0x01, 0x05, 0])
        reader = BinaryReader(data)
        
        header = ActionHeader.parse(reader)
        
        assert header.sender == 0x0105  # 261 in decimal
    
    def test_action_header_to_dict(self):
        """Should serialize to dict correctly."""
        # frame_delta=5, sender=10, type=3
        data = bytes([5, 0, 10, 3])
        reader = BinaryReader(data)
        
        header = ActionHeader.parse(reader)
        result = header.to_dict()
        
        assert result["frame_delta"] == 5
        assert result["sender"] == 10
        assert result["action_type"] == 3
        assert result["action_type_name"] == "PLAYER_INPUT"


class TestMessageAction:
    """Test Type 0: Message action."""
    
    def test_parse_message_action_fields(self):
        """Should parse message action fields correctly."""
        # Create minimal message action data
        # header: frame_delta=1, sender=0, type=0
        header_data = bytes([1, 0, 0, 0])
        # message: "Test" (varint length=5, then 4 bytes)
        message_data = bytes([5]) + b"Test"
        # color: 0xFF0000FF (red) as uint32_be
        color_data = struct.pack(">I", 0xFF0000FF)
        # style: 1 (byte)
        style_data = bytes([1])
        # sound: 1 (byte)
        sound_data = bytes([1])
        
        data = header_data + message_data + color_data + style_data + sound_data
        reader = BinaryReader(data)
        
        header = ActionHeader.parse(reader)
        action = MessageAction.parse(header, reader)
        
        assert action.message == "Test"
        assert action.color == 0xFF0000FF
        assert action.style == 1
        assert action.sound == 1
        assert action.frame_delta == 1
        assert action.sender == 0
    
    def test_message_action_to_dict(self):
        """Should serialize message action to dict."""
        header_data = bytes([1, 0, 0, 0])
        message_data = bytes([4]) + b"Hi!"
        color_data = struct.pack(">I", 0xFFFFFFFF)
        style_data = bytes([0])
        sound_data = bytes([0])
        
        data = header_data + message_data + color_data + style_data + sound_data
        reader = BinaryReader(data)
        
        header = ActionHeader.parse(reader)
        action = MessageAction.parse(header, reader)
        result = action.to_dict()
        
        assert result["type"] == "message"
        assert result["message"] == "Hi!"
        assert result["color"] == 0xFFFFFFFF
        assert result["style"] == 0
        assert result["sound"] == 0


class TestToggleChatAction:
    """Test Type 1: Toggle chat action."""
    
    def test_parse_toggle_chat_action(self):
        """Should parse toggle chat action correctly."""
        # header + value=1
        data = bytes([1, 0, 0, 1, 1])
        reader = BinaryReader(data)
        
        header = ActionHeader.parse(reader)
        action = ToggleChatAction.parse(header, reader)
        
        assert action.value == 1
    
    def test_toggle_chat_to_dict(self):
        """Should include enabled boolean in dict."""
        data = bytes([1, 0, 0, 1, 1])
        reader = BinaryReader(data)
        
        header = ActionHeader.parse(reader)
        action = ToggleChatAction.parse(header, reader)
        result = action.to_dict()
        
        assert result["type"] == "toggle_chat"
        assert result["value"] == 1
        assert result["enabled"] is True


class TestPlayerInput:
    """Test Type 3: Player input action."""
    
    def test_parse_player_input(self):
        """Should parse player input correctly."""
        # header + input=0x0001 (left) as uint16_be
        data = bytes([1, 0, 1, 3, 0x00, 0x01])
        reader = BinaryReader(data)
        
        header = ActionHeader.parse(reader)
        action = PlayerInput.parse(header, reader)
        
        assert action.input == 0x0001
    
    def test_player_input_bitfield_left(self):
        """Should detect left key press."""
        data = bytes([1, 0, 1, 3, 0x00, 0x01])  # bit0 = left
        reader = BinaryReader(data)
        
        header = ActionHeader.parse(reader)
        action = PlayerInput.parse(header, reader)
        
        assert action.is_left is True
        assert action.is_right is False
        assert action.is_up is False
        assert action.is_down is False
        assert action.is_kick is False
    
    def test_player_input_bitfield_right(self):
        """Should detect right key press."""
        data = bytes([1, 0, 1, 3, 0x00, 0x02])  # bit1 = right
        reader = BinaryReader(data)
        
        header = ActionHeader.parse(reader)
        action = PlayerInput.parse(header, reader)
        
        assert action.is_left is False
        assert action.is_right is True
        assert action.is_up is False
        assert action.is_down is False
        assert action.is_kick is False
    
    def test_player_input_bitfield_up(self):
        """Should detect up key press."""
        data = bytes([1, 0, 1, 3, 0x00, 0x04])  # bit2 = up
        reader = BinaryReader(data)
        
        header = ActionHeader.parse(reader)
        action = PlayerInput.parse(header, reader)
        
        assert action.is_up is True
    
    def test_player_input_bitfield_down(self):
        """Should detect down key press."""
        data = bytes([1, 0, 1, 3, 0x00, 0x08])  # bit3 = down
        reader = BinaryReader(data)
        
        header = ActionHeader.parse(reader)
        action = PlayerInput.parse(header, reader)
        
        assert action.is_down is True
    
    def test_player_input_bitfield_kick(self):
        """Should detect kick key press."""
        data = bytes([1, 0, 1, 3, 0x00, 0x10])  # bit4 = kick
        reader = BinaryReader(data)
        
        header = ActionHeader.parse(reader)
        action = PlayerInput.parse(header, reader)
        
        assert action.is_kick is True
    
    def test_player_input_bitfield_multiple(self):
        """Should detect multiple keys pressed."""
        data = bytes([1, 0, 1, 3, 0x00, 0x15])  # bits 0,2,4 = left+up+kick
        reader = BinaryReader(data)
        
        header = ActionHeader.parse(reader)
        action = PlayerInput.parse(header, reader)
        
        assert action.is_left is True
        assert action.is_right is False
        assert action.is_up is True
        assert action.is_down is False
        assert action.is_kick is True


class TestMatchStartAction:
    """Test Type 7: Match start action."""
    
    def test_parse_match_start_no_additional_data(self):
        """Should parse match start with no additional data."""
        # header only
        data = bytes([1, 0, 0, 7])
        reader = BinaryReader(data)
        
        header = ActionHeader.parse(reader)
        action = MatchStartAction.parse(header, reader)
        
        assert action.frame_delta == 1
        assert action.sender == 0
        assert action.action_type == ActionType.MATCH_START


class TestMatchStoppedAction:
    """Test Type 8: Match stopped action."""
    
    def test_parse_match_stopped_no_additional_data(self):
        """Should parse match stopped with no additional data."""
        # header only
        data = bytes([1, 0, 0, 8])
        reader = BinaryReader(data)
        
        header = ActionHeader.parse(reader)
        action = MatchStoppedAction.parse(header, reader)
        
        assert action.frame_delta == 1
        assert action.sender == 0
        assert action.action_type == ActionType.MATCH_STOPPED


class TestDesyncedAction:
    """Test Type 16: Desynced action (synthetic)."""
    
    def test_parse_desynced_no_additional_data(self):
        """Should parse desynced with no additional data."""
        # Note: Untested with real fixture
        # header only
        data = bytes([1, 0, 0, 16])
        reader = BinaryReader(data)
        
        header = ActionHeader.parse(reader)
        action = DesyncedAction.parse(header, reader)
        
        assert action.frame_delta == 1
        assert action.sender == 0
        assert action.action_type == ActionType.DESYNCED


class TestPlayerTeamChangeAction:
    """Test Type 12: Player team change action."""
    
    def test_parse_player_team_change(self):
        """Should parse player team change correctly."""
        # header + player_id=100 (uint32_be) + team_id=1 (signed byte)
        data = bytes([1, 0, 0, 12]) + struct.pack(">I", 100) + struct.pack("b", 1)
        reader = BinaryReader(data)
        
        header = ActionHeader.parse(reader)
        action = PlayerTeamChangeAction.parse(header, reader)
        
        assert action.player_id == 100
        assert action.team_id == 1


class TestStadiumUpdateAction:
    """Test Type 11: Stadium update action (synthetic)."""
    
    def test_parse_stadium_update(self):
        """Should parse stadium update correctly."""
        # Note: Untested with real fixture
        # header + stadium_json
        stadium_json = '{"name":"Test"}'
        data = bytes([1, 0, 0, 11]) + bytes([len(stadium_json) + 1]) + stadium_json.encode()
        reader = BinaryReader(data)
        
        header = ActionHeader.parse(reader)
        action = StadiumUpdateAction.parse(header, reader)
        
        assert action.stadium_json == stadium_json


class TestPlayerOrderChangeAction:
    """Test Type 20: Player order change action (synthetic)."""
    
    def test_parse_player_order_change(self):
        """Should parse player order change correctly."""
        # Note: Untested with real fixture
        # header + count=2 + player_ids=[10, 20]
        data = bytes([1, 0, 0, 20, 2]) + struct.pack(">I", 10) + struct.pack(">I", 20)
        reader = BinaryReader(data)
        
        header = ActionHeader.parse(reader)
        action = PlayerOrderChangeAction.parse(header, reader)
        
        assert action.count == 2
        assert action.player_ids == [10, 20]


class TestKickRateLimitAction:
    """Test Type 21: Kick rate limit action (synthetic)."""
    
    def test_parse_kick_rate_limit(self):
        """Should parse kick rate limit correctly."""
        # Note: Untested with real fixture
        # header + min=1 + rate=2 + burst=3 (all uint32_be)
        data = bytes([1, 0, 0, 21]) + struct.pack(">I", 1) + struct.pack(">I", 2) + struct.pack(">I", 3)
        reader = BinaryReader(data)
        
        header = ActionHeader.parse(reader)
        action = KickRateLimitAction.parse(header, reader)
        
        assert action.min == 1
        assert action.rate == 2
        assert action.burst == 3


class TestPlayerAvatarSetAction:
    """Test Type 22: Player avatar set action (synthetic)."""
    
    def test_parse_player_avatar_set(self):
        """Should parse player avatar set correctly."""
        # Note: Untested with real fixture
        # header + player_id=100 (uint32_be) + avatar="AB"
        avatar = "AB"
        data = bytes([1, 0, 0, 22]) + struct.pack(">I", 100) + bytes([len(avatar) + 1]) + avatar.encode()
        reader = BinaryReader(data)
        
        header = ActionHeader.parse(reader)
        action = PlayerAvatarSetAction.parse(header, reader)
        
        assert action.player_id == 100
        assert action.avatar == avatar


class TestActionsCollection:
    """Test Actions collection."""
    
    def test_actions_len(self):
        """Should return correct length."""
        # Create simple actions data (2 match start actions)
        data = bytes([1, 0, 0, 7, 1, 0, 0, 7])
        reader = BinaryReader(data)
        
        actions = Actions.parse(reader)
        
        assert len(actions) == 2
    
    def test_actions_iteration(self):
        """Should support iteration."""
        data = bytes([1, 0, 0, 7, 1, 0, 0, 8])
        reader = BinaryReader(data)
        
        actions = Actions.parse(reader)
        action_list = list(actions)
        
        assert len(action_list) == 2
        assert action_list[0].action_type == ActionType.MATCH_START
        assert action_list[1].action_type == ActionType.MATCH_STOPPED
    
    def test_actions_getitem(self):
        """Should support indexing."""
        data = bytes([1, 0, 0, 7, 1, 0, 0, 8])
        reader = BinaryReader(data)
        
        actions = Actions.parse(reader)
        
        assert actions[0].action_type == ActionType.MATCH_START
        assert actions[1].action_type == ActionType.MATCH_STOPPED
    
    def test_filter_by_type(self):
        """Should filter actions by type."""
        # Create 3 actions: start, stop, start
        data = bytes([1, 0, 0, 7, 1, 0, 0, 8, 1, 0, 0, 7])
        reader = BinaryReader(data)
        
        actions = Actions.parse(reader)
        start_actions = actions.filter_by_type(ActionType.MATCH_START)
        
        assert len(start_actions) == 2
        assert all(a.action_type == ActionType.MATCH_START for a in start_actions)
    
    def test_filter_by_sender(self):
        """Should filter actions by sender."""
        # Create actions with different senders
        data = bytes([1, 0, 1, 7, 1, 0, 2, 7, 1, 0, 1, 7])
        reader = BinaryReader(data)
        
        actions = Actions.parse(reader)
        sender1_actions = actions.filter_by_sender(1)
        
        assert len(sender1_actions) == 2
        assert all(a.sender == 1 for a in sender1_actions)
    
    def test_get_absolute_frames(self):
        """Should calculate absolute frame numbers."""
        # frame_deltas: 10, 5, 3
        data = bytes([10, 0, 0, 7, 5, 0, 0, 7, 3, 0, 0, 7])
        reader = BinaryReader(data)
        
        actions = Actions.parse(reader)
        absolute_frames = actions.get_absolute_frames()
        
        assert absolute_frames == [10, 15, 18]  # 10, 10+5, 10+5+3


class TestParseActionFactory:
    """Test parse_action factory function."""
    
    def test_parse_action_creates_correct_type(self):
        """Should create correct action type based on header."""
        # Create header for Type 7 (MatchStart)
        header = ActionHeader(frame_delta=1, sender=0, action_type=ActionType.MATCH_START)
        reader = BinaryReader(bytes([]))
        
        action = parse_action(header, reader)
        
        assert isinstance(action, MatchStartAction)
    
    def test_parse_action_invalid_type_raises_error(self):
        """Should raise ValueError for invalid action type."""
        # ActionType enum raises ValueError for invalid type during header parsing
        data = bytes([1, 0, 0, 24])  # 24 is invalid (only 0-23 valid)
        reader = BinaryReader(data)
        
        with pytest.raises(ValueError):
            header = ActionHeader.parse(reader)
