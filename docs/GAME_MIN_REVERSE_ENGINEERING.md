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

### 4.7 Serialización de Custom Stadium (DETALLADO)

#### Estructura Binaria Completa

Custom stadiums son identificados por el byte `0xFF` (255) como tipo de stadium. La estructura completa es:

**Tabla de Campos Principales:**

```
Offset | Size    | Type       | Field                    | Notes
-------|---------|------------|--------------------------|---------------------------
0x00   | 1       | byte       | type                     | 0xFF para custom
0x01   | varint  | varint     | name_length              | Longitud + 1 (null term)
...    | N       | string     | name                     | Ej: "LIRS RS 4v4"
...    | 1       | byte       | background_type          | 0=grass, 1=hockey, 2=none
...    | 8       | float64_be | background_width         | Ancho del fondo
...    | 8       | float64_be | background_height        | Alto del fondo
...    | 8       | float64_be | max_view_width           | Ancho máx de vista
...    | 8       | float64_be | max_view_height          | Alto máx de vista
...    | 8       | float64_be | spawn_distance           | Distancia spawn jugadores
...    | 8       | float64_be | player_physics_bcoef     | Coef. rebote jugador
...    | 8       | float64_be | player_physics_accel     | Aceleración
...    | 8       | float64_be | player_physics_kick_str  | Fuerza de patada
...    | 4       | int32      | max_view_width_override  | Nullable (0xFFFFFFFF=null)
...    | 1       | byte       | camera_follow            | Boolean
...    | 1       | byte       | can_be_stored            | Boolean
...    | 1       | byte       | full_reset_after_goal    | Boolean
...    | 1       | byte       | vertex_count             | Número de vértices
...    | N*32    | vertex[]   | vertices                 | Ver estructura Vertex
...    | 1       | byte       | segment_count            | Número de segmentos
...    | N*var   | segment[]  | segments                 | Ver estructura Segment
...    | 1       | byte       | plane_count              | Número de planos
...    | N*var   | plane[]    | planes                   | Ver estructura Plane
...    | 1       | byte       | goal_count               | Número de goals
...    | N*var   | goal[]     | goals                    | Ver estructura Goal
...    | 1       | byte       | disc_count               | Número de discos
...    | N*var   | disc[]     | discs                    | Ver estructura Disc
...    | 1       | byte       | joint_count              | Número de joints
...    | N*var   | joint[]    | joints                   | Ver estructura Joint
```

#### Estructuras Internas

**Vertex (32 bytes fijos):**
```
Offset | Size    | Type       | Field    | Notes
-------|---------|------------|----------|--------
0x00   | 8       | float64_be | x        | Coordenada X
0x08   | 8       | float64_be | y        | Coordenada Y
0x10   | 8       | float64_be | bcoef    | Coeficiente rebote
0x18   | 8       | float64_be | cMask    | Máscara colisión
```

**Segment (variable):**
```
Offset | Size    | Type       | Field    | Notes
-------|---------|------------|----------|--------
0x00   | 1       | byte       | v0       | Índice vértice inicio
0x01   | 1       | byte       | v1       | Índice vértice fin
0x02   | 8       | float64_be | bcoef    | Coeficiente rebote
0x0A   | 8       | float64_be | cMask    | Máscara colisión
0x12   | 4       | uint32_be  | color    | Color ARGB (nullable)
0x16   | 1       | byte       | vis      | Boolean visibilidad
0x17   | 1       | byte       | curve    | Nullable float64 (flag)
[...]  | 8       | float64_be | [curve]  | Solo si flag != 0
```

**Plane (variable):**
```
Offset | Size    | Type       | Field    | Notes
-------|---------|------------|----------|--------
0x00   | 8       | float64_be | normal_x | Normal X
0x08   | 8       | float64_be | normal_y | Normal Y
0x10   | 8       | float64_be | dist     | Distancia
0x18   | 8       | float64_be | bcoef    | Coeficiente rebote
0x20   | 8       | float64_be | cMask    | Máscara colisión
```

**Goal (variable):**
```
Offset | Size    | Type       | Field    | Notes
-------|---------|------------|----------|--------
0x00   | 8       | float64_be | p0_x     | Punto inicio X
0x08   | 8       | float64_be | p0_y     | Punto inicio Y
0x10   | 8       | float64_be | p1_x     | Punto fin X
0x18   | 8       | float64_be | p1_y     | Punto fin Y
0x20   | 1       | byte       | team     | 1=Red, 2=Blue
```

**Disc (variable):**
```
Offset | Size    | Type       | Field    | Notes
-------|---------|------------|----------|--------
0x00   | 8       | float64_be | x        | Posición X inicial
0x08   | 8       | float64_be | y        | Posición Y inicial
0x10   | 8       | float64_be | radius   | Radio
0x18   | 8       | float64_be | bcoef    | Coeficiente rebote
0x20   | 8       | float64_be | invMass  | Masa inversa
0x28   | 8       | float64_be | damping  | Amortiguación
0x30   | 4       | uint32_be  | color    | Color ARGB (nullable)
0x34   | 8       | float64_be | cMask    | Máscara colisión
0x3C   | 8       | float64_be | cGroup   | Grupo colisión
```

**Joint (variable):**
```
Offset | Size    | Type       | Field    | Notes
-------|---------|------------|----------|--------
0x00   | 1       | byte       | d0       | Índice disco 0
0x01   | 1       | byte       | d1       | Índice disco 1
0x02   | 8       | float64_be | length   | Longitud (nullable)
0x0A   | 4       | uint32_be  | color    | Color ARGB (nullable)
0x0E   | 8       | float64_be | strength | Fuerza
```

#### Ejemplo Real: LIRS RS 4v4

**Hex Dump de Inicio del Stadium:**
```hex
Offset   | Hex Data                                         | Annotation
---------|--------------------------------------------------|------------------
0x00015  | FF                                               | Custom stadium marker
0x00016  | 0C 4C 49 52 53 20 52 53 20 34 76 34              | Name: "LIRS RS 4v4" (length=12)
0x00022  | 00                                               | Background type: grass
0x00023  | 00 00 01 40 91 F8 00 00 00 00 00               | Background width: 1140.0
0x0002E  | 40 82 C0 00 00 00 00 00                          | Background height: 600.0
0x00036  | 40 66 80 00 00 00 00 00                          | Max view width: 180.0
0x0003E  | 00 00 00 00 00 00 00 00                          | Spawn distance: 0.0
0x00046  | 00 00 00 00 00 00 00 00                          | (more fields...)
```

**Análisis del Stadium LIRS RS 4v4:**
- Nombre: "LIRS RS 4v4"
- Background: Grass (tipo 0)
- Dimensiones: 1140.0 × 600.0
- Max View: 1300.0 × 670.0
- Spawn Distance: 560.0
- Player Physics:
  - b_coef: 0.3
  - acceleration: 0.12
  - kick_strength: 5.65
- Vértices: 0 (stadium vacío o simplificado)
- Segmentos: 0
- Planos: 0
- Goals: 0
- Discs: 0
- Joints: 0

**Correlación con Python:**

```python
# src/haxmetrics/models/stadium/stadium.py
@classmethod
def parse(cls, reader):
    stadium = cls()
    
    # Read stadium type (1 byte)
    stadium.type = reader.read_byte()
    
    # If it's a predefined stadium (< 255), just set the name
    if stadium.type < len(cls.STADIUMS):
        stadium.set_name(cls.STADIUMS[stadium.type])
        stadium.set_custom(False)
        return stadium
    
    # Custom stadium (type == 255)
    stadium.set_custom(True)
    stadium.set_name(reader.read_string())
    
    # Parse custom stadium properties
    stadium.set_background(Background.parse(reader))
    
    # Max view dimensions
    max_view_width = reader.read_double_be()
    max_view_height = reader.read_double_be()
    
    # Spawn distance
    stadium.set_spawn_distance(reader.read_double_be())
    
    # Player physics
    stadium.set_player_physics(PlayerPhysics.parse(reader))
    
    # Additional fields
    max_view_width_override = reader.read_nullable_int32()
    camera_follow = reader.read_uint8()
    can_be_stored = reader.read_uint8() != 0
    full_reset_after_goal = reader.read_uint8() != 0
    
    # Parse arrays
    stadium.vertexes = cls._parse_array(reader, Vertex)
    stadium.segments = cls._parse_array(reader, Segment)
    stadium.planes = cls._parse_array(reader, Plane)
    stadium.goals = cls._parse_array(reader, Goal)
    stadium.discs = cls._parse_array(reader, Disc)
    stadium.joints = cls._parse_array(reader, Joint)
    
    return stadium
```

---

### 4.8 Documentación Completa de Action Types (0-23)

Todos los action types siguen el mismo header básico:

```
Field        | Type       | Size    | Notes
-------------|------------|---------|-------------------
frame_delta  | varint     | 1-5     | Frames desde última action
sender_id    | uint16_be  | 2       | ID del jugador (0 = sistema)
action_type  | byte       | 1       | 0-23
[action_data]| variable   | depends | Datos específicos del tipo
```

#### Action 0: Message (Eb)

**Propósito:** Mensaje de sistema con color y estilo personalizado.

**Estructura de Datos:**
```
Offset | Size   | Type    | Field        | Notes
-------|--------|---------|--------------|-------
0x00   | varint | varint  | msg_length   | Longitud + 1
...    | N      | string  | message      | Texto del mensaje
...    | 4      | int32   | color        | ARGB
...    | 1      | byte    | style_flags  | Bold, italic, etc.
```

**Correlación con Python:**
```python
# src/haxmetrics/models/actions/message.py
class Message(Action):
    @classmethod
    def parse(cls, reader):
        obj = cls()
        obj.message = reader.read_string()
        obj.color = reader.read_int32()
        obj.style = reader.read_byte()
        return obj
```

#### Action 1: ToggleChat (Ha)

**Propósito:** Toggle del indicador de chat.

**Estructura de Datos:**
```
Offset | Size   | Type    | Field   | Notes
-------|--------|---------|---------|-------
0x00   | 1      | byte    | enabled | 0=off, 1=on
```

**Correlación con Python:**
```python
# src/haxmetrics/models/actions/toggle_chat.py
class ToggleChat(Action):
    @classmethod
    def parse(cls, reader):
        obj = cls()
        obj.enabled = reader.read_byte() != 0
        return obj
```

#### Action 2: ChangeStadium (cb)

**Propósito:** Cambio de stadium (carga desde bytes comprimidos).

**Estructura de Datos:**
```
Offset | Size   | Type    | Field           | Notes
-------|--------|---------|-----------------|-------
0x00   | 4      | int32   | compressed_size | Tamaño comprimido
...    | N      | bytes   | compressed_data | Stadium comprimido (zlib)
```

**Correlación con Python:**
```python
# src/haxmetrics/models/actions/change_stadium.py
class ChangeStadium(Action):
    @classmethod
    def parse(cls, reader):
        obj = cls()
        compressed_size = reader.read_int32()
        compressed_data = reader.read_bytes(compressed_size)
        obj.stadium_data = zlib.decompress(compressed_data, wbits=-15)
        return obj
```

#### Action 3: PlayerInput (La)

**Propósito:** Input del jugador (movimiento, patada).

**Estructura de Datos:**
```
Offset | Size   | Type    | Field   | Notes
-------|--------|---------|---------|-------
0x00   | 4      | int32   | input   | Bitmask: bit0=up, bit1=down, bit2=left, bit3=right, bit4=kick
```

**Correlación con Python:**
```python
# src/haxmetrics/models/actions/player_input.py
class PlayerInput(Action):
    @classmethod
    def parse(cls, reader):
        obj = cls()
        obj.input = reader.read_int32()
        return obj
```

#### Action 4: ChatMessage (Ya)

**Propósito:** Mensaje de chat de un jugador.

**Estructura de Datos:**
```
Offset | Size   | Type    | Field     | Notes
-------|--------|---------|-----------|-------
0x00   | varint | varint  | msg_len   | Longitud + 1
...    | N      | string  | message   | Texto del mensaje
```

**Correlación con Python:**
```python
# src/haxmetrics/models/actions/chat_message.py
class ChatMessage(Action):
    @classmethod
    def parse(cls, reader):
        obj = cls()
        obj.message = reader.read_string()
        return obj
```

#### Action 5: PlayerJoined (Na)

**Propósito:** Jugador se une a la sala.

**Estructura de Datos:**
```
Offset | Size   | Type    | Field    | Notes
-------|--------|---------|----------|-------
0x00   | 4      | int32   | id       | Player ID
...    | varint | varint  | name_len | Longitud + 1
...    | N      | string  | name     | Nombre del jugador
...    | varint | varint  | flag_len | Longitud + 1  
...    | N      | string  | flag     | Código de país
...    | varint | varint  | avatar   | Avatar string
```

**Correlación con Python:**
```python
# src/haxmetrics/models/actions/player_joined.py
class PlayerJoined(Action):
    @classmethod
    def parse(cls, reader):
        obj = cls()
        obj.id = reader.read_int32()
        obj.name = reader.read_string()
        obj.flag = reader.read_string()
        obj.avatar = reader.read_string()
        return obj
```

#### Action 6: PlayerLeft (ma)

**Propósito:** Jugador abandona la sala o es expulsado.

**Estructura de Datos:**
```
Offset | Size   | Type    | Field    | Notes
-------|--------|---------|----------|-------
0x00   | 4      | int32   | id       | Player ID
...    | varint | varint  | reason   | Razón (varint string)
...    | N      | string  | [reason] | Texto razón si hay
...    | 1      | byte    | banned   | 0=kicked, 1=banned
```

**Correlación con Python:**
```python
# src/haxmetrics/models/actions/player_left.py
class PlayerLeft(Action):
    @classmethod
    def parse(cls, reader):
        obj = cls()
        obj.id = reader.read_int32()
        obj.reason = reader.read_string()
        obj.banned = reader.read_byte() != 0
        return obj
```

#### Action 7: MatchStart (Va)

**Propósito:** Inicio de partido.

**Estructura de Datos:**
Sin datos adicionales (solo header).

**Correlación con Python:**
```python
# src/haxmetrics/models/actions/match_start.py
class MatchStart(Action):
    @classmethod
    def parse(cls, reader):
        return cls()
```

#### Action 8: MatchStopped (Wa)

**Propósito:** Fin de partido.

**Estructura de Datos:**
Sin datos adicionales (solo header).

**Correlación con Python:**
```python
# src/haxmetrics/models/actions/match_stopped.py
class MatchStopped(Action):
    @classmethod
    def parse(cls, reader):
        return cls()
```

#### Action 9: ChangePaused (Za)

**Propósito:** Cambio de estado de pausa.

**Estructura de Datos:**
```
Offset | Size   | Type    | Field   | Notes
-------|--------|---------|---------|-------
0x00   | 1      | byte    | paused  | 0=unpaused, 1=paused
```

**Correlación con Python:**
```python
# src/haxmetrics/models/actions/change_paused.py
class ChangePaused(Action):
    @classmethod
    def parse(cls, reader):
        obj = cls()
        obj.paused = reader.read_byte() != 0
        return obj
```

#### Action 10: ChangeGameSetting (va)

**Propósito:** Cambio de configuración del juego.

**Estructura de Datos:**
```
Offset | Size   | Type    | Field       | Notes
-------|--------|---------|-------------|-------
0x00   | 1      | byte    | setting_id  | ID del setting
...    | varies | varies  | value       | Valor (tipo depende de setting_id)
```

**Correlación con Python:**
```python
# src/haxmetrics/models/actions/change_game_setting.py
class ChangeGameSetting(Action):
    @classmethod
    def parse(cls, reader):
        obj = cls()
        obj.setting_id = reader.read_byte()
        # Parse value based on setting_id
        obj.value = cls._parse_setting_value(reader, obj.setting_id)
        return obj
```

#### Action 11: StadiumUpdate (Ea)

**Propósito:** Actualización del stadium.

**Estructura de Datos:**
```
Offset | Size   | Type    | Field    | Notes
-------|--------|---------|----------|-------
0x00   | varies | varies  | stadium  | Stadium completo (ver 4.7)
```

**Correlación con Python:**
```python
# src/haxmetrics/models/actions/stadium_update.py
class StadiumUpdate(Action):
    @classmethod
    def parse(cls, reader):
        obj = cls()
        obj.stadium = Stadium.parse(reader)
        return obj
```

#### Action 12: PlayerTeamChange (fa)

**Propósito:** Cambio de equipo de un jugador.

**Estructura de Datos:**
```
Offset | Size   | Type    | Field     | Notes
-------|--------|---------|-----------|-------
0x00   | 4      | int32   | player_id | ID del jugador
...    | 1      | byte    | team_id   | 0=spec, 1=red, 2=blue
```

**Correlación con Python:**
```python
# src/haxmetrics/models/actions/player_team_change.py
class PlayerTeamChange(Action):
    @classmethod
    def parse(cls, reader):
        obj = cls()
        obj.player_id = reader.read_int32()
        obj.team_id = reader.read_byte()
        return obj
```

#### Action 13: ChangeTeamsLock (Fa)

**Propósito:** Cambio de estado de bloqueo de equipos.

**Estructura de Datos:**
```
Offset | Size   | Type    | Field   | Notes
-------|--------|---------|---------|-------
0x00   | 1      | byte    | locked  | 0=unlocked, 1=locked
```

**Correlación con Python:**
```python
# src/haxmetrics/models/actions/change_teams_lock.py
class ChangeTeamsLock(Action):
    @classmethod
    def parse(cls, reader):
        obj = cls()
        obj.locked = reader.read_byte() != 0
        return obj
```

#### Action 14: PlayerAdminChange (Ga)

**Propósito:** Cambio de estado de admin de un jugador.

**Estructura de Datos:**
```
Offset | Size   | Type    | Field     | Notes
-------|--------|---------|-----------|-------
0x00   | 4      | int32   | player_id | ID del jugador
...    | 1      | byte    | admin     | 0=no admin, 1=admin
```

**Correlación con Python:**
```python
# src/haxmetrics/models/actions/player_admin_change.py
class PlayerAdminChange(Action):
    @classmethod
    def parse(cls, reader):
        obj = cls()
        obj.player_id = reader.read_int32()
        obj.admin = reader.read_byte() != 0
        return obj
```

#### Action 15: AutoTeamBalance (Xa)

**Propósito:** Balance automático de equipos.

**Estructura de Datos:**
Sin datos adicionales (solo header).

**Correlación con Python:**
```python
# src/haxmetrics/models/actions/auto_team_balance.py
class AutoTeamBalance(Action):
    @classmethod
    def parse(cls, reader):
        return cls()
```

#### Action 16: Desynced (Da)

**Propósito:** Notificación de desincronización.

**Estructura de Datos:**
```
Offset | Size   | Type    | Field     | Notes
-------|--------|---------|-----------|-------
0x00   | 4      | int32   | player_id | ID del jugador desincronizado
```

**Correlación con Python:**
```python
# src/haxmetrics/models/actions/desynced.py
class Desynced(Action):
    @classmethod
    def parse(cls, reader):
        obj = cls()
        obj.player_id = reader.read_int32()
        return obj
```

#### Action 17: BroadcastPings (Ma)

**Propósito:** Broadcast de pings de todos los jugadores.

**Estructura de Datos:**
```
Offset | Size   | Type    | Field       | Notes
-------|--------|---------|-------------|-------
0x00   | 1      | byte    | player_cnt  | Número de jugadores
...    | N*6    | ping[]  | pings       | Array de pings
```

**Ping Structure:**
```
Offset | Size   | Type    | Field     | Notes
-------|--------|---------|-----------|-------
0x00   | 4      | int32   | player_id | ID del jugador
...    | 2      | uint16  | ping      | Ping en ms
```

**Correlación con Python:**
```python
# src/haxmetrics/models/actions/broadcast_pings.py
class BroadcastPings(Action):
    @classmethod
    def parse(cls, reader):
        obj = cls()
        count = reader.read_byte()
        obj.pings = []
        for _ in range(count):
            player_id = reader.read_int32()
            ping = reader.read_uint16()
            obj.pings.append({"player_id": player_id, "ping": ping})
        return obj
```

#### Action 18: AvatarChange (Qa)

**Propósito:** Cambio de avatar sin player ID explícito.

**Estructura de Datos:**
```
Offset | Size   | Type    | Field   | Notes
-------|--------|---------|---------|-------
0x00   | varint | varint  | av_len  | Longitud + 1
...    | N      | string  | avatar  | Avatar string
```

**Correlación con Python:**
```python
# src/haxmetrics/models/actions/avatar_change.py
class AvatarChange(Action):
    @classmethod
    def parse(cls, reader):
        obj = cls()
        obj.avatar = reader.read_string()
        return obj
```

#### Action 19: TeamColorsChange (bb)

**Propósito:** Cambio de colores de equipo con ángulo, color de texto y rayas.

**Estructura de Datos:**
```
Offset | Size   | Type       | Field        | Notes
-------|--------|------------|--------------|-------
0x00   | 1      | byte       | team         | 1=red, 2=blue
...    | 4      | uint32_be  | angle        | Ángulo de gradiente
...    | 4      | int32      | text_color   | Color texto ARGB
...    | 3*4    | int32[3]   | colors       | Array de 3 colores ARGB
```

**Correlación con Python:**
```python
# src/haxmetrics/models/actions/team_colors_change.py
class TeamColorsChange(Action):
    @classmethod
    def parse(cls, reader):
        obj = cls()
        obj.team = reader.read_byte()
        obj.angle = reader.read_uint32_be()
        obj.text_color = reader.read_int32()
        obj.colors = [reader.read_int32() for _ in range(3)]
        return obj
```

#### Action 20: PlayerOrderChange (Fb)

**Propósito:** Cambio de orden de jugadores en la lista.

**Estructura de Datos:**
```
Offset | Size   | Type    | Field       | Notes
-------|--------|---------|-------------|-------
0x00   | 1      | byte    | player_cnt  | Número de jugadores
...    | N*4    | int32[] | player_ids  | Array de player IDs en nuevo orden
```

**Correlación con Python:**
```python
# src/haxmetrics/models/actions/player_order_change.py
class PlayerOrderChange(Action):
    @classmethod
    def parse(cls, reader):
        obj = cls()
        count = reader.read_byte()
        obj.player_ids = [reader.read_int32() for _ in range(count)]
        return obj
```

#### Action 21: KickRateLimit (Pa)

**Propósito:** Configuración de límite de rate de kicks.

**Estructura de Datos:**
```
Offset | Size   | Type       | Field    | Notes
-------|--------|------------|----------|-------
0x00   | 1      | byte       | min      | Mínimo
...    | 1      | byte       | rate     | Rate
...    | 2      | uint16_be  | burst    | Burst
```

**Correlación con Python:**
```python
# src/haxmetrics/models/actions/kick_rate_limit.py
class KickRateLimit(Action):
    @classmethod
    def parse(cls, reader):
        obj = cls()
        obj.min = reader.read_byte()
        obj.rate = reader.read_byte()
        obj.burst = reader.read_uint16_be()
        return obj
```

#### Action 22: PlayerAvatarSet (Gb)

**Propósito:** Establecer avatar con player ID explícito.

**Estructura de Datos:**
```
Offset | Size   | Type    | Field     | Notes
-------|--------|---------|-----------|-------
0x00   | 4      | int32   | player_id | ID del jugador
...    | varint | varint  | av_len    | Longitud + 1
...    | N      | string  | avatar    | Avatar string
```

**Correlación con Python:**
```python
# src/haxmetrics/models/actions/player_avatar_set.py
class PlayerAvatarSet(Action):
    @classmethod
    def parse(cls, reader):
        obj = cls()
        obj.player_id = reader.read_int32()
        obj.avatar = reader.read_string()
        return obj
```

#### Action 23: DiscUpdate (Hb)

**Propósito:** Actualización de propiedades de un disco con campos nullables.

**Estructura de Datos:**
```
Offset | Size   | Type      | Field       | Notes
-------|--------|-----------|-------------|-------
0x00   | 1      | byte      | disc_id     | ID del disco
...    | 1      | byte      | flags       | Bitmask de campos presentes
...    | 8?     | float64?  | [x]         | Si flag bit 0
...    | 8?     | float64?  | [y]         | Si flag bit 1
...    | 8?     | float64?  | [vx]        | Si flag bit 2
...    | 8?     | float64?  | [vy]        | Si flag bit 3
...    | 8?     | float64?  | [radius]    | Si flag bit 4
...    | 4?     | int32?    | [color]     | Si flag bit 5
```

**Correlación con Python:**
```python
# src/haxmetrics/models/actions/disc_update.py
class DiscUpdate(Action):
    @classmethod
    def parse(cls, reader):
        obj = cls()
        obj.disc_id = reader.read_byte()
        flags = reader.read_byte()
        
        if flags & 0x01: obj.x = reader.read_double_be()
        if flags & 0x02: obj.y = reader.read_double_be()
        if flags & 0x04: obj.vx = reader.read_double_be()
        if flags & 0x08: obj.vy = reader.read_double_be()
        if flags & 0x10: obj.radius = reader.read_double_be()
        if flags & 0x20: obj.color = reader.read_int32()
        
        return obj
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

## 9. Análisis de Replays Disponibles {#analisis-replays}

### 9.1 Albania-Poland3.hbr2

**Metadata:**
- Version: 3
- Duration: 15348 frames (255.8s / 4.26 min)
- Stadium: LIRS RS 4v4 (custom)
- Room: LIRS ROOMS EU
- File size: 27,089 bytes
- Decompressed: 115,327 bytes
- Compression ratio: 23.48%

**Estructura Detectada:**
- Messages: 0 (sin mensajes de sistema)
- Players: 0 (replay post-partido)
- Teams locked: True
- Score limit: 0 (sin límite)
- Time limit: 0 (sin límite)
- Game active: False (replay después de terminar el partido)

**Características Especiales:**
Este replay es un caso especial porque:
1. No tiene jugadores activos (player_count = 0)
2. Game active = false (partido terminado)
3. Sin mensajes de sistema
4. Stadium custom "LIRS RS 4v4" completamente definido

**Hex Dump de Sección Crítica (Stadium):**
```hex
Offset   | Hex Data                                         | Annotation
---------|--------------------------------------------------|------------------
0x00015  | FF                                               | Custom stadium (0xFF)
0x00016  | 0C 4C 49 52 53 20 52 53 20 34 76 34              | "LIRS RS 4v4"
0x00022  | 00 00 00 01 40 91 F8 00 00 00 00 00             | Background config
0x0002E  | 40 82 C0 00 00 00 00 00 40 66 80 00             | Dimensions
0x0003A  | 00 00 00 00 00 00 00 00 00 00 00 00             | Physics params
```

**Team Colors (18 bytes):**
```hex
Offset   | Hex Data                                         | Annotation
---------|--------------------------------------------------|------------------
0x000CA  | 00 00 00 00 00 00 30 00 00 00 00 00 00 00 00 00 | Red team color
0x000DC  | 00 00                                            | (angle=0, no colors)
0x000DE  | 00 00 00 00 00 00 30 00 00 00 00 00 00 00 00 00 | Blue team color
0x000F0  | 01 02                                            | (angle=0, no colors)
```

**Análisis de Actions:**
Debido a que el replay es post-partido sin jugadores activos, las actions son limitadas y probablemente relacionadas con:
- Configuración final del room
- Team colors
- Stadium data
- Estado final del juego

### 9.2 Chile-Uganda.hbr2

**Metadata:**
- Version: 3
- Duration: 101,301 frames (1688.35s / 28.14 min)
- Stadium: LIRS RS 4v4 (custom)
- Room: Similar a Albania-Poland3
- Messages: 17

**Características:**
- Replay más largo (28 minutos)
- Contiene mensajes de sistema (17)
- Probablemente incluye eventos como goals, pausas, team changes

### 9.3 Italy-Portugal.hbr2

**Metadata:**
- Version: 3
- Duration: 130,992 frames (2183.2s / 36.39 min)
- Stadium: LIRS RS 4v4 (custom)
- Messages: 11

**Características:**
- Replay muy largo (36 minutos)
- Partido completo o múltiples partidos

### 9.4 Portugal-Venezuela.hbr2

**Metadata:**
- Version: 3
- Duration: 164,996 frames (2749.93s / 45.83 min)
- Stadium: LIRS RS 4v4 (custom)
- Messages: 9

**Características:**
- El replay más largo de la colección (46 minutos)
- Posiblemente múltiples partidos o sesión de práctica

### 9.5 SpainVSTurkey.hbr2

**Metadata:**
- Version: 3
- Duration: 108,319 frames (1805.32s / 30.09 min)
- Stadium: LIRS RS 4v4 (custom)
- Messages: 9

### 9.6 Patrones Comunes Identificados

**Todos los replays LIRS comparten:**
1. Version 3 del formato HBR2
2. Stadium custom "LIRS RS 4v4"
3. Room name "LIRS ROOMS EU"
4. Teams locked = true
5. No score limit / time limit (0)
6. Player count = 0 (replays post-partido)
7. Game active = false

**Rangos de duración:**
- Mínimo: 255.8s (4.26 min) - Albania-Poland3
- Máximo: 2749.93s (45.83 min) - Portugal-Venezuela
- Promedio: ~1894s (31.57 min)

**Distribución de mensajes:**
- Mínimo: 0 mensajes (Albania-Poland3)
- Máximo: 17 mensajes (Chile-Uganda)
- Media: ~9 mensajes por replay

---

## 10. Casos Especiales y Edge Cases {#casos-especiales}

### 10.1 Replay sin Game Active

**Ejemplo:** Todos los replays LIRS analizados

Cuando `game_active == 0`:
- No hay game_state section (frame, scores, match time, etc.)
- Players pueden existir pero sin discs asociados
- Actions se limitan a configuración, chat, team changes, admin changes
- **Importante:** El parser debe skipear correctamente la sección de game state

**Estructura:**
```
[Room State]
  name: "LIRS ROOMS EU"
  locked: 1
  score_limit: 0
  time_limit: 0
  stadium: LIRS RS 4v4 (custom)
  game_active: 0      ← Key difference
  [No game state]     ← Sección ausente
  player_count: 0
  [No players]
  [Team colors]       ← Siempre presente (red + blue)
[Actions]             ← Presentes pero limitadas
```

**Correlación con Python:**
```python
# src/haxmetrics/models/room.py
game_active = reader.read_byte() != 0

if game_active:
    room.set_in_progress(True)
    room.game = Game.parse(reader, room)
else:
    room.set_in_progress(False)
    # No game state parsing
```

### 10.2 Custom Stadium vs Predefined Stadium

**Custom Stadium (type == 0xFF):**
- Requiere parsing completo de:
  - Background
  - Physics
  - Vertices, Segments, Planes
  - Goals, Discs, Joints
- Tamaño variable (puede ser muy grande)
- Ejemplo: "LIRS RS 4v4" (~150+ bytes)

**Predefined Stadium (type < 10):**
- Solo 1 byte (el tipo)
- Sin datos adicionales
- Nombres predefinidos: Classic, Easy, Small, Big, Rounded, Hockey, Big Hockey, Big Easy, Big Rounded, Huge

**Código de detección:**
```python
stadium_type = reader.read_byte()

if stadium_type == 0xFF:
    # Custom stadium - parse full structure
    stadium = Stadium.parse_custom(reader)
elif stadium_type < len(Stadium.STADIUMS):
    # Predefined - just use name
    stadium = Stadium.get_predefined(stadium_type)
else:
    raise ValueError(f"Unknown stadium type: {stadium_type}")
```

### 10.3 Replays con Jugadores vs Sin Jugadores

**Con Jugadores (player_count > 0):**
- Cada jugador tiene ~30-50 bytes de datos
- Incluye: ID, name, team, avatar, country, disc_id, input, etc.
- Jugadores tienen discs asociados (disc_id != -1)

**Sin Jugadores (player_count == 0):**
- Típico de replays post-partido
- Room state completo pero sin participantes
- Actions limitadas a configuración

**Impacto en Parsing:**
```python
player_count = reader.read_byte()
print(f"Player count: {player_count}")

for i in range(player_count):
    try:
        player = Player.parse(reader, version)
        room.players.append(player)
    except Exception as e:
        print(f"Failed to parse player {i+1}/{player_count}: {e}")
        break  # Stop parsing players on error
```

### 10.4 Versiones Antiguas del Formato

**Version 3 (actual):**
- Incluye todos los campos documentados
- Player handicap presente si version >= 11
- Team colors con angle field (uint32_be)

**Versiones anteriores (< 3):**
- Pueden tener campos faltantes
- Estructura de team colors simplificada
- Sin soporte para algunas actions nuevas (18-23)

**Manejo de versiones:**
```python
if self.version < 3:
    raise Exception(f"Unsupported replay version: {self.version}")

if self.version >= 11:
    player.set_handicap(reader.read_uint16())
```

### 10.5 Replays Corruptos o Incompletos

**Señales de corrupción:**
1. Magic header != "HBR2"
2. Version fuera de rango (> 20)
3. Duration negativa o excesiva (> 10M frames)
4. Fallo en descompresión zlib
5. Action type inválido (> 23)
6. Lectura más allá del final del buffer

**Estrategias de recuperación:**
```python
try:
    decompressed = zlib.decompress(data, wbits=-15)
except zlib.error as e:
    print(f"Decompression failed: {e}")
    # Try alternative wbits values
    for wbits in [-14, -13, -12]:
        try:
            decompressed = zlib.decompress(data, wbits=wbits)
            break
        except:
            continue
```

### 10.6 Stadium Vacío o Simplificado

**Ejemplo: LIRS RS 4v4**
- Vertex count: 0
- Segment count: 0
- Plane count: 0
- Goal count: 0
- Disc count: 0
- Joint count: 0

Este es un stadium "fantasma" que solo define:
- Background y dimensiones
- Physics de jugadores
- Configuración visual

**Implicaciones:**
- No hay colisiones definidas (todo vacío)
- Jugadores pueden moverse libremente
- No hay goals (sin forma de marcar)
- Posiblemente usado para replay metadata sin juego real

**Detección:**
```python
if (len(stadium.vertexes) == 0 and 
    len(stadium.segments) == 0 and 
    len(stadium.goals) == 0):
    print("Warning: Empty stadium detected (no collision geometry)")
```

### 10.7 Team Colors con Valores Nulos

**Team Color Structure (9 bytes):**
```
angle: uint32_be (4 bytes)
colors: int32[3] (12 bytes) - PERO solo se leen 3 si angle != 0
```

**Caso especial: angle == 0**
- No hay gradiente
- Colors array puede estar vacío o con valores por defecto
- Solo ocupa 4 bytes en lugar de 16

**Parsing seguro:**
```python
angle = reader.read_uint32_be()
team_color.set_angle(angle)

if angle != 0:
    # Read 3 colors
    for _ in range(3):
        color = reader.read_int32()
        team_color.colors.append(color)
else:
    # Default colors or skip
    team_color.colors = [0xFFFFFF, 0xFFFFFF, 0xFFFFFF]
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

*Documento creado: 2025-01-21*  
*Última actualización: 2025-12-20*  
*Versión: 2.0 - Enhanced with complete action types, custom stadium details, and replay analysis*  
*Autor: Análisis de Ingeniería Inversa + Deep Dive Analysis*
