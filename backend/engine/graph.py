"""Load the corridor graph from data/ and expose plain lookup helpers.

Pure stdlib, no side effects beyond reading JSON.
"""


def load_graph(path):
    data = _read(path)
    return {
        "nodes": data["nodes"],
        "edges": data["edges"],
        "meta": data["_meta"],
        # undirected adjacency: node -> list[(neighbor_id, edge)]
        "adj": _adjacency(data["edges"]),
        "by_name": {n["name"]: nid for nid, n in data["nodes"].items()},
        "campus": {nid for nid, n in data["nodes"].items() if n.get("campus")},
    }


def resolve_node(g, value):
    """Accept a landmark name ('pitampura') or a node id ('N1825166887')."""
    if value in g["nodes"]:
        return value
    low = str(value).strip().lower().replace(" ", "_")
    if low in g["by_name"]:
        return g["by_name"][low]
    raise KeyError(f"unknown node or landmark: {value!r}")


def landmark_names(g):
    return [n["name"] for nid, n in g["nodes"].items() if n.get("name", nid) != nid]


def _read(path):
    import json
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _adjacency(edges):
    adj = {}
    for e in edges:
        adj.setdefault(e["u"], []).append((e["v"], e))
        adj.setdefault(e["v"], []).append((e["u"], e))
    return adj
