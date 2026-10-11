"""The CONTRACT: request/response shapes shared with web/src/types.ts (additive only)."""

API_VERSION = "v1"
MODES = ("walk", "jog", "cycle")


def routes_response(panel, explanation):
    """Shape of GET /routes and POST /v1/routes/health-aware payloads."""
    return {
        "ok": True,
        "api_version": API_VERSION,
        "mode": panel["mode"],
        "route_fastest": panel["route_fastest"],
        "route_healthy": panel["route_healthy"],
        "tradeoff": panel["tradeoff"],
        "hotspots": panel["hotspots"],
        "explanation": explanation,           # {sentence, source, validated}
        "ui": {"map_nodes": panel["path_nodes"], "smog": panel.get("smog", []), "puffs": panel.get("puffs", [])},
    }


def error_response(code, message):
    return {"ok": False, "api_version": API_VERSION, "error": {"code": code, "message": message}}
