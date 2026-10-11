# DEMO.md — film/final_cut.mp4 (2:21) beat sheet — the video IS the submission

Rendered from the REAL handler payloads (`web/frames/mk_beats.py`), shot via Edge headless
(`shot_all.ps1` + `shot_aws.ps1`), assembled in WSL ffmpeg (`/tmp/eco_assemble9.sh`).
Every narration sentence has something on screen at that second (Beacon rule).

| Beats | Narration (voice-over or on-card) | On camera | AWS visibility |
|---|---|---|---|
| 1 · 0:00–0:16 | "October Delhi. Your navigation optimises TIME — not what your lungs get." | dark hero card, kicker `BAD-AIR DAY` | — |
| 2 · 0:16–0:32 | "Rank routes by inhaled dose — a published formula, deterministic engine, no AI in the math." | dose formula card | — |
| 3 · 0:32–0:48 | "Measured trip: Route B costs +0.1 minutes, inhales 9.1% LESS. Worst segment named." | two route cards, +0.1→−9.1% pill, hot-edge badge | — |
| 4 · 0:48–1:04 | "Why trust it? The engine computes, the AI words it — one sentence, validator-gated." | explanation quote + validator badges | — |
| 5 · 1:04–1:21 | "The product: real Delhi roads, hot corridor flagged, doses on the side." | LIVE MAP (beat5 wide shot) | — |
| 6 · 1:21–1:37 | "Real OSM roads and real dose math; pollution bands modelled until the live refresh lands." | honest-limits card | — |
| 7 · 1:37–1:53 | "The receipts console: 14 declared services, 11 workflow events, every row traceable." | ops console strip; MOCK→LIVE quote | 14 svc names |
| 8 · 1:53–2:09 | "Judges sign in with one click. Product AND ops console — the same session." | demo login card | — |
| 9 · 2:09–2:21 | "Deploy kit: plan first, receipts always. Dry-run proved ₹0 spent — apply waits for team keys." | deploy command + receipt line | EventBridge/SFN/SNS in template |

Durations: 8×16.2 s + 12.6 s tail ≈ 141 s ✓ (<3:00; room for a spoken intro if the user records it).
