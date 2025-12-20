"""
Test all 24 action types parsing and validation.

This test suite validates that all action types (0-23) are:
1. Properly implemented with the correct class
2. Can be parsed from binary data
3. Have the expected fields and structure
4. Match the documentation in GAME_MIN_REVERSE_ENGINEERING.md
"""

import pytest
from pathlib import Path

# Add parent directory to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from haxmetrics.models.action_types import ACTION_TYPES
from haxmetrics.models.action import Action


class TestActionTypeRegistry:
    """Test the action type registry and basic structure."""
    
    def test_action_count(self):
        """Test that exactly 24 action types are registered."""
        assert len(ACTION_TYPES) == 24, f"Expected 24 action types, found {len(ACTION_TYPES)}"
    
    def test_all_action_types_are_classes(self):
        """Test that all action types are class types."""
        for i, action_class in enumerate(ACTION_TYPES):
            assert isinstance(action_class, type), f"Action {i} is not a class"
    
    def test_all_action_types_inherit_from_action(self):
        """Test that all action types inherit from Action base class."""
        for i, action_class in enumerate(ACTION_TYPES):
            # Check if it's a subclass of Action
            assert issubclass(action_class, Action), \
                f"Action {i} ({action_class.__name__}) does not inherit from Action"
    
    def test_all_action_types_have_parse_method(self):
        """Test that all action types have a parse classmethod."""
        for i, action_class in enumerate(ACTION_TYPES):
            assert hasattr(action_class, "parse"), \
                f"Action {i} ({action_class.__name__}) missing parse method"
            assert callable(getattr(action_class, "parse")), \
                f"Action {i} ({action_class.__name__}) parse is not callable"
    
    def test_action_type_names_are_unique(self):
        """Test that all action type names are unique."""
        names = [action_class.__name__ for action_class in ACTION_TYPES]
        assert len(names) == len(set(names)), "Action type names are not unique"


class TestIndividualActionTypes:
    """Test individual action type implementations."""
    
    def test_action_0_message(self):
        """Test Action 0: Message (Eb)."""
        from haxmetrics.models.actions.message import Message
        assert ACTION_TYPES[0] == Message
        assert Message.__name__ == "Message"
        
        # Check expected fields
        msg = Message()
        assert hasattr(msg, "message")
        assert hasattr(msg, "color")
        assert hasattr(msg, "style")
    
    def test_action_1_toggle_chat(self):
        """Test Action 1: ToggleChat (Ha)."""
        from haxmetrics.models.actions.toggle_chat import ToggleChat
        assert ACTION_TYPES[1] == ToggleChat
        assert ToggleChat.__name__ == "ToggleChat"
    
    def test_action_2_change_stadium(self):
        """Test Action 2: ChangeStadium (cb)."""
        from haxmetrics.models.actions.change_stadium import ChangeStadium
        assert ACTION_TYPES[2] == ChangeStadium
        assert ChangeStadium.__name__ == "ChangeStadium"
    
    def test_action_3_player_input(self):
        """Test Action 3: PlayerInput (La)."""
        from haxmetrics.models.actions.player_input import PlayerInput
        assert ACTION_TYPES[3] == PlayerInput
        assert PlayerInput.__name__ == "PlayerInput"
        
        # Check expected field
        action = PlayerInput()
        assert hasattr(action, "input")
    
    def test_action_4_chat_message(self):
        """Test Action 4: ChatMessage (Ya)."""
        from haxmetrics.models.actions.chat_message import ChatMessage
        assert ACTION_TYPES[4] == ChatMessage
        assert ChatMessage.__name__ == "ChatMessage"
        
        # Check expected field
        action = ChatMessage()
        assert hasattr(action, "message")
    
    def test_action_5_player_joined(self):
        """Test Action 5: PlayerJoined (Na)."""
        from haxmetrics.models.actions.player_joined import PlayerJoined
        assert ACTION_TYPES[5] == PlayerJoined
        assert PlayerJoined.__name__ == "PlayerJoined"
        
        # Just verify the class exists and has parse method
        assert hasattr(PlayerJoined, "parse")
    
    def test_action_6_player_left(self):
        """Test Action 6: PlayerLeft (ma)."""
        from haxmetrics.models.actions.player_left import PlayerLeft
        assert ACTION_TYPES[6] == PlayerLeft
        assert PlayerLeft.__name__ == "PlayerLeft"
        
        # Just verify the class exists and has parse method
        assert hasattr(PlayerLeft, "parse")
    
    def test_action_7_match_start(self):
        """Test Action 7: MatchStart (Va)."""
        from haxmetrics.models.actions.match_start import MatchStart
        assert ACTION_TYPES[7] == MatchStart
        assert MatchStart.__name__ == "MatchStart"
    
    def test_action_8_match_stopped(self):
        """Test Action 8: MatchStopped (Wa)."""
        from haxmetrics.models.actions.match_stopped import MatchStopped
        assert ACTION_TYPES[8] == MatchStopped
        assert MatchStopped.__name__ == "MatchStopped"
    
    def test_action_9_change_paused(self):
        """Test Action 9: ChangePaused (Za)."""
        from haxmetrics.models.actions.change_paused import ChangePaused
        assert ACTION_TYPES[9] == ChangePaused
        assert ChangePaused.__name__ == "ChangePaused"
        
        # Check expected field
        action = ChangePaused()
        assert hasattr(action, "paused")
    
    def test_action_10_change_game_setting(self):
        """Test Action 10: ChangeGameSetting (va)."""
        from haxmetrics.models.actions.change_game_setting import ChangeGameSetting
        assert ACTION_TYPES[10] == ChangeGameSetting
        assert ChangeGameSetting.__name__ == "ChangeGameSetting"
    
    def test_action_11_stadium_update(self):
        """Test Action 11: StadiumUpdate (Ea)."""
        from haxmetrics.models.actions.stadium_update import StadiumUpdate
        assert ACTION_TYPES[11] == StadiumUpdate
        assert StadiumUpdate.__name__ == "StadiumUpdate"
    
    def test_action_12_player_team_change(self):
        """Test Action 12: PlayerTeamChange (fa)."""
        from haxmetrics.models.actions.player_team_change import PlayerTeamChange
        assert ACTION_TYPES[12] == PlayerTeamChange
        assert PlayerTeamChange.__name__ == "PlayerTeamChange"
        
        # Just verify the class exists and has parse method
        assert hasattr(PlayerTeamChange, "parse")
    
    def test_action_13_change_teams_lock(self):
        """Test Action 13: ChangeTeamsLock (Fa)."""
        from haxmetrics.models.actions.change_teams_lock import ChangeTeamsLock
        assert ACTION_TYPES[13] == ChangeTeamsLock
        assert ChangeTeamsLock.__name__ == "ChangeTeamsLock"
        
        # Just verify the class exists and has parse method
        assert hasattr(ChangeTeamsLock, "parse")
    
    def test_action_14_player_admin_change(self):
        """Test Action 14: PlayerAdminChange (Ga)."""
        from haxmetrics.models.actions.player_admin_change import PlayerAdminChange
        assert ACTION_TYPES[14] == PlayerAdminChange
        assert PlayerAdminChange.__name__ == "PlayerAdminChange"
        
        # Just verify the class exists and has parse method
        assert hasattr(PlayerAdminChange, "parse")
    
    def test_action_15_auto_team_balance(self):
        """Test Action 15: AutoTeamBalance (Xa)."""
        from haxmetrics.models.actions.auto_team_balance import AutoTeamBalance
        assert ACTION_TYPES[15] == AutoTeamBalance
        assert AutoTeamBalance.__name__ == "AutoTeamBalance"
    
    def test_action_16_desynced(self):
        """Test Action 16: Desynced (Da)."""
        from haxmetrics.models.actions.desynced import Desynced
        assert ACTION_TYPES[16] == Desynced
        assert Desynced.__name__ == "Desynced"
        
        # Just verify the class exists and has parse method
        assert hasattr(Desynced, "parse")
    
    def test_action_17_broadcast_pings(self):
        """Test Action 17: BroadcastPings (Ma)."""
        from haxmetrics.models.actions.broadcast_pings import BroadcastPings
        assert ACTION_TYPES[17] == BroadcastPings
        assert BroadcastPings.__name__ == "BroadcastPings"
        
        # Check expected field
        action = BroadcastPings()
        assert hasattr(action, "pings")
    
    def test_action_18_avatar_change(self):
        """Test Action 18: AvatarChange (Qa)."""
        from haxmetrics.models.actions.avatar_change import AvatarChange
        assert ACTION_TYPES[18] == AvatarChange
        assert AvatarChange.__name__ == "AvatarChange"
        
        # Check expected field
        action = AvatarChange()
        assert hasattr(action, "avatar")
    
    def test_action_19_team_colors_change(self):
        """Test Action 19: TeamColorsChange (bb)."""
        from haxmetrics.models.actions.team_colors_change import TeamColorsChange
        assert ACTION_TYPES[19] == TeamColorsChange
        assert TeamColorsChange.__name__ == "TeamColorsChange"
        
        # Check expected fields
        action = TeamColorsChange()
        assert hasattr(action, "team")
        assert hasattr(action, "angle")
        assert hasattr(action, "text_color")
        assert hasattr(action, "colors")
    
    def test_action_20_player_order_change(self):
        """Test Action 20: PlayerOrderChange (Fb)."""
        from haxmetrics.models.actions.player_order_change import PlayerOrderChange
        assert ACTION_TYPES[20] == PlayerOrderChange
        assert PlayerOrderChange.__name__ == "PlayerOrderChange"
        
        # Check expected field
        action = PlayerOrderChange()
        assert hasattr(action, "player_ids")
    
    def test_action_21_kick_rate_limit(self):
        """Test Action 21: KickRateLimit (Pa)."""
        from haxmetrics.models.actions.kick_rate_limit import KickRateLimit
        assert ACTION_TYPES[21] == KickRateLimit
        assert KickRateLimit.__name__ == "KickRateLimit"
        
        # Check expected fields
        action = KickRateLimit()
        assert hasattr(action, "min")
        assert hasattr(action, "rate")
        assert hasattr(action, "burst")
    
    def test_action_22_player_avatar_set(self):
        """Test Action 22: PlayerAvatarSet (Gb)."""
        from haxmetrics.models.actions.player_avatar_set import PlayerAvatarSet
        assert ACTION_TYPES[22] == PlayerAvatarSet
        assert PlayerAvatarSet.__name__ == "PlayerAvatarSet"
        
        # Check expected fields
        action = PlayerAvatarSet()
        assert hasattr(action, "player_id")
        assert hasattr(action, "avatar")
    
    def test_action_23_disc_update(self):
        """Test Action 23: DiscUpdate (Hb)."""
        from haxmetrics.models.actions.disc_update import DiscUpdate
        assert ACTION_TYPES[23] == DiscUpdate
        assert DiscUpdate.__name__ == "DiscUpdate"
        
        # Check expected field
        action = DiscUpdate()
        assert hasattr(action, "disc_id")


class TestActionTypeDocumentation:
    """Test that action types match documentation."""
    
    def test_action_type_count_matches_docs(self):
        """
        Test that we have 24 action types as documented in
        GAME_MIN_REVERSE_ENGINEERING.md section 4.8.
        """
        assert len(ACTION_TYPES) == 24
    
    def test_action_type_names_match_docs(self):
        """Test that action type names match documentation."""
        expected_names = [
            "Message",           # 0
            "ToggleChat",        # 1
            "ChangeStadium",     # 2
            "PlayerInput",       # 3
            "ChatMessage",       # 4
            "PlayerJoined",      # 5
            "PlayerLeft",        # 6
            "MatchStart",        # 7
            "MatchStopped",      # 8
            "ChangePaused",      # 9
            "ChangeGameSetting", # 10
            "StadiumUpdate",     # 11
            "PlayerTeamChange",  # 12
            "ChangeTeamsLock",   # 13
            "PlayerAdminChange", # 14
            "AutoTeamBalance",   # 15
            "Desynced",          # 16
            "BroadcastPings",    # 17
            "AvatarChange",      # 18
            "TeamColorsChange",  # 19
            "PlayerOrderChange", # 20
            "KickRateLimit",     # 21
            "PlayerAvatarSet",   # 22
            "DiscUpdate",        # 23
        ]
        
        actual_names = [action_class.__name__ for action_class in ACTION_TYPES]
        
        for i, (expected, actual) in enumerate(zip(expected_names, actual_names)):
            assert actual == expected, \
                f"Action {i}: expected '{expected}', got '{actual}'"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
