"""Named demo trips per city: hand-picked real-road corridors, by length.

Each pair has a real trade (same_route=False) so any trip tells the story.
The km figures are the engine's route length — measured, not estimated.
"""

TRIPS = {
    "delhi": {
        "short": {"origin": "ashok_vihar", "dest": "model_town", "km": 3.1},
        "medium": {"origin": "ashok_vihar", "dest": "pitampura", "km": 4.0},
        "long": {"origin": "rohini", "dest": "pitampura", "km": 5.7},
    },
    "blr": {
        "short": {"origin": "koramangala", "dest": "indiranagar", "km": 4.8},
        "medium": {"origin": "indiranagar", "dest": "koramangala", "km": 4.8},
        "long": {"origin": "jayanagar", "dest": "indiranagar", "km": 4.5},
    },
}
DEFAULT_TRIP = "short"


def resolve(trip, city="delhi"):
    """trip name -> {key, origin, dest, km} for a city; unknown falls back to short."""
    table = TRIPS.get(city, TRIPS["delhi"])
    key = DEFAULT_TRIP if trip not in table else trip
    t = table[key]
    return {"key": key, "origin": t["origin"], "dest": t["dest"], "km": t["km"]}
