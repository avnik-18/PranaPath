"""The AWS ops-panel CONTRACT (additive only, mirrors schemas.py style)."""

AWS_API_VERSION = "v1"


def aws_panel_response(payload):
    """Shape of GET /aws/panel — {ok, api_version, data:{switch,mode,probe,inventory,activities,receipts,counts,trip}}."""
    return {"ok": True, "api_version": AWS_API_VERSION, "data": payload}


def aws_status_response(state):
    """Shape of GET /aws/status — {ok, api_version, data:{mode,region,probe,reason}}."""
    return {"ok": True, "api_version": AWS_API_VERSION, "data": state}


def aws_error(code, message):
    return {"ok": False, "api_version": AWS_API_VERSION, "error": {"code": code, "message": message}}
