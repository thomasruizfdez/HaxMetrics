from __future__ import annotations
import argparse
from haxmetrics.io.hbr2_reader import read_hbr2
from haxmetrics.io.decoder import iter_raw_tokens


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--replay", required=True)
    ap.add_argument("--limit", type=int, default=2000, help="nº de tokens a mostrar")
    args = ap.parse_args()

    rep = read_hbr2(args.replay)
    print(
        f"version={rep.header.version} header_len={rep.header.header_len} payload_len={rep.header.payload_len}"
    )
    print("meta keys:", list(rep.meta.keys()))
    print("payload zlib head:", rep.payload_raw[:4].hex(" "))

    for i, tk in enumerate(iter_raw_tokens(rep.payload_inflated)):
        if i >= args.limit:
            break
        print(f"{i:06d} @{tk.at:08d} {tk.kind} {tk.args!r}")


if __name__ == "__main__":
    main()
