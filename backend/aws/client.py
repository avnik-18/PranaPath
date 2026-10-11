"""AWS access through env credentials ONLY. Every failure is soft (None), never a crash."""

import os

_factory = None  # tests inject here: _factory(kind, name) -> fake client; None = real boto3


def region():
    return os.environ.get("AWS_REGION", "ap-south-1")


def has_creds():
    if os.environ.get("AWS_ACCESS_KEY_ID") and os.environ.get("AWS_SECRET_ACCESS_KEY"):
        return True
    return bool(os.environ.get("AWS_PROFILE"))


def mode():
    """live|mock — auto resolves to live iff credentials exist."""
    want = os.environ.get("ECOROUTE_AWS_MODE", "auto")
    if want in ("live", "mock"):
        return want
    return "live" if has_creds() else "mock"


def _boto(name):
    if _factory is not None:
        return _factory(name)
    import boto3
    return boto3.client(name, region_name=region())


_PROBES = (
    ("dynamodb_ok", "dynamodb", "list_tables"),
    ("lambda_ok", "lambda", "list_functions"),
    ("bedrock_ok", "bedrock", "list_foundation_models"),
)


def _probe(client, method):
    try:
        if client is None:
            return None
        getattr(client, method)()
        return True
    except Exception:  # noqa: BLE001 — any failure is availability, per house rule
        return False


def aws_state():
    """Availability picture for the ops console; probes None in mock, attempted in live."""
    if not has_creds() or mode() == "mock":
        return {
            "mode": "mock",
            "region": region(),
            "probe": {"dynamodb_ok": None, "lambda_ok": None, "bedrock_ok": None},
            "reason": "no AWS credentials in the environment — copy .env.example to .env "
                      "and add the team account keys to go live",
        }
    probe, reasons = {}, []
    for key, service, method in _PROBES:
        try:
            result = _probe(_boto(service), method)
        except Exception as exc:  # client construction itself failed (e.g. boto3 missing)
            result, reasons = False, reasons + [f"{service}: {exc}"]
            probe[key] = result
            continue
        probe[key] = result
        if result is False:
            reasons.append(f"{service}: probe failed")
    return {
        "mode": "live",
        "region": region(),
        "probe": probe,
        "reason": "" if all(v is True for v in probe.values()) else "; ".join(reasons),
    }
