# infra/ CLAUDE.md — RING 6 (AWS lives ONLY here; nothing imports it)

One reason: one CloudShell command turns this repo into deployed AWS, free-tier bound.

Plan (locked with user — see docs/decisions-log.md): SAM template `template.yaml`
- Lambda ×2 — `ecoroute-engine` (handler.py; writes DDB) + `ecoroute-explainer` (Bedrock invoke; READ-ONLY role — Beacon two-roles-one-direction).
- API Gateway (HTTP API) → engine Lambda.
- DynamoDB — one table `EcoRouteTrips` (on-demand; free tier).
- Bedrock InvokeModel — Nova Lite with inference-bound timeout (12 s → fallback template inside guardian).
- Powertools for AWS (Lambda) — our ≥1-AWS-OSS-tool eligibility card; X-Ray trace toggle.
- EventBridge Scheduler (15-min AQI refresh → DDB snapshot) + 06:00 advisory state machine via Step Functions (`AdvisoryOrchestrator`) → SNS email.
- Cognito user pool — LAST, only if event stays green.
- Amplify Hosting — web/ as ZIP deploy (no-git site upload, Factcade trick).

Deploy = `bash infra/deploy.sh` run inside AWS CloudShell (uploads repo zip; prints API + site URLs). Fail-closed: refuses when BEDROCK model access missing (prints fallback notice).

Cost guards (all free-tier; worst-case cents): no OpenSearch/RDS/NAT/EC2; DDB on-demand only; scheduler low-frequency; kill switch `APPLY_ENABLED=false` flips advisory off.

Free-tier ledger (monthly, nothing billable at demo scale)
| Service | Free tier we use | Demo burns |
|---|---|---|
| Lambda 3 fns | 1M req + 400k GB-s | minutes |
| HttpApi | 1M calls | hundreds |
| DynamoDB on-demand | 25 GB + 25 WCUs | KBs |
| Bedrock Nova Lite | pay-per-token only when ON | sentences |
| EventBridge schedules | free cron | 96/day |
| Step Functions | 4k state transitions | 1/day ×2 |
| SNS email | 1k/month | ≤5 |
| X-Ray/CloudWatch | traces 50k, logs 5 GB | KBs |
| Amplify hosting | 12 months free 5 GB | static |

Rules
- Template changes UPDATE `docs/ARCHITECTURE.md` map + `docs/honest-limits.md` (services=14 locked).
- No secret values in templates; Secrets Manager/OpenAQ key only if OPENAQ wired.
- env discipline: template variables from `.env.example` names only (cf. ALERT_EMAIL at deploy time).

Folder skill (working here)
1. Every infra change = +1 line in decision log; 2. always print "what changed live" after deploy; 3. refund unused: delete created demo resources before submission if advisory unneeded.
