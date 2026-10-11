# prompts/ — the 10 section runbook (submission night)

Ten self-contained `.prompt` files. Each one immerses a fresh agent in exactly one
slice of the remaining work; each call must do ONLY that section's work.

## Table

| # | File | Ring touched | Key deliverable |
|---|------|--------------|-----------------|
| 01 | `01-landing-shell.prompt` | web | landing face + demo login + App switcher |
| 02 | `02-landing-content.prompt` | web | about / rings / proof / honest-limits sections |
| 03 | `03-aws-client.prompt` | backend/aws | env-cred client + receipts ledger |
| 04 | `04-mock-aws.prompt` | backend/aws | deterministic mock state for 14 services |
| 05 | `05-api-aws.prompt` | backend/api | /aws/status · /aws/panel + contract tests |
| 06 | `06-aws-view.prompt` | web | AWS receipts console (mock view) + go-live card |
| 07 | `07-deploy-kit.prompt` | infra | template.yaml + deploy.py + runbook |
| 08 | `08-film-aws.prompt` | film | beats 7–9 + final ≤3:00 film |
| 09 | `09-pack.prompt` | docs | README/DEMO/CREDITS/writeups/zip audit |
| 10 | `10-gate.prompt` | all | PASS/FAIL gate report + fresh-machine drill |

## How to fire one

- **In this Claude desktop session:** say "run section N" — I execute only that section and report against its Verify block.
- **Fresh session elsewhere:** paste the entire file content of `0N-….prompt` as the first message. It is self-contained (paths, machine rules, stop-lines, verify commands).
- **Skip order at your peril:** 03 → 05 → 06 ship the visible receipts view; 07 needs creds tomorrow (deploys only with team account).
- Landmarks: `.env` untracked; receipt lines in `data/receipts/`; Edge screenshots PowerShell side only.
