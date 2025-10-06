from __future__ import annotations
import argparse
from haxmetrics.io.hbr2_reader import read_hbr2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--replay", required=True)
    ap.add_argument("--hex", action="store_true", help="dump hex de la cabecera")
    args = ap.parse_args()

    rep = read_hbr2(args.replay)
    print(
        f"version={rep.header.version} header_len={rep.header.header_len} payload_len={rep.header.payload_len}"
    )
    print("meta keys:", list(rep.meta.keys()))
    if args.hex:
        print("raw_header hex:", rep.header.raw_header.hex(" "))


if __name__ == "__main__":
    main()
