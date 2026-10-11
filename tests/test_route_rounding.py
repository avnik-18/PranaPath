import unittest

from tests.common import panel, graph
from backend.engine.routes import compare_routes


class DeterminismTest(unittest.TestCase):
    """Rule: identical inputs -> identical dicts (down to the last rounding digit)."""

    def test_panel_is_reproducible(self):
        once = panel()
        again = panel()
        self.assertEqual(once, again)

    def test_minutes_are_tenths(self):
        p = panel()
        for key in ("route_fastest", "route_healthy"):
            minutes = p[key]["minutes"]
            self.assertEqual(minutes, round(minutes, 1))


class GraphIntegrityTest(unittest.TestCase):
    """Rule: input data sanity — connectivity for landmarks, pm bands as generated."""

    def test_landmarks_exist(self):
        g = graph()
        for name in ("rohini", "ashok_vihar", "pitampura", "model_town"):
            self.assertIn(name, g["by_name"])

    def test_two_routes_differ_or_warn(self):
        p = panel("rohini", "pitampura", "jog")
        # not asserting they differ (borderline pairs may tie): the truth flag must say so either way
        self.assertEqual(p["tradeoff"]["same_route"],
                         p["route_fastest"]["path"] == p["route_healthy"]["path"])


if __name__ == "__main__":
    unittest.main()
