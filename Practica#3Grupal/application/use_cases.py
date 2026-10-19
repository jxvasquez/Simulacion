"""Casos de uso; no conocen HTTP ni elementos visuales."""
from dataclasses import asdict
from domain.models import Config, DEFAULT_DURATION, DEFAULT_SEED
from domain.queueing import theoretical
from infrastructure.simpy_engine import MM1Engine

SCENARIOS = [
    {'name': 'Estable', 'arrival_rate': 2.0, 'service_rate': 3.0},          # ρ = 0.67.
    {'name': 'Mayor utilización', 'arrival_rate': 2.5, 'service_rate': 3.0},  # ρ = 0.83.
    {'name': 'Cerca de saturación', 'arrival_rate': 2.9, 'service_rate': 3.0},  # ρ = 0.97.
]


def simulate(config: Config) -> dict:
    """Ejecuta una simulación y combina sus resultados teóricos y simulados.

    Parámetros:
        config: Tasas λ y μ, duración y semilla de la simulación.

    Devuelve:
        dict: Configuración, teoría M/M/1, eventos, trabajos y resumen.
    """
    simulation = MM1Engine().run(config)  # Simulación de eventos discretos.
    return {
        'config': asdict(config),  # Parámetros efectivamente utilizados.
        'theory': theoretical(config).to_dict(),  # Cálculo analítico M/M/1.
        **simulation,  # Añade eventos, trabajos y resumen de la simulación.
    }


def compare(duration: float = DEFAULT_DURATION, seed: int = DEFAULT_SEED) -> list:
    """Compara teoría y simulación para los tres escenarios de la práctica.

    Parámetros:
        duration: Horizonte simulado compartido por los escenarios.
        seed: Semilla compartida para que la comparación sea reproducible.

    Devuelve:
        list: Una fila por escenario con parámetros, teoría y resumen simulado.
    """
    rows = []  # Filas acumuladas para la tabla comparativa.
    for scenario in SCENARIOS:
        # Cada escenario conserva su λ y μ, pero comparte T y semilla.
        cfg = Config(scenario['arrival_rate'], scenario['service_rate'], duration, seed)
        result = simulate(cfg)
        rows.append({
            'scenario': scenario['name'],  # Nombre visible del escenario.
            **scenario,  # Incluye arrival_rate y service_rate.
            'theory': result['theory'],  # Indicadores analíticos.
            'simulated': result['summary'],  # Indicadores observados en SimPy.
        })
    return rows
