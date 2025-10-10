from ..action import Action


class DiscUpdate(Action):
    """Action 23 (Hb): Disc property update with nullable fields"""
    def __init__(self):
        super().__init__()
        self.disc_id = None
        self.x = None
        self.y = None
        self.xspeed = None
        self.yspeed = None
        self.xgravity = None
        self.ygravity = None
        self.radius = None
        self.bcoeff = None
        self.invmass = None
        self.damping = None
        self.for_player = None

    @classmethod
    def parse(cls, reader):
        obj = cls()
        # Read flags that indicate which fields are present
        flags = reader.read_uint32_be()
        
        # Parse disc ID (always present)
        obj.disc_id = reader.read_uint32_be()
        
        # Check if this is for a specific player's disc
        obj.for_player = (flags & 0x80) != 0
        
        # Parse nullable float fields based on flags
        # Each bit in flags indicates if that field is present
        if (flags & 0x01) != 0:
            obj.x = reader.read_float_le()
        if (flags & 0x02) != 0:
            obj.y = reader.read_float_le()
        if (flags & 0x04) != 0:
            obj.xspeed = reader.read_float_le()
        if (flags & 0x08) != 0:
            obj.yspeed = reader.read_float_le()
        if (flags & 0x10) != 0:
            obj.xgravity = reader.read_float_le()
        if (flags & 0x20) != 0:
            obj.ygravity = reader.read_float_le()
        if (flags & 0x40) != 0:
            obj.radius = reader.read_float_le()
        if (flags & 0x100) != 0:
            obj.bcoeff = reader.read_float_le()
        if (flags & 0x200) != 0:
            obj.invmass = reader.read_float_le()
        if (flags & 0x400) != 0:
            obj.damping = reader.read_float_le()
        
        return obj

    def get_data(self):
        data = {"disc_id": self.disc_id, "for_player": self.for_player}
        # Only include non-None values
        if self.x is not None:
            data["x"] = self.x
        if self.y is not None:
            data["y"] = self.y
        if self.xspeed is not None:
            data["xspeed"] = self.xspeed
        if self.yspeed is not None:
            data["yspeed"] = self.yspeed
        if self.xgravity is not None:
            data["xgravity"] = self.xgravity
        if self.ygravity is not None:
            data["ygravity"] = self.ygravity
        if self.radius is not None:
            data["radius"] = self.radius
        if self.bcoeff is not None:
            data["bcoeff"] = self.bcoeff
        if self.invmass is not None:
            data["invmass"] = self.invmass
        if self.damping is not None:
            data["damping"] = self.damping
        return data
