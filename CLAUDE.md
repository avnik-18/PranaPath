# EcoRoute AI — root CLAUDE.md (ring architecture governance)

One-line: navigation ranked by what you breathe, not just how fast you arrive.
Track: Air (Environmental Hacks, Oct 8–11 2026). Deliverables: repo + deployed URL + 3-min video + writeup/blog.

## RING RULES (the whole architecture in 6 lines)
- Ring 1 `data/` — JSON + keyless fetchers. No AWS import. No business logic.
- Ring 2 `backend/engine/` — pure stdlib maths. Imports: Ring 1 data only. NO network, NO AWS.
- Ring 3 `backend/guardian/` — the caged agent. Imports: Ring 2. AI adapter lives HERE alone (`explain.py` + `bedrock.py`). Fallback template always exists.
- Ring 3.5 `backend/aws/` — env-cred AWS client + receipts ledger (`client.py` + `receipts.py` + deterministic mock). Imported ONLY by api handlers and infra. Credentials never leave `.env`; mock rows are labeled mock.
- Ring 4 `backend/api/` — thin entry points. Imports Rings 2–3. NO logic, NO AI, NO AWS beyond the Lambda runtime.
- Ring 5 `web/` — frontend. Imports NOTHING from backend (contracts are JSON via `lib/api.ts`).
- Ring 6 `infra/` — nothing imports from here. It only references what rings expose.

### Import matrix (violations = revert)
```
data     → (nothing)
engine   → data
guardian → engine            (+ bedrock adapter, own file)
api      → engine, guardian, aws  (thin glue only)
web      → api CONTRACT ONLY (JSON shapes in web/src/types.ts)
infra    → (nothing imports it)
tests    → data only (offline, fixtures, moto-optional)
```

## Working rules
- One reason per file; target ≤150 lines/file; one component/widget per file.
- AI tools used for coding MUST be listed in `CREDITS.md` (event rule).
- No new dependency, no new AWS service, no new endpoint without asking first.
- Tests are named after the rule they protect (`test_llm_outage.py` = Beacon pattern).
- Commit rhythm: engine → tests green → UI → deploy → film. Never "works on my machine" claims (*see `.claude/skills/ring-guard`*).
- Secrets: ONLY in `.env` (git-ignored). `.env.example` documents every key with an empty value. No AWS keys in the repo, ever.

## Where everything discussed lives (docs index)
| Topic | File |
|---|---|
| Build order + phases | `docs/PLAN.md` |
| Ring architecture + AWS map (14 svcs) | `docs/ARCHITECTURE.md` |
| Winner study (what we copied, 91 cues) | `docs/winners-methods.md` (+ `../winner_cool_points.md` in the parent study folder) |
| Credits research ($200 trial / $25 team / prizes) | `docs/research-aws-credits.md` |
| Decision log (every choice made with the user) | `docs/decisions-log.md` |
| Known gaps, assumptions, honest limits | `docs/honest-limits.md` |
| Demo film beats | `DEMO.md` |
| Scope + non-goals + 3-stage vision | `IDEA_SCOPE.md` |

## Folder map (each folder has its own CLAUDE.md = its rules)
`data/` · `backend/` (→ `engine/`, `guardian/`, `api/`) · `web/` · `infra/` · `tests/` · `docs/`

**How to explain to the user:** they are new to git/AWS/formats — one paragraph at a time, concrete ₹-number examples, define every term inline, offer to zoom into ONE idea when confused.
