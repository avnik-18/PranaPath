# WRUN.md — operator runbook: every command from zero to demo (expand in S07)

Local demo tonight (no AWS):
```bash
wsl python3 data/build_delhi_graph.py --offline   # once; cache reused after
wsl python3 -m unittest discover -s tests        # 33/33 green is the gate
python3 backend/api/local_server.py 8787         # API: /state /routes /aws/status /aws/panel
```
Web: `wsl cd web && npx vite build` → serve `web/dist` statically (8929-style) or dev server.

API contract today (Ring 4, thin doors only):

| Endpoint | Returns |
|---|---|
| `GET /state` | readiness + fixture presence |
| `GET /routes?origin&dest&mode` | two routes, doses, hotspots, validated explanation |
| `GET /aws/status` | availability: `mode live|mock`, region, probe booleans |
| `GET /aws/panel?origin&dest&mode` | full ops panel: switch/mode/probe/inventory(14)/activities/receipts/counts |

Mock-discipline: no creds in `.env` → `/aws/*` serves the deterministic MOCK view
(labeled per row); deploy via `infra/deploy.py` after team keys arrive.

## Zero → deployed (when the team account is ready) — 6 commands

```bash
# 1. once — offline proofs
wsl python3 -m unittest discover -s tests          # all green, incl deploy-kit rules
wsl python3 infra/deploy.py --dry-run              # PLAN ok, "what changed live: NOTHING"

# 2. leader's phone/laptop — CloudShell (or any runner with env-only creds)
cp .env.example .env                               # team keys ONLY here
export $(grep -E '^AWS_(ACCESS_KEY_ID|SECRET_ACCESS_KEY|REGION)=' .env | head -3)

# 3. push the declared stack (10 resources → 14 services)
python3 infra/deploy.py --apply                    # CAPABILITY_IAM; receipts print keys of outputs

# 4. wire the web island to the LIVE API
#   .env: VITE_API_BASE=https://<from-ApiBaseUrl-output>  VITE_FIXTURE=false
wsl bash -lc 'cd web && npx vite build'

# 5. Amplify Hosting — ZIP-upload web/dist (no-git site), Factcade trick
# 6. re-run the BA drill: ops console flips MOCK → LIVE (probe-backed rows green)
```
