"""Teoría M/M/1, válida en régimen estacionario si λ < μ."""
from .models import Config, Theory


def theoretical(config: Config) -> Theory:
    """Calcula los indicadores teóricos de una cola M/M/1.

    Parámetros:
        config: Configuración con las tasas de llegada λ y de servicio μ.

    Devuelve:
        Theory: Utilización ρ y métricas L, Lq, W y Wq. Si λ ≥ μ, el sistema
        es inestable y las métricas distintas de ρ se devuelven como None.

    Lanza:
        ValueError: Si la configuración no pasa Config.validate().
    """
    config.validate()

    # Tasas medias: λ = llegadas por unidad de tiempo; μ = servicios por unidad.
    lam, mu = config.arrival_rate, config.service_rate

    # Utilización del servidor: ρ = λ / μ.
    rho = lam / mu

    # Con λ ≥ μ la cola crece indefinidamente: no existe régimen estacionario.
    if lam >= mu:
        return Theory(rho, None, None, None, None, False)

    # Fórmulas de estado estacionario para M/M/1:
    #   L  = λ / (μ - λ)          número medio de paquetes en el sistema
    #   Lq = λ² / (μ(μ - λ))      número medio de paquetes en cola
    #   W  = 1 / (μ - λ)          tiempo medio en el sistema
    #   Wq = λ / (μ(μ - λ))       tiempo medio de espera en cola
    return Theory(
        rho,                          # ρ: utilización del servidor.
        lam / (mu - lam),             # L: paquetes medios en el sistema.
        lam * lam / (mu * (mu - lam)),  # Lq: paquetes medios en cola.
        1 / (mu - lam),               # W: tiempo medio en el sistema.
        lam / (mu * (mu - lam)),      # Wq: tiempo medio de espera.
        True,                         # stable: λ < μ, existe régimen estacionario.
    )
