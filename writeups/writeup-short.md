# EcoRoute AI — short writeup (≤120 words)

Navigation ranked by what you breathe, not how fast you arrive. EcoRoute computes inhaled
dose per street segment (`C × IR × minutes`, published formula, deterministic engine) on a real
OpenStreetMap cut of Delhi, returning fastest vs breath-safe routes — demo trip:
**+0.1 min → −9.1% dose**. A caged AI explains the route in one sentence; a validator rejects
any number or ID it didn't receive from the engine; LLM down → template speaks. AWS ring
declared: 14 free-tier services (ap-south-1) — Amplify, API GW, Lambda engine, Bedrock Nova
explainer, DynamoDB, EventBridge AQI refresh, 06:00 Step Functions advisory → SNS,
CloudWatch/X-Ray/IAM/Powertools. Every action receipted; mocks say MOCK. AI-assisted.
