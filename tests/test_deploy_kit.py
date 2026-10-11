"""Rules: dry-run prints PLAN + never applies; template declares the stack; zips build clean."""

import contextlib
import io
import os
import tempfile
import unittest
from unittest import mock
from pathlib import Path
import importlib.util

from backend.aws import receipts

_SPEC = importlib.util.spec_from_file_location(
    "ecoroute_deploy", str(Path(__file__).resolve().parents[1] / "infra" / "deploy.py"))
deploy = importlib.util.module_from_spec(_SPEC)


def _setUpModule():
    _SPEC.loader.exec_module(deploy)


class DeployDryRunRules(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        _setUpModule()

    def test_dry_run_is_plan_only_and_never_prints_secrets(self):
        with tempfile.TemporaryDirectory() as folder:
            with mock.patch.object(receipts, "RECEIPTS_DIR", folder):
                buf = io.StringIO()
                with contextlib.redirect_stdout(buf):
                    rc = deploy.main(["--dry-run"])
                self.assertEqual(rc, 0)
                out = buf.getvalue()
                self.assertIn("PLAN", out)
                self.assertIn("NOTHING", out.upper())
                self.assertNotIn("AKIA", out)
                self.assertEqual(receipts.tail(1)[0]["kind"], "deploy.dry-run")

    def test_template_declares_the_deployed_ring(self):
        text = deploy.template_text()
        for needle in ("EcoRouteTrips", "EngineFunction", "ExplainerFunction", "AqiFunction",
                       "HttpApi", "AdvisoryStateMachine", "AdvisoryTopic",
                       "AdvisorySubscription", "Rule0600Start", "Rule0600Role"):
            self.assertIn(needle, text)
        self.assertGreaterEqual(deploy.resources_in_template(), 10)

    def test_apply_without_creds_is_blocked_not_crash(self):
        with tempfile.TemporaryDirectory() as folder:
            with mock.patch.object(receipts, "RECEIPTS_DIR", folder), \
                 mock.patch.dict(os.environ, {}, clear=False):
                os.environ.pop("AWS_ACCESS_KEY_ID", None)
                os.environ.pop("AWS_SECRET_ACCESS_KEY", None)
                buf = io.StringIO()
                with contextlib.redirect_stdout(buf):
                    rc = deploy.main(["--apply"])
                self.assertEqual(rc, 1)
                self.assertIn("APPLY blocked", buf.getvalue())

    def test_zips_build_with_expected_names_and_size(self):
        with tempfile.TemporaryDirectory() as folder:
            with mock.patch.object(receipts, "RECEIPTS_DIR", folder):
                zips = deploy.build_zips()
        names = [n for n, _ in zips]
        self.assertEqual(names, ["awslambda_engine.zip", "awslambda_explainer.zip", "refresh_aqi.zip"])
        for _, size in zips:
            self.assertGreater(size, 0)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
