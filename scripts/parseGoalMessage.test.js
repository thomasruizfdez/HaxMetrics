'use strict';

const { parseGoalMessage } = require('./parseGoalMessage');

describe('parseGoalMessage', () => {
  test('parses "GOAL!" format with assist', () => {
    const msg = 'GOAL! \u{1F7E5} 1 - 0 \u{1F7E6} \u{1F552}1:42 ⚽SACHA. (Assist: Člyburn)';
    expect(parseGoalMessage(msg)).toEqual({ scorerName: 'SACHA.', assisterName: 'Člyburn' });
  });

  test('parses "GOAL!" format without assist', () => {
    const msg = 'GOAL! \u{1F7E5} 1 - 1 \u{1F7E6} \u{1F552}3:51 ⚽vMarius';
    expect(parseGoalMessage(msg)).toEqual({ scorerName: 'vMarius', assisterName: null });
  });

  test('parses "OWN GOAL!" format with assist', () => {
    const msg = 'OWN GOAL! \u{1F7E5} 7 - 4 \u{1F7E6} \u{1F552}11:51 \u{1F438}Bandolero (Assist: mev)';
    expect(parseGoalMessage(msg)).toEqual({ scorerName: 'Bandolero', assisterName: 'mev' });
  });

  test('parses "Goal by" format with assist', () => {
    const msg = '⚽ [08:45] Goal by nzsu ! Assist by tehito. Goal speed : 7.88km/h.';
    expect(parseGoalMessage(msg)).toEqual({ scorerName: 'nzsu', assisterName: 'tehito' });
  });

  test('parses "Goal by" format without assist', () => {
    const msg = '⚽ [08:31] Goal by Colcho ! Goal speed : 48.91km/h.';
    expect(parseGoalMessage(msg)).toEqual({ scorerName: 'Colcho', assisterName: null });
  });

  test('returns null for an unrelated chat message', () => {
    expect(parseGoalMessage('gg wp')).toBeNull();
  });

  test('returns null for non-string input', () => {
    expect(parseGoalMessage(undefined)).toBeNull();
    expect(parseGoalMessage(null)).toBeNull();
  });
});
