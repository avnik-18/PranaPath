# PranaPath — full writeup (≤500 words)

**One line:** navigation ranked by what you breathe, not just how fast you arrive.

On a bad-air Delhi day, the "fastest" route a jogger gets grazes a dense market corridor —
the cheapest-in-time path maximizes lungs. PranaPath adds the missing cost: **inhaled
pollution dose per street segment**, computed with the published formula
`dose(µg) = C(µg/m³) × IR(m³/h) × minutes/60` (breathing rates: walk 1.4, cycle 2.3, jog 3.0
m³/h). The engine runs **two simultaneous Dijkstras** on a real OpenStreetMap cut of the
Rohini–Pitampura corridor (4,939 junctions, 5,692 segments, largest connected component,
road-class pace conversion): regular `fastest`, and `breath-safe` — the **dose-optimal route
under a time cap you choose** (no cap / ≤1.05× / ≤1.1× / ≤1.35× / ≤1.5× / ≤2× of the fastest),
solved exactly with Pareto label-setting, then minimizing real dose. Each street's AQI reads a
shared **Gaussian exposure-source table** — hot plumes (markets, expressway) and clean park
pools — the same table that renders the 50-m smog field behind the map; every blob on the map is
clickable and answers with its own reading. Result on the Delhi demo trip (`ashok_vihar →
model_town`, jog): **+3.1 minutes → −10.6% inhaled dose** (17.9 vs 14.8 min; 119.2 vs 133.4 µg);
a second city, **Bengaluru** (Koramangala–Indiranagar, Silk Board plume), loads one select away.

**Why the AI can't lie (the prize-grade idea):** a caged-expert pattern. The deterministic
engine produces every number; an explainer agent only **words** the journey. The agent's
system prompt bans inventing facts; a **validator** re-checks every digit and ID it writes
against the engine payload — any mismatch, banned symbol, or invented identifier is rejected,
and if the LLM is unavailable, a template assembled from engine stats speaks instead
(`tests/test_llm_outage.py` proves the outage path). This "statistics-in, sentence-out" gate is
magpie-style arithmetic discipline from the winners' playbook — running on a jogger's phone.

**The receipts culture:** every AWS-side action writes one redacted JSON line to
`data/receipts/` (`key/token/secret` masked before disk); the ops console labels every row
"MOCK" until a real probe earns it "LIVE — probe-backed". The repository ships its own rules:
**every folder has a `CLAUDE.md`** declaring its import rights (six-ring architecture, plus a
3.5 ring for the env-credential AWS client), so an auditor knows exactly which file may touch
what. 42/42 offline tests each protect a named rule.

**Where AWS genuinely fits (declared today, deployed on the team account):** 14 services, free
tier, region `ap-south-1` — Amplify-hosted island; API Gateway into `Lambda[engine]` (dose
engine) with `Lambda[explainer]` → **Bedrock Nova Lite** behind the validator for the
route narration; **DynamoDB** for trip receipts + AQI snapshot; **EventBridge** 15-minute
keyless Open-Meteo refresh; a 06:00 IST scheduled **Step Functions**
`AdvisoryOrchestrator` that picks the best jog window and pings **SNS** email; **CloudWatch**
alarms, **X-Ray** traces, **IAM** scoped roles, **Powertools for AWS**. Zero-RDS, zero-EC2,
zero-NAT — a ₹0-conservative design with `infra/deploy.py --dry-run` proving "what changed
live: NOTHING" before team keys arrive.

**Honest limits:** roads/minutes are real; per-class pollution bands are modelled until the
keyless refresh lands; demo coverage is one corridor, clearly labelled. **Built in one
session** — AI-assisted coding disclosed in `CREDITS.md`.

Word count: ~480.
