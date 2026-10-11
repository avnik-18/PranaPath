# honest-limits.md — the truth table (judges reward this; grows with the build)

| Claim | Status |
|---|---|
| AQI numbers in offline demo are real Delhi-scale magnitudes | **illustrative** (bundled snapshot; station values representative, not certified) |
| Road graph | pending OSM extraction — will be a real mapped corridor subset (committed as JSON; generator documented) |
| Route-B search weight | health cost = minutes × (1 + 4.0 × pm25/150 µg/m³) — a routing weight, not a health claim; sensitivity value documented in `backend/engine/routes.py` (HEALTH_SENSITIVITY) |
| PM contrast in demo data | bands 60/150/260/420 µg/m³ across green/base/highway/market corridor edges — labeled illustrative (real OSM+AQI wiring is Phase 3) |
| Health claims framing | "less inhaled pollution dose" only — never promises health outcomes |
| Bedrock explainer | live only after AWS deploy; offline demo uses template fallback (test_llm_outage) |
| Stage 3 citywide analysis | built lite only if time allows; otherwise future work |

Auto-rule: any new claim enters this table BEFORE it enters the README/demo.
