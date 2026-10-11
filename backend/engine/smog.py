"""1-km smog cells over the corridor: deterministic ORGANIC polygons, never circles.

For each ~1 km grid cell around the route corridor, the blob radius breathes with
seeded harmonics (sha1 of the cell id) so the rendered haze looks like smog, not
porcelain. Cell pm is broadcast from the nearest hotspot point, else the route
baseline. Same inputs -> same polygons, every run, every machine.
"""
import hashlib
from math import cos, pi, radians, sin, sqrt

KM_PER_DEG_LAT = 111.32
CELL_KM = 1.0                 # grid step: the 1 km zone resolution
POLY_KM = 0.78                # blob footprint, km (radius peak < 1.0)
JITTER_KM = 0.34              # anchor wander inside the cell
MAX_CELLS = 12
VERTICES = 22
PAD_KM = 2.6

KIND_HIGH, KIND_MID = 250.0, 170.0


def level_of(pm):
    """Honest bucket for a µg/m³ reading (reference day = 150)."""
    return "high" if pm >= KIND_HIGH else ("mid" if pm >= KIND_MID else "low")


def build_smog(path_nodes, hot_points, baseline_pm):
    """path_nodes: [{lat,lon}]; hot_points: [{lat,lon,pm25}]; -> 1-km smog cells."""
    pts = [(p["lat"], p["lon"]) for p in path_nodes] or []
    if not pts:
        return []
    lats = [p[0] for p in pts]
    lons = [p[1] for p in pts]
    mid_lat = sum(lats) / len(lats)
    km_lon = KM_PER_DEG_LAT * max(cos(radians(mid_lat)), 0.25)

    def deg(km, is_lat):
        return km / KM_PER_DEG_LAT if is_lat else km / km_lon

    cells = []
    row = 0
    lat = min(lats) - deg(PAD_KM, True)
    while lat <= max(lats) + deg(PAD_KM, True):
        col = 0
        lon = min(lons) - deg(PAD_KM, False)
        while lon <= max(lons) + deg(PAD_KM, False):
            jy, jx = _seeded_offsets(row, col)
            plat = lat + deg(jy, True)
            plon = lon + deg(jx, False)
            pm = _cell_pm(plon, plat, hot_points, baseline_pm, km_lon)
            cells.append((plat, plon, pm, row, col))
            lon += deg(CELL_KM, False)
            col += 1
        lat += deg(CELL_KM, True)
        row += 1

    cells.sort(key=lambda c: (-c[2], c[3], c[4]))
    return [_polygon(c, km_lon) for c in cells[:MAX_CELLS]]


def _polygon(cell, km_lon):
    plat, plon, pm, row, col = cell
    ring = []
    for k in range(VERTICES):
        theta = 2 * pi * k / VERTICES
        r = _radius(_seed_int(row, col) + k, theta)
        ring.append([
            round(plon + deg_km(r * cos(theta), km_lon), 5),
            round(plat + deg_km(r * sin(theta), km_lon, lat=True), 5),
        ])
    ring.append(ring[0])                      # GeoJSON: exterior ring closes explicitly
    return {"polygon": ring, "pm25": round(pm, 1), "level": level_of(pm)}


def deg_km(km, km_lon, lat=False):
    """Project a km distance to degrees (cos-adjusted for lon at this latitude)."""
    return km / KM_PER_DEG_LAT if lat else km / km_lon


def _radius(seed, theta):
    """Radius (km) = seeded harmonic breathing; clamped so blobs stay irregular."""
    a1 = 0.18 + (seed % 7) / 100.0
    a2 = 0.08 + ((seed >> 3) % 7) / 100.0
    a3 = 0.05 + ((seed >> 5) % 5) / 100.0
    f = (a1 * sin(2 * theta + (seed % 13) / 2.0)
         + a2 * sin(3 * theta + ((seed >> 2) % 11) / 3.0)
         + a3 * sin(5 * theta + ((seed >> 4) % 17) / 5.0))
    r = POLY_KM * (0.62 + 0.38 * (f + 0.31))
    return max(min(r, 1.0), 0.45)


def _seed_int(*parts):
    blob = hashlib.sha1("|".join(str(p) for p in parts).encode("utf-8")).hexdigest()
    return int(blob[:8], 16)


def _seeded_offsets(row, col):
    s = _seed_int("anchor", row, col)
    jy = ((s % 1000) / 1000.0 - 0.5) * 2 * JITTER_KM
    jx = (((s >> 9) % 1000) / 1000.0 - 0.5) * 2 * JITTER_KM
    return jy, jx


def _cell_pm(plon, plat, hot_points, baseline_pm, km_lon):
    """Nearest hotspot reading blended toward the baseline over ~1.5 km — smog mellows with distance."""
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
