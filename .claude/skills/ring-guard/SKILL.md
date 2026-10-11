---
name: ring-guard
description: Pre-commit architecture gate for ecoroute-ai — verifies ring import rules (data<engine<guardian<api, web isolated, infra referenced-only), env hygiene (no .env committed, no AWS keys in code), and file-size/single-responsibility caps. Run before every commit or when asked "commit / is the structure clean".
---

# ring-guard — checks (commands in WSL, cwd = repo root)

1. **Import direction (source scan):**
```bash
cd /mnt/d/Hackathon/first_commit/Project/ecoroute-ai
grep -rn "import bedrock" backend/engine backend/api data web 2>/dev/null | grep -v guardian/CLAUDE.md && echo RULE1 FAIL || echo RULE1 PASS  # AI adapter only inside guardian
grep -rn "boto3" backend/engine backend/guardian data tests web | grep -v "bedrock.py" && echo RULE2 FAIL || echo RULE2 PASS         # boto3 only in api/handler.py + guardian/bedrock.py
grep -rn "data" web/src backend/guardian backend/api/backend/engine -l 2>/dev/null | head        # web must not import backend
```
2. **Env hygiene:** `git status --porcelain | grep '.env$'` must be empty; `.env` in .gitignore; no `AKIA` anywhere: `grep -rn AKIA . --exclude-dir=node_modules`
3. **Size caps:** `wc -l` on changed files — flag any >200 lines & ask to split.
4. **Contract sync:** web/src/types.ts fields ⊆ api Schemas — spot-check after any schema change.
5. **Honesty:** every new data file has `_meta.note` ∈ {illustrative, measured}.
Output PASS/FAIL per rule, stop the commit on any FAIL.
