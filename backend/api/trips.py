"""Named demo trips: three hand-picked corridors on real roads, by length.

Each pair has a real trade (same_route=False) so any trip tells the story:
short pays +0.12 min for −9.1% dose, long +0.15 min for −5.3%.
"""

TRIPS = {
    "short": {"origin": "ashok_vihar", "dest": "model_town", "km": 3.1},
    "medium": {"origin": "ashok_vihar", "dest": "pitampura", "km": 4.0},
    "long": {"origin": "rohini", "dest": "pitampura", "km": 5.7},
}
DEFAULT_TRIP = "short"


def resolve(trip):
    """trip name -> {key, origin, dest, km}; unknown names fall back to short."""
    key = DEFAULT_TRIP if trip not in TRIPS else trip
    t = TRIPS[key]
    return {"key": key, "origin": t["origin"], "dest": t["dest"], "km": t["km"]}
