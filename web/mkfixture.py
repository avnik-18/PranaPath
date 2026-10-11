"""Write web/public/fixture-panel.json (the offline demo bundle) from the real handlers.

python3-web-data generator: uses the SAME production code path as the AW deployment.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from backend.api import handler as hp  # noqa: E402

TRIP = ('rohini', 'pitampura', 'jog')          # flagship pair for the film

out = Path(__file__).with_name('public')
out.mkdir(exist_ok=True)
payload = hp.handle_routes(*TRIP)
path = out / 'fixture-panel.json'
path.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding='utf-8')
stat = payload['tradeoff']
print(f"wrote {path.name}: trip={TRIP} tradeoff={stat['time_extra_minutes']}min / {stat['dose_saving_pct']}%")
