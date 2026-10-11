# EcoRoute AI — form-field writeup (≤150 words)

**The problem:** a jogger's fastest route grazes a market corridor even on Delhi's worst-air
days — maps optimize minutes, never lungs.

**Built:** EcoRoute AI ranks routes by **inhaled dose** — `dose(µg)=Σ C×IR×minutes`
computed deterministically per segment over a real OpenStreetMap cut (4,939 junctions).
Demo trip **+0.1 min → −9.1% dose**, worst street named. A caged AI explains the choice in one
sentence; a validator rejects any digit or ID not received from the engine; outage → template
(tested).

**AWS:** 14 free-tier services for `ap-south-1` — Amplify, API GW → Lambda dose engine,
Bedrock Nova Lite (validator-gated), DynamoDB receipts + AQI snapshot, EventBridge 15-min
refresh + 06:00 Step Functions advisory → SNS, CloudWatch, X-Ray, IAM, Powertools. Every
action redacted-receipted.

**Honesty:** real roads, real math; pollution bands modelled until the keyless feed lands.
AI-assisted (Claude Code).
