"""Rules for the AQI blob field: organic shapes, full coverage, honest bands."""
import unittest
from math import cos, radians

from backend.engine.smog import FIELD_R_KM, MAX_BLOBS, PUFF_KM, PUFFS_MAX, build_puffs, find_field, level_of

BOUNCE = [{"lat": 28.70, "lon": 77.12}, {"lat": 28.72, "lon": 77.15},
          {"lat": 28.69, "lon": 77.17}]
HOTS = [{"lat": 28.705, "lon": 77.13, "pm25": 420.0},
        {"lat": 28.715, "lon": 77.16, "pm25": 310.0}]


class TestFieldRules(unittest.TestCase):
    def setUp(self):
        self.field = find_field(BOUNCE, HOTS, 180.0)

    def test_every_blob_is_organic_and_closed(self):
        self.assertGreater(len(self.field), 0, "corridor must produce a blob field")
        rings = [r for band in self.field for r in band["polygon"]]
        self.assertGreater(len(rings), 200, "small corridor must still be dense")
        for ring in rings:
            self.assertEqual(ring[0], ring[-1], "ring closes explicitly")
            cx = sum(p[0] for p in ring[:-1]) / (len(ring) - 1)
            cy = sum(p[1] for p in ring[:-1]) / (len(ring) - 1)
            km_lon = 111.32 * cos(radians(cy))
            rs = [(((p[0] - cx) * km_lon) ** 2 + ((p[1] - cy) * 111.32) ** 2) ** 0.5
                  for p in ring[:-1]]
            self.assertLessEqual(max(rs), FIELD_R_KM * 1.06, "blob respects its radius")
            self.assertGreater(max(rs) - min(rs), 0.002,
                               "blob must not be a perfect circle")

    def test_field_covers_the_whole_corridor_box(self):
        lats = [p["lat"] for p in BOUNCE]
        lons = [p["lon"] for p in BOUNCE]
        centers = []
        for band in self.field:
            for ring in band["polygon"]:
                centers.append((sum(p[0] for p in ring[:-1]) / (len(ring) - 1),
                                sum(p[1] for p in ring[:-1]) / (len(ring) - 1)))
        for fl in (0.1, 0.5, 0.9):
            for fo in (0.1, 0.5, 0.9):
                y = min(lats) + fl * (max(lats) - min(lats))
                x = min(lons) + fo * (max(lons) - min(lons))
                near = min(((cy - y) * 111.32) ** 2 + ((cx - x) * 97.5) ** 2 for cx, cy in centers) ** 0.5
                self.assertLessEqual(near, 0.2,
                                     f"blob field must cover ({x:.3f},{y:.3f}) — no empty zones")

    def test_bands_differ_and_hot_band_exists(self):
        bands = {band["pm25"] for band in self.field}
        self.assertGreaterEqual(len(bands), 3, "many blobs with DIFFERENT aqi")
        self.assertGreaterEqual(max(bands), 300, "the 420 hotspot must lead a band")
        for band in self.field:
            self.assertEqual(band["level"], level_of(band["pm25"]))

    def test_same_inputs_same_field(self):
        self.assertEqual(self.field, find_field(BOUNCE, HOTS, 180.0))

    def test_blob_budget_is_bounded(self):
        total = sum(band["count"] for band in self.field)
        self.assertLessEqual(total, MAX_BLOBS)


class TestPuffRules(unittest.TestCase):
    def test_puffs_deterministic_capped_and_within_50m(self):
        puffs = build_puffs([{"id": f"u{i}-v{i}", "lat": 28.70 + 0.004 * i,
                              "lon": 77.12 + 0.004 * i, "pm25": 380.0 - 12 * i}
                             for i in range(8)])
        self.assertEqual(build_puffs([{"id": "p", "lat": 28.71, "lon": 77.13, "pm25": 400.0}]),
                         build_puffs([{"id": "p", "lat": 28.71, "lon": 77.13, "pm25": 400.0}]))
        self.assertGreaterEqual(len(puffs), 5, "8 spread points must yield ≥5 puffs")
        self.assertLessEqual(len(puffs), PUFFS_MAX)
        for p in puffs:
            ring = p["polygon"][:-1]
            ax = sum(pt[0] for pt in ring) / len(ring)
            ay = sum(pt[1] for pt in ring) / len(ring)
            km_lon = 111.32 * cos(radians(ay))
            r_km = max((((px[0] - ax) * km_lon) ** 2 + ((px[1] - ay) * 111.32) ** 2) ** 0.5
                       for px in ring)
            self.assertLessEqual(r_km, PUFF_KM * 1.05,
                                 "a 50 m puff must never exceed its 50 m radius promise")


if __name__ == "__main__":
    unittest.main()
