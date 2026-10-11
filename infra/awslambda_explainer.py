"""Deploy-zip Lambda entry for the caged explainer: stats in, one gated sentence out."""
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from backend.guardian.explain import explain_route  # noqa: E402

try:                                    # AWS OSS card: Powertools for AWS (Lambda)
    from aws_lambda_powertools import Logger
    _log = Logger(service="ecoroute-explainer")
except ImportError:                     # offline builds — the deploy layer provides it
    class _FallbackLog:
        def info(self, msg, **kw):
            print("[ecoroute-explainer] " + msg)
    _log = _FallbackLog()

_CORS = {"Access-Control-Allow-Origin": "*"}


def handler(event, context):
    try:
        body = json.loads(event.get("body") or "{}")
    except ValueError:
        body = {}
    out = explain_route(body.get("panel", body), use_ai=True)
    _log.info("explained", extra={"source": out.get("source"), "validated": out.get("validated")})
    return {
        "statusCode": 200,
        "headers": _CORS,
        "body": json.dumps(out, ensure_ascii=False),
    }
