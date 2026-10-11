# data/ CLAUDE.md — RING 1 (raw materials only)

One reason: hold the world's facts as plain files. No code logic, no AWS imports, no UI.

Rules
- Everything here is JSON + one keyless fetcher script per source. Fetchers may NOT be imported by the engine directly in tests (tests load the JSON fixtures offline).
- Every file carries `_meta`: { source, generated_utc, note: "illustrative|measured" } — honesty labels (slate/honest-limits rule).
- Keyless sources: Open-Meteo air-quality (no key), Overpass/OSM (no key). OpenAQ = optional slot, key stays in `.env` (OPENAQ_API_KEY), never in code.
- Files stay small and versioned (committed) for reproducibility; realistic cap ≈ a few MB per file; larger → note the generator + ship a representative sample instead.

Files (present / pending)
- `aqi_snapshot.json` — bundled readings (present)
- `delhi_graph.json` — nodes/edges for the demo corridor (pending; generator script documents OSM provenance)

Folder skill (what Claude does when working here)
1. Add/refresh only via fetcher script outputs; 2. keep labels honest; 3. never hand-craft sensor numbers without marking them illustrative.
