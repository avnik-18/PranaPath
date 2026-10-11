"""Rules for the constrained route: cap honored, dose best-in-class, deterministic."""
import unittest
from pathlib import Path

from backend.engine import graph as gy
from backend.engine import exposure as ex
from backend.engine import routes as rr
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
        from backend.engine import routes as rr
        cls.fast_minutes = rr.compare_routes(cls.g, "ashok_vihar", "model_town",
                                             cls.mode, budget=None)["route_fastest"]["minutes"]

    def _run(self, budget):
        return search_with_cap(self.g, self.o, self.d, self.scale,
                               cap_min=self.fast_minutes * budget + 0.25,
                               health_w=HEALTH_SENSITIVITY, pm_ref=PM_REFERENCE,
                               ir=ex.IR_M3H[self.mode])

    def test_cap_one_cannot_widen_past_fastest(self):
        r = self._run(1.0)
        self.assertIsNotNone(r)
        self.assertLessEqual(r["minutes"], self.fast_minutes + 0.3,
                             "cap 1.0 stays within the fastest time's display rounding")

    def test_cap_honored_and_dose_never_worse(self):
        panel = rr.compare_routes(self.g, "ashok_vihar", "model_town", self.mode, budget=None)
        fast_dose = panel["route_fastest"]["dose_ug"]
        for budget in (1.05, 1.1, 1.35):
            r = self._run(budget)
            self.assertIsNotNone(r, f"cap {budget} reachable")
            self.assertLessEqual(r["minutes"], round(self.fast_minutes * budget, 1) + 1e-9,
                                 f"cap {budget} must be honored")
            dose, _ = ex.dose_on_edges(r["edges"], self.mode)
            self.assertLessEqual(round(dose, 1), fast_dose,
                                 f"budget {budget}: dose must not be worse than fastest")

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
