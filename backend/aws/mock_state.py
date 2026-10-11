"""Deterministic, honest mock of the deployed stack.

EVERY number here is derived from the real route panel passed in — nothing clock-based,
nothing invented (Factcade rule: mocks must be reproducible).
"""

import json

# The 14 services of docs/ARCHITECTURE.md — the deployed contract.
SERVICES = (
    ("Amplify", "hosts the web island (static)", "front"),
    ("API Gateway", "HTTPS door: /routes · /aws/*", "edge"),
    ("Lambda[engine]", "routes + dose computation", "edge"),
    ("Lambda[explainer]", "caged-AI glue, read-only", "edge"),
    ("Bedrock Nova Lite", "one sentence, validator-gated", "edge"),
    ("DynamoDB", "trip receipts + AQI snapshot", "data"),
    ("EventBridge 15-min", "AQI refresh cadence", "health"),
    ("Lambda[aqi-refresh]", "snapshot extender", "health"),
    ("EventBridge 06:00", "daily advisory trigger", "advisory"),
    ("Step Functions", "AdvisoryOrchestrator state machine", "advisory"),
    ("SNS", "best jog window email", "advisory"),
    ("CloudWatch", "structured logs + alarms", "ops"),
    ("X-Ray", "trace on every route decision", "ops"),
    ("Powertools", "Lambda observability middleware", "ops"),
)

_LIVE_MAPPED = {  # service -> probe key that actually proves it when live
    "DynamoDB": "dynamodb_ok",
    "Lambda[engine]": "lambda_ok",
    "Lambda[explainer]": "lambda_ok",
    "Bedrock Nova Lite": "bedrock_ok",
}


def service_inventory(live_state=None):
    rows = []
    probe = (live_state or {}).get("probe", {})
    for name, role, group in SERVICES:
        # honesty rule: a row may say (live) ONLY when a probe of THIS deployment proves it
        status = "GREEN (live)" if probe.get(_LIVE_MAPPED.get(name)) is True else "GREEN (mock)"
        rows.append({"service": name, "role": role, "group": group, "status": status})
    return rows


def recent_activities(route_panel, origin="rohini", dest="pitampura"):
    """Derived from the REAL payload. Latency formula (documented once):
    ms = 2.1 + 0.28 * edge_count (engine); downstream fractions of it."""
    fast, brf = route_panel["route_fastest"], route_panel["route_healthy"]
    exp = route_panel["explanation"]
    edges = len(fast.get("path", []))
    base = round(2.1 + 0.28 * edges, 1)

    def at(frac):
        return f"t+{round(base * frac, 1)}ms"

    acts = [
        {"ts": at(0.0), "service": "API Gateway", "event": "GET /routes served",
         "detail": f"{origin}->{dest} ({route_panel['mode']})"},
        {"ts": at(1.0), "service": "Lambda[engine]", "event": "routes + doses computed",
         "detail": f"fastest {fast['minutes']} min / {fast['dose_ug']} µg vs breathe-safe "
                   f"{brf['minutes']} min / {brf['dose_ug']} µg · {edges} segments"},
        {"ts": at(1.6), "service": "DynamoDB", "event": "PutItem trips",
         "detail": "1 trip row · decision receipt linked for X-Ray"},
        {"ts": at(2.4), "service": "Lambda[explainer]", "event": "explainer invoked",
         "detail": f"stats-only payload · validator {'passed' if exp['validated'] else 'FAILED'} "
                   f"· source={exp['source']}"},
        {"ts": at(3.2), "service": "Bedrock Nova Lite", "event": "sentence gated",
         "detail": f"model text must repeat engine numbers back; template fallback armed "
                   f"(used: {exp['source'] == 'template'})"},
        {"ts": at(3.8), "service": "EventBridge 15-min", "event": "aqi-refresh cadence",
         "detail": "next 15-min tick queued — 1 snapshot put"},
        {"ts": at(4.4), "service": "EventBridge 06:00", "event": "daily advisory trigger",
         "detail": "Step Functions AdvisoryOrchestrator armed for 06:00 IST"},
        {"ts": at(5.0), "service": "Step Functions", "event": "execution schedule",
         "detail": "best jog window scan overnight -> SNS publish"},
        {"ts": at(5.6), "service": "CloudWatch", "event": "structured logs",
         "detail": ""},
        {"ts": at(6.2), "service": "X-Ray", "event": "trace recorded",
         "detail": "1 service map: web -> api -> engine -> guardian"},
        {"ts": at(6.8), "service": "Powertools", "event": "middleware headers",
         "detail": "logger/metrics/tracer wired on every lambda"},
    ]
    acts[8]["detail"] = f"{len(acts)} structured events emitted · alarm set on 5xx + p99"
    return acts


_MOCK_RECEIPTS = [
    {"kind": "deploy.dry-run", "payload": {"step": "template validated offline", "charges": "₹0"}},
    {"kind": "probe.snapshot", "payload": {"services": 14, "note": "mock mode"}},
    {"kind": "engine.route", "payload": {"engine": "stdlib", "ai": "validator-gated"}},
]


def sample_receipts(live=False):
    rows = json.loads(json.dumps(_MOCK_RECEIPTS))  # deep copy keeps determinism
    for r in rows:
        r["mock"] = not live
    return rows
