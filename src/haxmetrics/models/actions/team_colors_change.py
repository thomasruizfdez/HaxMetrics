from ..action import Action


class TeamColorsChange(Action):
    """Action 19 (bb): Team colors change"""
    def __init__(self):
        super().__init__()
        self.team = None
        self.angle = None
        self.text_color = None
        self.colors = None

    @classmethod
    def parse(cls, reader):
        obj = cls()
        # Parse team: 1 = red, 2 = blue, 0 = spectator (from zf() method)
        team_byte = reader.read_uint8()
        obj.team = 1 if team_byte == 1 else (2 if team_byte == 2 else 0)
        
        # Parse TeamColor object (wa class in original)
        obj.angle = reader.read_uint32_be()
        obj.text_color = reader.read_uint32_be()
        
        # Parse array of 3 or 4 colors
        count = reader.read_uint8()
        obj.colors = []
        for _ in range(count):
            obj.colors.append(reader.read_uint32_be())
        
        return obj

    def get_data(self):
        return {
            "team": self.team,
            "angle": self.angle,
            "text_color": self.text_color,
            "colors": self.colors
        }
