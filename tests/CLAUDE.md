# tests/ CLAUDE.md — every test protects a rule (Beacon-style naming)

One reason: prove the rules, offline, fast, with zero AWS calls.

Planned set (a rule without a test = an opinion; a test without a rule = clutter)
- `test_dose_math.py` — dose formula exactness per segment (engine ring).
- `test_route_rounding.py` — determinism + rounding edges.
- `test_guardian_validation.py` — validator rejects invented numbers/IDs.
- `test_llm_outage.py` — Bedrock down → fallback template still answers (Suraksha test_llm_outage clone).
- `test_api_contract.py` — schema + status codes; fixture mode only.
- `conftest.py` — loads `data/*.json` fixtures; monkeypatched clock for determinism.

Rules
- Stdlib `unittest` or pytest (pytest if python3.14-venv-free invocation works outside WSL — never pip-install into WSL).
- AWS calls absent — moto only if and where we truly need it later; otherwise fixtures.
- Every failing red test blocks a commit (root CLAUDE.md rhythm).

Folder skill (working here)
1. New rule → name the test file FIRST, then write it; 2. no test may hit network; 3. keep each test ≤ 40 lines.
