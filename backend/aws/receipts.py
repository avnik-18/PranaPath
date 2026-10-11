"""Append-only runtime receipts: every AWS-side action leaves one redacted JSON line."""

import json
import os
from datetime import datetime, timezone

RECEIPTS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "data", "receipts",
)

_SECRET_SUFFIXES = ("key", "token", "secret")


def _redact(payload):
    """Drop secrets to *** before they ever touch disk (flat or nested dicts)."""
    out = {}
    for key, value in payload.items():
        lower = key.lower()
        if any(lower.endswith(suf) for suf in _SECRET_SUFFIXES):
            out[key] = "***"
        elif isinstance(value, dict):
            out[key] = _redact(value)
        else:
            out[key] = value
    return out


def record(kind, payload):
    """Append one {ts, kind, payload} line to data/receipts/<yyyymmdd>.ndjson."""
    line = json.dumps({
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "kind": kind,
        "payload": _redact(payload),
    }, ensure_ascii=False)
    try:
        os.makedirs(RECEIPTS_DIR, exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%d")
        with open(os.path.join(RECEIPTS_DIR, f"{stamp}.ndjson"), "a", encoding="utf-8") as fh:
            fh.write(line + "\n")
        return True
    except OSError:
        return False


def tail(n=5):
    """Last n receipt dicts (newest file, newest lines), [] when nothing present."""
    try:
        files = sorted(f for f in os.listdir(RECEIPTS_DIR) if f.endswith(".ndjson"))
        if not files:
            return []
        with open(os.path.join(RECEIPTS_DIR, files[-1]), encoding="utf-8") as fh:
            lines = fh.read().strip().splitlines()
        return [json.loads(x) for x in lines[-n:]]
    except (OSError, ValueError):
        return []
