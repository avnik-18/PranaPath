"""Read-only tools the AI may call (Factcade rule: tools return engine facts, nothing else)."""

TOOL_SCHEMAS = {
    "get_route_panel": {"desc": "full comparison payload (minutes, doses, tradeoff)"},
    "get_hotspots": {"desc": "segments responsible for the dose, ranked with shares"},
    "get_dose_totals": {"desc": "~ the two totals in µg and the % saving"},
}


def get_route_panel(panel):
    return panel


def get_hotspots(panel):
    return panel.get("hotspots", {})


def get_dose_totals(panel):
    a, b = panel["route_fastest"], panel["route_healthy"]
    return {
        "fastest_dose_ug": a["dose_ug"],
        "healthy_dose_ug": b["dose_ug"],
        "dose_saving_pct": panel["tradeoff"]["dose_saving_pct"],
        "time_extra_minutes": panel["tradeoff"]["time_extra_minutes"],
        "same_route": panel["tradeoff"]["same_route"],
    }


RUN_TOOLS = {
    "get_route_panel": get_route_panel,
    "get_hotspots": get_hotspots,
    "get_dose_totals": get_dose_totals,
}
