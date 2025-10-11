from ..action import Action


class AutoTeamBalance(Action):
    """
    Action index 15 (Xa in original JS)
    Auto team balance - no data fields
    xa(): (empty)
    """
    def __init__(self):
        super().__init__()
        self.type = "AutoTeamBalance"

    @classmethod
    def parse(cls, reader):
        obj = cls()
        # No fields to parse
        return obj

    def get_data(self):
        return {}
