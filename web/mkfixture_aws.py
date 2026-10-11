"""Bake web/public/fixture-aws-panel.json from the REAL aws handler (offline judges see truth)."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from backend.api import aws_handler as ah  # noqa: E402

payload = ah.handle_aws_panel("ashok_vihar", "pitampura", "jog")
assert payload.get("ok"), payload
out = ROOT / "web" / "public" / "fixture-aws-panel.json"
out.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"fixture-aws-panel.json written ({out.stat().st_size // 1024} KB)")
