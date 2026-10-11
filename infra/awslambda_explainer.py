"""Deploy-zip Lambda entry for the caged explainer: stats in, one gated sentence out."""
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from backend.guardian.explain import explain_route  # noqa: E402

_CORS = {"Access-Control-Allow-Origin": "*"}


def handler(event, context):
    try:
        body = json.loads(event.get("body") or "{}")
    except ValueError:
        body = {}
    out = explain_route(body.get("panel", body), use_ai=True)
    return {
        "statusCode": 200,
        "headers": _CORS,
        "body": json.dumps(out, ensure_ascii=False),
    }
