# PranaPath — short writeup (≤120 words)

Navigation ranked by what you breathe, not how fast you arrive. PranaPath computes inhaled
dose per street segment (`C × IR × minutes`, published formula, deterministic engine) on real
OpenStreetMap cuts of Delhi + Bengaluru, returning fastest vs breath-safe routes under a time
cap you choose — demo trip: **+3.1 min → −10.6% dose**. A caged AI explains the route in one
sentence; a validator rejects any number or ID it didn't receive from the engine; LLM down →
template speaks. Built on AWS open source: SAM CLI + Powertools + Cedar policy — the contest's
eligibility door, test-proven (`test_oss_card.py`), no keys needed. Cloud ring declared: 14
free-tier services (ap-south-1). Every action receipted; mocks say MOCK. AI-assisted.
