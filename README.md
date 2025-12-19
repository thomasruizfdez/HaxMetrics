# HaxMetrics

HaxMetrics es una herramienta para analizar replays de Haxball en formato .hbr2 y extraer métricas útiles para el análisis de partidos.

## Herramientas

### Decoder HBR2 a JSON

El proyecto incluye dos decoders de Node.js para archivos .hbr2:

1. **Decoder Básico** (`decode_hbr2.js`): Extrae metadatos básicos
2. **Decoder Completo** (`decode_hbr2_complete.js`): Extrae TODOS los datos usando el código original de Haxball

#### Instalación

```bash
npm install
```

#### Uso del Decoder Completo (Recomendado)

El decoder completo utiliza el código JavaScript original de Haxball para decodificar completamente los archivos .hbr2:

```bash
# Usar con npm
npm run decode:full -- <archivo.hbr2> [salida.json]

# Ejemplo
npm run decode:full -- src/replays/prueba.hbr2 output.json

# Si no se especifica archivo de salida, se usa el mismo nombre con .json
npm run decode:full -- src/replays/prueba.hbr2
```

#### Datos Extraídos por el Decoder Completo

El decoder completo extrae TODA la información del replay:

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
- **Players** (Jugadores):
  - ID, nombre, admin status
  - Avatar, país
  - Equipo asignado
  - Posición en el campo (x, y)
  - Radio del disco
- **Game State** (Estado del juego):
  - Tiempo actual
  - Límites de tiempo y score
  - Score actual (rojo vs azul)
  - Posiciones y velocidades de todos los discos (pelota + jugadores)
- **Teams** (Equipos):
  - Configuración de colores
  - Información de espectadores, equipo rojo y azul

#### Ejemplo de Salida JSON (Decoder Completo)

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
      "disc": null
    }
  ],
  "gameState": null,
  "teams": {
    "spectators": null,
    "red": { /* colores y configuración */ },
    "blue": { /* colores y configuración */ }
  }
}
```

#### Uso del Decoder Básico

El decoder básico extrae metadatos principales del replay:

```bash
# Usar con npm
npm run decode -- <archivo.hbr2> [salida.json]

# Ejemplo
npm run decode -- src/replays/prueba.hbr2 output.json
```

#### Limitaciones del Decoder Básico

El decoder básico extrae los metadatos principales del replay. Para análisis completo, **use el decoder completo** (`npm run decode:full`).

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
