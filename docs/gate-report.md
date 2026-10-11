# gate-report.md — submission-gate run (2026-10-11, before tonight's final submit)

Drill evidence: 42/42 tests OK 1.65 s · TSC_OK · BUILD_OK (dist fresh 11:14 UTC) ·
dry-run PLAN "what changed live: NOTHING" · film 1920×1080, 141.0 s, 11.3 MB ·
first commit 607eee7 @ 2026-10-11 11:13 UTC (window Oct 8–11 ✓) · work-tree clean.

| # | Gate line | Result | Note (evidence) |
|---|---|---|---|
| A1 | First commit inside window | PASS | 2026-10-11 11:13 UTC; `git log --reverse` |
| A2 | AI tools declared (README + CREDITS) | PASS | Claude Code in both; Bedrock marked RUN-time only |
| A3 | AWS OSS credited OR region/live URL | PARTIAL | Powertools/X-Ray credited; region ap-south-1 declared; live URL waits for team account (WRUN ladder ready) |
| A4 | No secrets in repo | PASS | grep: only rule-text + `AKIATEST` test dummies + the no-AKIA rule test; receipts leak scan NONE; .env ignored |
| B5 | README problem→stack→architecture→limits | PASS | live URL slot marked pending (honest) |
| B6 | CREDITS lists libs + AI + license | PASS | OSM ODbL, Open-Meteo, MapLibre, Claude Code |
| B7 | Metrics reproducible in-repo | PASS | `web/mkfixture.py` + `web/frames/mk_beats.py` regenerate every number from handlers |
| B8 | Dated plans; no "we plan to" | PASS | decisions-log entries dated; README road-map framing under honest-limits |
| C9 | Live URL 200 | FAIL | no deploy — team account pending; tonight's DEMO is the honest offline one |
| C10 | Offline tests, zero AWS calls | PASS | 42/42 in 1.65 s |
| C11 | Cost: free-tier, worst-case ₹0–cents | PASS | ledger in infra/CLAUDE.md; no always-on resources |
| C12 | Film features ↔ traceable logs | PASS | every beat's claim maps to receipts/panels (`/aws/panel` == lambda shim path) |
| D13 | Beat-sheet coverage + AWS ≥3 beats | PARTIAL | beats 4/7/9 show AWS assets; "live URL bar" naturally absent while undeployed |
| D14 | Narration ↔ screen at the second | PASS | DEMO.md table built from the actual renders |
| D15 | 1920×1080 ≤3:00, captions, audio | PARTIAL | 1080p ✓ 141 s ✓; voiceover not recorded — cards carry the copy tonight |
| D16 | Upload + signed-out link test | FAIL | platform upload pending user |
| B17 | Blog draft (problem/numbers/failures/lesson) | PARTIAL | `writeups/writeup-full.md` has problem/technique/numbers/limits; needs the final 15 min polish |

## The 3 most urgent fixes (none code-blocking)
1. **Live URL** — when the leader's team keys land: WRUN.md 6-command ladder, `deploy.py --apply`, stick the ApiBaseUrl into README A3 + C9 rerun.
2. **Voiceover** — record user voice (or say "AI voice") + burn captions; slides already carry every line (DEMO.md).
3. **Blog + upload** — 15-min polish of writeup-full → blog; upload to the platform; test the signed-out link.

**PASS count today: 11/17 — +2 partial, 4 blocked on user/team-account actions (9, 16) or optional voice/blog (D15/B17). No code FAIL.**
