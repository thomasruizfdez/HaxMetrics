# HaxMetrics — Domain Glossary

## Core Concepts

**Replay**
A recorded Haxball match stored as a `.hbr2` binary file. Contains an initial state snapshot plus a sparse event stream. Does NOT store per-frame disc positions — per-frame data requires physics simulation.

**Frame**
A single physics tick in the Haxball simulation, running at 60Hz (60 frames/second). The `frame_delta` field in every action is relative to the previous action; the Actions collection accumulates these into absolute frame numbers.

**Disc**
The fundamental physics entity in Haxball. Both the ball and each player avatar are discs. Properties: position (x, y), velocity (vx, vy), radius, bounce coefficient (bCoef), damping, inverse mass (invMass), collision group/mask.

**PlayerInput**
An event (Action type 3) recording a change in a player's keyboard state: left, right, up, down, kick. Only emitted when input changes — not every frame.

**DiscUpdate**
An event (Action type 23) recording the physics state of a disc at a specific frame. Emitted sparsely when disc state changes significantly. Serves as a simulation checkpoint: if a simulation produces positions matching all DiscUpdates in the file, the simulation is correct.

**GameState**
The initial snapshot of all disc positions and game metadata (scores, frame, kickoff team) recorded at the start of the replay. The starting point for physics simulation.

**Simulation**
Running the Haxball physics engine tick-by-tick from the initial GameState, applying PlayerInput events at their correct frames, to produce per-frame disc positions. Required for complex statistics (distance, heatmaps, pass trajectories).

**Oracle**
The JS simulation component (`simulator/simulate.js`) that drives `game-min.js` to produce authoritative per-frame data. Used as ground truth to validate the Python parser.

**Actions**
The ordered stream of 24 event types encoded sparsely in the HBR2 file after the initial state sections. Includes player lifecycle, match lifecycle, inputs, disc checkpoints, and room settings.

**Stadium**
The map/arena where the match is played. Either predefined (types 0–9) or custom (type 0xFF). Defines the geometry (vertices, segments, planes, goals) and physics constants (gravity, player physics, ball physics) needed for simulation.
