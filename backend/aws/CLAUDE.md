# backend/aws/ CLAUDE.md — RING 3.5 (env-cred AWS access; mock is honest, live is receipted)

One reason: talk to AWS ONLY through credentials arriving via environment/`.env`, and
leave one receipt line per AWS-side action — while never breaking the offline demo.

Contract
- `client.py` — `aws_state()` returns `{mode, region, probe:{dynamodb_ok,lambda_ok,bedrock_ok}, reason}`.
  boto3 is lazy-imported (same pattern as `guardian/bedrock.py`); every probe fails soft
  to `None` (never crashes the demo). `ECOROUTE_AWS_MODE=live|mock|auto` (default auto:
  live iff creds present). Tests inject fakes through the module-level `_factory` hook.
- `receipts.py` — `record(kind, payload)` appends one JSON line to `data/receipts/<yyyymmdd>.ndjson`
  with `ts/kind/payload`; keys ending `key|token|secret` are masked to `***` BEFORE write;
  any OSError → silently returns False (demo continues). `tail(n)` reads recent lines.

Rules (violations = revert)
- No credentials in code, tests, logs or receipts — env vars (`AWS_ACCESS_KEY_ID`,
  `AWS_SECRET_ACCESS_KEY`, `AWS_REGION` default `ap-south-1`, optional `AWS_PROFILE`) only.
- Mock is a labeled truth: anything not mode `live` says so; nothing pretends.
- This folder is imported by `api/` handlers ONLY (thin glue); it imports nothing from rings.
- Every change lands with a test named after the rule it protects.
