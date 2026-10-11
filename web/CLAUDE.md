# web/ CLAUDE.md — RING 5 (frontend island: talks only to the API contract)

One reason: show two routes + doses on a map so a runner understands in 5 seconds.

Rules
- Stack: Vite + React + **TypeScript** + MapLibre GL (OSM tiles, keyless). No CSS framework before asking; design tokens live in `src/index.css` only.
- NEVER import from `backend/` — the only bridge is `src/lib/api.ts` (fixture mode via `VITE_FIXTURE=true` against `data/*.json`).
- **1 widget = 1 file = 1 component**: `components/{MapView,RoutePanel,DoseChart,HotspotBadges,AirBanner}.tsx` (CampusEvac widget-split pattern).
- **hooks/** folder: reusable state in `hooks/useRoutesRuntime.ts` etc.; components receive everything by **typed props** — hooks return plain typed objects (no giant context god-object).
- `types.ts` mirrors `backend/api/schemas.py` fields — additive-only contract (rename requires both sides + tests, per root CLAUDE.md).
- No AWS SDK in web (no anonymous Cognito yet unless user asks); no maps secret (keyless tiles).
- Numbers displayed come ONLY from the API payload — re-formatted, never recomputed (Magpie rule: the grid never re-maths).

Folder skill (working here)
1. New on-screen thing → new component file + typed props + a `hooks/` entry if stateful; 2. verify against `webapp-testing` skill after wiring; 3. keep `<200 lines/file`; design tokens before colors.
