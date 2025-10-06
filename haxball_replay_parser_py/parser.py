import sys
import json
from typing import List, Any, Dict

class HaxballPlayer:
    def __init__(self, data: Dict[str, Any]):
        self.id = data.get("id")
        self.name = data.get("name")
        self.team = data.get("team")
        self.auth = data.get("auth")
        self.avatar = data.get("avatar")
        self.conn = data.get("conn")
        self.join_time = data.get("join_time")

    def to_dict(self):
        return self.__dict__

class HaxballEvent:
    def __init__(self, data: Dict[str, Any]):
        self.type = data.get("type")
        self.time = data.get("time")
        self.details = data.get("details", {})

    def to_dict(self):
        return self.__dict__

class HaxballReplay:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.players: List[HaxballPlayer] = []
        self.events: List[HaxballEvent] = []
        self.metadata: Dict[str, Any] = {}
        self.frames: List[Any] = []
        self._parse()

    def _parse(self):
        # Aquí va la lógica de decodificación real
        # Por ahora, simula la estructura.
        self.metadata = {"stub": True}  # Para reemplazar por metadata real
        self.players = [HaxballPlayer({"id": 1, "name": "Jugador1", "team": "red"})]
        self.events = [HaxballEvent({"type": "goal", "time": 123.4, "details": {"scorer": "Jugador1"}})]
        self.frames = []  # Lista vacía, implementar en el parseo real

    def to_dict(self):
        return {
            "metadata": self.metadata,
            "players": [p.to_dict() for p in self.players],
            "events": [e.to_dict() for e in self.events],
            "frames": self.frames,
        }

def parse_hbr2_file(file_path: str) -> Dict[str, Any]:
    replay = HaxballReplay(file_path)
    return replay.to_dict()

def main():
    if len(sys.argv) != 3:
        print("Uso: python parser.py input.hbr2 output.json")
        sys.exit(1)
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    data = parse_hbr2_file(input_path)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Exportado {output_path}")

if __name__ == "__main__":
    main()