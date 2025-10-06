import sys
import json
from HaxballReplay import HaxballReplay


def parse_hbr2_file(file_path: str):
    replay = HaxballReplay(file_path)
    return replay.to_dict()


def main():
    if len(sys.argv) != 3:
        print("Uso: python parser.py input.hbr2 output.json")
        sys.exit(1)
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    data = parse_hbr2_file(input_path)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Exportado {output_path}")


if __name__ == "__main__":
    main()
