# IDEA_SCOPE.md — the idea, the three stages, and the cuts

## The idea (user's own, refined with the winners' method)
1. **Stage 1 — personal health routing (THE BUILD):** jog/cycl/walk routes ranked by inhaled
   pollution dose, not only time. Route B may cost minutes; the panel shows the exact trade-off.
2. **Stage 2 — platform API (one endpoint demo):** `POST /v1/routes/health-aware` — a
   Rapido-style mobility or delivery app could call the same math. Shipped as part of the same
   Lambda; demoed with a curl in the film.
3. **Stage 3 — city brain (lite):** one analysis screen — road graph with
   hotspot/bottleneck nodes (articulation points / betweenness). Built only if the event stays green; otherwise a "future work" line.

## Non-goals (do NOT build before asking — Slate/Daks discipline)
- Google Maps API anything (ToS/cost).  - Voice interfaces (Transcribe/Polly).  - Auth beyond Cognito-optional-late.  - Multi-city.  - ML weather models.  - Payments/integrations with real mobility platforms.  - Celebrity-level polish before the film exists.

## The one feature that must exist end-to-end
Two routes, real dose numbers, one honest trade-off sentence, all visible in-browser with the
engine producing the numbers — everything else may be marked "future work" if the clock wins.
