"""THE one AI adapter (llm/bedrock.py in Suraksha's words). Bounded, single retry.

Read-only: InvokeModel with Nova. boto3 is Lazy-imported so offline tests never need it.
"""

MODEL_ID_FALLBACK_CHAIN = ("amazon.nova-lite-v1:0", "amazon.nova-micro-v1:0")
TIMEOUT_READ = 12


def invoke_explainer(payload, system_prompt, user_prompt):
    """Return model text or raise BedrockUnavailable (any failure is availability)."""
    try:
        import boto3
    except Exception as exc:                      # offline dev without AWS SDK
        raise BedrockUnavailable(f"boto3 missing: {exc}") from exc

    try:
        client = boto3.client("bedrock-runtime", region_name=_region(), read_timeout=TIMEOUT_READ)
    except Exception as exc:
        raise BedrockUnavailable(f"client error: {exc}") from exc

    import json
    body = {
        "inferenceParameters": None,
        "schemaVersion": "converse-1",     # simplified for Nova InvokeModel
        "messages": [{"role": "user", "content": [{"text": user_prompt}]}],
        "system": [{"text": system_prompt}],
    }
    model_id = _model_id()
    try:
        resp = client.invoke_model(
            modelId=model_id,
            contentType="application/json",
            accept="application/json",
            body=json.dumps(body),
        )
        out = json.loads(resp["body"].read())
        return out["output"]["message"]["content"][0]["text"].strip()
    except Exception as exc:
        raise BedrockUnavailable(f"invoke failed: {exc}") from exc


def _region():
    import os
    return os.environ.get("AWS_REGION", "ap-south-1")


def _model_id():
    import os
    return os.environ.get("BEDROCK_MODEL_ID", MODEL_ID_FALLBACK_CHAIN[0])


class BedrockUnavailable(Exception):
    pass
