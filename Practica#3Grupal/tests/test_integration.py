import unittest
from domain.models import Config
try:
    from application.use_cases import simulate  # Motor SimPy a través del caso de uso.
    SIMPY_AVAILABLE = True  # Marca que la dependencia está instalada.
except ModuleNotFoundError as exc:
    if exc.name != "simpy":  # Solo se tolera la ausencia de SimPy.
        raise
    SIMPY_AVAILABLE = False  # Permite omitir las pruebas de integración.

@unittest.skipUnless(SIMPY_AVAILABLE, "SimPy no está instalado")


class SimulationTests(unittest.TestCase):
    """Comprueba reproducibilidad, conservación de paquetes y FIFO."""

    def test_reproducible_and_conserves_packages(self):
        """La misma semilla produce los mismos eventos y no pierde paquetes."""
        config = Config(2, 3, 200, 42)  # λ=2, μ=3, T=200, semilla=42.
        one = simulate(config)
        two = simulate(config)
        self.assertEqual(one['events'], two['events'])  # Reproducibilidad exacta.
        summary = one['summary']
        self.assertEqual(summary['arrived'], summary['completed'] + summary['pending'])  # Conservación.
        self.assertEqual(one['events'][-1]['type'], 'end')  # Cierre del registro.
        self.assertTrue(0 <= summary['utilization'] <= 1)  # ρ es una proporción.
        self.assertTrue(all(e['queue'] >= 0 for e in one['events']))  # Cola no negativa.

    def test_fifo(self):
        """Los paquetes se atienden en el mismo orden en que llegan."""
        jobs = simulate(Config(2.9, 3, 200, 9))['jobs']  # Escenario casi saturado.
        self.assertEqual([j['id'] for j in jobs], sorted(j['id'] for j in jobs))  # Orden FIFO.


if __name__ == '__main__':
    unittest.main()
