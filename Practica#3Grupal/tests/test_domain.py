import unittest
from domain.models import Config
from domain.queueing import theoretical


class TheoryTests(unittest.TestCase):
    """Comprueba las fórmulas analíticas y la validación de M/M/1."""

    def test_case_1(self):
        """Caso estable λ=2, μ=3: ρ=2/3, L=2, Lq=4/3, W=1, Wq=2/3."""
        t = theoretical(Config(2, 3))
        self.assertAlmostEqual(t.rho, 2 / 3)  # ρ = λ / μ.
        self.assertAlmostEqual(t.L, 2)  # L = λ / (μ - λ).
        self.assertAlmostEqual(t.Lq, 4 / 3)  # Lq = λ² / (μ(μ - λ)).
        self.assertAlmostEqual(t.W, 1)  # W = 1 / (μ - λ).
        self.assertAlmostEqual(t.Wq, 2 / 3)  # Wq = λ / (μ(μ - λ)).

    def test_heavy_load(self):
        """Cerca de saturación λ=2.9, μ=3: L=29 y W=10."""
        t = theoretical(Config(2.9, 3))
        self.assertAlmostEqual(t.L, 29)  # L = 2.9 / 0.1.
        self.assertAlmostEqual(t.W, 10)  # W = 1 / 0.1.

    def test_unstable(self):
        """Con λ=μ no hay régimen estacionario y W debe ser None."""
        t = theoretical(Config(3, 3))
        self.assertFalse(t.stable)  # ρ = 1: cola inestable.
        self.assertIsNone(t.W)  # La espera media no está definida.

    def test_bad_config(self):
        """Una tasa negativa debe ser rechazada antes de calcular."""
        with self.assertRaises(ValueError):
            theoretical(Config(-1, 3))  # λ inválida.


if __name__ == '__main__':
    unittest.main()
