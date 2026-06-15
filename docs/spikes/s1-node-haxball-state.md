# S1 — Mapeo del objeto `state` de node-haxball (spike #27)

> **Estado:** entregable para **revisión humana (HITL)**. Resultado de ejecutar la sonda
> desechable `scripts/spikes/s1_probe_state.js` sobre replays reales del corpus.
> Lo que queda **incierto** está marcado con ⚠️ y se deja para **iterar** en fases
> posteriores; el invariante de S2 (marcador reconstruido == grabado) es la red de
> seguridad.

## Cómo reproducir

```bash
node scripts/spikes/s1_probe_state.js [ruta.hbr2] [numFrames]
# default: src/tests/fixtures/actions/HBReplay-2026-04-28-23h50m.hbr2, 10 frames
# vuelca además un JSON crudo en %TEMP%/s1-state-dump.json
```

La sonda usa **sólo** la API pública de `node-haxball@2.3.0`:
`const { Replay } = require('node-haxball')()`.

### Dos descubrimientos de método (clave para todo lo demás)

1. **La API "amistosa" son getters NO enumerables del prototipo.** `reader.state` y los
   discos/jugadores exponen, además de sus campos minificados internos (`U_`, `L`, `$`…),
   getters con nombre (`players`, `pos`, `playerId`, `team`…) definidos en el prototipo.
   `Object.keys()` NO los ve; hay que recorrer `getOwnPropertyNames` por la cadena de
   prototipos. **Conclusión: leer siempre por los getters con nombre, ignorar los campos
   minificados.**
2. **`setCurrentFrameNo(n)` REPRODUCE hasta `n` vía el bucle de `requestAnimationFrame`.**
   Sin un RAF que avance, el reader se queda clavado en el frame 0 (estado vacío, 0
   discos). La sonda inyecta un RAF manual con reloj virtual ("pump") y avanza de forma
   **determinista y sincrónica** hasta cada frame objetivo. Esta es la técnica de stepping
   que necesitará S2 para volcar frames a Parquet.

## Replays usadas

**La sonda corre limpia (exit 0) sobre las 14 replays del corpus.** Todas `version 3`.
Hay **dos familias de estadio**, y la regla `disc.playerId != null` aísla correctamente
los discos-jugador en ambas:

| Familia | replays | discs físicos | discos-jugador |
|---|---|---|---|
| 4v4 | 12 | 36 | 8 |
| 7v7 (FFL 7x7 Oficial v2) | 2 | 25 | 14 |

Ejemplos analizados en detalle: `HBReplay-2026-04-28-23h50m` (7v7, 25 discos),
`HBReplay-2026-01-18-22h42m` (4v4, 170 928 frames, 19 goles),
`HBReplay-2026-03-24-23h30m` (4v4, 7 goles).

---

## 1. Estructura del estado

```
Replay.readAll(bytes) -> ReplayData            (estática, sin física por frame)
  .version            (== 3)
  .totalFrames
  .goalMarkers[]      -> { frameNo, teamId }    (ver §5: semántica de teamId ⚠️)
  .events[]

Replay.read(bytes, callbacks, options) -> reader
  .state              -> RoomState
      .players[]      -> PlayerObject
      .stadium        -> Stadium
      .scoreLimit / .timeLimit / .teamsLocked / .teamColors
  .gameState          -> GameState | null   (null fuera de juego / fin de partido)
      .redScore / .blueScore
      .timeElapsed    (ms del periodo de juego actual; se reinicia en saques)
      .goalConcedingTeam
      .physicsState.discs[]   <-- AQUÍ viven los discos (balón + estadio + jugadores)
  .maxFrameNo / .getCurrentFrameNo() / .setCurrentFrameNo(n) / .length()
```

> ⚠️ **`gameState` es `null`** en frames sin juego activo (antes del saque inicial y tras
> el final de la partida; en el corpus, los últimos frames devuelven `discs=0`).
> S2 debe tolerarlo.

---

## 2. Disco-balón

- Los discos están en **`reader.gameState.physicsState.discs`**.
- El **número total de discos varía según el estadio** (25 en el 7v7, 36 en los 4v4),
  porque incluye los discos del propio estadio (postes, etc.). Por tanto **NO** se puede
  asumir un total fijo.
- **El balón es `discs[0]`** (convención Haxball). Verificado empíricamente: su
  trayectoria arranca en `(0,0)` en cada saque y se mueve de forma continua coherente con
  los goles. Propiedades del balón (replay 7v7): `radius 6.4`, `cGroup 193`, `cMask 63`,
  `invMass 1.575`, `bCoef 0.41975`, `damping 0.99`, `playerId: null`.
- ⚠️ **Robustez:** en el corpus `discs[0]` siempre fue el balón, pero la señal más
  fiable sería identificarlo por sus **flags de colisión** (`API.CollisionFlags`; el balón
  lleva el flag de "ball/score"). Si alguna replay rompiera la convención índice-0, ése es
  el fallback. Se deja para iterar.

---

## 3. Mapeo disco ↔ jugador

- **El enlace es `disc.playerId`.** Cada disco de jugador expone `playerId` = id del
  `PlayerObject`. El balón y los discos de estadio tienen `playerId: null`.
- ⚠️ **`player.disc` devuelve `null` en el reader de replay** (se rellena en salas en
  vivo, no aquí). **No usar `player.disc`**; en su lugar:
  ```js
  const playerDiscs = physicsState.discs.filter(d => d.playerId != null);
  const discOf = id => physicsState.discs.find(d => d.playerId === id);
  ```
- Regla robusta independiente del estadio: **disco de jugador ⇔ `playerId != null`**
  (verificado en 7v7 y 4v4; los discos de jugador tenían `radius 15`).
- Evidencia (frame 58 802 del 7v7): discos índice 11–24 con `playerId` 137–143 y 113–169,
  cada uno casando con un jugador de `state.players` por id.

---

## 4. Coordenadas x/y

- **`disc.pos` = `{ x, y }`** y **`disc.speed` = `{ x, y }`** (objetos, no arrays).
  `disc.radius` escalar.
- **Origen = centro del campo:** en cada saque el balón está exactamente en `(0,0)`.
- **Escala:** `stadium.width` / `stadium.height` (1265 × 630 en el 7v7). Los valores
  observados de x del balón llegan a ±1172 y de jugadores a ±1096, justo por debajo de
  1265 → **`width`/`height` parecen ser SEMI-extensiones** (centro→borde), no el tamaño
  total. ⚠️ Confirmar contra `stadium.vertices` / `stadium.goals`.
- **Orientación:** convención Haxball (coordenadas de pantalla) → **+x a la derecha,
  +y hacia ABAJO**. ⚠️ El **mapeo lado-del-campo ↔ equipo** (qué portería está en +x)
  no se fijó en este spike; la fuente canónica es `team.defenseDir` (ver §5) y/o las
  coordenadas de `stadium.goals`. Se deja para iterar.

---

## 5. Equipos

- **`player.team`** es un objeto `TeamObject` con **`team.id`**:
  **`0` = espectador, `1` = rojo, `2` = azul** (estándar Haxball; en el corpus los
  jugadores en cancha salen con `teamId` 1 y 2, espectadores con 0).
- El `TeamObject` también expone `color`, `cGroup`, `cMask` y **`defenseDir`** (sentido de
  defensa: fuente canónica para saber qué lado del campo defiende cada equipo).
- Marcador en `gameState.redScore` / `gameState.blueScore`.
- ⚠️ **Semántica de `goalMarker.teamId` (la incertidumbre más importante):** parece ser el
  **equipo que ENCAJA el gol (conceding), NO el que marca.** Evidencia (replay 7v7): primer
  gol `{frameNo: 53148, teamId: 1}` y justo después el marcador pasa a `red 0 – blue 1`,
  es decir **marcó el equipo 2 (azul) aunque el marker diga `teamId: 1`**. Esto debe
  **confirmarse en S2** con el invariante "marcador reconstruido == grabado"; hasta
  entonces, NO asumir que `teamId` = goleador.

---

## 6. Resumen para S2 (qué se puede cimentar con fiabilidad)

| Dato | Cómo leerlo | Fiabilidad |
|---|---|---|
| Frames totales | `Replay.readAll(bytes).totalFrames` | ✅ |
| Goles (frame + equipo) | `readAll().goalMarkers[]` `{frameNo, teamId}` | ✅ frame / ⚠️ semántica teamId |
| Marcador por frame | `gameState.redScore` / `blueScore` | ✅ |
| Stepping por frame | RAF manual + `setCurrentFrameNo(n)` (ver sonda) | ✅ |
| Balón (pos/vel) | `gameState.physicsState.discs[0].pos/.speed` | ✅ (✔ índice 0 en el corpus; fallback por flags ⚠️) |
| Discos de jugador | `discs.filter(d => d.playerId != null)` | ✅ |
| Disco ↔ jugador | `disc.playerId` ↔ `player.id` (NO `player.disc`) | ✅ |
| Equipo de un jugador | `player.team.id` (0/1/2) | ✅ |
| Lado de campo ↔ equipo | `team.defenseDir` / `stadium.goals` | ⚠️ iterar |
| Escala/orientación x/y | origen centro; +x→der, +y→abajo; width/height = semi-ext | ✅ origen / ⚠️ escala y goal-side |

### Pendientes a iterar (no bloquean S2)
1. ~~Confirmar semántica de `goalMarker.teamId` (conceding vs scoring)~~ **RESUELTO en S2 (#28):**
   `goalMarker.teamId` = equipo que ENCAJA → `scoring_team = 3 - teamId`. El invariante
   "marcador reconstruido == grabado" pasa en **14/14** replays. Matiz descubierto en S2: el
   `gameState` puede traer un **marcador inicial pre-existente** (grabación iniciada a mitad de
   partido) y **reiniciarse entre partidos** (replays multi-match) → el marcador "de la replay"
   se cuenta por **incrementos** del score (con baseline en el primer frame).
2. Identificación del balón por flags de colisión como fallback al índice 0.
3. `width`/`height` semi-extensión vs total, y mapeo portería→equipo (`stadium.goals` / `defenseDir`).
