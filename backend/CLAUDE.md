# backend/ CLAUDE.md — Rings 2–4 (one serverless-python package)

One reason: all non-frontend computation, in three strictly layered sub-folders.

Import order (enforced)
- `engine/` ← imports `data/` loaders ONLY. Pure stdlib. Deterministic output.
- `guardian/` ← imports `engine/` only. Owns ALL AI (`bedrock.py`) + validator + fallback.
- `api/` ← imports `engine/`, `guardian/`. THIN handlers, no business rules.

Rules
- No AWS import above engine/guardian/api glue; boto3 appears ONLY in `api/handler.py` (Lambda runtime) and guardian's `bedrock.py`.
- `data/` is never mutated by backend code.
- Every public function has a tiny `__doc__` one-liner — the user reads these.

Folder skill (working here)
1. Add logic to the owning subfolder only ("one reason per folder"); 2. if two folders need the same helper, promote it to `engine/` (pure) or duplicate 3 lines rather than invent a shared-with-side-effects helper; 3. run `tests/` after every change — a rule without a test is an opinion.
