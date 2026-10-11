import unittest

from backend.api import handler as hp
from tests.common import panel


class ApiContractTest(unittest.TestCase):
    """Rule: endpoint payload is stable for web/src/types.ts; errors are clean 4xx-shaped."""

    def test_state_ok(self):
        st = hp.handle_state()
        self.assertTrue(st["ok"])
        self.assertTrue(all(st["fixtures_present"].values()))

    def test_routes_payload_keys(self):
        out = hp.handle_routes("ashok_vihar", "pitampura", "jog")
        self.assertTrue(out["ok"])
        for key in ("route_fastest", "route_healthy", "tradeoff", "hotspots", "explanation", "ui"):
            self.assertIn(key, out)
        self.assertIn(out["explanation"]["source"], ("template", "bedrock"))
        self.assertTrue(out["tradeoff"]["dose_saving_pct"] >= 0.0)

    def test_map_nodes_have_coords(self):
        out = hp.handle_routes("ashok_vihar", "pitampura", "jog")
        for node in out["ui"]["map_nodes"]:
            self.assertIn("lat", node)
            self.assertIn("lon", node)
            self.assertIn("id", node)

    def test_unknown_node_is_clean_error(self):
        out = hp.handle_routes("ashok_vihar", "ravana", "jog")
        self.assertFalse(out["ok"])
        self.assertEqual(out["error"]["code"], "unknown_node")

    def test_engine_matches_handler(self):
        # same engine under the hood: minutes must tie with the direct call
        direct = panel("ashok_vihar", "pitampura", "jog")
        out = hp.handle_routes("ashok_vihar", "pitampura", "jog")
        self.assertEqual(out["route_fastest"]["minutes"], direct["route_fastest"]["minutes"])


if __name__ == "__main__":
    unittest.main()
