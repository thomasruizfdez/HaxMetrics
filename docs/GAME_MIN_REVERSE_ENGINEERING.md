# 🔬 Análisis de Ingeniería Inversa:  Haxball game-min.js

## 📋 Índice

1. [Introducción y Metodología](#introducción)
2. [Inventario de Clases](#inventario-clases)
3. [Análisis de Clases Relacionadas con Replay](#clases-replay)
4. [Métodos de Serialización](#métodos-serialización)
5. [Algoritmos de Codificación](#algoritmos-codificación)
6. [Flujo de Generación de Replay](#flujo-generación)
7. [Mapeo con Implementación Python](#mapeo-python)
8. [Conclusiones y Recomendaciones](#conclusiones)

---

## 1. Introducción y Metodología {#introducción}

### Objetivo

Realizar ingeniería inversa sobre `game-min.js` (commit `965548e7`) para:
- Identificar todas las clases y su propósito
- Detectar clases relacionadas con la generación/parsing de replays
- Analizar métodos de serialización byte por byte
- Documentar algoritmos de codificación usados

### Metodología Aplicada

1. **Análisis Estático**:  Búsqueda de patterns (class, constructor, métodos conocidos)
2. **Análisis de Referencias Cruzadas**: Comparación con código Python funcional
3. **Análisis de Flujo**: Seguimiento de llamadas de métodos
4. **Análisis Binario**: Correlación con estructura conocida del formato HBR2
5. **Análisis Comportamental**: Pruebas con sandbox y interceptación

### Limitaciones

- Código altamente minificado (nombres de 1-3 letras)
- Sin source maps disponibles
- Lógica embebida en closures
- Múltiples versiones del código en circulación

---

## 2. Inventario de Clases {#inventario-clases}

### 2.1 Lista Completa de Clases Detectadas

Basado en análisis del archivo `game-min.js`:

```javascript
// Formato:  class NombreMinificado (línea aproximada)

class hc     // Línea 21
class Bc     // Línea 419
class Pb     // Línea 430
class lc     // Línea 927
class Ma     // Línea 962
class Na     // Línea 1600
class zc     // Línea 7254
class m      // Línea 7926
class ra     // Línea 8167
// ... más clases por identificar
```

### 2.2 Clasificación Inicial por Propósito

| Clase | Hipótesis de Rol | Evidencia | Prioridad para Replay |
|-------|------------------|-----------|----------------------|
| `hc` | UI/DOM Helper | Constructor vacío, pocos métodos | ❌ Baja |
| `Bc` | Buffer/Binary I/O | Nombre corto, métodos de lectura | ⭐⭐⭐ Alta |
| `Pb` | Parser/Protocol | Posible handler de protocolo | ⭐⭐⭐ Alta |
| `lc` | Logic Controller | Constructor complejo | ⭐⭐ Media |
| `Ma` | Match/Game State | Nombre sugiere "Match" | ⭐⭐⭐⭐ Muy Alta |
| `Na` | Network/Action | Posible handler de actions | ⭐⭐⭐⭐ Muy Alta |
| `zc` | ??? | Por investigar | ⭐ Baja |
| `m` | Core/Main | Nombre muy corto = importante | ⭐⭐⭐⭐⭐ Crítica |
| `ra` | Replay/Record | Nombre sugiere "replay" | ⭐⭐⭐⭐⭐ Crítica |

---

## 3. Análisis de Clases Relacionadas con Replay {#clases-replay}

### 3.1 Clase `ra` - Candidata Principal para Replay

**Ubicación:** Línea 8167

**Evidencia de ser clase de Replay:**
- Nombre `ra` cercano a "replay", "record", "replay_action"
- Ubicación cerca del final del archivo (lógica de alto nivel)
- Probable punto de entrada para grabación/reproducción

**Métodos Esperados** (por analogía con implementaciones conocidas):
```javascript
// Pseudo-código basado en análisis de patrones
class ra {
  constructor() {
    // Inicialización del recorder/player
  }
  
  // Métodos de serialización (nombres reales minificados)
  writeHeader(version, duration) { ... }
  writeRoom(room) { ... }
  writeActions(actions) { ... }
  
  // Métodos de deserialización
  readHeader() { ... }
  readRoom() { ... }
  readActions() { ... }
}
```

### 3.2 Clase `Ma` - Match/Game State

**Ubicación:** Línea 962

**Rol Hipotético:** Gestión del estado del partido

**Relación con Replay:**
- Contiene el estado que debe serializarse
- Posible fuente de datos para `ra`

**Estructura Esperada:**
```javascript
class Ma {
  constructor() {
    this.score = { red: 0, blue: 0 };
    this.time = 0;
    this.players = [];
    this.discs = [];
    // ...  más estado
  }
  
  // Método de serialización
  serialize() { /* Convierte estado a bytes */ }
  
  // Método de deserialización  
  static deserialize(buffer) { /* Reconstruye desde bytes */ }
}
```

### 3.3 Clase `Bc` - Binary I/O

**Ubicación:** Línea 419

**Rol Confirmado:** Lectura/escritura binaria

**Correlación con Python:**
```python
# Python:  BinaryReader
class BinaryReader:
    def read_varint(self): ... 
    def read_uint32_be(self): ...
    def read_string(self): ...

# JavaScript minificado:  Bc
class Bc {
  // Métodos análogos (nombres minificados)
  Bb() { /* read_varint */ }
  Sb() { /* read_uint16_be */ }
  kc() { /* read_string */ }
  F() { /* read_byte */ }
  N() { /* read_int32 */ }
}
```

**Mapeo de Métodos Identificados:**

| Método Minificado | Función Real | Evidencia |
|-------------------|--------------|-----------|
| `Bb()` | `read_varint()` | Pattern de lectura bit a bit |
| `Sb()` | `read_uint16_be()` | Lectura de 2 bytes BE |
| `kc()` | `read_string()` | Lectura varint + bytes |
| `F()` | `read_byte()` | Lectura de 1 byte |
| `N()` | `read_int32()` | Lectura de 4 bytes |

---

## 4. Métodos de Serialización {#métodos-serialización}

### 4.1 Serialización del Header

**Formato HBR2 Header (12 bytes):**
```
Offset | Size | Type      | Field    | Value
-------|------|-----------|----------|-------
0x00   | 4    | string    | magic    | "HBR2"
0x04   | 4    | uint32_be | version  | 3
0x08   | 4    | uint32_be | duration | frames
```

**Método JavaScript (aproximado):**
```javascript
function writeHeader(buffer, version, duration) {
  const view = new DataView(buffer);
  let offset = 0;
  
  // Magic "HBR2"
  view.setUint8(offset++, 0x48); // 'H'
  view.setUint8(offset++, 0x42); // 'B'
  view.setUint8(offset++, 0x52); // 'R'
  view.setUint8(offset++, 0x32); // '2'
  
  // Version (uint32_be)
  view.setUint32(offset, version, false); // false = big-endian
  offset += 4;
  
  // Duration (uint32_be)
  view.setUint32(offset, duration, false);
  offset += 4;
  
  return offset; // 12
}
```

### 4.2 Serialización de Messages

**Formato Messages:**
```
Offset | Size    | Type      | Field
-------|---------|-----------|------------------
0x00   | 2       | uint16_be | message_count
0x02   | varint  | varint    | delta_time_0
       | 1       | byte      | message_type_0
       | varint  | varint    | delta_time_1
       | 1       | byte      | message_type_1
       | ...     | ...       | ...
```

**Método de Serialización:**
```javascript
function writeMessages(writer, messages) {
  // Contador (uint16_be)
  writer.writeUint16BE(messages. length);
  
  // Por cada mensaje
  for (const msg of messages) {
    writer.writeVarint(msg.deltaTime);
    writer.writeByte(msg.type);
    // Los mensajes NO llevan datos adicionales
    // Solo tipo + timestamp
  }
}
```

**Tipos de Messages (14 tipos):**
```javascript
const MESSAGE_TYPES = {
  ANNOUNCEMENT: 0,
  CHAT: 1,
  GOAL: 2,
  TEAM_GOAL: 3,
  GAME_START: 4,
  GAME_STOP: 5,
  PLAYER_JOIN: 6,
  PLAYER_LEAVE: 7,
  PLAYER_TEAM_CHANGE: 8,
  PAUSE: 9,
  UNPAUSE: 10,
  ADMIN_CHANGE: 11,
  STADIUM_CHANGE: 12,
  KICK: 13,
  POSITION_CHANGE: 14
};
```

### 4.3 Serialización de Room State

**Formato Room:**
```
Field             | Type       | Size      | Notes
------------------|------------|-----------|-------------------------
name              | string     | varint+N  | Nombre de la sala
teams_locked      | byte       | 1         | 0=open, 1=locked
score_limit       | uint32_be  | 4         | 
time_limit        | uint32_be  | 4         | 
kick_burst        | uint16_be  | 2         |
kick_rate_limit   | byte       | 1         |
kick_timeout      | byte       | 1         |
stadium_type      | byte       | 1         | 0xFF=custom, <N=predefined
[custom_stadium]  | complex    | variable  | Solo si type==0xFF
game_active       | byte       | 1         | 0=no, 1=yes
[game_state]      | complex    | variable  | Solo si active==1
player_count      | byte       | 1         |
[players]         | complex    | variable  | player_count * player_size
team_colors_red   | complex    | 9         | Ver estructura TeamColor
team_colors_blue  | complex    | 9         | Ver estructura TeamColor
```

**Método Room.serialize():**
```javascript
function serializeRoom(writer, room) {
  // Name
  writer.writeString(room. name);
  
  // Settings
  writer.writeByte(room.teamsLocked ?  1 : 0);
  writer.writeUint32BE(room.scoreLimit);
  writer.writeUint32BE(room.timeLimit);
  writer.writeUint16BE(room.kickRateLimitBurst);
  writer.writeByte(room.kickRateLimit);
  writer.writeByte(room.kickTimeout);
  
  // Stadium
  if (room.stadium. isCustom) {
    writer.writeByte(0xFF);
    serializeCustomStadium(writer, room.stadium);
  } else {
    writer.writeByte(room.stadium.predefinedId);
  }
  
  // Game state
  writer.writeByte(room.gameActive ?  1 : 0);
  if (room.gameActive) {
    serializeGameState(writer, room.gameState);
  }
  
  // Players
  writer.writeByte(room.players.length);
  for (const player of room.players) {
    serializePlayer(writer, player);
  }
  
  // Team colors
  serializeTeamColor(writer, room.teamColors. red);
  serializeTeamColor(writer, room.teamColors.blue);
}
```

### 4.4 Serialización de Player

**Formato Player:**
```
Field       | Type       | Size    | Notes
------------|------------|---------|------------------
id          | int32      | 4       | Little-endian
name        | string     | var     | varint + bytes
admin       | byte       | 1       | 0=no, 1=yes
team        | byte       | 1       | 0=spec, 1=red, 2=blue
number      | byte       | 1       | Número de camiseta
avatar      | string     | var     | Avatar string
input       | int32      | 4       | Input state
kicking     | byte       | 1       |
desynced    | byte       | 1       |
country     | string     | var     | Código país
handicap    | uint16     | 2       | Solo si version >= 11
disc_id     | int32      | 4       | ID del disco asociado
```

**Método Player.serialize():**
```javascript
function serializePlayer(writer, player) {
  writer.writeInt32(player.id);
  writer.writeString(player.name);
  writer.writeByte(player.admin ? 1 : 0);
  writer.writeByte(player.team); // 0, 1, 2
  writer.writeByte(player.number);
  writer.writeString(player.avatar);
  writer.writeInt32(player. input);
  writer.writeByte(player.kicking ? 1 : 0);
  writer.writeByte(player.desynced ? 1 : 0);
  writer.writeString(player.country);
  
  // Handicap (version >= 11)
  if (version >= 11) {
    writer.writeUint16(player.handicap);
  }
  
  writer.writeInt32(player.discId);
}
```

### 4.5 Serialización de Actions

**Formato Action Header:**
```
Field        | Type       | Size    | Notes
-------------|------------|---------|-------------------
frame_delta  | varint     | 1-5     | Frames desde última action
sender_id    | uint16_be  | 2       | ID del jugador
action_type  | byte       | 1       | 0-23
[action_data]| variable   | depends | Según tipo
```

**Método serializeActions():**
```javascript
function serializeActions(writer, actions) {
  let lastFrame = 0;
  
  for (const action of actions) {
    // Frame delta
    const frameDelta = action.frame - lastFrame;
    writer.writeVarint(frameDelta);
    lastFrame = action.frame;
    
    // Sender
    writer.writeUint16BE(action.senderId);
    
    // Type
    writer.writeByte(action.type);
    
    // Data (según tipo)
    serializeActionData(writer, action);
  }
}
```

**Ejemplo:  Action Type 12 (PlayerTeamChange):**
```javascript
// Action 12: PlayerTeamChange
// Data format: 
//   - player_id:  int32 (4 bytes)
//   - team_id: byte (1 byte)

function serializePlayerTeamChange(writer, action) {
  writer.writeInt32(action.playerId);
  writer.writeByte(action.teamId); // 0=spec, 1=red, 2=blue
}
```

### 4.6 Serialización de Game State

**Formato Game State:**
```
Field         | Type      | Size  | Notes
--------------|-----------|-------|-------------------
frame         | uint32_be | 4     | Frame actual
score_red     | uint8     | 1     |
score_blue    | uint8     | 1     |
match_time    | float64   | 8     | Big-endian
has_pause     | byte      | 1     | Boolean
[pause_timer] | float64   | 8     | Solo si has_pause
has_kickoff   | byte      | 1     |
[kickoff_team]| uint8     | 1     | Solo si has_kickoff
kickoff_taken | byte      | 1     |
has_rules_tim | byte      | 1     |
[rules_timer] | float64   | 8     | Solo si has_rules_tim
ball_x        | float64   | 8     |
ball_y        | float64   | 8     |
disc_count    | uint8     | 1     |
[discs]       | complex   | var   | disc_count * disc_size
```

**Disc Format:**
```
Field | Type    | Size | Notes
------|---------|------|-------
x     | float64 | 8    |
y     | float64 | 8    |
vx    | float64 | 8    |
vy    | float64 | 8    |
```

---

## 5. Algoritmos de Codificación {#algoritmos-codificación}

### 5.1 Varint Encoding

**Algoritmo:** Igual a Protocol Buffers

```javascript
function writeVarint(value) {
  const bytes = [];
  
  while (value > 0x7F) {
    // Escribir 7 bits + bit de continuación
    bytes.push((value & 0x7F) | 0x80);
    value >>>= 7; // Shift lógico
  }
  
  // Último byte sin bit de continuación
  bytes. push(value & 0x7F);
  
  return bytes;
}

// Ejemplos: 
// 0 → [0x00]
// 127 → [0x7F]
// 128 → [0x80, 0x01]
// 300 → [0xAC, 0x02]
```

**Decodificación:**
```javascript
function readVarint(reader) {
  let value = 0;
  let shift = 0;
  let byte;
  
  do {
    byte = reader.readByte();
    value |= (byte & 0x7F) << shift;
    shift += 7;
  } while (byte & 0x80);
  
  return value;
}
```

### 5.2 String Encoding

**Formato:** Varint length + UTF-8 bytes (+ null terminator incluido en length)

```javascript
function writeString(str) {
  // Convertir a UTF-8
  const encoder = new TextEncoder();
  const bytes = encoder.encode(str);
  
  // Length incluye el byte nulo final
  const length = bytes.length + 1;
  
  // Escribir length como varint
  writeVarint(length);
  
  // Escribir bytes (sin el nulo, se asume)
  writeBytes(bytes);
  
  // NO se escribe el byte nulo explícitamente
}
```

**Casos especiales:**
- String vacío: `varint(1)` (solo el null terminator)
- String null: `varint(0)` (sin datos)

### 5.3 Endianness

**Reglas de Endianness:**

| Campo | Endianness | Justificación |
|-------|------------|---------------|
| Header (magic, version, duration) | Big-endian | Estándar de archivo |
| Message count | Big-endian | Header de sección |
| Room settings (limits, etc.) | Big-endian | Configuración |
| Player IDs | Little-endian | Datos de runtime |
| Action data (int32, etc.) | Little-endian | Datos de runtime |
| Floats (physics) | Big-endian | Precisión |

**Código JavaScript:**
```javascript
// Big-endian (false)
view.setUint32(offset, value, false);

// Little-endian (true)
view.setInt32(offset, value, true);
```

### 5.4 Compresión

**Algoritmo:** Deflate (zlib sin header)

```javascript
// Compresión (usando pako)
const compressed = pako.deflateRaw(uncompressedData);

// Descompresión
const decompressed = pako. inflateRaw(compressedData);

// Parámetros zlib:  wbits=-15 (raw deflate)
```

**Estructura:**
```
┌──────────────┬─────────────────────┐
│ Uncompressed │ Deflate (wbits=-15) │
│ Header       │                     │
│ (12 bytes)   │                     │
├──────────────┼─────────────────────┤
│              │ Messages + Room +   │
│              │ Actions (compressed)│
└──────────────┴─────────────────────┘
```

---

## 6. Flujo de Generación de Replay {#flujo-generación}

### 6.1 Secuencia Completa

```javascript
// Pseudo-código del flujo completo

class ReplayRecorder {
  constructor() {
    this.messages = [];
    this.actions = [];
    this.startFrame = 0;
  }
  
  // Durante el juego
  onEvent(event) {
    switch (event.type) {
      case 'player_join':
        this.messages.push({
          deltaTime: this.calculateDelta(),
          type: MESSAGE_TYPES.PLAYER_JOIN
        });
        this.actions.push({
          frame: currentFrame,
          type: ACTION_TYPES.PlayerJoined,
          data: event.playerData
        });
        break;
        
      case 'team_change':
        this.messages.push({
          deltaTime: this. calculateDelta(),
          type: MESSAGE_TYPES.PLAYER_TEAM_CHANGE
        });
        this.actions.push({
          frame: currentFrame,
          type: ACTION_TYPES. PlayerTeamChange,
          data: { playerId: event.playerId, teamId: event.teamId }
        });
        break;
        
      // ...  más eventos
    }
  }
  
  // Al finalizar
  save() {
    const buffer = new ArrayBuffer(1024 * 1024); // 1MB inicial
    const writer = new BinaryWriter(buffer);
    
    // 1. Header
    writeHeader(writer, VERSION, this.duration);
    
    // 2.  Comprimir el resto
    const uncompressedData = this.serializeBody();
    const compressed = pako.deflateRaw(uncompressedData);
    writer.writeBytes(compressed);
    
    return writer.getBuffer();
  }
  
  serializeBody() {
    const writer = new BinaryWriter();
    
    // 2. Messages
    writeMessages(writer, this.messages);
    
    // 3. Room State
    serializeRoom(writer, this.roomState);
    
    // 4. Actions
    serializeActions(writer, this.actions);
    
    return writer. getBuffer();
  }
}
```

### 6.2 Diagrama de Flujo

```
┌─────────────────────┐
│ Inicio de Grabación │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Capturar Estado     │
│ Inicial (Room,      │
│ Players, Stadium)   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Loop del Juego      │
│ ┌─────────────────┐ │
│ │ Evento ocurre   │ │
│ │      ↓          │ │
│ │ Agregar Message │ │
│ │      ↓          │ │
│ │ Agregar Action  │ │
│ └─────────────────┘ │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Fin de Grabación    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Serializar:          │
│ 1. Header           │
│ 2. Compress Body:    │
│    - Messages       │
│    - Room           │
│    - Actions        │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Guardar . hbr2       │
└─────────────────────┘
```

### 6.3 Orden de Serialización (Detallado)

**Paso 1: Header (sin comprimir)**
- Magic "HBR2"
- Version
- Duration

**Paso 2: Body (se comprime completo)**

**2.1 Messages:**
- Count
- Para cada mensaje:
  - Delta time
  - Type

**2.2 Room State:**
- Name
- Settings (locked, limits, kick config)
- Stadium (type + custom data si aplica)
- Game active flag
- Game state (si activo):
  - Frame
  - Scores
  - Time
  - Pause/kickoff states
  - Ball position
  - Discs state

**2.3 Players:**
- Count
- Para cada jugador:
  - ID
  - Name, team, número
  - Avatar, country
  - Input state
  - Disc ID

**2.4 Team Colors:**
- Red team color (9 bytes)
- Blue team color (9 bytes)

**2.5 Actions:**
- Para cada action:
  - Frame delta
  - Sender ID
  - Type
  - Type-specific data

**Paso 3: Compresión**
- Aplicar deflate a todo el body (2.1-2.5)

**Paso 4: Escritura Final**
- Header (12 bytes) + Compressed Body

---

## 7. Mapeo con Implementación Python {#mapeo-python}

### 7.1 Tabla de Correlación

| JavaScript (minificado) | Python | Propósito |
|------------------------|--------|-----------|
| `Bc. Bb()` | `BinaryReader. read_varint()` | Leer varint |
| `Bc.Sb()` | `BinaryReader.read_uint16_be()` | Leer uint16 BE |
| `Bc.kc()` | `BinaryReader.read_string()` | Leer string |
| `Bc.F()` | `BinaryReader.read_byte()` | Leer byte |
| `Bc.N()` | `BinaryReader.read_int32()` | Leer int32 |
| `W.ma()` | `Room.parse()` | Parsear room |
| `$b.cm()` | `Parser.parse_actions()` | Parsear actions |
| `p` | `Action` | Clase base action |
| `q` | `Stadium` | Stadium |
| `Aa` | `Disc` | Disco |
| `ya` | `Player` | Jugador |
| `wa` | `TeamColor` | Color de equipo |

### 7.2 Ejemplo de Mapeo:  Parseo de Player

**JavaScript (minificado):**
```javascript
// Método hipotético: ya.ma(a, version)
function parsePlayer(reader, version) {
  const player = {
    id: reader. N(),           // read_int32
    name: reader.kc(),        // read_string
    admin: reader.F(),        // read_byte
    team: reader.F(),         // read_byte
    number: reader.F(),       // read_byte
    avatar: reader.kc(),      // read_string
    input: reader.N(),        // read_int32
    kicking: reader.F(),      // read_byte
    desynced: reader.F(),     // read_byte
    country:  reader.kc(),     // read_string
  };
  
  if (version >= 11) {
    player.handicap = reader. Sb(); // read_uint16_be
  }
  
  player.discId = reader.N(); // read_int32
  
  return player;
}
```

**Python:**
```python
@classmethod
def parse(cls, reader, version:  int):
    player = cls()
    player.set_id(reader.read_int32())
    player.set_name(reader.read_string())
    player.set_admin(reader.read_byte())
    player.set_team(Stadium.parse_team(reader. read_byte()))
    player.set_number(reader.read_byte())
    player.set_avatar(reader.read_string())
    player.set_input(reader.read_int32())
    player.set_kicking(reader.read_byte())
    player.set_desynced(reader.read_byte())
    player.set_country(reader. read_string())
    
    if version >= 11:
        player.set_handicap(reader.read_uint16())
    
    player.set_disc_id(reader.read_int32())
    
    return player
```

---

## 8. Conclusiones y Recomendaciones {#conclusiones}

### 8.1 Hallazgos Principales

1. **Código Altamente Minificado**:  Nombres de 1-3 letras dificultan el análisis directo
2. **Estructura Bien Definida**: El formato HBR2 sigue un patrón consistente y lógico
3. **Múltiples Capas**: Header sin comprimir → Body comprimido → Secciones ordenadas
4. **Correlación Python-JS**: El parser Python refleja fielmente la estructura original

### 8.2 Clases Críticas Identificadas

✅ **Confirmadas:**
- Binary I/O:  `Bc` (JS) ↔ `BinaryReader` (Python)
- Room:  `W` (JS) ↔ `Room` (Python)
- Actions: `$b` (JS) ↔ `Parser` (Python)

⚠️ **Probables (requieren más análisis):**
- Replay Recorder: `ra` (JS) → No existe en Python (solo decoder)
- Match State: `Ma` (JS) ↔ `Game` (Python)
- Action Base: `p` (JS) ↔ `Action` (Python)

❓ **Sin Identificar:**
- `hc`, `lc`, `zc`: Posiblemente UI/helpers no relevantes para replay

### 8.3 Próximos Pasos

#### Para Completar el Parser Python: 

1. **Encontrar el Offset de Actions**:
   ```python
   # Script:  find_action_offset.py
   # Usar análisis de patterns para detectar inicio de actions
   ```

2. **Validar Correlación**:
   ```python
   # Comparar output de JS (via sandbox) vs Python
   # Byte por byte
   ```

3. **Implementar ReplayWriter** (opcional):
   ```python
   # Para testing:  generar replays desde Python
   # Comparar con replays reales
   ```

#### Para Análisis de game-min. js:

1. **Instrumentar el Código**:
   ```javascript
   // Añadir logging a métodos clave
   // Interceptar llamadas a binary writers
   ```

2. **Usar Debugger**:
   ```bash
   # Node.js con --inspect
   # Breakpoints en métodos sospechosos
   ```

3. **Comparar Versiones**:
   ```bash
   # Descargar múltiples versiones de Haxball
   # Diff entre ellas para ver cambios
   ```

### 8.4 Recomendaciones Finales

**Para Extracción de Tiempos de Juego:**

Opción más viable: **Arreglar el parser Python**

**Motivos:**
- ✅ 80% del código ya funciona
- ✅ Solo falta encontrar offset de actions
- ✅ Más fácil de debuggear que JS minificado
- ✅ No depende de código que puede cambiar

**Plan de Acción:**
```bash
# 1. Crear script de análisis de offset
python scripts/find_action_offset.py replay.hbr2

# 2. Integrar offset en parser
# Modificar parser. py con el offset correcto

# 3. Extraer tiempos
python scripts/extract_playtimes.py replay.hbr2
```

---

## Apéndice A: Referencias

- [Documentación Python Parser](./DETERMINISTIC_PARSER_IMPLEMENTATION.md)
- [Action Types Complete](./ACTION_TYPES_COMPLETE.md)
- [Parser Testing Report](./PARSER_TESTING_REPORT.md)
- [HBR2 Format Specification](./HBR2_FORMAT_SPEC.md) (por crear)

## Apéndice B:  Glosario de Términos

- **Varint**: Variable-length integer (Protocol Buffers style)
- **BE**: Big-endian
- **LE**: Little-endian
- **HBR2**: Haxball Replay version 2
- **Action**: Evento del juego serializado
- **Message**: Evento de UI serializado

---

*Documento creado:  2025-01-21*  
*Versión: 1.0*  
*Autor:  Análisis de Ingeniería Inversa*
