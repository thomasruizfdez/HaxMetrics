from typing import Any, Dict, Optional


class Action:
    def __init__(self):
        self.type: Optional[str] = None
        self.frame: Optional[int] = None
        self.sender: Optional[int] = None

    @classmethod
    def parse(cls, reader):
        # In actual subclasses, override with real parsing logic
        return cls()

    def json_serialize(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            "frame": self.frame,
            "replayTime": self.get_replay_time(),
            "sender": self.sender,
            "info": self.get_data(),
        }

    def set_frame(self, frame: int):
        self.frame = int(frame)
        return self

    def get_frame(self) -> Optional[int]:
        return self.frame

    def get_replay_time(self) -> Optional[float]:
        # 60 ticks/frames per second (standard for Haxball)
        return round(self.frame / 60, 2) if self.frame is not None else None

    def set_sender(self, sender: int):
        self.sender = int(sender)
        return self

    def get_sender(self) -> Optional[int]:
        return self.sender

    def get_type(self) -> Optional[str]:
        return self.type

    def get_data(self) -> Any:
        # Abstract: subclasses should override
        raise NotImplementedError("get_data must be implemented in subclasses")
