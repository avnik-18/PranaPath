# build_manifest.md — the judge's 2-minute tour

## What this is
EcoRoute AI: route planning ranked by **inhaled dose** (`C × IR × minutes`), deterministic
engine over a real OpenStreetMap cut; caged AI never computes numbers; 14 free-tier AWS
services declared for `ap-south-1` deployment, receipted to `data/receipts/`.

## The 5-command tour
```bash
python3 backend/api/local_server.py 8787        # ① API: /state /routes /aws/status /aws/panel
cd web && npm ci && npm run build               # ② the island (fixture mode = judge-grade offline)
                                                # ③ open the built site → one-click demo login
python3 infra/deploy.py --dry-run               # ④ PLAN printed, ₹0, "what changed live: NOTHING"
wsl python3 -m unittest discover -s tests       # ⑤ 42/42 rule-tests green
```

## File map (one reason per item)
| Folder | Meaning |
|---|---|
| `data/` | OSM graph JSON + AQI snapshot + fetcher/generator scripts — nothing here imports up |
| `backend/engine/` | pure-stdlib dose + dual-Dijkstra maths |
| `backend/guardian/` | the caged explainer: tools/prompt/validator/bedrock/template |
| `backend/aws/` | env-cred client + receipts ledger + deterministic mock (Ring 3.5) |
| `backend/api/` | thin doors: `handler.py`, `aws_handler.py`, `local_server.py`, schemas |
| `web/` | Vite+React+TS island: landing face, map compare, ops receipts console |
| `tests/` | 42 rule-tests (dose exactness, determinism, validator, outage, contracts, deploy kit) |
| `infra/` | `template.yaml` (the declared stack) + `deploy.py` (plan/apply) + lambda entries |
| `docs/` | ARCHITECTURE, WRUN (runbook), honest-limits, decisions-log, winners-methods |
| `writeups/` | 500 / 150 / 120-word submission-ready copy |
| `film/final_cut.mp4` | the 2:21 submission film (9 beats) |

## Proof points a judge can click
- `data/receipts/*.ndjson` — real deploy.dry-run receipts already there.
- `docs/honest-limits.md` — the truth table: measured vs modelled vs mocked.
- The landing page = the whole claims table visible in 40 seconds of scroll.
