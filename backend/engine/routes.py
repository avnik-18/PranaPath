"""Two-route comparison: fastest by minutes vs healthy by dose-weighted cost.

Objective A: minimize travel minutes        (speed)
Objective B: minimize harm-minutes          (dose proxy: minutes × pm25/150)
Dijkstra on undirected adjacency; mode scaling: walk/jog/cycle pace factors.
Never consults an AI; deterministic for identical inputs.
"""

PACE = {"walk": 1.25, "jog": 0.9, "cycle": 0.7}   # minutes multiplier per mode
PM_REFERENCE = 150.0                              # µg/m³ 'city-day neutral'
HEALTH_SENSITIVITY = 10.0                         # health-cost weight × (pm25/reference)
DEFAULT_BUDGET = 1.35                             # 'breathe-safe' = cleanest within +35% time


def compare_routes(g, origin, dest, mode, budget=None):
    o = _resolve_or_raise(g, origin)
    d = _resolve_or_raise(g, dest)
    scale = PACE.get(mode) or (lambda: (_ for _ in ()).throw(ValueError(f"mode {mode!r}")))()

    a = _search(g, o, d, scale=scale, use_health=False)
    b = _budgeted(g, o, d, scale, a["minutes"], budget, mode)
    if a is None:
        return {"ok": False, "error": f"unreachable: {origin} -> {dest}"}

    from . import exposure
    total_a, per_a = exposure.dose_on_edges(a["edges"], mode)
    total_b, per_b = exposure.dose_on_edges(b["edges"], mode)

    panel = {
        "ok": True,
        "mode": mode,
        "origin": o,
        "destination": d,
        "route_fastest": _shape_route(g, "A", a, total_a, per_a),
        "route_healthy": _shape_route(g, "B", b, total_b, per_b),
        "tradeoff": {},
    }
    extra_min = round(b["minutes"] - a["minutes"], 1)
    same = a["path"] == b["path"]
    saving_pct = round(100.0 * (total_a - total_b) / total_a, 1) if (total_a > 0 and not same) else 0.0
    panel["tradeoff"] = {
        "time_extra_minutes": extra_min,
        "dose_saving_pct": max(saving_pct, 0.0),
        "same_route": same,
    }
    panel["hotspots"] = {
        "fastest": exposure.hotspots(per_a, a["edges"]),
        "healthy": exposure.hotspots(per_b, b["edges"]),
    }
    panel["smog"] = self_smog(g, panel, a["edges"] + b["edges"])
    return panel


def self_smog(g, panel, route_edges):
    """The full-area 50 m blob field + street puffs the map paints (engine-owned)."""
    from . import smog as sm
    pts = []
    for rid in ("route_fastest", "route_healthy"):
        pts += _pts(g, panel[rid]["path"])
    baseline = sum(e["pm25_ug_m3"] for e in route_edges) / max(len(route_edges), 1)
    hot = sorted({e["id"]: e for e in route_edges}.values(), key=lambda e: -e["pm25_ug_m3"])
    panel["puffs"] = sm.build_puffs(_hot_points(g, hot[:6]))
    sources = g.get("sources", [])
    return sm.find_field(pts, sources, baseline)


def _budgeted(g, o, d, scale, fastest_min, budget, mode):
    """'breathe-safe' = the real-dose-minimising route whose minutes ≤ budget×fastest."""
    value = DEFAULT_BUDGET if not budget or budget <= 0 else budget
    from .constrained import search_with_cap
    from .exposure import IR_M3H
    r = search_with_cap(g, o, d, scale, cap_min=fastest_min * value + 0.25,
                        health_w=HEALTH_SENSITIVITY, pm_ref=PM_REFERENCE, ir=IR_M3H.get(mode, 3.0))
    if r is None:                        # cap unreachable (cap too tight) → health search
        return _search(g, o, d, scale=scale, use_health=True)
    r["via"] = _via_names(g, r["path"])
    return r


def _pts(g, ids):
    n = g["nodes"]
    return [{"lat": n[i]["lat"], "lon": n[i]["lon"]} for i in set(ids)]


def _hot_points(g, edges):
    pts = []
    for e in edges:
        u, v = e["id"].split("-")
        a2, b2 = g["nodes"][u], g["nodes"][v]
        pts.append({
            "id": e["id"],
            "lat": (a2["lat"] + b2["lat"]) / 2,
            "lon": (a2["lon"] + b2["lon"]) / 2,
            "pm25": e["pm25_ug_m3"],
        })
    return pts


# ---------- internals ----------

def _resolve_or_raise(g, name):
    from . import graph as gg
    return gg.resolve_node(g, name)


def _search(g, start, goal, scale, use_health):
    import heapq
    adj = g["adj"]
    best = {start: 0.0}
    prev = {}
    heap = [(0.0, start)]
    while heap:
        pend, node = heapq.heappop(heap)
        if pend > best.get(node, float("inf")):
            continue
        if node == goal:
            return _reconstruct(g, prev, goal, scale)
        for nxt, edge in adj.get(node, []):
            m = edge["minutes"] * scale
            cost = m if not use_health else m * (1.0 + HEALTH_SENSITIVITY * (edge["pm25_ug_m3"] / PM_REFERENCE))
            nd = pend + cost
            if nd < best.get(nxt, float("inf")):
                best[nxt] = nd
                prev[nxt] = (node, edge)
                heapq.heappush(heap, (nd, nxt))
    return None


def _reconstruct(g, prev, goal, _scale):
    path, edges = [goal], []
    cur = goal
    while cur in prev:
        before, edge = prev[cur]
        edges.append(edge)
        path.append(before)
        cur = before
    path.reverse()
    edges.reverse()
    minutes = round(sum(e["minutes"] for e in edges), 1)
    return {
        "path": path,
        "edges": edges,
        "minutes": minutes,          # bus-waitless, mode-scaled at call site
        "via": _via_names(g, path),
    }


def _via_names(g, path):
    names = []
    for nid in path:
        n = g["nodes"][nid]
        if n.get("name", nid) != nid:
            names.append(n["name"])
    return names


def _shape_route(g, rid, found, total_ug, per):
    return {
        "route_id": rid,
        "path": found["path"],
        "via": found["via"],
        "minutes": found["minutes"],
        "km": _path_km(g, found["path"]),
        "dose_ug": round(total_ug, 1),
        "dose_per_edge": {k: round(v, 2) for k, v in per.items()},
    }


def _path_km(g, ids):
    """Haversine-free flat-earth distance over the ordered path (demo scale)."""
    from .smog import KM_PER_DEG_LAT
    from math import cos, radians, sqrt
    if len(ids) < 2:
        return 0.0
    km_lon = KM_PER_DEG_LAT * max(cos(radians(g["nodes"][ids[0]]["lat"])), 0.25)
    total = 0.0
    for u, v in zip(ids, ids[1:]):
        a2, b2 = g["nodes"][u], g["nodes"][v]
        dx = (b2["lon"] - a2["lon"]) * km_lon
        dy = (b2["lat"] - a2["lat"]) * KM_PER_DEG_LAT
        total += sqrt(dx * dx + dy * dy)
    return round(total, 1)
