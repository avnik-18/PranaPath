# winners-methods.md — what this repo copied from the 12 First Commit winners

Source of the detailed study: `../winner_cool_points.md` (~91 cues, all 12 teams) and ../../PROJECT_CONTEXT.md. This file = only what EcoRoute actually reuses.

| Pattern | Stolen from | Where it lives in this repo |
|---|---|---|
| Deterministic core does the math; AI never computes | Factcade ("AI never computes money") | engine/ vs guardian/ split |
| Read-only tools + "never invent IDs/numbers" promo | Factcade system prompt | guardian/tools.py + prompt.py |
| Validator rejecting invented values | Magpie arithmetic gate | guardian/validate.py |
| Bedrock-down fallback, plus a test named for the outage | Suraksha test_llm_outage.py | guardian/fallback template + tests/test_llm_outage.py |
| Two IAM roles, one direction | Beacon (agent 0 writes; actor scoping) | infra: engine writes DDB; explainer read-only |
| Tests named after rules | Beacon 244 tests / Suraksha | tests/ file naming |
| One reason per file; thin lambdas | Suraksha ally/ | every backend/ file |
| Infra as its own isolated package | CampusEvac infra/ | infra/ |
| Widget-per-file frontend | CampusEvac simulation/components | web/src/components/ |
| .env.example at root AND packages | Suraksha | ./.env.example + backend/web copies |
| Honest limits + "what fought back" writeup | Magpie/Beacon | docs/honest-limits.md |
| Scope board + non-goals, ask-first | Slate CLAUDE.md | IDEA_SCOPE.md + root CLAUDE.md |
| Deploy via CloudShell zip (no laptop toolchain) | Factcade | infra/deploy.sh |
| Structured logs w/ decision receipts on camera | Beacon/Slate (Cedar lines) | Powertools logging on every route decision |
| Screenshot/HTML-built demo film + narration | Beacon video/ | .claude/skills/demo-video |
| Metaphor for the signature move | nay "Sleep Contract"/"ngrok for events" | "breathe-safe routing" / "HotLeaf"? (name live during writing) |
