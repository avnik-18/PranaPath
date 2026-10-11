"""Produce THE sentence: Bedrock if available+valid, else deterministic template (source-tagged).

Callers never learn which backend spoke. The template is reproducible (seeded from panel).
"""

import random

from . import bedrock, prompt
from .bedrock import BedrockUnavailable
from .validate import validate_sentence


def explain_route(panel, use_ai=True, seed=None):
    if use_ai:
        try:
            raw = _ask_bedrock(panel)
            ok, _why = validate_sentence(raw, panel)
            if ok:
                return {"sentence": raw.strip(), "source": "bedrock", "validated": True}
        except BedrockUnavailable:
            pass
    return {"sentence": template_sentence(panel, seed=seed), "source": "template", "validated": True}


def template_sentence(panel, seed=None):
    """Pure fallback: assembled ONLY from engine facts; deterministic for same panel."""
    f = _facts(panel)
    if f["same_route"]:
        return (
            f"Both routes are the same {f['healthy_min']} minutes; dose stays "
            f"{f['healthy_dose']} µg, so there is no health trade this option."
        )
    hot = (f["hotspots"]["fastest"] or [{}])[0]
    rng = random.Random(seed if seed is not None else int(abs(f["time_extra"]) * 10) + int(f["healthy_dose"]))
    line = rng.choice([
        (f"Take A for speed: {f['fastest_min']} minutes, {f['fastest_dose']} µg. "
         f"Route B adds {f['time_extra']} minutes but cuts the inhaled dose by "
         f"{f['saving']}% ({f['healthy_dose']} vs {f['fastest_dose']} µg)."),
        (f"Route B costs {f['time_extra']} extra minutes but breathes {f['saving']}% less — "
         f"{f['healthy_min']} minutes against {f['fastest_min']} minutes, everything else equal."),
    ])
    if hot.get("edge_id"):
        line += f" Worst segment on A: {hot['edge_id']} ({hot['share_pct']}% of dose)."
    return line


def _ask_bedrock(panel):
    payload = dict(panel)
    return bedrock.invoke_explainer(
        payload,
        prompt.SYSTEM_PROMPT,
        prompt.USER_TEMPLATE.format(payload=payload, mode=panel["mode"]),
    )


def _facts(panel):
    t = panel["tradeoff"]
    return {
        "fastest_min": panel["route_fastest"]["minutes"],
        "healthy_min": panel["route_healthy"]["minutes"],
        "fastest_dose": panel["route_fastest"]["dose_ug"],
        "healthy_dose": panel["route_healthy"]["dose_ug"],
        "saving": t["dose_saving_pct"],
        "time_extra": t["time_extra_minutes"],
        "same_route": t["same_route"],
        "hotspots": panel["hotspots"],
    }
