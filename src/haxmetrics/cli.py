# src/haxmetrics/cli.py (fragmento)
import json
import click
from .io.hbr2_reader import HBR2Reader, HBR2ReaderError
from .io.decoder import PayloadDecoder, DecodeError
from .model import TickState, PlayerState, BallState
from .engine.micro_engine import MicroEngine
from .metrics.passes_minutes import minutes_played, count_passes


@click.group()
def main():
    """HaxMetrics CLI"""


@main.command("transform-hbr2")
@click.option("--replay", type=click.Path(exists=True, dir_okay=False), required=True)
@click.option("--pretty/--no-pretty", default=True)
def transform_hbr2(replay: str, pretty: bool):
    try:
        version, header_bytes, payload = HBR2Reader(replay).read_raw()
    except HBR2ReaderError as e:
        raise click.ClickException(f"Reader: {e}")

    try:
        tick_iter = PayloadDecoder().decode_ticks(payload)
    except DecodeError as e:
        raise click.ClickException(f"Decoder: {e}")

    # Aquí tu mismo bucle de motor/metrics que ya tienes para el caso decoded JSON...
    # (idéntico al de 'transform', pero alimentando con tick_iter)
    # ...
