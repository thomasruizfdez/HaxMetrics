from typing import List, Dict, Any, Optional


class TeamColor:
    def __init__(self):
        self.angle: Optional[int] = None
        self.text_color: Optional[str] = None
        self.stripes: List[str] = []

    @classmethod
    def parse(cls, reader):
        """
        Parse team color from binary data according to HaxBall's ta.ma(a) method.
        Based on game-min.js class ta, method ma().
        
        Structure:
        - sd: byte (angle)
        - pd: int32 big-endian (text color)
        - num_stripes: byte (max 3)
        - stripes: array of int32 big-endian
        """
        model = cls()
        
        # this.sd = a.F(); - angle is a BYTE, not uint32!
        model.set_angle(reader.read_byte())
        
        # this.pd = a.N(); - text color is int32 big-endian
        model.set_text_color(hex(reader.read_uint32_be())[2:])
        
        # let b = a.F(); - number of stripes (byte)
        num_stripes = reader.read_byte()
        
        # if (3 < b) throw v.C("too many"); - max 3 stripes
        if num_stripes > 3:
            raise ValueError(f"Too many stripes: {num_stripes} (max 3)")
        
        stripes = []
        for _ in range(num_stripes):
            # this.hb.push(a.N()); - each stripe color is int32 big-endian
            stripes.append(hex(reader.read_uint32_be())[2:])
        model.set_stripes(stripes)
        
        return model

    def json_serialize(self) -> Dict[str, Any]:
        return {
            "angle": self.angle,
            "textColor": self.text_color,
            "stripes": self.stripes,
        }

    def get_angle(self) -> Optional[int]:
        return self.angle

    def set_angle(self, angle: int):
        self.angle = angle
        return self

    def get_text_color(self) -> Optional[str]:
        return self.text_color

    def set_text_color(self, text_color: str):
        self.text_color = text_color
        return self

    def get_stripes(self) -> List[str]:
        return self.stripes

    def set_stripes(self, stripes: List[str]):
        self.stripes = stripes
        return self
