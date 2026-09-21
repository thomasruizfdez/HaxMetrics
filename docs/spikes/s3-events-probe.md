# S3 — Sonda de `data.events[]` de node-haxball (issue #29)

> **Estado:** entregable para revisión humana (HITL). Resultado de ejecutar la sonda
> desechable `scripts/spikes/s3_probe_events.js` sobre las 14 replays reales del corpus
> y sobre las fixtures sintéticas de un solo tipo de acción usadas por el parser Python
> deprecado (`src/tests/fixtures/actions/*_action.hbr2`).

## Cómo reproducir

```bash
node scripts/spikes/s3_probe_events.js
# vuelca además un JSON crudo en %TEMP%/s3-events-dump.json
```

## Hallazgo 1 — `data.events[]` ES el stream completo de Actions (24 tipos)

`Replay.readAll(bytes).events[]` no es una lista genérica de "eventos de sala": es la
misma secuencia de **Actions** de 24 tipos (0-23) documentada en
`docs/HBR2_PARSING_GUIDE.md` y ya modelada en el parser Python deprecado
(`src/haxmetrics/models/actions/action_type.py`). El campo discriminador es
**`eventType`** (no `kind` ni `type`, que no existen o devuelven valores irrelevantes de
otros getters del prototipo). La numeración coincide exactamente con
`ActionType` de Python — confirmado cruzando las fixtures sintéticas de un solo tipo de
acción:

| `eventType` | Acción (Python `ActionType`) | Campos relevantes vistos |
|---|---|---|
| 0 | `MESSAGE` (mensaje de sistema, incl. anuncios de gol de bots de sala) | `msg`, `color`, `style`, `sound` |
| 3 | `PLAYER_INPUT` | `byId`, `input` — el grueso del volumen (~1 evento/frame/jugador activo) |
| 5 | `PLAYER_JOINED` | `id` (confirmado presente en corpus real: 1-12 joins por replay) |
| 6 | `PLAYER_LEFT` | `id`, `reason`, `ban` |
| 7 | `MATCH_START` | — |
| 8 | `MATCH_STOPPED` | — |
| 12 | `PLAYER_TEAM_CHANGE` | `playerId`, `team` (objeto `{id, color, defenseDir, ...}`) |
| 17 | `BROADCAST_PINGS` | `pings` (array) — ruido, no relevante para stats |

✅ **Join/leave/team_change son 100% estructurados y fiables** — no requieren heurística
ni parsing de texto. Confirmado en el corpus real: todas las 14 replays excepto una
tienen joins/leaves/team_changes (0 a 21 por replay), consistente con partidas donde
entra y sale gente.

⚠️ `player_joined_action.hbr2` (fixture sintética) no pudo leerse con
`Replay.readAll` (`Offset is outside the bounds of the DataView`) — parece ser una
fixture minimal incompatible con el parser más estricto de node-haxball. No bloquea:
el `eventType 5` para joins ya se confirmó por otra vía (corpus real + enum Python).

## Hallazgo 2 — NO hay un campo estructurado "autor del gol"

`goalMarkers[]` solo trae `{frameNo, teamId}` (equipo que encaja, ver spike S1). No
existe ningún `eventType` dedicado a "gol marcado por jugador X" en las 24 acciones del
protocolo — el motor de HaxBall no registra el autor como dato de sala.

**Lo que SÍ hay: mensajes de sistema (`eventType 0`) generados por el BOT/SCRIPT de la
sala**, que en la práctica anuncian el gol con el nombre del autor. Encontramos **dos
formatos distintos** según el script de la sala (esto es contenido de terceros, no del
protocolo HaxBall):

1. `GOAL! 🟥 {red} - {blue} 🟦 🕒{mm:ss} ⚽{scorer}` (+ opcional ` (Assist: {assister})`),
   con variante `OWN GOAL! ... 🐸{scorer}` para autogoles.
2. `⚽ [{mm:ss}] Goal by {scorer} ! Assist by {assister}. Goal speed : {speed}km/h.`

Ambos aparecen 1-3 frames después del `goalMarker.frameNo` correspondiente.
**Cobertura verificada: 86/86 goles (100%) en las 14 replays del corpus** tienen un
mensaje de alguno de los dos formatos dentro de ±10 frames del `goalMarker`.

⚠️ **Esto es un mejor-esfuerzo, NO una garantía protocolaria.** Solo cubre salas que
corren uno de estos dos scripts/bots concretos. Una sala con otro bot (o sin bot de
anuncios) no tendrá ningún mensaje de gol parseable, y el campo de autor deberá quedar
`null`. No existe una tercera vía estructurada de respaldo sin recurrir a heurística
física (último jugador con `kicking=true` cerca del frame del gol), que queda fuera de
esta pasada (ver plan de issue #29).

## Resumen para la implementación de #29

| Dato | Fuente | Fiabilidad |
|---|---|---|
| Roster por equipo | `players.parquet` (ya existe) | ✅ |
| Altas/bajas (join/leave) | `events[]` `eventType` 5/6, campo `id` | ✅ estructurado |
| Cambio de equipo | `events[]` `eventType` 12, campos `playerId`/`team.id` | ✅ estructurado |
| Tiempo jugado | ya implementado (`analytics.py`) | ✅ |
| Autor del gol | `events[]` `eventType` 0, texto libre de bot de sala — 2 formatos conocidos | ⚠️ mejor-esfuerzo, `null` si no matchea ningún formato conocido |
