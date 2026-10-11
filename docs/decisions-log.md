# decisions-log.md — decisions made WITH the user (dated)

2026-10-11 (late night)
16. **Best-trip re-scan upgraded the headline** — `mk_beats.py` re-scan picked `ashok_vihar→model_town jog`: +0.1 min → −9.1% (was −5.3%). Landing hero/proof captions and app defaults synced; final cut rebuilt 141 s. *Why: deterministic re-scan kept the film, app and fixture on one story.*
14. **Deploy kit replaces deploy.sh** — `infra/template.yaml` (SAM/CFN, 10 resources → 14 services) + `infra/deploy.py` with `--dry-run` default (packages 3 lambda zips, plans, receipts; AWS untouched) and `--apply` blocked until team creds land in env. Lambda entries at infra/ root (`awslambda_engine.py`, `awslambda_explainer.py`, `refresh_aqi.py`) so Ring 4 stays thin. *Why: user's conservative-AWS rule; `deploy.sh`+CloudShell zip-upload kept, but receipts-first.*
15. **Demo login theater** — user asked for "login"; ONE gate at app entry (demo creds pre-filled, zero real auth) unlocks product + ops console in the same session.

2026-10-11 (evening)
11. **Real OSM graph** — user caught routes not following roads; data ring switched from the synthetic grid to a real OpenStreetMap cut (Overpass POST, 4,939 junctions / 5,692 segments, largest connected component, road-class pace conversions, mid-route market hot-corridor on rohini→pitampura). Engine/tests untouched conceptually; minutes now real; PM bands class-based (260/150/60) + 420 hotspot. *Why: the demo's credibility; the user's one-line catch. Earlier draws failed for two independent reasons: Overpass GET 406 (→POST+UA), ways not sharing node ids (→union-find snapping).*
12. **Web island verified in-browser** (dark CARTO style): real road-hugging polylines for both routes, hotspots, trade-off pills, validator-passed chip; fixture bundle `rohini→pitampura jog` = +0.1 min → −5.3% (fixture trip may be re-picked before the film if a more dramatic one is wanted by re-running `web/mkfixture.py`).
13. Layer order B-under-A so both stay visible; map layer addSource guarded by style-loaded (race fixed).
1. **Stack:** Bedrock Nova (not Grok/OpenAI) — "built-on-AWS" points + winner lineage; rule-template fallback per Factcade. *Why: user offered Grok; we reverted with reason; user structure locked.*
2. **Data:** Open-Meteo (keyless) first; OpenAQ optional later with OPENAQ_API_KEY in `.env` only. Zero keys needed to build.
3. **Credits:** no personal spend ever — ONE team AWS account (captain creates, Free plan); $25 team top-up code claimable via captain-only form; trial $200 belongs to that account (research: `docs/research-aws-credits.md`).
4. **Video:** winners-style 3-min film; Beacon precedent for Chatterbox/Playwright/ffmpeg — our own pipeline in `.claude/skills/demo-video` (WSL ffmpeg).
5. **AI tools disclosure:** Claude Code listed in CREDITS.md (event rule).
6. **Structure:** 6 rings, one reason per file/folder, CLAUDE.md in EVERY folder (this repo ships rules with code).
7. **Integration layers:** skills installed in parent Project (.claude/skills — 15), marketplaces at D:\Hackathon\tools (ZIP flow; company laptop, no Windows git ever).
8. **Skills per folder:** folder CLAUDE.md doubles as the folder's skill/rulebook; root-only `.claude/skills/` holds repo-wide ones (ring-guard).
9. **Stack shape:** stdlib-Python backend + Vite/React/TS/MapLibre frontend — chosen for zero-install dev, free-tier deploy lightness, and Factcade precedent.
10. Grok/other APIs: ask user only when actually blocked; nothing blocked at build time.
