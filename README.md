# HaxMetrics

HaxMetrics es una herramienta para analizar replays de Haxball en formato .hbr2 y extraer métricas útiles para el análisis de partidos.

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
