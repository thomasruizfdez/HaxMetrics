from ..action import Action


class PlayerTeamChange(Action):
    """
    Action index 12 (fa in original JS)
    Player team change
    xa(): int Ud (player_id), byte team (1=red, 2=blue, 0=spec)
    """
    def __init__(self):
        super().__init__()
        self.type = "PlayerTeamChange"
        self.player_id = None
        self.team = None

    @classmethod
    def parse(cls, reader):
        obj = cls()
        obj.player_id = reader.read_int32()  # N() - int32
        obj.team = reader.read_uint8()  # zf() or F() - byte
        return obj

    def get_data(self):
        return {"player_id": self.player_id, "team": self.team}
