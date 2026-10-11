import unittest

from backend.engine.exposure import segment_dose_minutes, dose_on_edges, hotspots


class DoseFormulaTest(unittest.TestCase):
    """Rule: dose = C × IR × hours, per mode, deterministic."""

    def test_jog_two_minutes_bound(self):
        # 150 µg/m³ × 3.0 m³/h × (2/60) h = 15.0 µg
        self.assertAlmostEqual(segment_dose_minutes(150.0, 2.0, "jog"), 15.0, places=6)

    def test_walk_lower_than_jog(self):
        walk = segment_dose_minutes(150.0, 2.0, "walk")
        jog = segment_dose_minutes(150.0, 2.0, "jog")
        self.assertLess(walk, jog)

    def test_unknown_mode_raises(self):
        with self.assertRaises(ValueError):
            segment_dose_minutes(150.0, 1.0, "teleport")


class DoseAggregationTest(unittest.TestCase):
    """Rule: totals sum per-edge; hotspots = share ≥ 12%, ranked, capped."""

    def _edges(self):
        e_low = {"id": "L", "minutes": 2.0, "pm25_ug_m3": 150.0, "length_m": 400, "u": "a", "v": "b"}
        e_hot = {"id": "H", "minutes": 2.0, "pm25_ug_m3": 600.0, "length_m": 400, "u": "b", "v": "c"}
        return [e_low, e_hot]

    def test_total_and_hotspot(self):
        edges = self._edges()
        total, per = dose_on_edges(edges, "jog")
        low, hot = per["L"], per["H"]
        self.assertAlmostEqual(total, low + hot, places=6)
        self.assertGreater(hot / total, 0.6)                    # H carries most of the dose
        hs = hotspots(per, edges)
        self.assertEqual(hs[0]["edge_id"], "H")
        self.assertGreaterEqual(hs[0]["share_pct"], 12.0)


if __name__ == "__main__":
    unittest.main()
