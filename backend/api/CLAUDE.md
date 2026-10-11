# backend/api/ CLAUDE.md — RING 4 (thin glue: the door, not the house)

One reason: expose engine+guardian over HTTP; zero business logic of its own.

Files
- `handler.py` — Lambda entry (event → routes). The ONLY file that may import boto3 lazily for Powertools logging/metrics — and even that stays 3 lines.
- `schemas.py` — request/response shapes (dataclasses) shared by tests and web's `types.ts` — the CONTRACT. Additive changes only; ask before breaking.
- `local_server.py` — stdlib HTTP server wrapping the same handlers for offline dev (`python3 backend/api/local_server.py`.

Endpoints (planned; additive only; ask before adding)
- `GET /state` — readiness + fixtures present (Factcade-style).
- `GET /routes?origin&dest&mode` — panel: two routes, doses, hotspots.
- `POST /v1/plan/health-aware`– Stage-2 Rapido-style integration endpoint (same engine).
- `POST /explain` — one sentence via guardian (validator-gated). BACKEND.

Folder skill (working here)
1. Handler ≤ 3 lines per entity: parse → call engine/guardian → shape schema; 2. never compute a number here; 3. every route change = update `schemas.py` + `tests/test_api_contract.py` in the same commit.
