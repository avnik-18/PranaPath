# backend/guardian/ CLAUDE.md — RING 3 (the caged agent: BizRule broken here can be fatal; nothing uncaged may bark)

One reason: turn engine NUMBERS into one human sentence, safely.

Contract (non-negotiable; Factcade/Beacon/MarkMagpie lineage)
- `tools.py` — read-only tools the AI may call: `get_route_panel()`, `get_hotspots()`, `get_dose_totals()`. Values come ONLY from the engine.
- `prompt.py` — static system prompt: "call each tool once; never invent numbers or IDs; output one sentence."
- `explain.py` — produces either: (a) `bedrock.py` invocation → validated sentence, or (b) TEMPLATE fallback assembled from engine stats when Bedrock errors/times out (mirrors Factcade's `rule_plan` and is what `test_llm_outage.py` asserts).
- `validate.py` — rejects any sentence containing a number/ID not present in tool output; rejects wrong IDs; returns error → caller falls back. (Magpie's arithmetic gate pattern.)
- `bedrock.py` — the ONLY boto3/AI call: Bedrock `InvokeModel` (Nova). Bounded timeout (12s), single retry, then fallback.

Rules
- The agent NEVER writes state, never mutates data, has no other tools.
- Any new AI capability proposed here → must add (a) a validator rule and (b) an outage test, or it gets rejected.

Folder skill (working here)
1. Every change touches: tool → validator → test trio together; 2. if wording changes, check the fallback template too (they must mean the same thing); 3. no secrets here — Bedrock auth flows by IAM role in Lambda, never by key.
