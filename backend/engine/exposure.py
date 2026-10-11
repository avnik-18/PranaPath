"""Inhaled dose math — the claim the whole app makes. Deterministic, published form.

dose(µg) for a segment = C(µg/m³) × IR(m³/h) × minutes/60
IR defaults (m³/h, literature-backed gentle values, labeled in honest-limits.md):
walk 1.4, cycle 2.3, jog 3.0.
"""

IR_M3H = {"walk": 1.4, "cycle": 2.3, "jog": 3.0}
HOTSPOT_SHARE = 0.12          # a segment is a hotspot if it carries ≥12% of route dose


def segment_dose_minutes(pm25_ug_m3, minutes, mode):
    ir = IR_M3H.get(mode)
    if ir is None:
        raise ValueError(f"unknown mode {mode!r}; expected one of {sorted(IR_M3H)}")
    return pm25_ug_m3 * ir * (minutes / 60.0)


def dose_on_edges(edges, mode):
    """Return (total µg, per-edge doses keyed by edge id)."""
    per = {e["id"]: segment_dose_minutes(e["pm25_ug_m3"], e["minutes"], mode) for e in edges}
    return sum(per.values()), per


def hotspots(per_edge, edges, share=HOTSPOT_SHARE, limit=3):
    """Segments responsible for most of the dose, ranked, with share of total."""
    total = sum(per_edge.values())
    if total <= 0:
        return []
    by_edge = {e["id"]: e for e in edges}
    ranked = sorted(per_edge.items(), key=lambda kv: (-(kv[1] / total), kv[0]))
    out = []
    for eid, dose in ranked:
        seg = by_edge[eid]
        ratio = dose / total
        if ratio < share:
            break
        out.append({
            "edge_id": eid,
            "pm25_ug_m3": seg["pm25_ug_m3"],
            "minutes": seg["minutes"],
            "share_pct": round(as_pct(ratio), 1),
        })
        if len(out) >= limit:
            break
    return out


def as_pct(x):
    return 100.0 * x
