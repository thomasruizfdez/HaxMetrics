import sys
from haxmetrics.parser import Parser


def main(filepath):
    with open(filepath, "rb") as f:
        data = f.read()
    parser = Parser(data)
    replay = parser.parse()

    # Muestra algunos datos relevantes
    print("Versión:", replay["version"])
    print("Frames:", replay["frames"])
    print("Room:", replay["room_info"].name if replay["room_info"] else None)
    if replay["room_info"] and replay["room_info"].stadium:
        print("Stadium:", replay["room_info"].stadium.name)
    print("Jugadores:")
    for p in replay["players"]:
        print("-", p.name, p.team)
    print("Discos:", len(replay["discs"]))
    print("Acciones:", len(replay["actions"]))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python test_parser.py <archivo.hbr2>")
    else:
        main(sys.argv[1])
