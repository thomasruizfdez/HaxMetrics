from dataclasses import dataclass, field, asdict


@dataclass
class PlayerPhysics:
    b_coef: float = 0.5
    inv_mass: float = 0.5
    damping: float = 0.96
    acceleration: float = 0.1
    kicking_acceleration: float = 0.07
    kicking_damping: float = 0.96
    kick_strength: float = 5

    defaults = {
        "b_coef": 0.5,
        "inv_mass": 0.5,
        "damping": 0.96,
        "acceleration": 0.1,
        "kicking_acceleration": 0.07,
        "kicking_damping": 0.96,
        "kick_strength": 5,
    }

    @staticmethod
    def parse(reader):
        return PlayerPhysics(
            b_coef=reader.read_double(),
            inv_mass=reader.read_double(),
            damping=reader.read_double(),
            acceleration=reader.read_double(),
            kicking_acceleration=reader.read_double(),
            kicking_damping=reader.read_double(),
            kick_strength=reader.read_double(),
        )

    def to_json(self):
        # Solo incluye los campos que son diferentes del default
        data = {}
        for prop, default in self.defaults.items():
            if getattr(self, prop) != default:
                data[prop] = getattr(self, prop)
        return data
