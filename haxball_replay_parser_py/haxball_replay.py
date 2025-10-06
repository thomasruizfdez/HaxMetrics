from binary_reader import BinaryReader
import zlib
import gzip


def try_decompress(data):
    # Prueba zlib
    try:
        return zlib.decompress(data)
    except Exception:
        pass
    # Prueba gzip
    try:
        return gzip.decompress(data)
    except Exception:
        pass
    # Prueba raw DEFLATE
    try:
        return zlib.decompress(data, wbits=-15)
    except Exception:
        pass
    # No se pudo descomprimir
    return None


class HaxballReplay:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.metadata = {}
        self.players = []
        self.events = []
        self.frames = []
        self.parse()

    def parse(self):
        # === 1. Lee el archivo binario completo ===
        with open(self.file_path, "rb") as f:
            data = f.read()
        reader = BinaryReader(data)

        # === 2. Lee los campos principales según el formato ===
        header = reader.read_string(4)
        version = reader.read_uint32_be()
        frames = reader.read_uint32_be()
        # El resto es el bloque comprimido
        compressed_data = reader.read_bytes(len(data) - reader.offset)

        # === 3. Descomprime el bloque ===
        decompressed = try_decompress(compressed_data)
        if decompressed is None:
            print("No se pudo descomprimir, usando datos directos.")
            decompressed = compressed_data
        else:
            print("¡Bloque descomprimido correctamente!")

        # === 4. Nuevo reader sobre el bloque descomprimido ===
        room_reader = BinaryReader(decompressed)

        # === 5. Parsear RoomInfo ===
        # Aquí solo parseamos el nombre de sala como ejemplo;
        # en un parser completo deberías seguir el flujo del parser original
        timestamp = room_reader.read_uint32_be()
        for _ in range(7):
            room_reader.read_uint8()
        room_name_len = room_reader.read_uint8()
        room_name = room_reader.read_string(room_name_len)

        self.metadata = {
            "header": header,
            "version": version,
            "frames": frames,
            "room_name": room_name,
        }
        # Aquí puedes seguir parseando discos, jugadores, etc. como en haxball-replay-parser

    def to_dict(self):
        return {
            "metadata": self.metadata,
            "players": self.players,
            "events": self.events,
            "frames": self.frames,
        }
