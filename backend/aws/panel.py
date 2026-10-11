"""One honest ops-panel payload: inventory + activities + receipts, MOCK-labeled unless live."""

import json

from backend.aws import mock_state, receipts


def build_panel(route_panel, live_state=None, origin="rohini", dest="pitampura"):
    """Merge deterministic mock state with a live probe picture (None = mock)."""
    live_mode = bool(live_state and live_state.get("mode") == "live")
    acts = mock_state.recent_activities(route_panel, origin=origin, dest=dest)
    for a in acts:
        a["mock"] = not live_mode

    inventory = mock_state.service_inventory(live_state if live_mode else None)
    rcpts = receipts.tail(5) if live_mode else mock_state.sample_receipts()
    green_live = sum(1 for row in inventory if row["status"] == "GREEN (live)")

    return {
        "switch": "live" if live_mode else "mock",
        "mode": live_state.get("mode") if live_mode else "mock",
        "region": ((live_state or {}).get("region")) or "ap-south-1",
        "probe": (live_state or {}).get("probe") or {"dynamodb_ok": None, "lambda_ok": None, "bedrock_ok": None},
        "reason": ("" if live_mode else "no team AWS credentials in .env yet — everything below is a "
                                        "deterministic mock, every number traceable to the real panel")
                  or (live_state or {}).get("reason", ""),
        "inventory": inventory,
        "activities": acts,
        "receipts": rcpts,
        "counts": {
            "services": len(inventory),
            "green_live": green_live,
            "green_mock": len(inventory) - green_live,
            "events": len(acts),
            "receipts": len(rcpts),
        },
    }


def counts_summary(panel_payload):
    """Mirror of counts for tests/logging (no recompute in callers)."""
    return json.dumps(panel_payload.get("counts", {}), sort_keys=True)
