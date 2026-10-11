# backend/engine/ CLAUDE.md — RING 2 (deterministic core; the "money" of the product — AI never computes it)

One reason: route search + inhaled-dose maths in pure stdlib.

Contents plan (each file ≤ ~100 lines)
- `graph.py` — load `data/delhi_graph.json`; Dijkstra/A* by (minutes, dose) with a λ-mix; expose `shortest_by(objective, origin, dest, k=2)`.
- `exposure.py` — `dose = Σ C(segment) × IR(activity) × minutes(segment)`; `IR()` per mode (walk ~0.35 m³/h scaled, jog ~0.8, cycle ~0.7); returns per-segment hotspots + totals.
- `routing.py` — two-route comparison payload (fastest vs healthiest), hotspot list, deltas.

Rules
- Zero side effects, zero network, zero AWS; float determinism (round at the API edge, not in math).
- No AI text generation here — engines produce NUMBERS only (Factcade rule).

Folder skill (working here)
1. New maths → new pure test in `tests/` FIRST (Beacon: test names = rules); 2. keep helpers ≤3 callers before promoting into a shared file; 3. precision bugs > perf speedups (it's a demo scale, few hundred nodes).
