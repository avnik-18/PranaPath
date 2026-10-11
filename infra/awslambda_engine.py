"""Deploy-zip Lambda entry: forward to backend.api handlers. Ring 4 stays thin."""
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from backend.api.handler import handle_routes, handle_state  # noqa: E402

_CORS = {"Access-Control-Allow-Origin": "*"}


def handler(event, context):
    qs = event.get("queryStringParameters") or {}
    raw = event.get("rawPath") or event.get("path") or "/routes"
    if raw.startswith("/aws/status"):
        from backend.api.aws_handler import handle_aws_status
        payload = handle_aws_status()
    elif raw.startswith("/aws/panel"):
        from backend.api.aws_handler import handle_aws_panel
        payload = handle_aws_panel(
            qs.get("origin", "ashok_vihar"),
            qs.get("dest", "pitampura"),
            qs.get("mode", "jog"),
        )
    elif raw.startswith("/state"):
        payload = handle_state()
    else:
        payload = handle_routes(
            qs.get("origin", "ashok_vihar"),
            qs.get("dest", "pitampura"),
            qs.get("mode", "jog"),
            trip=qs.get("trip"),
            budget=qs.get("budget"),
            city=qs.get("city"),
        )
    return {
        "statusCode": 200 if payload.get("ok") else 400,
        "headers": _CORS,
        "body": json.dumps(payload, ensure_ascii=False),
    }
