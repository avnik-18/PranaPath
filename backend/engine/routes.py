"""Two-route comparison: fastest by minutes vs healthy by dose-weighted cost.

Objective A: minimize travel minutes        (speed)
Objective B: minimize harm-minutes          (dose proxy: minutes × pm25/150)
Dijkstra on undirected adjacency; mode scaling: walk/jog/cycle pace factors.
Never consults an AI; deterministic for identical inputs.
"""

PACE = {"walk": 1.25, "jog": 0.9, "cycle": 0.7}   # minutes multiplier per mode
PM_REFERENCE = 150.0                              # µg/m³ 'city-day neutral'
HEALTH_SENSITIVITY = 4.0                          # health-cost weight × (pm25/reference)


def compare_routes(g, origin, dest, mode):
    o = _resolve_or_raise(g, origin)
    d = _resolve_or_raise(g, dest)
    scale = PACE.get(mode) or (lambda: (_ for _ in ()).throw(ValueError(f"mode {mode!r}")))()

    a = _search(g, o, d, scale=scale, use_health=False)
    b = _search(g, o, d, scale=scale, use_health=True)
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
    return panel


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
        "dose_ug": round(total_ug, 1),
        "dose_per_edge": {k: round(v, 2) for k, v in per.items()},
    }


def _pct_down(fast, healthy):
    if fast <= 0:
        return 0.0
    p = 100.0 * (1 - _safe(fast, healthy))
    return round(p, 1)


def _safe(fast, healthy):
    ratio = healthy / fast
    return 1.0 - ratio if ratio <= 1.0 else 0.0
