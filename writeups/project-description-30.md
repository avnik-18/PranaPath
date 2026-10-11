# PranaPath — project description (30 lines)

1. PranaPath is a navigation app for the bad-air season: it ranks routes by what your lungs inhale, not just by minutes.
2. The question it answers: two streets can both say "14 minutes" — but one walks you past a market corridor and one detours two blocks; which one do you breathe?
3. Every dose number comes from one published formula: dose (µg) = Σ pollution (µg/m³) × breathing-rate (m³/h) × minutes (per street segment).
4. The engine is deterministic — pure Python, no AI, no network; it sums segment by segment and shows its work.
5. Roads are real: a live OpenStreetMap cut of 4,939 junctions across North-West Delhi (Ashok Vihar, Model Town, Pitampura, Rohini).
6. Demo trip, jog mode, Ashok Vihar → Model Town: fastest route 14.8 min for 125.6 µg inhaled; breathe-safe route 14.9 min for 114.2 µg.
7. Trade: +0.1 minutes → −9.1% less inhaled dose. One extra minute-rate sliver of time, ~11 µg you never pull into your lungs.
8. The map draws both routes on the real corridor — fastest dashed orange, breathe-safe blue — and flags the worst hot segment (~420 µg/m³).
9. The AI never does math. Bedrock (Nova Lite) only words the result in runner-speak.
10. A validator re-checks every digit the model writes against the engine payload; an invented number gets the whole sentence rejected.
11. If Bedrock is down or timing out, an offline template speaks instead — the app never blocks on AI.
12. Architecture is a ring: data → engine → caged guardian → thin API → web; nothing imports "up", and tests are named after the rules they protect.
13. The cloud half is declared and deploy-ready: 14 AWS services in `infra/template.yaml`, region ap-south-1, free tier only, ₹0 so far.
14. It includes 3 Lambdas (routing engine, AI explainer, 15-min AQI refresher on Open-Meteo), API Gateway, DynamoDB, Bedrock, two EventBridge schedules, Step Functions, SNS morning advisories, CloudWatch + X-Ray, IAM with Powertools.
14b. Built on AWS open source — SAM CLI template, Powertools for AWS in every Lambda zip, and a real Cedar policy (`infra/policies.cedar`) — the contest's "≥1 AWS open-source tool" eligibility door, proven by `tests/test_oss_card.py`, no account needed.
15. Step Functions + EventBridge + SNS turn it proactive: a 06:00 advisory lands before the morning jog.
16. Every AWS-side action writes one redacted receipt line to a ledger (`data/receipts/*.ndjson`) — ops you can audit.
17. The web receipts console shows all 14 services and the event feed with an explicit OFFLINE stamp until real keys flip it to LIVE — zero code change.
18. `deploy.py --dry-run` prints the plan and writes a deploy receipt while touching AWS zero times; `--apply` is locked until the team account keys exist.
19. 42/42 offline tests: engine math, validator containment, outage fallback, mock honesty, receipts redaction — the fake-free rules are the test suite.
20. The site right now: one demo sign-in → map app (both routes + doses + hotspots + AI wording) → receipts console behind the same session.
21. The demo is a film: 2 minutes 21 seconds, 9 beats, every number on screen straight from the live engine payloads.
22. Writeups ship at three sizes (449 / 116 / 142 words) plus a build log for the judges.
23. Honest limits, built in and stated on screen: pollution bands per road class are modelled until the live AQI feed lands with the cloud half; the demo is one corridor, not a city.
24. Pollution per road class is relative (market ≈1.4×, quiet ≈0.85×) and summed within each cell — it stays truthful even while the absolute baseline scales up later.
25. Why this is defensible for judges: background + local-adjustment is how real exposure studies model it; dose is relative, so the headline number survives resolution questions.
26. Nothing is faked where a camera can check: MOCK stamps, redacted receipts, no invented numbers, ₹0 spent, dry-run proof on film.
27. Security: credentials only in `.env` (git-ignored), never in code or logs; receipts redact anything key-like before disk.
28. AI tools used are disclosed in CREDITS.md per the event rule; the deterministic core is hand-built.
29. One-line pitch: "Your navigation optimises time. Not what your lungs get. We rank the same streets by dose — +0.1 min buys −9.1% inhaled."
30. Repo: deterministic core, caged AI, receipted AWS ops — built to be checked, not believed.
