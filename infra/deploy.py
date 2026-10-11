"""One-command deploy: package lambda zips, plan, and (only with team creds) push the stack.

Never prints credentials; every step leaves a receipt (data/receipts). Dry run touches AWS never.
Run: wsl python3 infra/deploy.py --dry-run   |   --apply (only after creds land in .env)
"""
import argparse
import os
import random
import re
import string
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from backend.aws.receipts import record  # noqa: E402 – ledger is infra's evidence store

INFRA = Path(__file__).resolve().parent
BUILD = INFRA / "build"

ZIP_PLANS = (
    ("awslambda_engine.zip", ("backend",), ("infra/awslambda_engine.py",)),
    ("awslambda_explainer.zip", ("backend",), ("infra/awslambda_explainer.py",)),
    ("refresh_aqi.zip", (), ("infra/refresh_aqi.py",)),
)

STACK = "EcoRouteAI"


def template_text():
    return (INFRA / "template.yaml").read_text(encoding="utf-8")


def resources_in_template():
    return len(re.findall(r"^  ([A-Za-z][A-Za-z0-9]+):\n    Type: ", template_text(), flags=re.M))


def build_zips():
    BUILD.mkdir(exist_ok=True)
    made = []
    for name, dirs, singles in ZIP_PLANS:
        zip_path = BUILD / name
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
            for d in dirs:
                for f in sorted((ROOT / d).rglob("*")):
                    if f.is_file() and "__pycache__" not in f.parts:
                        z.write(f, arcname=str(f.relative_to(ROOT)))
            for single in singles:
                z.write(ROOT / single, arcname=Path(single).name)
        made.append((name, zip_path.stat().st_size))
    return made


def _creds_present():
    return bool(os.environ.get("AWS_ACCESS_KEY_ID") and os.environ.get("AWS_SECRET_ACCESS_KEY"))


def _apply(region, res, zips):
    try:
        import boto3
    except Exception as exc:
        print(f"boto3 missing ({exc}) — install on the runner (CloudShell/phone), never into the repo")
        return 1
    s3 = boto3.client("s3", region_name=region)
    cfn = boto3.client("cloudformation", region_name=region)
    bucket = "ecoroute-artifacts-" + "".join(random.choices(string.ascii_lowercase, k=13))
    s3.create_bucket(Bucket=bucket, CreateBucketConfiguration={"LocationConstraint": region})
    for name, _ in zips:
        s3.upload_file(str(BUILD / name), bucket, name)
    text = template_text()
    for name, _ in zips:
        text = text.replace(f"build/{name}", f"s3://{bucket}/{name}")
    cfn.create_stack(
        StackName=STACK, TemplateBody=text,
        Parameters=[{"ParameterKey": "AlertEmail",
                     "ParameterValue": os.environ.get("ALERT_EMAIL", "nobody@example.com")}],
        Capabilities=["CAPABILITY_IAM"],
    )
    cfn.get_waiter("stack_create_complete").wait(StackName=STACK, WaiterConfig={"Delay": 10, "MaxAttempts": 36})
    outputs = cfn.describe_stacks(StackName=STACK)["Stacks"][0].get("Outputs", [])
    for o in outputs:
        print(f"  {o['OutputKey']}: {o['OutputValue']}")
    record("deploy.apply", {"region": region, "resources": res,
                            "bucket": bucket, "outputs": [o["OutputKey"] for o in outputs]})
    print("what changed live: stack EcoRouteAI created — see Outputs above + data/receipts")
    print(f"next: set VITE_API_BASE to the ApiBaseUrl output, rebuild web, Amplify ZIP-upload web/dist")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="EcoRoute deploy (free-tier, receipted)")
    ap.add_argument("--dry-run", action="store_true", help="package + plan; AWS untouched")
    ap.add_argument("--apply", action="store_true", help="real push; needs team keys in env")
    a = ap.parse_args(argv)
    region = os.environ.get("AWS_REGION", "ap-south-1")
    zips = build_zips()
    res = resources_in_template()
    if a.apply:
        if not _creds_present():
            print("PLAN ok, APPLY blocked — add AWS_ACCESS_KEY_ID + AWS_SECRET_ACCESS_KEY to .env "
                  "(team account keys, never personal).")
            record("deploy.plan-blocked", {"region": region, "zips": [n for n, _ in zips]})
            return 1
        return _apply(region, res, zips)
    for name, size in zips:
        print(f"  zip {name}: {size / 1024:.1f} KB")
    print(f"PLAN region={region} · free-tier · zips={len(zips)} · template resources={res} · "
          "on --apply: s3 upload + CloudFormation change-set push")
    record("deploy.dry-run", {"region": region, "zips": [n for n, _ in zips], "resources": res})
    print("what changed live: NOTHING (dry run)")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
