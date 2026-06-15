'use strict';

const { buildPlayerMaps } = require('./buildPlayerMaps');

describe('buildPlayerMaps', () => {
  test('maps player id to team id', () => {
    const players = [{ id: 1, team: { id: 1 }, isKicking: false, input: 0 }];
    const { teamById } = buildPlayerMaps(players);
    expect(teamById.get(1)).toBe(1);
  });

  test('spectator with null team gets team 0', () => {
    const players = [{ id: 2, team: null, isKicking: false, input: 0 }];
    const { teamById } = buildPlayerMaps(players);
    expect(teamById.get(2)).toBe(0);
  });

  test('maps player id to isKicking boolean', () => {
    const players = [{ id: 3, team: null, isKicking: true, input: 0 }];
    const { kickingById } = buildPlayerMaps(players);
    expect(kickingById.get(3)).toBe(true);
  });

  test('maps player id to input bitmask', () => {
    const players = [{ id: 4, team: null, isKicking: false, input: 5 }];
    const { inputById } = buildPlayerMaps(players);
    expect(inputById.get(4)).toBe(5);
  });

  test('missing isKicking coerces to false', () => {
    const players = [{ id: 5, team: null, input: 0 }];
    const { kickingById } = buildPlayerMaps(players);
    expect(kickingById.get(5)).toBe(false);
  });

  test('handles multiple players across all three maps', () => {
    const players = [
      { id: 1, team: { id: 1 }, isKicking: false, input: 0 },
      { id: 2, team: { id: 2 }, isKicking: true, input: 3 },
    ];
    const { teamById, kickingById, inputById } = buildPlayerMaps(players);
    expect(teamById.size).toBe(2);
    expect(teamById.get(1)).toBe(1);
    expect(teamById.get(2)).toBe(2);
    expect(kickingById.get(2)).toBe(true);
    expect(inputById.get(2)).toBe(3);
  });
});
