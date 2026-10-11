"""Rules: thin door only; contract keys; clean unknown_node; thinness == engine numbers."""

import json
import unittest

from backend.api import aws_handler as ah
from backend.api.aws_schemas import AWS_API_VERSION
from tests.common import graph


class AwsPanelContract(unittest.TestCase):
    def test_panel_payload_contract_keys(self):
        p = ah.handle_aws_panel("ashok_vihar", "pitampura", "jog")
        self.assertTrue(p["ok"])
        self.assertEqual(p["api_version"], AWS_API_VERSION)
        data = p["data"]
        for key in ("switch", "mode", "region", "probe", "inventory",
                    "activities", "receipts", "counts", "trip"):
            self.assertIn(key, data)
        self.assertEqual(data["counts"]["services"], 14)
        self.assertEqual(data["trip"],
                         {"origin": "ashok_vihar", "dest": "pitampura", "mode": "jog"})

    def test_every_activity_carries_mock_flag(self):
        data = ah.handle_aws_panel("ashok_vihar", "pitampura", "jog")["data"]
        self.assertTrue(all(isinstance(a.get("mock"), bool) for a in data["activities"]))
        self.assertTrue(data["counts"]["events"] >= 10)

    def test_unknown_node_is_clean_error(self):
        p = ah.handle_aws_panel("nowhere_x", "pitampura", "jog")
        self.assertFalse(p["ok"])
        self.assertEqual(p["error"]["code"], "unknown_node")

    def test_status_ok_with_mode_and_region(self):
        s = ah.handle_aws_status()
        self.assertTrue(s["ok"])
        self.assertEqual(s["api_version"], AWS_API_VERSION)
        self.assertIn(s["data"]["mode"], ("live", "mock"))
        self.assertEqual(s["data"]["region"], "ap-south-1")


class ThinnessRule(unittest.TestCase):
    def test_door_never_maths_minutes_match_engine(self):
        from backend.engine.routes import compare_routes
        eng = compare_routes(graph(), "ashok_vihar", "pitampura", "jog")
        blob = json.dumps(ah.handle_aws_panel("ashok_vihar", "pitampura", "jog")["data"])
        self.assertIn(str(eng["route_fastest"]["minutes"]), blob)
        self.assertIn(str(eng["route_healthy"]["dose_ug"]), blob)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
