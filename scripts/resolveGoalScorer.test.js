'use strict';

const { resolveGoalScorer } = require('./resolveGoalScorer');

describe('resolveGoalScorer', () => {
  const nameToId = new Map([['SACHA.', 216], ['vMarius', 55]]);

  test('resolves the scorer id from a nearby GOAL! message', () => {
    const events = [
      { eventType: 3, frameNo: 7889 },
      { eventType: 0, frameNo: 7892, msg: 'GOAL! 🟥 1 - 0 🟦 🕒1:42 ⚽SACHA. (Assist: Člyburn)' },
      { eventType: 3, frameNo: 7893 },
    ];
    expect(resolveGoalScorer(events, 7891, nameToId)).toBe(216);
  });

  test('returns null when no message is within the frame window', () => {
    const events = [
      { eventType: 0, frameNo: 500, msg: 'GOAL! 🟥 1 - 0 🟦 🕒1:42 ⚽SACHA.' },
    ];
    expect(resolveGoalScorer(events, 7891, nameToId)).toBeNull();
  });

  test('returns null when the message does not match a known goal format', () => {
    const events = [{ eventType: 0, frameNo: 7892, msg: 'gg wp' }];
    expect(resolveGoalScorer(events, 7891, nameToId)).toBeNull();
  });

  test('returns null when the scorer name has no known player id', () => {
    const events = [
      { eventType: 0, frameNo: 7892, msg: 'GOAL! 🟥 1 - 0 🟦 🕒1:42 ⚽Unknown' },
    ];
    expect(resolveGoalScorer(events, 7891, nameToId)).toBeNull();
  });

  test('ignores non-MESSAGE events even if close by', () => {
    const events = [{ eventType: 3, frameNo: 7891, msg: 'GOAL! ⚽SACHA.' }];
    expect(resolveGoalScorer(events, 7891, nameToId)).toBeNull();
  });
});
