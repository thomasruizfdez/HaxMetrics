# haxmetrics/models/replay_messages.py

"""
Legacy replay messages model.

.. deprecated:: 1.0.0
    Use `haxmetrics.models.messages.Messages` instead.
    This module will be removed in version 2.0.0.
"""

import warnings
from dataclasses import dataclass
from typing import Any, Dict, List

warnings.warn(
    "replay_messages.py is deprecated. Use messages.Messages instead. "
    "This module will be removed in v2.0.0.",
    DeprecationWarning,
    stacklevel=2,
)


@dataclass
class ReplayMessage:
    """Represents a message within a HaxBall replay"""

    index: int
    delta_time: int
    type: int
    data: Any = None


class MessageType:
    """
    Constants for message types in HaxBall replays
    based on the original source code
    """

    ANNOUNCEMENT = 0  # System announcement message
    CHAT = 1  # Player chat message
    GOAL = 2  # Goal scored
    TEAM_GOAL = 3  # Team goal
    GAME_START = 4  # Game start
    GAME_STOP = 5  # Game end
    PLAYER_JOIN = 6  # Player joins
    PLAYER_LEAVE = 7  # Player leaves
    PLAYER_TEAM_CHANGE = 8  # Team change
    PAUSE = 9  # Game paused
    UNPAUSE = 10  # Game resumed
    ADMIN_CHANGE = 11  # Admin change
    STADIUM_CHANGE = 12  # Stadium change
    KICK = 13  # Player kicked
    POSITION_CHANGE = 14  # Position change

    @staticmethod
    def get_name(type_id: int) -> str:
        """Returns the name of the message type"""
        types = {
            0: "ANNOUNCEMENT",
            1: "CHAT",
            2: "GOAL",
            3: "TEAM_GOAL",
            4: "GAME_START",
            5: "GAME_STOP",
            6: "PLAYER_JOIN",
            7: "PLAYER_LEAVE",
            8: "PLAYER_TEAM_CHANGE",
            9: "PAUSE",
            10: "UNPAUSE",
            11: "ADMIN_CHANGE",
            12: "STADIUM_CHANGE",
            13: "KICK",
            14: "POSITION_CHANGE",
        }
        return types.get(type_id, f"UNKNOWN_{type_id}")


class ReplayMessages:
    """
    Class to parse and represent messages at the start of a HaxBall replay
    after the header and decompression.

    .. deprecated:: 1.0.0
        Use `Messages` class from haxmetrics.models.messages instead.
        This class will be removed in version 2.0.0.
    """

    def __init__(self):
        self.count: int = 0
        self.messages: List[ReplayMessage] = []
        self.end_position: int = 0  # Position after last message

    def __len__(self) -> int:
        """Return the number of messages for len() support"""
        return len(self.messages)

    def __iter__(self):
        """Make the class iterable"""
        return iter(self.messages)

    def __getitem__(self, index):
        """Allow indexing"""
        return self.messages[index]

    @classmethod
    def parse(cls, data) -> "ReplayMessages":
        """
        Parse messages from decompressed binary data.

        Args:
            data: DataReader object positioned at the start of the messages section

        Returns:
            ReplayMessages: Object with parsed messages
        """
        messages = cls()

        # 1. Read message count (2 bytes big-endian)
        messages.count = data.read_uint16_be()

        # 2. Read each message
        for i in range(messages.count):
            # Read delta time (VarInt)
            delta_time = data.read_varint()

            # Read message type
            msg_type = data.read_uint8()

            # Read additional data based on type
            msg_data = cls._parse_message_data(data, msg_type)

            # Create and add the message
            message = ReplayMessage(
                index=i, delta_time=delta_time, type=msg_type, data=msg_data
            )
            messages.messages.append(message)

        # Save current position to know where messages section ends
        messages.end_position = data.position

        print(f"Parsed {messages.count} messages")
        print(f"End position after messages: {messages.end_position}")
        print(f"Message details:")
        for msg in messages.messages:
            print(f" - Message {msg.index}: {MessageType.get_name(msg.type)}")

        return messages

    @staticmethod
    def _parse_message_data(data, msg_type) -> Dict[str, Any]:
        """
        Parse message metadata. In HaxBall replays, messages only store the type
        and timestamp - the actual data (player names, text, etc.) is reconstructed
        from the actions during playback.

        Args:
            data: DataReader object positioned just after the message type
            msg_type: Message type

        Returns:
            Dict: Empty dict or minimal metadata for the message type
        """
        # Messages in replays don't store their full data, only the type
        # The data is reconstructed from actions during playback
        return {"type": msg_type}
