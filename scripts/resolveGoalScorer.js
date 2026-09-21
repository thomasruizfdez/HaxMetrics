'use strict';

const { parseGoalMessage } = require('./parseGoalMessage');

const DEFAULT_WINDOW_FRAMES = 10;

function resolveGoalScorer(events, goalFrameNo, nameToId, windowFrames = DEFAULT_WINDOW_FRAMES) {
  for (const e of events) {
    if (e.eventType !== 0 || e.frameNo == null) continue;
    if (Math.abs(e.frameNo - goalFrameNo) > windowFrames) continue;
    const parsed = parseGoalMessage(e.msg);
    if (parsed && nameToId.has(parsed.scorerName)) return nameToId.get(parsed.scorerName);
  }
  return null;
}

module.exports = { resolveGoalScorer };
