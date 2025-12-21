# HaxMetrics

HaxMetrics es una herramienta para analizar replays de Haxball en formato .hbr2 y extraer métricas útiles para el análisis de partidos.

## Python Parser Architecture (v1.0+)

The Python parser now follows a **modular architecture** based on the official HBR2 format specification documented in `docs/HBR2_PARSING_GUIDE.md`.

### Parser Modules

```
src/haxmetrics/
├── binary_reader.py          # Low-level binary reading (Section 3)
│
├── models/                    # Data models (SOLID design)
│   ├── header.py             # ✅ Header (Section 4)
│   ├── messages.py           # ✅ Messages (Section 5)
│   ├── room.py               # ✅ Room Basic (Section 6.1)
│   ├── stadium/              # 🚧 Stadium (Section 6.2) [PR #3]
│   ├── game.py               # 🚧 Game State (Section 6.3) [PR #4]
│   ├── player.py             # 🚧 Players (Section 6.4) [PR #5]
│   ├── team_color.py         # 🚧 Team Colors (Section 6.5) [PR #6]
│   └── actions/              # 🚧 Actions (Section 7) [PR #7+]
│
└── parser.py                 # ⚠️ Legacy parser (deprecated, removal in v2.0.0)
```

### Usage Example

```python
import zlib
from haxmetrics.binary_reader import BinaryReader
from haxmetrics.models.header import Header
from haxmetrics.models.messages import Messages
from haxmetrics.models.room import RoomBasic

# Load replay file
with open('replay.hbr2', 'rb') as f:
    data = f.read()

# Parse header
reader = BinaryReader(data)
header = Header.parse(reader)
print(f"Version: {header.version}, Duration: {header.duration_seconds}s")

# Decompress and parse content
compressed = reader.get_remaining_bytes()
decompressed = zlib.decompress(compressed, wbits=-15)
reader = BinaryReader(decompressed)

# Parse sections
messages = Messages.parse(reader)
print(f"Messages: {messages.count}")

room = RoomBasic.parse(reader)
print(f"Room: {room.name}, Score Limit: {room.score_limit}")
```

### Documentation

- 📖 **[HBR2_PARSING_GUIDE.md](docs/HBR2_PARSING_GUIDE.md)** - Complete format specification
- 📖 **[MIGRATION.md](MIGRATION.md)** - Migration guide from old parser
- 📖 **[CHANGELOG.md](CHANGELOG.md)** - Version history

### Legacy Parser (Deprecated)

The old `Parser` class is deprecated and will be removed in v2.0.0. See [MIGRATION.md](MIGRATION.md) for migration guide.

---

## Herramientas

### Decoder HBR2 a JSON

El proyecto incluye tres decoders de Node.js para archivos .hbr2:

1. **Decoder Básico** (`decode_hbr2.js`): Extrae metadatos básicos
2. **Decoder Completo** (`decode_hbr2_complete.js`): Extrae TODOS los datos usando el código original de Haxball
3. **Decoder Completo V2** (`decode_hbr2_complete_v2.js`): **[RECOMENDADO]** Versión mejorada con mejor manejo de errores, sandbox completo y extracción de física detallada

#### Instalación

```bash
npm install
```

#### Uso del Decoder V2 (Recomendado)

El decoder V2 es una versión mejorada que incluye:

- **Sandbox completo**: Entorno de ejecución con mocks completos de Canvas, Audio, DOM
- **Multi-pattern matching**: Detecta automáticamente diferentes versiones del código minificado
- **Extracción mejorada**: Velocidades de discos, física completa (masa, damping, invMass), 14 tipos de eventos
- **Mejor manejo de errores**: Fallback automático cuando falla la extracción completa del estadio
- **Soporte completo para estadios personalizados**: Inicialización correcta de las clases de mensajes

```bash
# Usar con npm
npm run decode:v2 -- <archivo.hbr2> [salida.json]

# Ejemplo con estadio estándar
npm run decode:v2 -- src/replays/prueba.hbr2 output.json

# Ejemplo con estadio personalizado
npm run decode:v2 -- src/replays/prueba_custom.hbr2 output.json

# Si no se especifica archivo de salida, se usa el mismo nombre con .json
npm run decode:v2 -- src/replays/prueba.hbr2
```

#### Uso del Decoder V1 (Completo Original)

El decoder completo V1 utiliza el código JavaScript original de Haxball para decodificar completamente los archivos .hbr2:

```bash
# Usar con npm
npm run decode:full -- <archivo.hbr2> [salida.json]

# Ejemplo
npm run decode:full -- src/replays/prueba.hbr2 output.json

# Si no se especifica archivo de salida, se usa el mismo nombre con .json
npm run decode:full -- src/replays/prueba.hbr2
```

#### Diferencias entre V1 y V2

| Característica | V1 (decode:full) | V2 (decode:v2) |
|----------------|------------------|----------------|
| Sandbox Environment | Básico | Completo (Canvas, Audio, DOM) |
| Pattern Matching | Un patrón | Multi-patrón con fallbacks |
| Extracción de Física | Básica | Completa (velocidades, masa, damping) |
| Manejo de Errores | Básico | Granular con fallbacks |
| Estadios Personalizados | Soportado | Mejor soporte con inicialización correcta |
| Extracción de Velocidades | No | Sí (xSpeed, ySpeed) |
| Fallback Manual Stadium | No | Sí |
| Output Size | Variable | Típicamente mayor (14+ KB) |

#### Datos Extraídos por los Decoders Completos

Los decoders completos (V1 y V2) extraen TODA la información del replay:

- **Metadata**: 
  - Versión del formato
  - Duración del replay
  - Timestamp de inicio de grabación
- **Room Info**: 
  - Nombre de la sala
  - Estado de bloqueo
  - Límite de goles
  - Límite de tiempo
  - Reglas (kick rate limit, tamaño del equipo, rebote)
- **Stadium** (Estadio completo):
  - Nombre del estadio
  - Dimensiones (width, height)
  - Geometría completa: vértices, segmentos, planos, goals, discos
  - Física del estadio (playerPhysics, ballPhysics)
  - Background settings
  - Funciona con estadios predefinidos Y personalizados
  - **[V2]** Fallback a extracción manual si falla yk()
- **Players** (Jugadores):
  - ID, nombre, admin status
  - Avatar, país
  - Equipo asignado
  - Posición en el campo (x, y)
  - Radio del disco
  - **[V2]** Velocidades (xSpeed, ySpeed)
  - **[V2]** Física detallada (invMass, damping, bCoef)
- **Game State** (Estado del juego):
  - Tiempo actual
  - Límites de tiempo y score
  - Score actual (rojo vs azul)
  - Posiciones y velocidades de todos los discos (pelota + jugadores)
  - **[V2]** Física completa de cada disco (masa, damping, colisiones)
- **Teams** (Equipos):
  - Configuración de colores
  - Información de espectadores, equipo rojo y azul
- **Events** (Eventos):
  - Timeline completa con 14 tipos de eventos
  - Porcentaje de tiempo y tiempo absoluto
  - Tipo de evento (CHAT, GOAL, PLAYER_JOIN, etc.)

#### Ejemplo de Salida JSON (Decoder V2)

```json
{
  "metadata": {
    "version": 3,
    "duration": 34,
    "recordingStart": 1766183210080
  },
  "roomInfo": {
    "name": "Bandolero's room",
    "locked": false,
    "scoreLimit": 8,
    "timeLimit": 9,
    "rules": {
      "kickRateLimit": 2,
      "teamSize": 0,
      "bounciness": 1
    }
  },
  "stadium": {
    "name": "Huge",
    "width": 750,
    "height": 350,
    "bg": {
      "type": "grass",
      "width": 700,
      "height": 320,
      "kickOffRadius": 80
    },
    "vertexes": [ /* geometría completa */ ],
    "segments": [ /* ... */ ],
    "planes": [ /* ... */ ],
    "goals": [ /* ... */ ],
    "discs": [ /* ... */ ],
    "playerPhysics": { /* ... */ },
    "ballPhysics": "disc0"
  },
  "players": [
    {
      "id": 0,
      "name": "Bandolero",
      "admin": true,
      "position": 0,
      "avatar": "82",
      "country": null,
      "team": {
        "id": 0,
        "name": "Spectators"
      },
      "disc": {
        "x": 0,
        "y": 0,
        "xSpeed": 0,
        "ySpeed": 0,
        "radius": 15,
        "invMass": 0.5,
        "damping": 0.96,
        "bCoef": 0.5
      }
    }
  ],
  "gameState": {
    "time": 0,
    "timeLimit": 9,
    "scoreLimit": 8,
    "redScore": 0,
    "blueScore": 0,
    "discs": [
      {
        "x": 0,
        "y": 0,
        "xSpeed": 0,
        "ySpeed": 0,
        "radius": 10,
        "invMass": 1,
        "damping": 0.99,
        "bCoef": 0.5
      }
    ]
  },
  "teams": {
    "spectators": { /* configuración */ },
    "red": { /* colores y configuración */ },
    "blue": { /* colores y configuración */ }
  },
  "events": [
    {
      "index": 0,
      "timePercent": 0.25,
      "time": 8500,
      "kind": 2,
      "type": "GOAL"
    }
  ]
}
```

#### Script de Debugging

Si el decoder tiene problemas identificando las clases internas (debido a cambios en el código minificado), puedes usar el script de debugging:

```bash
npm run debug:replay
```

Este script lista todas las clases y funciones disponibles en `replay-min.js`, lo que ayuda a identificar los nombres correctos cuando cambia la versión del código.

#### Troubleshooting (Solución de Problemas)

**Problema: "Required classes not exposed"**

- **Causa**: El código minificado de Haxball ha cambiado y los nombres de las clases son diferentes
- **Solución**: 
  1. Ejecutar `npm run debug:replay` para ver las clases disponibles
  2. Buscar clases con 2-3 caracteres en mayúsculas
  3. Actualizar el script v2 con los nuevos nombres de clases

**Problema: "Stadium extraction warning" o "yk() method failed"**

- **Causa**: Estadio personalizado que requiere procesamiento especial
- **Efecto**: El decoder V2 automáticamente hace una extracción manual con información básica
- **Solución**: No requiere acción, la información básica del estadio se extrae correctamente

**Problema: Output size muy pequeño (<5 KB)**

- **Causa**: El replay puede no contener un juego activo o tiene pocos datos
- **Verificación**: Revisar el JSON de salida para ver qué secciones están vacías
- **Solución**: Intentar con un replay de un partido completo con múltiples eventos

**Problema: "pako module not found"**

- **Causa**: Dependencias no instaladas
- **Solución**: Ejecutar `npm install`

**Problema: Errores al extraer physics/velocities**

- **Causa**: Estructura interna del replay ha cambiado
- **Efecto**: El decoder V2 tiene manejo de errores granular y continúa con las demás secciones
- **Solución**: Revisar el output JSON - las secciones con error tendrán valores null pero el resto estará disponible

#### Uso del Decoder Básico

El decoder básico extrae metadatos principales del replay:

```bash
# Usar con npm
npm run decode -- <archivo.hbr2> [salida.json]

# Ejemplo
npm run decode -- src/replays/prueba.hbr2 output.json
```

#### Limitaciones del Decoder Básico

El decoder básico extrae los metadatos principales del replay. Para análisis completo, **use el decoder V2** (`npm run decode:v2`) que incluye todas las mejoras y mejor manejo de errores.

## Formato de archivo .hbr2

El formato de archivo .hbr2 es el formato utilizado por Haxball para almacenar las replays de los partidos. A continuación se detalla la estructura de estos archivos:

### Estructura Básica

1. **Encabezado**:

   - Identificador: `'HBR2'` (4 bytes) - Magic bytes que identifican el tipo de archivo
   - Versión: `uint32` (4 bytes) - Actualmente la versión es 3

2. **Datos Comprimidos**:
   - El resto del archivo está comprimido utilizando zlib
   - Método de descompresión en Python:
   ```python
   decompressed_data = zlib.decompress(compressed_data, wbits=-15)
   ```

Estructura de Datos Descomprimidos

Basado en el análisis realizado, los datos descomprimidos tienen la siguiente estructura:

    Cabecera de la Sala (primeros bytes):
        Estado (2 bytes): Valor 0x0000 para salas estándar, 0x0003 para salas con información adicional
        Nombre de la Sala:
            Longitud del nombre (1 byte): Indica la cantidad de bytes que ocupa el nombre
            Nombre (N bytes): El nombre de la sala como texto, donde N es la longitud especificada

    Configuración de la Sala:
        Estado de Equipos (1 byte): Indica si los equipos están bloqueados
        Límite de Goles (4 bytes): Número máximo de goles para finalizar el partido
        Límite de Tiempo (4 bytes): Tiempo máximo de juego en segundos
        Campo Desconocido (4 bytes): Función no identificada

    Información del Stadium (Mapa):
        Tipo de Stadium (1 byte): Si es 0xFF, indica que es un stadium personalizado
        Para stadiums personalizados:
            Longitud del nombre del stadium (1 byte)
            Nombre del stadium (N bytes)
        Campo de Configuración (4 bytes): Generalmente con valor 1, propósito exacto desconocido
        Datos del Stadium: Coordenadas, dimensiones y propiedades del mapa (formato en análisis)
