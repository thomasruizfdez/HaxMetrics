'use strict';

function buildPlayerMaps(players) {
  const teamById = new Map();
  const kickingById = new Map();
  const inputById = new Map();
  for (const p of players) {
    teamById.set(p.id, p.team ? p.team.id : 0);
    kickingById.set(p.id, !!p.isKicking);
    inputById.set(p.id, p.input | 0);
  }
  return { teamById, kickingById, inputById };
}

module.exports = { buildPlayerMaps };
