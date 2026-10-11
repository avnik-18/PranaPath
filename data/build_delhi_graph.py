"""Generate data/delhi_graph.json from REAL OpenStreetMap roads (Overpass, keyless).

Corridor: Paschim Vihar / Ashok Vihar / Pitampura / Model Town demo box (Delhi).
- Every edge lies on an actual mapped road segment; minutes = length / per-class pace.
- PM bands by road class (traffic-proximity proxy, illustrative):
    high (motorway|trunk|primary)      = 260 µg/m³
    mid  (secondary|tertiary|residential|unclassified) = 150
    low  (service|living_street|pedestrian)           = 60
- 3 'hot' market-corridor edges near the Pitampura market anchor = 420 (illustrative).

Overpass mirror rotation + POST (standard form). Cache: data/osm_raw.json;
--offline reuses the cache; --debug prints body head on failure.
"""
import json
import sys
import urllib.parse
import urllib.request
import urllib.error
from collections import deque
from pathlib import Path


def OVERLOOK_GET(n):
    return (n["lat"], n["lon"])

HERE = Path(__file__).resolve().parent
RAW = HERE / "osm_raw.json"
OUT = HERE / "delhi_graph.json"

BBOX = (28.695, 77.0955, 28.725, 77.1465)          # south, west, north, east
OVERPASS_MIRRORS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://maps.mail.ru/osm/tools/overpass/api/interpreter",
]
QUERY = ('[out:json][timeout:90];(way[highway~"^(motorway|trunk|primary|secondary|'
         'tertiary|residential|unclassified|service|living_street|pedestrian)$"]'
         '(%s,%s,%s,%s););(._;>;);out skel;' % BBOX)

CLASS_PM = {
    "motorway": 260, "trunk": 260, "primary": 260,
    "secondary": 150, "tertiary": 150, "residential": 150, "unclassified": 150,
    "service": 60, "living_street": 60, "pedestrian": 60,
}
PACE_M_PER_MIN = {
    "motorway": 560, "trunk": 500, "primary": 430,
    "secondary": 330, "tertiary": 260, "residential": 210,
    "unclassified": 210, "service": 170, "living_street": 150, "pedestrian": 150,
}

ANCHORS = {
    "rohini": (28.7035, 77.1020),
    "ashok_vihar": (28.7055, 77.1130),
    "pitampura": (28.6975, 77.1400),
    "model_town": (28.7050, 77.1330),
}
MARKET_ANCHOR = (28.7005, 77.1215)      # mid-corridor market block (Rani Bagh side)
HOT_COUNT = 3

OVERLOOK = {}          # node id -> (lat, lon), filled by _fill_overlook


def fetch_osm(force=True, debug=False):
    if not force and RAW.exists():
        print(f"[osm] using cache {RAW.name} ({RAW.stat().st_size} bytes)")
        return json.loads(RAW.read_text(encoding="utf-8"))

    body = urllib.parse.urlencode({"data": QUERY}).encode()
    last = None
    for mirror in OVERPASS_MIRRORS:
        req = urllib.request.Request(mirror, data=body, headers={"User-Agent": "ecoroute-demo/0.1"})
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                text = r.read()
            RAW.write_bytes(text)
            print(f"[osm] fetched via {mirror} ({len(text)} bytes)")
            return json.loads(text.decode("utf-8"))
        except urllib.error.HTTPError as e:
            last = e
            if debug:
                print(f"[osm] {mirror} -> HTTP {e.code}: {e.read()[:400]!r}")
            else:
                print(f"[osm] {mirror} -> HTTP {e.code}; trying next mirror")
        except Exception as e:
            last = e
            print(f"[osm] {mirror} -> {e}; trying next mirror")
    raise SystemExit(f"[osm] all mirrors failed: {last}")


def build(force=False, debug=False):
    osm = fetch_osm(force=force, debug=debug)
    nodes, edges = {}, []
    osm_nodes = {}
    for el in osm.get("elements", []):
        if el.get("type") == "node":
            osm_nodes[el["id"]] = (el["lat"], el["lon"])

    used = set()
    for el in osm.get("elements", []):
        if el.get("type") != "way":
            continue
        tags = el.get("tags", {}) or {}
        hwy = tags.get("highway", "unclassified")
        pace = PACE_M_PER_MIN.get(hwy, 210)
        pm = float(CLASS_PM.get(hwy, 150))
        refs = [r for r in el.get("nodes", []) if r in osm_nodes]
        for a, b in zip(refs, refs[1:]):
            if a == b:
                continue
            key = (min(a, b), max(a, b))
            if key in used:
                continue
            used.add(key)
            (la, lo), (lb, lo2) = osm_nodes[a], osm_nodes[b]
            length = _meters(la, lo, lb, lo2)
            if length < 12:
                continue
            for nid, (lat, lon) in ((a, (la, lo)), (b, (lb, lo2))):
                nodes.setdefault(f"N{nid}", {"lat": lat, "lon": lon, "name": f"N{nid}"})
            minutes = round(length / pace, 2)
            edges.append({"id": f"N{a}-N{b}", "u": f"N{a}", "v": f"N{b}",
                          "minutes": minutes, "length_m": int(length),
                          "pm25_ug_m3": pm, "cls": hwy})

    # ---- SNAP OSM ways that did not share node ids: union-find on rounded coords ----
    parent = {}
    for nid in nodes:
        parent[nid] = nid

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    buckets = {}
    for nid in nodes:                          # ~11 m buckets (4-decimal lat/lon)
        ld, lon = OVERLOOK_GET(nodes[nid])
        buckets.setdefault((round(ld, 4), round(lon, 4)), []).append(nid)
    for ids in buckets.values():
        for other in ids[1:]:
            union(ids[0], other)

    rep_edges, seen_kept = [], set()
    for e in edges:
        u2, v2 = find(e["u"]), find(e["v"])
        if u2 == v2:
            continue
        k2 = (u2, v2) if u2 < v2 else (v2, u2)
        if k2 in seen_kept:
            continue
        seen_kept.add(k2)
        rep_edges.append({**e, "u": u2, "v": v2, "id": f"{u2}-{v2}"})

    # cluster coordinates = midpoint of members (nearest 5-decimal)
    coords = {}
    for nid, n in nodes.items():
        coords.setdefault(find(nid), []).append((n["lat"], n["lon"]))
    s_nodes = {rid: {"lat": round(sum(p[0] for p in m) / len(m), 5),
                     "lon": round(sum(p[1] for p in m) / len(m), 5),
                     "name": rid}
               for rid, m in coords.items()}

    # ---- keep ONLY the largest connected component (topologically honest cut) ----
    adj = {}
    for e in rep_edges:
        adj.setdefault(e["u"], []).append(e["v"])
        adj.setdefault(e["v"], []).append(e["u"])
    seen, comps = set(), []
    for st in s_nodes:
        if st in seen:
            continue
        q, comp = [st], []
        seen.add(st)
        while q:
            cur = q.pop()
            comp.append(cur)
            for nxt in adj.get(cur, []):
                if nxt not in seen:
                    seen.add(nxt)
                    q.append(nxt)
        comps.append((len(comp), st))
    comps.sort(reverse=True)
    keep = set()
    q = deque([comps[0][1]])
    seen2 = {comps[0][1]}
    while q:
        cur = q.pop()
        keep.add(cur)
        for nxt in adj.get(cur, []):
            if nxt not in seen2:
                seen2.add(nxt)
                q.append(nxt)

    s_nodes = {k: v for k, v in s_nodes.items() if k in keep}
    s_edges = [e for e in rep_edges if e["u"] in keep and e["v"] in keep]

    # ---- pin landmarks to nearest junctions (inside the kept component) ----
    _fill_overlook(s_nodes)
    for name, (lat, lon) in ANCHORS.items():
        nid = _nearest_node(lat, lon)
        s_nodes[nid]["name"] = name

    ranked = _midroute_hot_edges(s_nodes, s_edges, "rohini", "pitampura", HOT_COUNT)
    for e in ranked:
        e["pm25_ug_m3"] = 420.0
        e["hotspot"] = True

    return {
        "_meta": {
            "source": "OpenStreetMap ways via Overpass (bbox %s); PM bands by road class; largest connected component" % (BBOX,),
            "generated_utc": "2026-10-11T07:30:00Z",
            "note": "illustrative",
            "hot_anchor": MARKET_ANCHOR,
            "components_dropped": len(comps) - 1,
        },
        "corridor": "Paschim Vihar - Ashok Vihar - Pitampura - Model Town (real OSM cut)",
        "nodes": s_nodes,
        "edges": s_edges,
    }


def _fill_overlook(nodes):
    for nid, n in nodes.items():
        OVERLOOK[nid] = (n["lat"], n["lon"])


def _mid(e):
    a, b = OVERLOOK[e["u"]], OVERLOOK[e["v"]]
    return ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)


def _midroute_hot_edges(s_nodes, s_edges, from_name, to_name, count):
    """Pick the middle `count` road segments of the rohini->pitampura fastest street —
    the market corridor through which the fastest route naturally rides."""
    adj = {}
    for e in s_edges:
        adj.setdefault(e["u"], []).append((e["v"], e))
        adj.setdefault(e["v"], []).append((e["u"], e))
    def _as_key(name):
        if name in s_nodes:
            return name
        hit = next((nid for nid, n in s_nodes.items() if n.get("name") == name), None)
        if hit is None:
            raise KeyError(f"landmark {name!r} not pinned")
        return hit

    source = _as_key(from_name)
    goal = _as_key(to_name)

    import heapq
    best, prev = {source: 0.0}, {}
    heap = [(0.0, source)]
    while heap:
        cand, cur = heapq.heappop(heap)
        if cand > best.get(cur, float("inf")):
            continue
        if cur == goal:
            break
        for nxt, e in adj.get(cur, []):
            nd = cand + e["minutes"]
            if nd < best.get(nxt, float("inf")):
                best[nxt] = nd
                prev[nxt] = (cur, e)
                heapq.heappush(heap, (nd, nxt))
    chain, cur = [], goal
    while cur in prev:
        before, e = prev[cur]
        chain.append(e)
        cur = before
    chain.reverse()
    if not chain:
        return []
    lo = (len(chain) - count) // 2
    return chain[max(lo, 0):lo + count]


def _nearest_node(lat, lon):
    best, bd = None, 1e18
    for nid, (la, lo) in OVERLOOK.items():
        d = _meters(lat, lon, la, lo)
        if d < bd:
            bd, best = d, nid
    return best


def _meters(la1, lo1, la2, lo2):
    import math
    dy = (la2 - la1) * 111000
    dx = (lo2 - lo1) * 111000 * math.cos(math.radians(la1))
    return math.hypot(dx, dy)


if __name__ == "__main__":
    offline = "--offline" in sys.argv
    debug = "--debug" in sys.argv
    g = build(force=not offline, debug=debug)
    OUT.write_text(json.dumps(g, indent=1), encoding="utf-8")
    kinds = sum(1 for e in g["edges"] if e.get("hotspot"))
    filesz = OUT.stat().st_size // 1024
    print(f"wrote {OUT.name}: {len(g['nodes'])} junctions, {len(g['edges'])} road segments, "
          f"{kinds} market-hot edges, {filesz} KB")
