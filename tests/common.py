"""Shared fixtures for offline tests: load graph once, build a canonical panel once."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def graph():
    from backend.engine import graph as gy
    return gy.load_graph(str(ROOT / "data" / "delhi_graph.json"))


def panel(origin="ashok_vihar", dest="pitampura", mode="jog"):
    from backend.engine.routes import compare_routes
    return compare_routes(graph(), origin, dest, mode)
