# docs/oss-toolchain.md — the AWS-OSS eligibility card, in code

The contest's freedom door: *no AWS account needed if the repo **uses at least one AWS
open-source tool***. PranaPath carries **three**, all exercised without a card:

| Tool (license) | Where it lives | What it does here |
|---|---|---|
| **Powertools for AWS (Lambda)** — Apache-2.0 | `infra/awslambda_engine.py`, `infra/awslambda_explainer.py` (offline-safe import; installed at deploy via the public layer or `infra/requirements-awslambda.txt`) | structured logging on every Lambda entry (`route computed`, `explained`) |
| **SAM CLI** — Apache-2.0 | `infra/template.yaml` (an AWS SAM template), `infra/deploy.py` (`--dry-run` prints the PLAN and writes a receipt; the eventual `--apply` builds with `sam build`) | serverless packaging + deployment pipeline for the 14-service stack |
| **Cedar** — Apache-2.0 | `infra/policies.cedar` + demo sign-in contract + `tests/test_oss_card.py` | one declarative permit: the demo principal views the receipts console |

The site itself is a static React build (`web/dist/`) and hosts free on any provider
(Vercel / Netlify / GitHub Pages — no card) while the Lambda+SAM half stays deploy-ready on
first key: the receipts console labels every row MOCK until then, so no claim is overstated.

Rule source: the event's eligibility table (Agents & AI / Serverless: SAM CLI, LocalStack /
Auth & policy: Cedar / Powertools, etc.). `tests/test_oss_card.py` keeps the card honest —
a rule without a test is an opinion.
