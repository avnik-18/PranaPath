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

out = Path(__file__).with_name('public')
out.mkdir(exist_ok=True)
for trip, t in sorted(TRIPS.items()):
    for mode in MODES:
        payload = hp.handle_routes(t["origin"], t["dest"], mode)
        if not payload.get("ok"):
            raise SystemExit(f"trip {trip} → {t['origin']},{t['dest']},{mode}: {payload.get('error')}")
        path = out / f'fixture-{trip}-{mode}.json'
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding='utf-8')
        st = payload['tradeoff']
        print(f"{path.name}: {payload['route_fastest']['km']} km {payload['route_fastest']['minutes']} min "
              f"trade +{st['time_extra_minutes']}/-{st['dose_saving_pct']}%")
