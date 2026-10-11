"""Rules for the constrained route: cap honored, dose best-in-class, deterministic."""
import unittest
from pathlib import Path

from backend.engine import graph as gy
from backend.engine import exposure as ex
from backend.engine.constrained import search_with_cap
from backend.engine.routes import HEALTH_SENSITIVITY, PM_REFERENCE, PACE

_ROOT = str(Path(__file__).resolve().parents[1])


class TestConstrainedRules(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.g = gy.load_graph(f"{_ROOT}/data/delhi_graph.json")
        cls.o = gy.resolve_node(cls.g, "ashok_vihar")
        cls.d = gy.resolve_node(cls.g, "model_town")
        cls.mode = "jog"
        cls.scale = PACE[cls.mode]
        cls.fast = search_with_cap(cls.g, cls.o, cls.d, cls.scale,
                                   cap_min=1e9, health_w=HEALTH_SENSITIVITY,
                                   pm_ref=PM_REFERENCE)

    def _run(self, budget):
        return search_with_cap(self.g, self.o, self.d, self.scale,
                               cap_min=self.fast["minutes"] * budget,
                               health_w=HEALTH_SENSITIVITY, pm_ref=PM_REFERENCE)

    def test_cap_one_is_the_fastest_route(self):
        r = self._run(1.0)
        self.assertEqual(r["minutes"], self.fast["minutes"], "cap 1.0 cannot widen")

    def test_cap_honored_and_dose_never_worse(self):
        fast_dose, _ = ex.dose_on_edges(self.fast["edges"], self.mode)
        for budget in (1.05, 1.1, 1.25):
            r = self._run(budget)
            self.assertIsNotNone(r, f"cap {budget} reachable")
            self.assertLessEqual(r["minutes"], round(self.fast["minutes"] * budget, 1) + 1e-9,
                                 f"cap {budget} must be honored")
            dose, _ = ex.dose_on_edges(r["edges"], self.mode)
            self.assertLessEqual(round(dose, 1), round(fast_dose, 1),
                                 f"budget {budget}: dose must not beat than fastest")

    def test_looser_cap_never_raises_dose(self):
        r_11 = self._run(1.1)
        r_125 = self._run(1.25)
        d11, _ = ex.dose_on_edges(r_11["edges"], self.mode)
        d125, _ = ex.dose_on_edges(r_125["edges"], self.mode)
        self.assertLessEqual(round(d125, 1), round(d11, 1), "more budget → no worse dose")

    def test_deterministic(self):
        self.assertEqual(self._run(1.1), self._run(1.1))


if __name__ == "__main__":
    unittest.main()
