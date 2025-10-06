from typing import List, Dict, Any, Optional


class TeamColor:
    def __init__(self):
        self.angle: Optional[int] = None
        self.text_color: Optional[str] = None
        self.stripes: List[str] = []

    @classmethod
    def parse(cls, reader):
        model = cls()
        model.set_angle(reader.read_uint16_be())
        # Convert uint32 to hex string, matching PHP dechex
        model.set_text_color(hex(reader.read_uint32_be())[2:])
        num_stripes = reader.read_uint8()
        stripes = []
        for _ in range(num_stripes):
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
