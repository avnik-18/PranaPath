"""Pure handlers: params -> dict payload. Adapters (local_server.py, Lambda) wrap these.

Glue only — no engine math, no AI calls beyond delegating to guardian.
"""

from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]


_GRAPHS = {}

def _graph(city=None):
    key = _city(city)
    if key not in _GRAPHS:
        from ..engine import graph as gy
        _GRAPHS[key] = gy.load_graph(str(_ROOT / "data" / f"{key}_graph.json"))
    return _GRAPHS[key]


def _city(raw):
    """'blr' → 'blr'; anything else stays on delhi."""
    return raw if raw in ("blr", "delhi") else "delhi"


def handle_routes(origin, dest, mode, trip=None, budget=None, city=None):
    from .schemas import routes_response, error_response

    key = _city(city)
    if trip:
        from .trips import resolve
        r = resolve(trip, key)
        origin, dest = r["origin"], r["dest"]
    try:
        panel = _routes().compare_routes(_graph(key), origin, dest, mode, budget=_budget(budget))
    except KeyError as exc:                      # unknown node/landmark -> clean 400, not 500
        return error_response("unknown_node", str(exc))
    if not panel.get("ok"):
        return error_response("unreachable", panel.get("error", ""))

    panel["path_nodes"] = shaped_nodes(panel, _graph(key))
    explanation = _explain().explain_route(panel)
    return routes_response(panel, explanation)


def handle_state():
    return {
        "ok": True,
        "api_version": "v1",
        "service": "ecoroute-engine",
        "fixtures_present": {
            "delhi_graph": (_ROOT / "data" / "delhi_graph.json").exists(),
            "aqi_snapshot": (_ROOT / "data" / "aqi_snapshot.json").exists(),
        },
    }


def _budget(raw):
    """'1.1' → 1.1; 'none'/'any'/'' → None (unconstrained). Anything else → None."""
    if raw in (None, "", "any", "none"):
        return None
    try:
        return float(raw)
    except (TypeError, ValueError):
        return None


def shaped_nodes(panel, g):
    """Deduped route corridors (A ∪ B) for the map, lat/lon + names from the graph."""
    seen, out = set(), []
    for nid in panel["route_fastest"]["path"] + panel["route_healthy"]["path"]:
        if nid not in seen:
            seen.add(nid)
            n = g["nodes"][nid]
            out.append({"id": nid, "name": n["name"], "lat": n["lat"], "lon": n["lon"]})
    return out


def _routes():
    from ..engine import routes as rr
    return rr


def _explain():
    from ..guardian import explain as ex
    return ex
