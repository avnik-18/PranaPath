"""Validator: the AI may not say a number/ID the engine did not produce (Magpie gate).

Checks on the sentence: every numeric token must exist in the allowlist derived from
the panel (rounded comparisons), and certain banned tokens are rejected outright.
Return (ok: bool, reason: str).
"""

import re

BANNED = {"$", "#", "guaranteed", "trails+"}   # "$" never; "guaranteed" never (health promises)


def validate_sentence(sentence, panel):
    if not sentence or len(sentence.split()) > 40:
        return False, "empty/overlong"
    low = sentence.lower()
    for tok in BANNED:
        if tok in low:
            return False, f"banned token {tok!r}"

    allowed = _allowed_numbers(panel)
    for num in _numbers(sentence):
        if not _matches_any(num, allowed):
            return False, f"invented number {num}"
    for token in _ids(sentence):
        if token not in _known_ids(panel):
            return False, f"invented id {token!r}"
    return True, "ok"


def _numbers(text):
    return [float(m.group()) for m in re.finditer(r"(?<![\w.])(\d+(?:\.\d+)?)", text)]


def _ids(text):
    return set(re.findall(r"\b[A-Z]\d(?:[A-Za-z]|\d)*\b", text)) - set()


def _matches_any(x, allowed):
    tol = 0.051
    return any(abs(x - a) <= tol for a in allowed)


def _known_ids(panel):
    ids = set()
    for key, routes in (("route_fastest", None), ("route_healthy", None)):
        ids.update(panel[key]["path"])
    for seg in panel.get("hotspots", {}).get("fastest", []):
        ids.add(seg["edge_id"])
    for seg in panel.get("hotspots", {}).get("healthy", []):
        ids.add(seg["edge_id"])
    return ids


def _allowed_numbers(panel):
    nums = []
    nums.append(panel["tradeoff"].get("time_extra_minutes", 0.0))
    nums.append(panel["tradeoff"].get("dose_saving_pct", 0.0))
    for key in ("route_fastest", "route_healthy"):
        r = panel[key]
        nums.append(float(r["minutes"]))
        nums.append(float(r["dose_ug"]))
    for side in ("fastest", "healthy"):
        for h in panel.get("hotspots", {}).get(side, []):
            nums.append(float(h["pm25_ug_m3"]))
            nums.append(float(h["minutes"]))
            nums.append(float(h["share_pct"]))
    words = {"one", "half", "a"}          # common words; not numbers to verify
    return nums
