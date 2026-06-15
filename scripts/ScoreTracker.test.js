'use strict';

const ScoreTracker = require('./ScoreTracker');

describe('ScoreTracker', () => {
  test('accumulates a red goal fed after init', () => {
    const score = new ScoreTracker();
    score.init(0, 0);
    score.feed(1, 0);
    expect(score.total).toEqual({ red: 1, blue: 0 });
  });

  test('pre-existing score at init is baseline and not counted', () => {
    const score = new ScoreTracker();
    score.init(2, 3); // recording started mid-match: 2-3 already on the board
    score.feed(3, 3); // one new red goal
    expect(score.total).toEqual({ red: 1, blue: 0 });
  });

  test('score decrease (between-game reset) is ignored', () => {
    const score = new ScoreTracker();
    score.init(0, 0);
    score.feed(1, 0); // red scores
    score.feed(0, 0); // score resets to 0 at start of next game — ignore
    expect(score.total).toEqual({ red: 1, blue: 0 });
  });

  test('accumulates multiple goals across both teams', () => {
    const score = new ScoreTracker();
    score.init(0, 0);
    score.feed(1, 0);
    score.feed(2, 0);
    score.feed(2, 1);
    expect(score.total).toEqual({ red: 2, blue: 1 });
  });

  test('initial exposes the baseline captured at init', () => {
    const score = new ScoreTracker();
    score.init(2, 3);
    expect(score.initial).toEqual({ red: 2, blue: 3 });
  });
});
