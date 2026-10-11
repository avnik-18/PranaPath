"""Rules: 14 services exactly; deterministic output; no fabricated dose numbers; honest mock flag."""

import json
import unittest

from backend.api.handler import handle_routes
from backend.aws import mock_state
from backend.aws import panel as aws_panel

# the REAL handler payload (engine + guardian template fallback), computed once, offline
PAYLOAD = handle_routes("ashok_vihar", "pitampura", "jog")

EXPECTED_SERVICES = (
    "Amplify", "API Gateway", "Lambda[engine]", "Lambda[explainer]",
    "Bedrock Nova Lite", "DynamoDB", "EventBridge 15-min", "Lambda[aqi-refresh]",
    "EventBridge 06:00", "Step Functions", "SNS", "CloudWatch", "X-Ray", "Powertools",
)


class MockInventoryRules(unittest.TestCase):
    def test_exactly_14_architecture_services(self):
        rows = mock_state.service_inventory()
        self.assertEqual(len(rows), 14)
        self.assertEqual({r["service"] for r in rows}, set(EXPECTED_SERVICES))
        self.assertTrue(all(r["status"].startswith(("GREEN", "DECLARED")) for r in rows))

    def test_without_probes_everything_stays_declared(self):
        live = {"mode": "live", "region": "ap-south-1", "probe": {}, "reason": ""}
        rows = mock_state.service_inventory(live)
        self.assertTrue(all(r["status"].startswith("DECLARED") for r in rows))

    def test_probe_backed_service_may_claim_live(self):
        live = {"mode": "live", "region": "ap-south-1",
                "probe": {"dynamodb_ok": True, "lambda_ok": True, "bedrock_ok": True},
                "reason": ""}
        rows = mock_state.service_inventory(live)
        backed = {r["service"] for r in rows if r["status"] == "GREEN (live)"}
        self.assertEqual(backed, {"DynamoDB", "Lambda[engine]", "Lambda[explainer]", "Bedrock Nova Lite"})


class MockDeterminismRule(unittest.TestCase):
    def test_run_twice_same_string(self):
        self.assertEqual(
            json.dumps(mock_state.recent_activities(PAYLOAD), sort_keys=True),
            json.dumps(mock_state.recent_activities(PAYLOAD), sort_keys=True),
        )


class MockTraceabilityRule(unittest.TestCase):
    def test_no_fabricated_dose_or_time_numbers(self):
        blob = json.dumps(mock_state.recent_activities(PAYLOAD))
        self.assertIn(str(PAYLOAD["route_fastest"]["dose_ug"]), blob)
        self.assertIn(str(PAYLOAD["route_healthy"]["dose_ug"]), blob)
        self.assertIn(str(PAYLOAD["route_fastest"]["minutes"]), blob)


class PanelMockFlagRules(unittest.TestCase):
    def test_no_live_state_means_every_mock_labeled(self):
        p = aws_panel.build_panel(PAYLOAD, origin="ashok_vihar")
        self.assertEqual(p["switch"], "mock")
        self.assertTrue(all(a["mock"] for a in p["activities"]))
        self.assertTrue(all(r["mock"] for r in p["receipts"]))
        self.assertEqual(p["counts"]["services"], 14)
        self.assertIn("traceable", p["reason"])

    def test_live_state_flips_flags_but_only_probe_backed_statuses(self):
        live = {"mode": "live", "region": "ap-south-1",
                "probe": {"dynamodb_ok": True, "lambda_ok": True, "bedrock_ok": True},
                "reason": ""}
        p = aws_panel.build_panel(PAYLOAD, live_state=live, origin="ashok_vihar")
        self.assertEqual(p["switch"], "live")
        self.assertFalse(any(a["mock"] for a in p["activities"]))
        self.assertEqual(p["counts"]["green_live"], 4)
        self.assertEqual(p["counts"]["green_mock"], 10)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
