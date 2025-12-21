# 📘 Guía Completa de Parseo de Archivos .HBR2

**Versión:** 1.0  
**Basado en:** game-min.js (HaxBall official client) + docs/GAME_MIN_REVERSE_ENGINEERING.md  
**Fecha:** 2025-12-20

---

## 📋 Índice

1. [Introducción](#introducción)
2. [Estructura General del Archivo](#estructura-general)
3. [Métodos de Lectura (BinaryReader)](#métodos-lectura)
4. [Sección 1: Header](#header)
5. [Sección 2: Messages (comprimido)](#messages)
6. [Sección 3: Room State (comprimido)](#room-state)
7. [Sección 4: Actions (comprimido)](#actions)
8. [Apéndices](#apéndices)

---

## 1. Introducción {#introducción}

Este documento describe **byte por byte** el formato binario .HBR2 usado por HaxBall para almacenar replays. Cada campo está documentado con:

- **Nombre del campo**
- **Método de lectura** (según game-min.js)
- **Bytes consumidos**
- **Tipo de dato**
- **Clase/método responsable** en game-min.js
- **Condiciones** (if/else que afectan la estructura)

### Notación Usada

- `F()` = read_byte (1 byte)
- `N()` = read_uint32_be (4 bytes, big-endian)
- `w()` = read_float64_be (8 bytes double, big-endian)
- `Ab()` = read_string (varint length + UTF-8 bytes)
- `kc()` = read_string (alias de Ab())
- `zf()` = read_signed_byte (1 byte, valor -128 a 127)
- `Di()` = read_int16_be (2 bytes signed, big-endian)
- `Bb()` = read_uint16_be (2 bytes unsigned, big-endian)
- `Sb()` = read_int32_be (4 bytes signed, big-endian)
- `Cg()` = read_varint (variable bytes, 1-5)

---

## 2. Estructura General del Archivo {#estructura-general}

```
┌──────────────────────────────────────┐
│ HEADER (sin comprimir)               │ 12 bytes
│  - Signature: "HBR2"                 │ 4 bytes
│  - Version                           │ 4 bytes (big-endian)
│  - Duration                          │ 4 bytes (big-endian)
├──────────────────────────────────────┤
│ COMPRESSED DATA (DEFLATE, zlib)     │ Variable
│  - Messages                          │ Variable
│  - Room State                        │ Variable
│  - Actions                           │ Variable
└──────────────────────────────────────┘
```

**CRÍTICO:** Después del header, TODO el contenido está comprimido con DEFLATE (zlib, wbits=-15).

---

## 3. Métodos de Lectura (BinaryReader) {#métodos-lectura}

### Clase `J` (BinaryReader) - game-min.js línea ~6116

Esta clase implementa todos los métodos de lectura binaria. **Por defecto usa BIG-ENDIAN**.

```javascript
class J {
  constructor(a, b) {
    this.s = a;      // DataView
    this.a = 0;      // position
    this.yb = b;     // little-endian flag (default: false = big-endian)
  }

  // Métodos de lectura:
  
  F() {              // read_byte
    // Lee 1 byte sin signo (0-255)
    return this.s.getUint8(this.a++);
  }
  
  zf() {             // read_signed_byte
    // Lee 1 byte con signo (-128 a 127)
    return this.s.getInt8(this.a++);
  }
  
  N() {              // read_uint32_be
    // Lee 4 bytes sin signo, BIG-ENDIAN
    let result = this.s.getUint32(this.a, false);
    this.a += 4;
    return result;
  }
  
  Sb() {             // read_int32_be
    // Lee 4 bytes con signo, BIG-ENDIAN
    let result = this.s.getInt32(this.a, false);
    this.a += 4;
    return result;
  }
  
  Bb() {             // read_uint16_be
    // Lee 2 bytes sin signo, BIG-ENDIAN
    let result = this.s.getUint16(this.a, false);
    this.a += 2;
    return result;
  }
  
  Di() {             // read_int16_be
    // Lee 2 bytes con signo, BIG-ENDIAN
    let result = this.s.getInt16(this.a, false);
    this.a += 2;
    return result;
  }
  
  w() {              // read_float64_be
    // Lee 8 bytes (double), BIG-ENDIAN
    let result = this.s.getFloat64(this.a, false);
    this.a += 8;
    return result;
  }
  
  Ab() {             // read_string (también kc())
    // Lee varint (length) + UTF-8 bytes
    let length = this.Cg();  // varint
    if (length == 0) return null;
    length -= 1;  // El varint incluye el null terminator
    
    let bytes = new Uint8Array(this.s.buffer, this.s.byteOffset + this.a, length);
    this.a += length;
    
    // Decodificar UTF-8
    let decoder = new TextDecoder("utf-8");
    return decoder.decode(bytes);
  }
  
  Cg() {             // read_varint
    // Lee entero variable (1-5 bytes)
    // Codificación: cada byte tiene 7 bits de datos + 1 bit de continuación
    let result = 0;
    let shift = 0;
    
    while (true) {
      let byte = this.F();
      result |= (byte & 0x7F) << shift;
      if ((byte & 0x80) == 0) break;
      shift += 7;
    }
    
    return result;
  }
}
```

---

## 4. Sección 1: Header (Sin Comprimir) {#header}

### Clase Responsable: Parser principal

**Ubicación en archivo:** Bytes 0-11 (12 bytes totales)

```
Offset | Bytes | Método | Tipo        | Campo    | Valor Esperado
-------|-------|--------|-------------|----------|---------------
0x00   | 4     | N/A    | string      | header   | "HBR2" (0x48 0x42 0x52 0x32)
0x04   | 4     | N()    | uint32_be   | version  | 3 (0x00 0x00 0x00 0x03)
0x08   | 4     | N()    | uint32_be   | duration | Frames totales (ej: 15348)
```

**Código game-min.js:**
```javascript
// No hay un método específico visible para header en game-min.js
// porque se lee antes de descomprimir. Estructura conocida por formato HBR2.
```

**Código Python equivalente:**
```python
def parse_header(reader):
    header = reader.read_fixed_string(4)      # 4 bytes: "HBR2"
    version = reader.read_uint32_be()         # 4 bytes: version number
    duration = reader.read_uint32_be()        # 4 bytes: total frames
    
    if header != "HBR2":
        raise ValueError("Not a valid HBR2 replay")
    
    return {
        "header": header,
        "version": version,
        "duration": duration
    }
```

**Total:** 12 bytes

---

## 5. Sección 2: Messages (Comprimido) {#messages}

### Clase `ReplayMessages` (Python) / Código inline en game-min.js

**Ubicación:** Después de descomprimir, primeros bytes del stream

**IMPORTANTE:** Esta sección puede ser **OPCIONAL**. Si el varint inicial es 0, no hay mensajes.

```
Offset | Bytes    | Método | Tipo       | Campo          | Notas
-------|----------|--------|------------|----------------|-------
0x00   | 1-5      | Cg()   | varint     | messages_count | Número de mensajes
```

**IF messages_count > 0:**

Para cada mensaje (i = 0 to messages_count-1):

```
Offset | Bytes    | Método | Tipo       | Campo         | Notas
-------|----------|--------|------------|---------------|-------
0x00   | 1-5      | Cg()   | varint     | frame         | Frame en que ocurre el mensaje
0x01   | 1-5      | Cg()   | varint     | msg_length    | Longitud del mensaje (incluye null)
...    | N        | N/A    | UTF-8      | message       | Texto del mensaje (msg_length - 1 bytes)
```

**Código Python equivalente:**
```python
def parse_messages(reader):
    """
    Clase: ReplayMessages
    Método: parse(reader)
    Ubicación: src/haxmetrics/models/replay_messages.py
    """
    messages = []
    messages_count = reader.read_varint()  # Cg()
    
    for i in range(messages_count):
        frame = reader.read_varint()       # Cg() - frame number
        message = reader.read_string()     # Ab() - varint length + UTF-8
        
        messages.append({
            "frame": frame,
            "message": message
        })
    
    return messages
```

**Total:** Variable (0 bytes si messages_count=0)

---

## 6. Sección 3: Room State (Comprimido) {#room-state}

### Clase `Sa` (Room) - game-min.js línea ~293

**Ubicación:** Después de messages, en el stream descomprimido

Esta es la sección más compleja. Contiene toda la información del estado de la sala.

### 6.1 Room State - Campos Básicos

**Clase:** `Sa` (línea 293)  
**Método:** `ma(a)` (línea 293-315)

```
Offset | Bytes | Método | Tipo         | Campo       | Clase.Campo | Notas
-------|-------|--------|--------------|-------------|-------------|-------
0x00   | 1-5   | Ab()   | string       | lc          | Sa.lc       | Nombre de la sala
...    | 1     | F()    | byte→bool    | Ac          | Sa.Ac       | Locked (0=false, !0=true)
...    | 4     | N()    | uint32_be    | kb          | Sa.kb       | Score limit
...    | 4     | N()    | uint32_be    | Ga          | Sa.Ga       | Time limit
...    | 2     | Di()   | int16_be     | me          | Sa.me       | (unknown)
...    | 1     | F()    | byte         | gd          | Sa.gd       | Rules type (0=default)
...    | 1     | F()    | byte         | Gd          | Sa.Gd       | (unknown)
```

**Código game-min.js (línea 293-303):**
```javascript
ma(a) {
  this.lc = a.Ab();           // room name (string)
  this.Ac = 0 != a.F();       // locked (bool from byte)
  this.kb = a.N();            // score limit (uint32)
  this.Ga = a.N();            // time limit (uint32)
  this.me = a.Di();           // unknown (int16)
  this.gd = a.F();            // rules type (byte)
  this.Gd = a.F();            // unknown (byte)
  this.T = q.ma(a);           // Stadium (call q.ma())
  var b = 0 != a.F();         // game_active (bool from byte)
  this.M = null;
  b && ((this.M = new Y()), this.M.ma(a, this));  // IF game_active, parse game state
  // ... player parsing continues
```

### 6.2 Stadium Parsing

**Clase:** `q` (Stadium)  
**Método:** `ma(a)` y `ws(a)` (game-min.js línea ~1900)

```
Offset | Bytes | Método | Tipo         | Campo        | Notas
-------|-------|--------|--------------|--------------|-------
0x00   | 1     | F()    | byte         | stadium_type | 0-11=predefined, 255=custom
```

#### 6.2.1 IF stadium_type == 255 (Custom Stadium)

**Clase:** `q` (Stadium)  
**Método:** `ws(a)` - custom stadium parsing

**⚠️ ORDEN CRÍTICO:** Debe seguirse exactamente como en game-min.js líneas 1918-1950.

##### A. Basic Configuration (~72 bytes)

```
Offset | Bytes    | Método | Tipo         | Campo              | Notas
-------|----------|--------|--------------|--------------------|-----------------
0x00   | 1-5      | Ab()   | string       | name               | Stadium name (varint + UTF-8)
...    | 4        | N()    | uint32_be    | bg_type            | 0=none, 1=grass, 2=hockey
...    | 8        | w()    | float64_be   | bg_width           | Background width
...    | 8        | w()    | float64_be   | bg_height          | Background height
...    | 8        | w()    | float64_be   | bg_kick_off_radius | Kick-off circle radius
...    | 8        | w()    | float64_be   | bg_corner_radius   | Corner arc radius
...    | 8        | w()    | float64_be   | bg_goal_line       | Goal line distance
...    | 4        | N()    | uint32_be    | bg_color           | Background color (ARGB)
...    | 8        | w()    | float64_be   | max_view_width     | Max viewport width
...    | 8        | w()    | float64_be   | max_view_height    | Max viewport height
...    | 8        | w()    | float64_be   | spawn_distance     | Distance for spawning
```

##### B. Player Physics (92 bytes)

**⚠️ CORRECCIÓN:** PlayerPhysics tiene **12 campos (92 bytes)**, no 7 u 8.

```
Offset | Bytes | Método | Tipo       | Campo              | Clase Ub  | Notas
-------|-------|--------|------------|--------------------|-----------|-----------------
0x00   | 8     | w()    | float64_be | bCoef              | this.o    | Bounce coefficient
0x08   | 8     | w()    | float64_be | inv_mass           | this.ca   | Inverse mass
0x10   | 8     | w()    | float64_be | damping            | this.Ea   | Damping
0x18   | 8     | w()    | float64_be | acceleration       | this.Qe   | Normal acceleration
0x20   | 8     | w()    | float64_be | kick_acceleration  | this.gf   | Kick acceleration
0x28   | 8     | w()    | float64_be | kick_damping       | this.hf   | Kick damping
0x30   | 8     | w()    | float64_be | kick_strength      | this.ef   | Kick strength
0x38   | 8     | w()    | float64_be | gravity_x          | b.x       | Gravity X component
0x40   | 8     | w()    | float64_be | gravity_y          | b.y       | Gravity Y component
0x48   | 4     | N()    | uint32_be  | c_group            | this.B    | Collision group
0x4C   | 8     | w()    | float64_be | radius             | this.V    | Player disc radius
0x54   | 8     | w()    | float64_be | inv_mass_2         | this.ff   | Second inverse mass
```

**Total:** 11×8 + 4 = 92 bytes

##### C. Additional Fields (~8 bytes)

```
Offset | Bytes | Método      | Tipo         | Campo                   | Notas
-------|-------|-------------|--------------|-------------------------|------------------
0x00   | 1-5   | Sb()        | nullable_int | max_view_width_override | Nullable int32
...    | 1     | F()         | byte         | camera_follow           | Camera mode
...    | 1     | F()         | byte→bool    | can_be_stored           | Storage flag
...    | 1     | F()         | byte→bool    | kick_off_reset          | Reset mode
...    | 1     | F()         | byte         | (unknown)               | ⚠️ Extra byte no documentado
```

**⚠️ NOTA:** Existe un byte extra (0x00) entre kick_off_reset y vertex_count que no está en game-min.js pero aparece en replays reales.

**Seguido de arrays de componentes** (cada uno empieza con count F()):

##### Vertices Array

```
Offset | Bytes | Método | Tipo    | Campo         | Notas
-------|-------|--------|---------|---------------|-------
0x00   | 1     | F()    | byte    | vertex_count  | Número de vértices (0-255)
```

**Por cada vértice (i = 0 to vertex_count-1):**

**⚠️ CORRECCIÓN:** Vertex tiene **32 bytes**, no 24. c_mask y c_group son **uint32**, no float64.

```
Offset | Bytes | Método | Tipo       | Campo     | Clase G   | Notas
-------|-------|--------|------------|-----------|-----------|-------
0x00   | 8     | w()    | float64_be | x         | b.x       | Coordenada X
0x08   | 8     | w()    | float64_be | y         | b.y       | Coordenada Y
0x10   | 8     | w()    | float64_be | bCoef     | this.o    | Bounce coefficient
0x18   | 4     | N()    | uint32_be  | cMask     | this.i    | Collision mask (⚠️ uint32, no float64)
0x1C   | 4     | N()    | uint32_be  | cGroup    | this.B    | Collision group (⚠️ uint32, no float64)
```

**Código game-min.js (clase G, línea ~394):**
```javascript
class G {
  ma(a) {
    let b = new P(0, 0);
    b.x = a.w();       // float64 - x coordinate
    b.y = a.w();       // float64 - y coordinate  
    this.S = b;
    this.o = a.w();    // float64 - bCoef (bounce coefficient)
    this.i = a.N();    // uint32 - cMask  ⚠️ CORRECCIÓN
    this.B = a.N();    // uint32 - cGroup ⚠️ CORRECCIÓN
  }
}
```

**Total por vértice:** 32 bytes (no 24)

##### Segments Array

```
Offset | Bytes | Método | Tipo    | Campo          | Notas
-------|-------|--------|---------|----------------|-------
0x00   | 1     | F()    | byte    | segment_count  | Número de segmentos (0-255)
```

**Por cada segmento (i = 0 to segment_count-1):**

**⚠️ CORRECCIÓN:** Segment usa **sistema de FLAGS** para tamaño variable (19-39 bytes).

```
Offset | Bytes | Método | Tipo         | Campo      | Clase I   | Notas
-------|-------|--------|--------------|------------|-----------|-------
0x00   | 1     | F()    | byte         | flags      | c         | Bitflags: &1=bias, &2=curve, &4=color, &8=visible
0x01   | 1     | F()    | byte         | v0         | this.$    | Índice vértice 0
0x02   | 1     | F()    | byte         | v1         | this.ea   | Índice vértice 1
...    | 8     | w()    | float64_be   | bias       | this.Hc   | Solo si (flags & 1), default 0
...    | 8     | w()    | float64_be   | curve      | this.vb   | Solo si (flags & 2), default infinity
...    | 4     | N()    | uint32_be    | color      | this.S    | Solo si (flags & 4), default 0
...    | -     | -      | bool         | visible    | this.bb   | De (flags & 8) != 0
...    | 8     | w()    | float64_be   | bCoef      | this.o    | Siempre presente
...    | 4     | N()    | uint32_be    | cMask      | this.i    | Siempre presente (⚠️ uint32)
...    | 4     | N()    | uint32_be    | cGroup     | this.B    | Siempre presente (⚠️ uint32)
```

**Código game-min.js (clase I, línea ~5425):**
```javascript
class I {
  ma(a, b) {
    let c = a.F();                    // flags byte
    this.$ = b[a.F()];                // v0 (byte) - vertex reference
    this.ea = b[a.F()];               // v1 (byte) - vertex reference
    this.Hc = 0 != (c & 1) ? a.w() : 0;        // bias (conditional)
    this.vb = 0 != (c & 2) ? a.w() : 1/0;      // curve (conditional, default infinity)
    this.S = 0 != (c & 4) ? a.N() : 0;         // color (conditional)
    this.bb = 0 != (c & 8);                     // visible (from flag)
    this.o = a.w();                   // bCoef (float64)
    this.i = a.N();                   // cMask (uint32) ⚠️ CORRECCIÓN
    this.B = a.N();                   // cGroup (uint32) ⚠️ CORRECCIÓN
    // ... más lógica interna
  }
}
```

**Tamaño por segmento:**
- Mínimo: 3 + 8 + 4 + 4 = **19 bytes** (sin campos opcionales)
- Máximo: 3 + 8 + 8 + 4 + 8 + 4 + 4 = **39 bytes** (todos los opcionales)

##### Planes Array

```
Offset | Bytes | Método | Tipo    | Campo        | Notas
-------|-------|--------|---------|--------------|-------
0x00   | 1     | F()    | byte    | plane_count  | Número de planos (0-255)
```

**Por cada plano (i = 0 to plane_count-1):**

```
Offset | Bytes | Método | Tipo         | Campo  | Clase.Campo | Notas
-------|-------|--------|--------------|--------|-------------|-------
0x00   | 8     | w()    | float64_be   | normal_x | Q.bb      | Normal X
0x08   | 8     | w()    | float64_be   | normal_y | Q.Ac      | Normal Y
0x10   | 8     | w()    | float64_be   | dist     | Q.lc      | Distancia
0x18   | 8     | w()    | float64_be   | bCoef    | Q.o       | Bounce coefficient
0x20   | 4     | N()    | uint32_be    | cMask    | Q.Kc      | Collision mask
0x24   | 4     | N()    | uint32_be    | cGroup   | Q.Mc      | Collision group
```

**Código game-min.js (clase Q, línea ~7227):**
```javascript
class Q {
  ma(a) {
    this.bb = a.w();     // normal_x (float64)
    this.Ac = a.w();     // normal_y (float64)
    this.lc = a.w();     // dist (float64)
    this.o = a.w();      // bCoef (float64)
    this.Kc = a.N();     // cMask (uint32)
    this.Mc = a.N();     // cGroup (uint32)
  }
}
```

**Total por plano:** 40 bytes

##### Goals Array

```
Offset | Bytes | Método | Tipo    | Campo       | Notas
-------|-------|--------|---------|-------------|-------
0x00   | 1     | F()    | byte    | goal_count  | Número de goals (0-255)
```

**Por cada goal (i = 0 to goal_count-1):**

```
Offset | Bytes | Método | Tipo         | Campo    | Clase.Campo | Notas
-------|-------|--------|--------------|----------|-------------|-------
0x00   | 8     | w()    | float64_be   | p0_x     | pb.ld       | Punto 0 X
0x08   | 8     | w()    | float64_be   | p0_y     | pb.md       | Punto 0 Y
0x10   | 8     | w()    | float64_be   | p1_x     | pb.nd       | Punto 1 X
0x18   | 8     | w()    | float64_be   | p1_y     | pb.od       | Punto 1 Y
0x20   | 1     | F()    | byte         | team     | pb.fa       | 1=red, 2=blue
```

**Código game-min.js (clase pb, línea ~1396):**
```javascript
class pb {
  ma(a) {
    this.ld = a.w();     // p0.x (float64)
    this.md = a.w();     // p0.y (float64)
    this.nd = a.w();     // p1.x (float64)
    this.od = a.w();     // p1.y (float64)
    this.fa = a.F();     // team (byte: 1=red, 2=blue)
  }
}
```

**Total por goal:** 33 bytes

##### Discs Array (Stadium Definition)

```
Offset | Bytes | Método | Tipo    | Campo      | Notas
-------|-------|--------|---------|------------|-------
0x00   | 1     | F()    | byte    | disc_count | Número de discos en stadium (0-255)
```

**Por cada disco (i = 0 to disc_count-1):**

```
Offset | Bytes | Método | Tipo         | Campo      | Clase.Campo | Notas
-------|-------|--------|--------------|------------|-------------|-------
0x00   | 8     | w()    | float64_be   | pos_x      | xa.S.x      | Posición X
0x08   | 8     | w()    | float64_be   | pos_y      | xa.S.y      | Posición Y
0x10   | 8     | w()    | float64_be   | speed_x    | xa.P.x      | Velocidad X
0x18   | 8     | w()    | float64_be   | speed_y    | xa.P.y      | Velocidad Y
0x20   | 8     | w()    | float64_be   | gravity_x  | xa.ee.x     | Gravedad X
0x28   | 8     | w()    | float64_be   | gravity_y  | xa.ee.y     | Gravedad Y
0x30   | 8     | w()    | float64_be   | radius     | xa.V        | Radio
0x38   | 8     | w()    | float64_be   | bCoef      | xa.o        | Bounce coefficient
0x40   | 8     | w()    | float64_be   | inv_mass   | xa.ca       | Masa inversa
0x48   | 8     | w()    | float64_be   | damping    | xa.Ea       | Damping
0x50   | 4     | N()    | uint32_be    | color      | xa.Z        | Color ARGB
0x54   | 4     | N()    | uint32_be    | cMask      | xa.Kc       | Collision mask
0x58   | 4     | N()    | uint32_be    | cGroup     | xa.Mc       | Collision group
```

**Código game-min.js (clase xa, línea ~5719):**
```javascript
class xa {
  ma(a) {
    var b = new P();
    b.x = a.w();              // pos.x (float64)
    b.y = a.w();              // pos.y (float64)
    this.S = b;
    
    b = new P();
    b.x = a.w();              // speed.x (float64)
    b.y = a.w();              // speed.y (float64)
    this.P = b;
    
    b = new P();
    b.x = a.w();              // gravity.x (float64)
    b.y = a.w();              // gravity.y (float64)
    this.ee = b;
    
    this.V = a.w();           // radius (float64)
    this.o = a.w();           // bCoef (float64)
    this.ca = a.w();          // inv_mass (float64)
    this.Ea = a.w();          // damping (float64)
    this.Z = a.N();           // color (uint32)
    this.Kc = a.N();          // cMask (uint32)
    this.Mc = a.N();          // cGroup (uint32)
  }
}
```

**Total por disco (stadium):** 92 bytes

##### Joints Array

```
Offset | Bytes | Método | Tipo    | Campo       | Notas
-------|-------|--------|---------|-------------|-------
0x00   | 1     | F()    | byte    | joint_count | Número de joints (0-255)
```

**Por cada joint (i = 0 to joint_count-1):**

```
Offset | Bytes | Método | Tipo         | Campo      | Clase.Campo | Notas
-------|-------|--------|--------------|------------|-------------|-------
0x00   | 1     | F()    | byte         | d0         | rb.ge       | Índice disco 0
0x01   | 1     | F()    | byte         | d1         | rb.he       | Índice disco 1
0x02   | 8     | w()    | float64_be   | strength   | rb.ye       | Fuerza
0x0A   | 8     | w()    | float64_be   | length     | rb.cd       | Longitud
0x12   | 4     | N()    | uint32_be    | color      | rb.Z        | Color ARGB (optional?)
```

**Código game-min.js (clase rb, línea ~4932):**
```javascript
class rb {
  ma(a) {
    this.ge = a.F();         // d0 (byte)
    this.he = a.F();         // d1 (byte)
    this.ye = a.w();         // strength (float64)
    this.cd = a.w();         // length (float64)
    // color parsing might be optional or conditional
  }
}
```

**Total por joint:** ~24-28 bytes (color podría ser opcional)

##### Player Physics Defaults

**⚠️ ELIMINADO:** Esta sección estaba incorrecta. Player Physics se parsea ANTES de los component arrays (ver sección B).

El orden correcto es:
1. Basic Configuration
2. **Player Physics (92 bytes) ← Aquí, no al final**
3. Additional Fields
4. Component Arrays (vertices, segments, planes, goals, discs, joints)
5. Spawn Points (red, blue)

#### 6.2.2 IF stadium_type != 255 (Predefined Stadium)

Si el stadium es predefinido (0-11), NO se leen más bytes. El parser carga el stadium desde una lista interna.

**Stadiums predefinidos:**
- 0 = Classic
- 1 = Easy
- 2 = Small
- 3 = Big
- 4 = Rounded
- 5 = Hockey
- 6 = Big Hockey
- 7 = Big Easy
- 8 = Big Rounded
- 9 = Huge
- 10 = (custom/unknown)
- 11 = (custom/unknown)

### 6.3 Game State (Conditional)

**Ubicación:** Después del stadium parsing, en el stream de room state

**⚠️ ORDEN CRÍTICO:** Los discos se parsean **PRIMERO**, luego los campos de estado del juego.

```
Offset | Bytes | Método | Tipo         | Campo       | Notas
-------|-------|--------|--------------|-------------|-------
0x00   | 1     | F()    | byte→bool    | game_active | 0=no game, !0=game active
```

#### IF game_active == true:

**Clase:** `Y` (Game State) - línea 7448 en game-min.js  
**Método:** `ma(a, parent)` - línea 7585 en game-min.js

##### 6.3.1 Discs (Game State) - **PARSEADOS PRIMERO**

**Clase:** `Sa` (Discs Container) - línea 61 en game-min.js  
**Método:** `this.va.ma(a)` - línea 78 en game-min.js

```
Offset | Bytes | Método | Tipo    | Campo      | Notas
-------|-------|--------|---------|------------|-------
0x00   | 1     | F()    | byte    | disc_count | Número de discos en juego (típicamente 5-6)
```

**Por cada disco (i = 0 to disc_count-1):**

**Clase:** `qa` (Disc) - línea 7927 en game-min.js  
**Método:** `d.ma(a)` - línea 8109 en game-min.js

```
Offset | Bytes | Método | Tipo         | Campo      | JS Field | Notas
-------|-------|--------|--------------|------------|----------|-------
0x00   | 8     | w()    | float64_be   | pos_x      | a.x      | Posición X
0x08   | 8     | w()    | float64_be   | pos_y      | a.y      | Posición Y
0x10   | 8     | w()    | float64_be   | vel_x      | G.x      | Velocidad X
0x18   | 8     | w()    | float64_be   | vel_y      | G.y      | Velocidad Y
0x20   | 8     | w()    | float64_be   | ra_x       | ra.x     | Unknown (acceleration?)
0x28   | 8     | w()    | float64_be   | ra_y       | ra.y     | Unknown (acceleration?)
0x30   | 8     | w()    | float64_be   | radius     | V        | Radio del disco
0x38   | 8     | w()    | float64_be   | bCoef      | o        | Bounce coefficient
0x40   | 8     | w()    | float64_be   | inv_mass   | ca       | Masa inversa
0x48   | 8     | w()    | float64_be   | damping    | Ea       | Damping
0x50   | 4     | jb()   | uint32_be    | color      | S        | Color ARGB (**SIEMPRE presente**)
0x54   | 4     | N()    | uint32_be    | cMask      | i        | Collision mask
0x58   | 4     | N()    | uint32_be    | cGroup     | B        | Collision group
```

**CRÍTICO:** 
- El campo `color` es **SIEMPRE uint32_be**, no es nullable. Valor típico: 0x00RRGGBB.
- El primer disco (disc[0]) es típicamente la pelota (radio=10.0, color=0xFFFFFF)
- Los discos 1..n son discos de jugadores

**Total por disco (game state):** 92 bytes

##### 6.3.2 Game Fields - **PARSEADOS DESPUÉS DE DISCOS**

Después de parsear TODOS los discos, vienen los campos del estado del juego:

**Ubicación en Y.ma():** Líneas 7586-7593 en game-min.js

```
Offset | Bytes | Método | Tipo         | Campo          | JS Field | Significado Confirmado
-------|-------|--------|--------------|----------------|----------|------------------------
0x00   | 4     | N()    | uint32_be    | frame          | yc       | Frame number (típ. 0 en snapshots)
0x04   | 4     | N()    | uint32_be    | field_cb       | Cb       | Unknown (0 o 1)
0x08   | 4     | N()    | uint32_be    | score_red      | Tb       | **Puntuación team red** ✓
0x0C   | 4     | N()    | uint32_be    | score_blue     | Ob       | **Puntuación team blue** ✓
0x10   | 8     | w()    | float64_be   | match_time     | Nc       | **Tiempo en segundos** ✓
0x18   | 4     | N()    | uint32_be    | time_or_pause  | Ta       | Time limit o Pause timer (0 o >0)
0x1C   | 1     | zf()   | byte         | kickoff_team   | ke       | Equipo kickoff (1=red, 2=blue, 0=none) ✓
```

**Total game fields:** 29 bytes

**Mapeo verificado con fixtures:**
- `Tb` (score_red): Confirmado en red_winning_1_0 (Tb=1, Ob=0) ✓
- `Ob` (score_blue): Confirmado en red_winning_2_1 (Tb=2, Ob=1) ✓
- `Nc` (match_time): Confirmado en time_played_32_seconds (Nc≈32.98s) ✓
- `Ta` (time_or_pause): 0 normalmente, 120 en game_paused ✓
- `zf()` (kickoff_team): 1=red, 2=blue observado en fixtures ✓

#### IF game_active == false:

No se leen bytes de game state. El parser continúa directamente con players.

### 6.4 Players

**Ubicación:** Después de game state (o después de stadium si game_active==false)

```
Offset | Bytes | Método | Tipo    | Campo        | Notas
-------|-------|--------|---------|--------------|-------
0x00   | 1     | F()    | byte    | player_count | Número de jugadores (0-255)
```

**Por cada jugador (i = 0 to player_count-1):**

**Clase:** `ua` (Player)  
**Método:** `xa(a, b)` (línea 6889-6907 en game-min.js)

```
Offset | Bytes    | Método | Tipo         | Campo         | Clase.Campo | Notas
-------|----------|--------|--------------|---------------|-------------|-------
0x00   | 1        | F()    | byte→bool    | admin         | ua.fb       | Admin (0=false, !0=true)
0x01   | 4        | N()    | uint32_be    | player_id     | ua.Nb       | Player ID
...    | 1-5+N    | Ab()   | string       | avatar        | ua.Zb       | Avatar string
...    | 1-5+N    | Ab()   | string       | unknown_str   | ua.Sd       | Unknown string
...    | 1        | F()    | byte→bool    | flag          | ua.Td       | Has country flag
...    | 1-5+N    | Ab()   | string       | country       | ua.country  | Country code (ej: "es")
...    | 4        | N()    | uint32_be    | unknown_int   | ua.gh       | Unknown integer
...    | 1-5+N    | Ab()   | string       | name          | ua.D        | Player name
...    | 4        | N()    | uint32_be    | input_state   | ua.W        | Input state
...    | 2        | Bb()   | uint16_be    | unknown_int16 | ua.Z        | Unknown short
...    | 1        | F()    | byte→bool    | kicking       | ua.Yb       | Is kicking
...    | 2        | Di()   | int16_be     | unknown_int16_2| ua.Bc      | Unknown short 2
...    | 1        | F()    | byte         | unknown_byte  | ua.Zc       | Unknown byte
...    | 1        | zf()   | signed byte  | team          | ua.fa.ba    | -1 to 2 (0=spec, 1=red, 2=blue)
...    | 2        | Di()   | int16_be     | disc_id       | ua.I.Il     | Disc ID (-1 si no tiene)
```

**Código game-min.js (línea 6889-6907):**
```javascript
xa(a, b) {
  this.fb = 0 != a.F();       // admin (bool from byte)
  this.Nb = a.N();            // player_id (uint32_be)
  this.Zb = a.Ab();           // avatar (string)
  this.Sd = a.Ab();           // unknown_str (string)
  this.Td = 0 != a.F();       // flag (bool from byte)
  this.country = a.Ab();      // country (string)
  this.gh = a.N();            // unknown_int (uint32_be)
  this.D = a.Ab();            // name (string)
  this.W = a.N();             // input_state (uint32_be)
  this.Z = a.Bb();            // unknown_int16 (uint16_be)
  this.Yb = 0 != a.F();       // kicking (bool from byte)
  this.Bc = a.Di();           // unknown_int16_2 (int16_be)
  this.Zc = a.F();            // unknown_byte (byte)
  let c = a.zf();             // team (signed byte)
  this.fa = 1 == c ? u.ia : 2 == c ? u.Da : u.Oa;  // Convert to team enum
  a = a.Di();                 // disc_id (int16_be)
  this.I = 0 > a ? null : b[a];  // Disc reference (null si -1)
}
```

**Total por jugador:** Variable (~40-80 bytes dependiendo de strings)

### 6.5 Team Colors

**Ubicación:** Después de players

**Clase:** `ta` (TeamColor)  
**Método:** `ma(a)` (ubicación en game-min.js a determinar)

Se leen **2 team colors** (red y blue) en ese orden:

**Por cada team color (i = 0 to 1):**

```
Offset | Bytes | Método | Tipo         | Campo       | Clase.Campo | Notas
-------|-------|--------|--------------|-------------|-------------|-------
0x00   | 1     | F()    | byte         | angle       | ta.angle    | Ángulo (0-255)
0x01   | 4     | N()    | uint32_be    | text_color  | ta.text     | Color del texto ARGB
0x05   | 1     | F()    | byte         | num_stripes | ta.num      | Número de rayas (max 3)
```

**IF num_stripes > 0:**

```
Offset | Bytes    | Método | Tipo       | Campo   | Notas
-------|----------|--------|------------|---------|-------
0x00   | 4*N      | N()    | uint32_be  | stripes | Array de colores (N = num_stripes)
```

**Código game-min.js (clase ta, aproximadamente línea 198):**
```javascript
class ta {
  ma(a) {
    this.angle = a.F();          // angle (byte)
    this.text = a.N();           // text_color (uint32_be)
    let b = a.F();               // num_stripes (byte)
    this.num = b;
    this.ma = [];                // stripes array
    for (let c = 0; c < b; c++) {
      this.ma.push(a.N());       // stripe color (uint32_be)
    }
  }
}
```

**Total por team color:** 6 + (4 * num_stripes) bytes

**EJEMPLO:** Colores por defecto (0 stripes):
- Red: 6 bytes (angle=0, text=0xFFFFFF, stripes=0)
- Blue: 6 bytes (angle=1, text=0xE56E56, stripes=0)
- **Total:** 12 bytes

---

## 7. Sección 4: Actions (Comprimido) {#actions}

**Ubicación:** Después de team colors, resto del stream descomprimido

Las actions son eventos que ocurrieron durante la partida. Cada action tiene:

1. **Frame delta** (varint): frames desde la última action
2. **Sender ID** (uint16_be): ID del jugador o sistema (0=sistema)
3. **Action type** (byte): 0-23

### 7.1 Action Header (Todas las Actions)

```
Offset | Bytes    | Método | Tipo       | Campo       | Notas
-------|----------|--------|------------|-------------|-------
0x00   | 1-5      | Cg()   | varint     | frame_delta | Frames desde última action
...    | 2        | Bb()   | uint16_be  | sender      | Player ID o 0 (sistema)
...    | 1        | F()    | byte       | type        | Action type (0-23)
```

Después del header, cada action type tiene su propia estructura de datos.

### 7.2 Action Types (0-23)

#### Action 0: Message (Eb)

**Clase JavaScript:** `Eb`

```
Offset | Bytes    | Método | Tipo       | Campo     | Notas
-------|----------|--------|------------|-----------|-------
0x00   | 1-5+N    | Ab()   | string     | message   | Texto del mensaje
...    | 4        | N()    | uint32_be  | color     | Color ARGB
...    | 1        | F()    | byte       | style     | Estilo (bold, italic, etc.)
...    | 1        | F()    | byte       | sound     | Sonido (0=no sound, 1=sound)
```

#### Action 1: ToggleChat (Ha)

**Clase JavaScript:** `Ha`

```
Offset | Bytes | Método | Tipo  | Campo  | Notas
-------|-------|--------|-------|--------|-------
0x00   | 1     | F()    | byte  | value  | 0=off, 1=on
```

#### Action 2: ChangeStadium (cb)

**Clase JavaScript:** `cb`

```
Offset | Bytes    | Método | Tipo     | Campo        | Notas
-------|----------|--------|----------|--------------|-------
0x00   | 1-5+N    | Ab()   | string   | stadium_json | Stadium en formato JSON
```

#### Action 3: PlayerInput (La)

**Clase JavaScript:** `La`

```
Offset | Bytes | Método | Tipo       | Campo | Notas
-------|-------|--------|------------|-------|-------
0x00   | 2     | Bb()   | uint16_be  | input | Bitfield de inputs
```

**Input bitfield:**
- Bit 0: Left
- Bit 1: Right
- Bit 2: Up
- Bit 3: Down
- Bit 4: Kick
- (otros bits por determinar)

#### Action 4: ChatMessage (Ya)

**Clase JavaScript:** `Ya`

```
Offset | Bytes    | Método | Tipo    | Campo   | Notas
-------|----------|--------|---------|---------|-------
0x00   | 1-5+N    | Ab()   | string  | message | Texto del mensaje
```

#### Action 5: PlayerJoined (Na)

**Clase JavaScript:** `Na`

```
Offset | Bytes    | Método | Tipo       | Campo      | Notas
-------|----------|--------|------------|------------|-------
0x00   | 4        | N()    | uint32_be  | player_id  | ID del jugador
...    | 1-5+N    | Ab()   | string     | name       | Nombre del jugador
...    | 1-5+N    | Ab()   | string     | country    | Código de país (ej: "es")
...    | 1-5+N    | Ab()   | string     | avatar     | Avatar string
...    | 1        | F()    | byte       | conn_id    | Connection ID (?)
```

#### Action 6: PlayerLeft (ma)

**Clase JavaScript:** `ma`

```
Offset | Bytes | Método | Tipo       | Campo      | Notas
-------|-------|--------|------------|------------|-------
0x00   | 4     | N()    | uint32_be  | player_id  | ID del jugador
```

#### Action 7: MatchStart (Va)

**Clase JavaScript:** `Va`

```
Offset | Bytes | Método | Tipo | Campo | Notas
-------|-------|--------|------|-------|-------
(ninguno - action sin datos adicionales)
```

#### Action 8: MatchStopped (Wa)

**Clase JavaScript:** `Wa`

```
Offset | Bytes | Método | Tipo | Campo | Notas
-------|-------|--------|------|-------|-------
(ninguno - action sin datos adicionales)
```

#### Action 9: ChangePaused (Za)

**Clase JavaScript:** `Za`

```
Offset | Bytes | Método | Tipo  | Campo  | Notas
-------|-------|--------|-------|--------|-------
0x00   | 1     | F()    | byte  | paused | 0=unpaused, 1=paused
```

#### Action 10: ChangeGameSetting (va)

**Clase JavaScript:** `va`

```
Offset | Bytes    | Método | Tipo      | Campo | Notas
-------|----------|--------|-----------|-------|-------
0x00   | 1-5+N    | Ab()   | string    | key   | Clave del setting (ej: "time_limit")
...    | 1-5+N    | Ab()   | string    | value | Valor del setting
```

#### Action 11: StadiumUpdate (Ea)

**Clase JavaScript:** `Ea`

```
Offset | Bytes    | Método | Tipo     | Campo        | Notas
-------|----------|--------|----------|--------------|-------
0x00   | 1-5+N    | Ab()   | string   | stadium_json | Stadium actualizado (JSON)
```

#### Action 12: PlayerTeamChange (fa)

**Clase JavaScript:** `fa`

```
Offset | Bytes | Método | Tipo       | Campo      | Notas
-------|-------|--------|------------|------------|-------
0x00   | 4     | N()    | uint32_be  | player_id  | ID del jugador
...    | 1     | zf()   | signed byte| team_id    | -1 to 2 (0=spec, 1=red, 2=blue)
```

#### Action 13: ChangeTeamsLock (Fa)

**Clase JavaScript:** `Fa`

```
Offset | Bytes | Método | Tipo  | Campo  | Notas
-------|-------|--------|-------|--------|-------
0x00   | 1     | F()    | byte  | locked | 0=unlocked, 1=locked
```

#### Action 14: PlayerAdminChange (Ga)

**Clase JavaScript:** `Ga`

```
Offset | Bytes | Método | Tipo       | Campo      | Notas
-------|-------|--------|------------|------------|-------
0x00   | 4     | N()    | uint32_be  | player_id  | ID del jugador
...    | 1     | F()    | byte       | admin      | 0=no admin, 1=admin
```

#### Action 15: AutoTeamBalance (Xa)

**Clase JavaScript:** `Xa`

```
Offset | Bytes | Método | Tipo  | Campo   | Notas
-------|-------|--------|-------|---------|-------
0x00   | 1     | F()    | byte  | enabled | 0=disabled, 1=enabled
```

#### Action 16: Desynced (Da)

**Clase JavaScript:** `Da`

```
Offset | Bytes | Método | Tipo | Campo | Notas
-------|-------|--------|------|-------|-------
(ninguno - action sin datos adicionales)
```

#### Action 17: BroadcastPings (Ma)

**Clase JavaScript:** `Ma`

```
Offset | Bytes    | Método | Tipo      | Campo | Notas
-------|----------|--------|-----------|-------|-------
0x00   | Variable | N/A    | array     | pings | Array de pings (estructura por determinar)
```

#### Action 18: AvatarChange (Qa)

**Clase JavaScript:** `Qa`

```
Offset | Bytes    | Método | Tipo       | Campo      | Notas
-------|----------|--------|------------|------------|-------
0x00   | 4        | N()    | uint32_be  | player_id  | ID del jugador
...    | 1-5+N    | Ab()   | string     | avatar     | Nuevo avatar
```

#### Action 19: TeamColorsChange (bb)

**Clase JavaScript:** `bb`

```
Offset | Bytes | Método | Tipo  | Campo   | Notas
-------|-------|--------|-------|---------|-------
0x00   | 1     | F()    | byte  | team    | 1=red, 2=blue
...    | ...   | ma()   | ...   | colors  | TeamColor structure (ver sección 6.5)
```

#### Action 20: PlayerOrderChange (Fb)

**Clase JavaScript:** `Fb`

```
Offset | Bytes    | Método | Tipo      | Campo | Notas
-------|----------|--------|-----------|-------|-------
0x00   | Variable | N/A    | array     | order | Array de player IDs (estructura por determinar)
```

#### Action 21: KickRateLimit (Pa)

**Clase JavaScript:** `Pa`

```
Offset | Bytes | Método | Tipo       | Campo       | Notas
-------|-------|--------|------------|-------------|-------
0x00   | 4     | N()    | uint32_be  | min         | Mínimo
...    | 4     | N()    | uint32_be  | rate        | Rate
...    | 4     | N()    | uint32_be  | burst       | Burst
```

#### Action 22: PlayerAvatarSet (Gb)

**Clase JavaScript:** `Gb`

```
Offset | Bytes    | Método | Tipo       | Campo      | Notas
-------|----------|--------|------------|------------|-------
0x00   | 4        | N()    | uint32_be  | player_id  | ID del jugador
...    | 1-5+N    | Ab()   | string     | avatar     | Avatar
```

#### Action 23: DiscUpdate (Hb)

**Clase JavaScript:** `Hb`

```
Offset | Bytes | Método | Tipo       | Campo    | Notas
-------|-------|--------|------------|----------|-------
0x00   | 2     | Bb()   | uint16_be  | disc_id  | ID del disco
...    | 8     | w()    | float64_be | pos_x    | Posición X
...    | 8     | w()    | float64_be | pos_y    | Posición Y
...    | 8     | w()    | float64_be | speed_x  | Velocidad X
...    | 8     | w()    | float64_be | speed_y  | Velocidad Y
```

---

## 8. Apéndices {#apéndices}

### A. Tabla de Conversión de Métodos

| Método game-min.js | Método Python         | Bytes | Tipo         | Endianness  |
|--------------------|-----------------------|-------|--------------|-------------|
| `F()`              | `read_byte()`         | 1     | uint8        | N/A         |
| `zf()`             | `read_signed_byte()`  | 1     | int8         | N/A         |
| `N()`              | `read_uint32_be()`    | 4     | uint32       | Big-endian  |
| `Sb()`             | `read_int32_be()`     | 4     | int32        | Big-endian  |
| `Bb()`             | `read_uint16_be()`    | 2     | uint16       | Big-endian  |
| `Di()`             | `read_int16_be()`     | 2     | int16        | Big-endian  |
| `w()`              | `read_float64_be()`   | 8     | float64      | Big-endian  |
| `Ab()`, `kc()`     | `read_string()`       | Var   | varint+UTF-8 | N/A         |
| `Cg()`             | `read_varint()`       | 1-5   | varint       | N/A         |

### B. Clase Stadium - Método `q.ma()` y `q.ws()`

**Ubicación:** game-min.js líneas ~1900-1950

El parsing del stadium es uno de los más complejos. Se divide en:

1. **Tipo de stadium** (byte): 0-11=predefined, 255=custom
2. **IF custom (255):**
   - Name (string)
   - Background config (8 campos: type, width, height, kick_off, corner, goal_line, color, max_view)
   - Spawn distance
   - **Player physics (92 bytes, 12 campos)** ← ANTES de arrays
   - Additional flags (max_view_override, camera, storage, reset)
   - Extra byte no documentado
   - Arrays: Vertices (32B), Segments (19-39B variable), Planes (40B), Goals (33B), Discs (92B), Joints (28B)
   - Spawn points (red, blue)

**⚠️ CORRECCIONES IMPORTANTES:**

1. **PlayerPhysics:** 92 bytes (no 64), 12 campos (no 7 u 8)
   - Incluye: gravity_x, gravity_y, c_group (uint32), radius, inv_mass_2
   
2. **Vertex:** 32 bytes (no 24)
   - c_mask y c_group son **uint32** (4 bytes), no float64 (8 bytes)
   
3. **Segment:** Tamaño variable (19-39 bytes)
   - Usa sistema de **FLAGS** para campos opcionales (bias, curve, color)
   - c_mask y c_group son **uint32**, no float64
   
4. **Orden de parsing:**
   - Player Physics va ANTES de los component arrays, no después
   - Spawn points van AL FINAL, después de todos los arrays

5. **Byte extra:** Existe un byte 0x00 no documentado entre kick_off_reset y vertex_count

### C. Validación de Parsing

Para validar que el parsing es correcto:

1. **Verificar posición final:** Debe llegar al final del stream sin bytes sobrantes
2. **Validar counts:** Todos los counts de arrays deben ser razonables (0-255)
3. **Validar strings:** No deben contener bytes nulos internos
4. **Validar team:** Debe ser -1, 0, 1, o 2
5. **Validar disc_id:** Debe ser -1 o índice válido en array de discos

### D. Casos Especiales

#### D.1 Replay sin Game Active

Si `game_active == 0`:
- No se parsea game state
- Players pueden existir pero sin discos asociados (disc_id = -1)
- Actions se limitan a chat, team changes, admin changes

#### D.2 Stadium Predefinido

Si `stadium_type != 255`:
- No se leen arrays de componentes
- El parser carga configuración desde lista interna

#### D.3 Player sin Disco

Si `disc_id == -1` (después de Di()):
- El jugador no está en juego (espectador o fuera del campo)

#### D.4 Strings Vacíos vs Null

- Varint 0 → `null`
- Varint 1 → string vacío "" (0 bytes de contenido)
- Varint N → string de N-1 bytes

---

## 9. Referencias

- **game-min.js:** Original HaxBall client JavaScript (minificado)
- **docs/GAME_MIN_REVERSE_ENGINEERING.md:** Análisis preliminar
- **src/haxmetrics/parser.py:** Implementación Python actual
- **src/haxmetrics/binary_reader.py:** BinaryReader Python

---

## 10. Notas de Implementación

### Endianness

**CRÍTICO:** HaxBall usa **BIG-ENDIAN** por defecto en JavaScript:

```javascript
// En game-min.js, clase J (BinaryReader)
constructor(a, b) {
  this.s = a;          // DataView
  this.a = 0;          // position
  this.yb = b;         // little-endian flag
}

// Los métodos usan false (big-endian) por defecto:
N() {
  let result = this.s.getUint32(this.a, false);  // false = big-endian
  this.a += 4;
  return result;
}
```

Esto significa que todos los int32, uint32, int16, uint16, y float64 se leen en **big-endian** a menos que se especifique lo contrario.

### Strings

Los strings se codifican como:
1. **Varint** con longitud (incluye null terminator)
2. **UTF-8 bytes** (longitud - 1 bytes)
3. **Null terminator implícito** (no se lee, se descuenta del varint)

**Ejemplo:**
```
Varint: 05 (length = 5)
Bytes: "test" (4 bytes)
Null: implícito (1 byte, no se lee)
```

### Colores

Los colores se codifican como **uint32_be** en formato ARGB:
- Byte 0 (MSB): Alpha
- Byte 1: Red
- Byte 2: Green
- Byte 3 (LSB): Blue

**Ejemplo:** 0xFFE30000 = rojo opaco (alpha=255, red=227, green=0, blue=0)

### Stadium Parsing - Lecciones Aprendidas

**Descubierto mediante ingeniería inversa de game-min.js (Diciembre 2024):**

1. **PlayerPhysics es más grande de lo documentado:**
   - Documentación original: 64 bytes (8 campos)
   - **Realidad:** 92 bytes (12 campos)
   - Campos faltantes: gravity_x, gravity_y, c_group, radius, inv_mass_2

2. **Vertex tiene máscaras uint32:**
   - Documentación original: 24 bytes (solo x, y, bCoef)
   - **Realidad:** 32 bytes (x, y, bCoef + c_mask + c_group)
   - c_mask y c_group son uint32 (4 bytes), NO float64 (8 bytes)

3. **Segment usa codificación variable:**
   - Documentación original: 36 bytes fijos
   - **Realidad:** 19-39 bytes con sistema de FLAGS
   - Byte de flags indica qué campos opcionales están presentes
   - Esto permite optimizar el tamaño cuando valores son default

4. **Orden de parsing corregido:**
   ```
   Correcto (game-min.js):        Incorrecto (doc vieja):
   1. Basic config                1. Basic config
   2. Player physics (92B)        2. Component arrays
   3. Additional flags            3. Player physics (64B)
   4. Component arrays            4. Additional flags
   5. Spawn points                5. Spawn points
   ```

5. **Byte misterioso:** 
   - Existe 1 byte (0x00) entre kick_off_reset y vertex_count
   - NO aparece en game-min.js pero SÍ en replays reales
   - Posible diferencia de versión o campo no documentado

**Impacto:** La documentación vieja dejaba ~1870 bytes sin parsear. La implementación corregida parsea TODOS los bytes del custom stadium.

---

**FIN DEL DOCUMENTO**
