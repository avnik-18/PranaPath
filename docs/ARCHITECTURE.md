# ARCHITECTURE.md — rings (source of truth for the picture)

## Offline ring picture (runs with zero AWS)
```
web (map)  --JSON-->  backend/api (local_server.py)
                         ├─ engine  = Dijkstra/A* + dose math  (data/*.json in)
                         └─ guardian = explain sentence         (bedrock.py OR template fallback)
```
## Deployed ring picture (14 AWS services, free tier)
```
Amplify (web) ──HTTPS──> API GW ──> Lambda[engine] ──> DynamoDB(trips+AQI snapshot)
                                   └─> Lambda[explainer, read-only role] ──> Bedrock Nova Lite (validator-gated)
EventBridge Scheduler ──> Lambda[aqi-refresh 15min] ──> DynamoDB
EventBridge 06:00 ──> Step Functions[AdvisoryOrchestrator] ──> SNS email (best jog window)
CloudWatch logs/alarms + X-Ray traces on every route decision  •  Powertools (AWS OSS card)
```
Data flow claim: engine numbers NEVER cross Bedrock as free prose — Bedrock receives computed stats only and must repeat them back; the validator enforces it.

Region planned `ap-south-1` (India, like Magpie). Entirely Free-tier: no RDS/EC2/OpenSearch/NAT anywhere.
