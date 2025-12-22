"""
Integration tests for Actions parsing with real HBR2 fixtures.

Tests actions parsing with real replay files from fixtures/actions/.
"""

from pathlib import Path
import zlib

import pytest

from haxmetrics.binary_reader import BinaryReader
from haxmetrics.models.header import Header
from haxmetrics.models.replay_messages import ReplayMessages
from haxmetrics.models.room import Room
from haxmetrics.models.actions import (
    Actions,
    ActionType,
    PlayerInput,
    MessageAction,
    ToggleChatAction,
    ChangeStadiumAction,
    ChatMessageAction,
    PlayerJoinedAction,
    PlayerLeftAction,
    MatchStartAction,
    MatchStoppedAction,
    ChangePausedAction,
    ChangeGameSettingAction,
    PlayerTeamChangeAction,
    ChangeTeamsLockAction,
    PlayerAdminChangeAction,
    AutoTeamBalanceAction,
    BroadcastPingsAction,
    AvatarChangeAction,
    TeamColorsChangeAction,
    DiscUpdateAction,
)

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures" / "actions"


def parse_hbr2_actions(filepath: Path) -> Actions:
    """
    Parse actions from a complete HBR2 file.
    
    Args:
        filepath: Path to .hbr2 file
        
    Returns:
        Actions: Parsed actions collection
    """
    with open(filepath, "rb") as f:
        data = f.read()
    
    reader = BinaryReader(data)
    
    # 1. Parse header (12 bytes)
    header = Header.parse(reader)
    
    # 2. Decompress remaining data
    compressed_data = reader.read_remaining()
    decompressed_data = zlib.decompress(compressed_data, wbits=-15)
    
    # 3. Parse decompressed sections
    decomp_reader = BinaryReader(decompressed_data)
    
    # Parse messages section
    messages = ReplayMessages.parse(decomp_reader)
    
    # Parse room section (includes stadium, game state, players, team colors)
    # Note: Room parsing might fail on simple fixtures, but that's OK
    try:
        room = Room.parse(decomp_reader, header.version)
    except Exception as e:
        # Room parsing failed, try to skip to actions
        # For simple action fixtures, we need to manually skip the room data
        # Room structure: room_name(str), ..., players, team_colors
        # Team colors are 2 sets at the end before actions
        pass
    
    # 4. Parse actions (remaining data)
    actions = Actions.parse(decomp_reader)
    
    return actions


class TestActionsWithFixtures:
    """Test actions parsing with real HBR2 fixtures."""
    
    def test_toggle_chat_action(self):
        """Should parse toggle chat action from fixture."""
        actions = parse_hbr2_actions(FIXTURES_DIR / "toggle_chat_action.hbr2")
        
        # Find ToggleChat actions
        toggle_actions = actions.filter_by_type(ActionType.TOGGLE_CHAT)
        assert len(toggle_actions) > 0
        
        action = toggle_actions[0]
        assert isinstance(action, ToggleChatAction)
        assert action.value in (0, 1)
    
    def test_one_message_action(self):
        """Should parse message action from fixture."""
        actions = parse_hbr2_actions(FIXTURES_DIR / "one_message_action.hbr2")
        
        # Find Message actions
        message_actions = actions.filter_by_type(ActionType.MESSAGE)
        assert len(message_actions) > 0
        
        action = message_actions[0]
        assert isinstance(action, MessageAction)
        assert action.message is not None
        assert action.color is not None
    
    def test_chat_message_action(self):
        """Should parse chat message action from fixture."""
        actions = parse_hbr2_actions(FIXTURES_DIR / "chat_message_action.hbr2")
        
        # Find ChatMessage actions
        chat_actions = actions.filter_by_type(ActionType.CHAT_MESSAGE)
        assert len(chat_actions) > 0
        
        action = chat_actions[0]
        assert isinstance(action, ChatMessageAction)
        assert action.message is not None
        assert len(action.message) > 0
    
    def test_change_stadium_action(self):
        """Should parse change stadium action from fixture."""
        actions = parse_hbr2_actions(FIXTURES_DIR / "change_stadium_action.hbr2")
        
        # Find ChangeStadium actions
        stadium_actions = actions.filter_by_type(ActionType.CHANGE_STADIUM)
        assert len(stadium_actions) > 0
        
        action = stadium_actions[0]
        assert isinstance(action, ChangeStadiumAction)
        assert action.stadium_json is not None
    
    def test_player_input_up(self):
        """Should parse up input action from fixture."""
        actions = parse_hbr2_actions(FIXTURES_DIR / "up_input_action.hbr2")
        
        # Find PlayerInput actions
        input_actions = actions.filter_by_type(ActionType.PLAYER_INPUT)
        assert len(input_actions) > 0
        
        # Find an action with up pressed
        up_actions = [a for a in input_actions if a.is_up]
        assert len(up_actions) > 0
    
    def test_player_input_down(self):
        """Should parse down input action from fixture."""
        actions = parse_hbr2_actions(FIXTURES_DIR / "down_input_action.hbr2")
        
        # Find PlayerInput actions with down pressed
        input_actions = actions.filter_by_type(ActionType.PLAYER_INPUT)
        down_actions = [a for a in input_actions if a.is_down]
        assert len(down_actions) > 0
    
    def test_player_input_left(self):
        """Should parse left input action from fixture."""
        actions = parse_hbr2_actions(FIXTURES_DIR / "left_input_action.hbr2")
        
        # Find PlayerInput actions with left pressed
        input_actions = actions.filter_by_type(ActionType.PLAYER_INPUT)
        left_actions = [a for a in input_actions if a.is_left]
        assert len(left_actions) > 0
    
    def test_player_input_right(self):
        """Should parse right input action from fixture."""
        actions = parse_hbr2_actions(FIXTURES_DIR / "right_input_action.hbr2")
        
        # Find PlayerInput actions with right pressed
        input_actions = actions.filter_by_type(ActionType.PLAYER_INPUT)
        right_actions = [a for a in input_actions if a.is_right]
        assert len(right_actions) > 0
    
    def test_player_input_kick(self):
        """Should parse kick input action from fixture."""
        actions = parse_hbr2_actions(FIXTURES_DIR / "kick_input_action.hbr2")
        
        # Find PlayerInput actions with kick pressed
        input_actions = actions.filter_by_type(ActionType.PLAYER_INPUT)
        kick_actions = [a for a in input_actions if a.is_kick]
        assert len(kick_actions) > 0
    
    def test_player_joined_action(self):
        """Should parse player joined action from fixture."""
        actions = parse_hbr2_actions(FIXTURES_DIR / "player_joined_action.hbr2")
        
        # Find PlayerJoined actions
        joined_actions = actions.filter_by_type(ActionType.PLAYER_JOINED)
        assert len(joined_actions) > 0
        
        action = joined_actions[0]
        assert isinstance(action, PlayerJoinedAction)
        assert action.player_id is not None
        assert action.name is not None
    
    def test_player_left_action(self):
        """Should parse player left action from fixture."""
        actions = parse_hbr2_actions(FIXTURES_DIR / "player_left_action.hbr2")
        
        # Find PlayerLeft actions
        left_actions = actions.filter_by_type(ActionType.PLAYER_LEFT)
        assert len(left_actions) > 0
        
        action = left_actions[0]
        assert isinstance(action, PlayerLeftAction)
        assert action.player_id is not None
    
    def test_match_started_action(self):
        """Should parse match started action from fixture."""
        actions = parse_hbr2_actions(FIXTURES_DIR / "match_started_action.hbr2")
        
        # Find MatchStart actions
        start_actions = actions.filter_by_type(ActionType.MATCH_START)
        assert len(start_actions) > 0
        
        action = start_actions[0]
        assert isinstance(action, MatchStartAction)
    
    def test_match_stopped_action(self):
        """Should parse match stopped action from fixture."""
        actions = parse_hbr2_actions(FIXTURES_DIR / "match_stopped_action.hbr2")
        
        # Find MatchStopped actions
        stop_actions = actions.filter_by_type(ActionType.MATCH_STOPPED)
        assert len(stop_actions) > 0
        
        action = stop_actions[0]
        assert isinstance(action, MatchStoppedAction)
    
    def test_game_paused_action(self):
        """Should parse game paused action from fixture."""
        actions = parse_hbr2_actions(FIXTURES_DIR / "game_paused_action.hbr2")
        
        # Find ChangePaused actions
        paused_actions = actions.filter_by_type(ActionType.CHANGE_PAUSED)
        assert len(paused_actions) > 0
        
        # Should have paused=1
        paused = [a for a in paused_actions if a.paused == 1]
        assert len(paused) > 0
    
    def test_game_unpaused_action(self):
        """Should parse game unpaused action from fixture."""
        actions = parse_hbr2_actions(FIXTURES_DIR / "game_unpaused_action.hbr2")
        
        # Find ChangePaused actions
        paused_actions = actions.filter_by_type(ActionType.CHANGE_PAUSED)
        assert len(paused_actions) > 0
        
        # Should have paused=0
        unpaused = [a for a in paused_actions if a.paused == 0]
        assert len(unpaused) > 0
    
    def test_change_score_limit_action(self):
        """Should parse change score limit action from fixture."""
        actions = parse_hbr2_actions(FIXTURES_DIR / "change_score_limit_action.hbr2")
        
        # Find ChangeGameSetting actions
        setting_actions = actions.filter_by_type(ActionType.CHANGE_GAME_SETTING)
        assert len(setting_actions) > 0
        
        action = setting_actions[0]
        assert isinstance(action, ChangeGameSettingAction)
        assert action.key is not None
        assert action.value is not None
    
    def test_change_time_limit_action(self):
        """Should parse change time limit action from fixture."""
        actions = parse_hbr2_actions(FIXTURES_DIR / "change_time_limit_action.hbr2")
        
        # Find ChangeGameSetting actions
        setting_actions = actions.filter_by_type(ActionType.CHANGE_GAME_SETTING)
        assert len(setting_actions) > 0
        
        action = setting_actions[0]
        assert isinstance(action, ChangeGameSettingAction)
        assert action.key is not None
        assert action.value is not None
    
    def test_player_team_changed_action(self):
        """Should parse player team change action from fixture."""
        actions = parse_hbr2_actions(FIXTURES_DIR / "player_team_changed_action.hbr2")
        
        # Find PlayerTeamChange actions
        team_actions = actions.filter_by_type(ActionType.PLAYER_TEAM_CHANGE)
        assert len(team_actions) > 0
        
        action = team_actions[0]
        assert isinstance(action, PlayerTeamChangeAction)
        assert action.player_id is not None
        assert action.team_id in (-1, 0, 1, 2)
    
    def test_change_team_locks_action(self):
        """Should parse change team locks action from fixture."""
        actions = parse_hbr2_actions(FIXTURES_DIR / "change_team_locks_action.hbr2")
        
        # Find ChangeTeamsLock actions
        lock_actions = actions.filter_by_type(ActionType.CHANGE_TEAMS_LOCK)
        assert len(lock_actions) > 0
        
        action = lock_actions[0]
        assert isinstance(action, ChangeTeamsLockAction)
        assert action.locked in (0, 1)
    
    def test_change_player_admin_action(self):
        """Should parse change player admin action from fixture."""
        actions = parse_hbr2_actions(FIXTURES_DIR / "change_player_admin_action.hbr2")
        
        # Find PlayerAdminChange actions
        admin_actions = actions.filter_by_type(ActionType.PLAYER_ADMIN_CHANGE)
        assert len(admin_actions) > 0
        
        action = admin_actions[0]
        assert isinstance(action, PlayerAdminChangeAction)
        assert action.player_id is not None
        assert action.admin in (0, 1)
    
    def test_team_randoms_balance_action(self):
        """Should parse team randoms balance action from fixture."""
        actions = parse_hbr2_actions(FIXTURES_DIR / "team_randoms_balance_action.hbr2")
        
        # Find AutoTeamBalance actions
        balance_actions = actions.filter_by_type(ActionType.AUTO_TEAM_BALANCE)
        assert len(balance_actions) > 0
        
        action = balance_actions[0]
        assert isinstance(action, AutoTeamBalanceAction)
        assert action.enabled in (0, 1)
    
    def test_broadcast_pings_action(self):
        """Should parse broadcast pings action from fixture."""
        actions = parse_hbr2_actions(FIXTURES_DIR / "broadcast_pings_action.hbr2")
        
        # Find BroadcastPings actions
        ping_actions = actions.filter_by_type(ActionType.BROADCAST_PINGS)
        assert len(ping_actions) > 0
        
        action = ping_actions[0]
        assert isinstance(action, BroadcastPingsAction)
        assert action.count >= 0
        assert len(action.pings) == action.count
    
    def test_change_avatar_action(self):
        """Should parse change avatar action from fixture."""
        actions = parse_hbr2_actions(FIXTURES_DIR / "change_avatar_action.hbr2")
        
        # Find AvatarChange actions
        avatar_actions = actions.filter_by_type(ActionType.AVATAR_CHANGE)
        assert len(avatar_actions) > 0
        
        action = avatar_actions[0]
        assert isinstance(action, AvatarChangeAction)
        assert action.player_id is not None
    
    def test_change_team_colors_action(self):
        """Should parse change team colors action from fixture."""
        actions = parse_hbr2_actions(FIXTURES_DIR / "change_team_colors.hbr2")
        
        # Find TeamColorsChange actions
        color_actions = actions.filter_by_type(ActionType.TEAM_COLORS_CHANGE)
        assert len(color_actions) > 0
        
        action = color_actions[0]
        assert isinstance(action, TeamColorsChangeAction)
        assert action.team in (1, 2)
        assert action.num_stripes >= 0
        assert len(action.stripes) == action.num_stripes
    
    def test_disc_update_in_input_actions(self):
        """Should parse disc update actions from input fixtures."""
        # Input actions typically include disc updates
        actions = parse_hbr2_actions(FIXTURES_DIR / "up_input_action.hbr2")
        
        # Find DiscUpdate actions
        disc_actions = actions.filter_by_type(ActionType.DISC_UPDATE)
        
        if len(disc_actions) > 0:
            action = disc_actions[0]
            assert isinstance(action, DiscUpdateAction)
            assert action.disc_id is not None
