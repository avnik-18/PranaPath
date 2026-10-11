# CREDITS — libraries, data, and AI tools (event-required disclosure)

Dated: 2026-10-11 · repo: PranaPath (first.commit Environmental Hacks, Track: Air)

## Open-source / data sources
- `data/delhi_graph.json` — road network extracted from **OpenStreetMap** (© OpenStreetMap contributors, ODbL) via Overpass API (keyless); generator: `data/build_delhi_graph.py`.
- Air quality — **Open-Meteo Air-Quality API** (keyless, free) for live snapshot refresh; the bundled `data/aqi_snapshot.json` carries an `illustrative` label where noted.
- Maps — **MapLibre GL JS** + OpenStreetMap raster tiles via the CARTO keyless style.
- Frontend stack — **React + Vite + TypeScript** (per-repo dev tooling; no CSS framework).
- Python — standard library only in the engine ring (no pip, no boto3 dependency at dev time).
- Patterns consciously copied from the 12 first.commit winners (see `docs/winners-methods.md`).

## AI tools used to write this project (explicit per event rules)
- **Claude Code (Anthropic)** — coding assistant for the entire repo (engine, guardian, API, web island, infra template, deploy kit, film pipeline) and this disclosure.
- **AWS Bedrock Nova Lite** — intended model for the deployed explainer at RUN time (validator-gated; **not** an author of code).

## Explicitly NOT used
- Google Maps APIs (ToS/cost) · paid tiles · Grok/OpenAI models (deliberately replaced by Bedrock Nova with a rule-based template fallback) · any personal-credit AWS spend.
