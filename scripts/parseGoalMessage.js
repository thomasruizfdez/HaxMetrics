'use strict';

// Los goles no llevan autor en el protocolo de HaxBall: sólo lo anuncian bots/scripts
// de sala vía mensajes de sistema de texto libre. Cubrimos los dos formatos vistos en
// el corpus real (ver docs/spikes/s3-events-probe.md); si ninguno matchea, se devuelve
// null y el autor queda sin resolver (mejor esfuerzo, no garantizado).
const PATTERNS = [
  /^(?:OWN )?GOAL! .*[⚽🐸](.+?)(?: \(Assist: (.+?)\))?$/,
  /^⚽ \[\d+:\d+\] Goal by (.+?) !(?: Assist by (.+?)\.)? Goal speed/,
];

function parseGoalMessage(msg) {
  if (typeof msg !== 'string') return null;
  for (const pattern of PATTERNS) {
    const m = pattern.exec(msg);
    if (m) return { scorerName: m[1], assisterName: m[2] || null };
  }
  return null;
}

module.exports = { parseGoalMessage };
