import unittest

from backend.guardian.validate import validate_sentence
from backend.guardian import explain as ex
from tests.common import panel


class ValidatorGateTest(unittest.TestCase):
    """Rule (Magpie gate): the AI may not say any number/ID the engine didn't produce."""

    def setUp(self):
        self.p = panel()

    def test_template_sentence_passes(self):
        s = ex.template_sentence(self.p)
        ok, why = validate_sentence(s, self.p)
        self.assertTrue(ok, why)

    def test_invented_number_rejected(self):
        ok, why = validate_sentence("Route B saves 97.3% of dose", self.p)
        self.assertFalse(ok)
        self.assertIn("invented number", why)

    def test_invented_id_rejected(self):
        ok, why = validate_sentence("avoid edge Z9 on the way", self.p)
        self.assertFalse(ok)
        self.assertIn("invented id", why)

    def test_banned_currency_rejected(self):
        ok, why = validate_sentence("This detour will save you $2", self.p)
        self.assertFalse(ok)


if __name__ == "__main__":
    unittest.main()
