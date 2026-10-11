"""Rules for the 1-km smog layer: organic shapes, determinism, honest levels."""
import unittest

from backend.engine.smog import build_smog, level_of

BOUNCE = [{"lat": 28.70, "lon": 77.12}, {"lat": 28.72, "lon": 77.15},
          {"lat": 28.69, "lon": 77.17}]
HOTS = [{"lat": 28.705, "lon": 77.13, "pm25": 420.0},
        {"lat": 28.715, "lon": 77.16, "pm25": 310.0}]


class TestSmogRules(unittest.TestCase):
    def test_cells_are_organic_not_circles(self):
        cells = build_smog(BOUNCE, HOTS, 180.0)
        self.assertGreater(len(cells), 0, "corridor must produce haze cells")
        for c in cells:
            ring = c["polygon"][:-1]          # drop the closing duplicate
            self.assertEqual(c["polygon"][0], c["polygon"][-1], "polygon must close the ring")
            cx = sum(p[0] for p in ring) / len(ring)
            cy = sum(p[1] for p in ring) / len(ring)
            radii = [((p[0] - cx) ** 2 + (p[1] - cy) ** 2) ** 0.5 for p in ring]
            spread_km = (max(radii) - min(radii)) * 111.32      # ° → km at this latitude
            self.assertGreater(spread_km, 0.05,
                               f"cell at {cx},{cy} is a perfect circle — smog must not be")

    def test_same_inputs_same_polygons(self):
        self.assertEqual(build_smog(BOUNCE, HOTS, 180.0), build_smog(BOUNCE, HOTS, 180.0))

    def test_hot_cell_inherits_hotspot_pm_and_level(self):
        cells = build_smog(BOUNCE, HOTS, 120.0)
        self.assertTrue(any(c["pm25"] > 300.0 and c["level"] == "high" for c in cells),
                        "a cell hugging the 420 hotspot must read hot")
        self.assertEqual(level_of(169.0), "low")
        self.assertEqual(level_of(170.0), "mid")
        self.assertEqual(level_of(250.0), "high")

    def test_cell_count_is_capped(self):
        from backend.engine.smog import MAX_CELLS
        self.assertLessEqual(len(build_smog(BOUNCE, HOTS, 200.0)), MAX_CELLS)


if __name__ == "__main__":
    unittest.main()
