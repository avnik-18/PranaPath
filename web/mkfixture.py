"""Write the web demo-bundle fixtures (fixture-{trip}-{mode}.json) from REAL handlers.

python3-web-data generator: uses the SAME production code path as the AW deployment.
fixture-panel.json is NOT touched here — the film bake (frames/mk_beats.py) owns it.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from backend.api import handler as hp  # noqa: E402
from backend.api.trips import TRIPS    # noqa: E402

MODES = ("jog", "cycle", "walk")
BUDGETS = (("any", None), ("1.05", 1.05), ("1.1", 1.1))   # cap = budget × fastest

out = Path(__file__).with_name('public')
out.mkdir(exist_ok=True)
for trip, t in sorted(TRIPS.items()):
    for mode in MODES:
        for bname, bval in BUDGETS:
            payload = hp.handle_routes(t["origin"], t["dest"], mode, budget=bval)
            if not payload.get("ok"):
                raise SystemExit(f"trip {trip} → {t['origin']},{t['dest']},{mode}: {payload.get('error')}")
            suffix = "" if bname == "any" else f"-b{bname}"
            path = out / f'fixture-{trip}-{mode}{suffix}.json'
            path.write_text(json.dumps(payload, separators=(',', ':')), encoding='utf-8')
            st = payload['tradeoff']
            smog_rings = sum(band["count"] for band in payload["ui"]["smog"])
            print(f"{path.name}: {payload['route_fastest']['km']} km "
                  f"B {payload['route_healthy']['minutes']} min {payload['route_healthy']['dose_ug']}µg "
                  f"cap {bname} · rings {smog_rings}")
