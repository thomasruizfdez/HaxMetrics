# HaxMetrics

HaxMetrics es una herramienta para analizar replays de Haxball en formato .hbr2 y extraer métricas útiles para el análisis de partidos.

## Herramientas

### Decoder HBR2 a JSON

El proyecto incluye un script de Node.js que decodifica archivos .hbr2 y exporta los metadatos a formato JSON.

#### Instalación

```bash
npm install
```

#### Uso

```bash
# Usar con npm
npm run decode -- <archivo.hbr2> [salida.json]

# Ejemplo
npm run decode -- src/replays/prueba.hbr2 output.json

# Si no se especifica archivo de salida, se usa el mismo nombre con .json
npm run decode -- src/replays/prueba.hbr2
```

#### Datos Extraídos

El script extrae los siguientes datos del replay:

- **Metadata**: Versión del formato, duración, tamaño del archivo
- **Room Info**: Nombre de la sala
- **Game Settings**: 
  - Equipos bloqueados
  - Límite de goles
  - Límite de tiempo
  - Configuración de kick (rate limit, burst, timeout)
- **Stadium**: 
  - Nombre del estadio
  - Tipo (predefinido o personalizado)
- **Messages**: Mensajes del sistema (si existen)
- **Game State**: Estado del juego (activo/inactivo)

#### Ejemplo de Salida JSON

```json
{
  "metadata": {
    "version": 3,
    "duration": 34,
    "fileSize": 76,
    "decompressedSize": 94
  },
  "roomInfo": {
    "name": "Bandolero's room"
  },
  "stadium": {
    "name": "Huge",
    "customStadium": false
  },
  "gameState": {
    "teamsLocked": false,
    "scoreLimit": 8,
    "timeLimit": 9,
    "kickRateLimitBurst": 1,
    "kickRateLimit": 0,
    "kickTimeout": 2,
    "gameActive": false
  },
  "messages": []
}
```

#### Limitaciones

El parser actual extrae los metadatos principales del replay. El análisis completo del flujo de acciones/eventos requeriría implementar la máquina de estados completa del código original de Haxball, lo cual está fuera del alcance de esta versión.

Para análisis detallado de acciones y eventos, se recomienda usar el parser Python incluido en el proyecto.

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
