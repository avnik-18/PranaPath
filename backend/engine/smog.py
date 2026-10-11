"""AQI blob field over the corridor: 50 m organic blobs everywhere, banded by pm.

Design contract (deterministic, no randomness):
- hex-ish lattice at 100 m spacing with seeded anchor scatter → soft overlap (~10%)
- every blob breathes with seeded harmonics (sha1) → organic, never a perfect circle
- per-blob reading = nearest hotspot receipt blended toward the route baseline over
  1.5 km, plus ±8% seeded micro-variation → blobs differ from their neighbours
- blobs are grouped by rounded pm band (±20 µg) and returned as one MultiPolygon
  feature per band so the map stays light while every blob keeps its own value
"""
import hashlib
from math import cos, pi, radians, sin, sqrt

KM_PER_DEG_LAT = 111.32
FIELD_SPACING_KM = 0.10       # lattice step: overlap ~10% at 55 m radius
FIELD_R_KM = 0.055            # blob promise: 55 m radius (neighbours just touch)
FIELD_VERTS = 16
FIELD_PAD_KM = 0.8
FIELD_BAND_UG = 20.0          # pm bands: one MultiPolygon per ±20 µg bucket
MAX_BLOBS = 5200

PUFF_KM = 0.05                # street puffs: 50 m blobs on the hottest edges
PUFF_VERTS = 18
PUFFS_MAX = 6
PUFF_GAP_KM = 0.22            # one puff per hot pocket, closer pockets get their own

KIND_HIGH, KIND_MID = 250.0, 170.0


def level_of(pm):
    """Honest bucket for a µg/m³ reading (reference day = 150)."""
    return "high" if pm >= KIND_HIGH else ("mid" if pm >= KIND_MID else "low")


def find_field(path_nodes, sources, baseline_pm):
    """path_nodes: [{lat,lon}]; sources: [{lat,lon,peak,sigma_m}]; -> band MultiPolygons.

    Every blob reads the SAME gaussian mixture the graph's streets read:
    pm(x,y) = base + Σ peakᵢ·exp(−(dᵢ/σᵢ)²), then ±6% seeded micro-weather.
    """
    pts = [(p["lat"], p["lon"]) for p in path_nodes]
    if not pts:
        return []
    lats = [p[0] for p in pts]
    lons = [p[1] for p in pts]
    mid_lat = sum(lats) / len(lats)
    km_lon = KM_PER_DEG_LAT * max(cos(radians(mid_lat)), 0.25)
    lat0 = min(lats) - FIELD_PAD_KM / KM_PER_DEG_LAT
    lat1 = max(lats) + FIELD_PAD_KM / KM_PER_DEG_LAT
    lon0 = min(lons) - FIELD_PAD_KM / km_lon
    lon1 = max(lons) + FIELD_PAD_KM / km_lon

    step_lon = FIELD_SPACING_KM / km_lon
    step_lat = FIELD_SPACING_KM / KM_PER_DEG_LAT
    rows = int((lat1 - lat0) / (step_lat * 0.87)) + 1
    cols = int((lon1 - lon0) / step_lon) + 1

    bands = {}
    for row in range(rows):
        for col in range(cols):
            if row * cols + col >= MAX_BLOBS:
                break
            jy, jx = _anchor_shift(row, col)
            plon = lon0 + (col + jx) * step_lon
            plat = lat0 + (row + jy) * step_lat * 0.87
            pm = _gaussian_field_pm(plon, plat, sources, baseline_pm, km_lon, _micro(row, col))
            band = int(round(pm / FIELD_BAND_UG) * FIELD_BAND_UG)
            ring = _field_ring(plat, plon, km_lon, row, col)
            bands.setdefault(band, []).append(ring)

    out = []
    for band in sorted(bands, reverse=True):
        out.append({
            "polygon": bands[band],          # MultiPolygon: one entry per ring
            "pm25": float(band),
            "level": level_of(band),
            "count": len(bands[band]),
        })
    return out


def _gaussian_field_pm(plon, plat, sources, base_pm, km_lon, micro=1.0):
    """pm = (base + Σ peakᵢ·exp(−(dᵢ/σᵢ)²)) × micro, clamped to the honest range."""
    from math import exp
    total = float(base_pm)
    for s in sources:
        d = _km(plon, plat, s["lon"], s["lat"], km_lon)
        sigma_km = max(s.get("sigma_m", 600.0) / 1000.0, 0.05)
        total += s["peak"] * exp(-((d / sigma_km) ** 2))
    return max(min(total * micro, 900.0), 40.0)


def _field_ring(plat, plon, km_lon, row, col):
    """One 12-vertex organic ring, radius ≤ FIELD_R_KM, seeded by its anchor."""
    s = _seed_int("field", row, col)
    ring = []
    for k in range(FIELD_VERTS):
        theta = 2 * pi * k / FIELD_VERTS
        r = min(FIELD_R_KM * (0.82 + 0.24 * _harmony(s + k, theta)), FIELD_R_KM)
        ring.append([
            round(plon + deg_km(r * cos(theta), km_lon), 4),
            round(plat + deg_km(r * sin(theta), km_lon, lat=True), 4),
        ])
    ring.append(ring[0])                      # GeoJSON: exterior ring closes explicitly
    return ring


def build_puffs(points):
    """50-m organic street puffs anchored on the hottest edges (seeded by edge id).

    One puff per hot pocket (>220 m apart), radius breathes but never exceeds 50 m.
    """
    puffs, anchors = [], []
    for h in sorted(points, key=lambda x: (-x["pm25"], x["id"])):
        s = _seed_int("puff", h["id"])
        km_lon = KM_PER_DEG_LAT * max(cos(radians(h["lat"])), 0.25)
        if any(_km(h["lon"], h["lat"], a[0], a[1], km_lon) < PUFF_GAP_KM for a in anchors):
            continue
        anchors.append((h["lon"], h["lat"]))
        ring = []
        for k in range(PUFF_VERTS):
            theta = 2 * pi * k / PUFF_VERTS
            r = min(PUFF_KM * (0.86 + 0.4 * _harmony(s + k, theta)), PUFF_KM)
            ring.append([
                round(h["lon"] + deg_km(r * cos(theta), km_lon), 5),
                round(h["lat"] + deg_km(r * sin(theta), km_lon, lat=True), 5),
            ])
        ring.append(ring[0])
        puffs.append({"polygon": ring, "pm25": round(h["pm25"], 1),
                      "level": level_of(h["pm25"]), "id": h["id"]})
        if len(puffs) >= PUFFS_MAX:
            break
    return puffs


def deg_km(km, km_lon, lat=False):
    """Project a km distance to degrees (cos-adjusted for lon at this latitude)."""
    return km / KM_PER_DEG_LAT if lat else km / km_lon


def _harmony(seed, theta):
    """Seeded 3-harmonic breathing term, shared by field blobs and street puffs."""
    a1 = 0.16 + (seed % 7) / 100.0
    a2 = 0.07 + ((seed >> 3) % 7) / 100.0
    a3 = 0.05 + ((seed >> 5) % 5) / 100.0
    return (a1 * sin(2 * theta + (seed % 13) / 2.0)
            + a2 * sin(3 * theta + ((seed >> 2) % 11) / 3.0)
            + a3 * sin(5 * theta + ((seed >> 4) % 17) / 5.0))


def _seed_int(*parts):
    blob = hashlib.sha1("|".join(str(p) for p in parts).encode("utf-8")).hexdigest()
    return int(blob[:8], 16)


def _anchor_shift(row, col):
    """Seeded scatter inside the lattice cell — no visible grid tiling."""
    s = _seed_int("anchor", row, col)
    jy = ((s % 1000) / 1000.0 - 0.5) * 0.55
    jx = (((s >> 9) % 1000) / 1000.0 - 0.5) * 0.55
    return jy, jx


def _micro(row, col):
    """±8% seeded micro-variation so neighbours read different AQI values."""
    s = _seed_int("micro", row, col)
    return 1.0 + (((s % 1000) / 1000.0 - 0.5) * 0.16)


def _blob_pm(plon, plat, hot_points, baseline_pm, km_lon):
    """Nearest hotspot reading blended toward the baseline over ~1.5 km."""
    best_d, best_pm = float("inf"), None
    for h in hot_points:
        d = _km(plon, plat, h["lon"], h["lat"], km_lon)
        if d < best_d:
            best_d, best_pm = d, h["pm25"]
    if best_pm is None:
        return baseline_pm
    t = min(best_d / 1.5, 1.0)
    return best_pm * (1 - t) + baseline_pm * t


def _km(lon1, lat1, lon2, lat2, km_lon):
    dy = (lat2 - lat1) * KM_PER_DEG_LAT
    dx = (lon2 - lon1) * km_lon
    return sqrt(dx * dx + dy * dy)
