"""The AWS-OSS eligibility card is code, not a claim: the files must exist and read right."""
import unittest
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]


class TestOssCard(unittest.TestCase):
    def test_cedar_policy_exists_and_permits_the_guest(self):
        ce = (_ROOT / "infra" / "policies.cedar").read_text(encoding="utf-8")
        self.assertIn("permit(", ce, "the cedar policy must state its permit rule")
        self.assertIn('User::"guest"', ce)
        self.assertIn('Console::"dashboard"', ce)

    def test_powertools_is_imported_in_deploy_zips(self):
        for name in ("awslambda_engine.py", "awslambda_explainer.py"):
            src = (_ROOT / "infra" / name).read_text(encoding="utf-8")
            self.assertIn("aws_lambda_powertools", src, f"{name} must import powertools (OSS card)")
            self.assertIn("except ImportError", src, f"{name} must stay offline-runnable")

    def test_requirements_naming_powertools(self):
        reqs = (_ROOT / "infra" / "requirements-awslambda.txt").read_text(encoding="utf-8")
        self.assertIn("aws-lambda-powertools", reqs)

    def test_template_declares_sam_oss_tooling(self):
        t = (_ROOT / "infra" / "template.yaml").read_text(encoding="utf-8")
        self.assertIn("AWS::Serverless", t, "the template is a SAM template (SAM CLI = OSS card)")


if __name__ == "__main__":
    unittest.main()
