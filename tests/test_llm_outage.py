import unittest

from backend.guardian import explain as ex
from backend.guardian.bedrock import BedrockUnavailable
from tests.common import panel


class OutageFallbackTest(unittest.TestCase):
    """Rule (Suraksha): Bedrock down => the template speaks; product never loses its mouth."""

    def setUp(self):
        self.p = panel()

    def test_outage_falls_back_to_template(self):
        def boom(*a, **k):
            raise BedrockUnavailable("no bedrock in this test")
        ex.bedrock.invoke_explainer = boom
        out = ex.explain_route(self.p, use_ai=True)
        self.assertEqual(out["source"], "template")
        self.assertTrue(out["validated"])
        self.assertIn("%", out["sentence"])          # a real trade-off must exist in the fallback

    def test_invalid_model_output_falls_back(self):
        ex.bedrock.invoke_explainer = lambda *a, **k: "Route B saves 97.3% and edge Z9 hates $ smog"
        out = ex.explain_route(self.p, use_ai=True)
        self.assertEqual(out["source"], "template")

    def test_valid_model_output_wins(self):
        def reply_with(good):
            return lambda *a, **k: good

        template = ex.explain_route(self.p, use_ai=False)      # facts guaranteed to validate
        ex.bedrock.invoke_explainer = reply_with(template["sentence"])
        out = ex.explain_route(self.p, use_ai=True)
        self.assertEqual(out["source"], "bedrock")
        self.assertTrue(out["validated"])


if __name__ == "__main__":
    unittest.main()
