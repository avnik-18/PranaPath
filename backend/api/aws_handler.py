"""Thin door for the ops panel: parse -> backend.aws -> schema. NO logic lives here."""

from backend.api import handler as hp
from backend.api.aws_schemas import (
    AWS_API_VERSION,
    aws_error,
    aws_panel_response,
    aws_status_response,
)
from backend.aws import client as aws_client
from backend.aws import panel as aws_panel


def handle_aws_status():
    """GET /aws/status — availability picture (mock when no credentials)."""
    return aws_status_response(aws_client.aws_state())


def handle_aws_panel(origin="ashok_vihar", dest="pitampura", mode="jog"):
    """GET /aws/panel — deterministic ops view for one REAL trip."""
    route_payload = hp.handle_routes(origin, dest, mode)
    if not route_payload.get("ok"):
        err = route_payload.get("error", {})
        return aws_error(err.get("code", "unknown_node"), err.get("message", "routes failed"))
    view = aws_panel.build_panel(
        route_payload, live_state=aws_client.aws_state(), origin=origin, dest=dest,
    )
    view["trip"] = {"origin": origin, "dest": dest, "mode": mode}
    view["trip_minutes"] = route_payload["route_fastest"]["minutes"]
    view["dose_fastest_ug"] = route_payload["route_fastest"]["dose_ug"]
    view["dose_breathe_safe_ug"] = route_payload["route_healthy"]["dose_ug"]
    return aws_panel_response(view)


if __name__ == "__main__":  # pragma: no cover — quick local smoke
    import json
    print(json.dumps(handle_aws_status(), indent=1)[:400])
    print("aws_api_version:", AWS_API_VERSION)
