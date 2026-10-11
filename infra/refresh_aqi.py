"""15-min tick: extend the AQI snapshot from Open-Meteo (keyless), PutItem when live."""
import json
import os


def handler(event, context):
    lat, lon = 28.71, 77.12
    table = os.environ.get("TRIPS_TABLE", "EcoRouteTrips")
    err = ""
    pm25 = None
    try:
        from urllib.request import urlopen
        url = (f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}"
               f"&longitude={lon}&hourly=pm2_5&count=1")
        data = json.loads(urlopen(url, timeout=10).read())
        pm25 = (data.get("hourly", {}).get("pm2_5") or [None])[0]
    except Exception as exc:  # keyless source flaking is a logged tick, not a crash
        err = f"{type(exc).__name__}: {exc}"

    if pm25 is None:
        return {"statusCode": 200, "body": json.dumps({
            "warning": "open-meteo unavailable this tick", "detail": err, "table": table,
        })}

    dynamodb_ok = False
    try:
        import boto3
        boto3.client("dynamodb").put_item(
            TableName=table,
            Item={"pk": {"S": "aqi_latest"}, "pm25": {"N": str(pm25)}},
        )
        dynamodb_ok = True
    except Exception as exc:  # no role / no creds → honest tick only
        err = f"{type(exc).__name__}: {exc}"

    return {"statusCode": 200, "body": json.dumps({
        "pm25": pm25, "dynamodb_ok": dynamodb_ok, "table": table, "detail": err,
    })}
