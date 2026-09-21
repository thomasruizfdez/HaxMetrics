'use strict';

function buildPlayerMaps(players) {
  const teamById = new Map();
  const kickingById = new Map();
  const inputById = new Map();
  let hasActiveTeam = false;
  for (const p of players) {
    const teamId = p.team ? p.team.id : 0;
    teamById.set(p.id, teamId);
    kickingById.set(p.id, !!p.isKicking);
    inputById.set(p.id, p.input | 0);
    if (teamId !== 0) hasActiveTeam = true;
  }
  return { teamById, kickingById, inputById, hasActiveTeam };
}

module.exports = { buildPlayerMaps };
