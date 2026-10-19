"""Entidades y contratos independientes de SimPy y de la interfaz."""
from dataclasses import dataclass, asdict

DEFAULT_DURATION = 120.0  # Horizonte de simulación por defecto (unidades de tiempo).
DEFAULT_SEED = 42  # Semilla por defecto para reproducir la simulación.


@dataclass(frozen=True)
class Config:
    """Parámetros de entrada de una simulación M/M/1."""

    arrival_rate: float = 2.0  # λ: llegadas por unidad de tiempo.
    service_rate: float = 3.0  # μ: servicios por unidad de tiempo.
    duration: float = DEFAULT_DURATION  # T: tiempo total simulado.
    seed: int = DEFAULT_SEED  # Semilla del generador aleatorio.

    def validate(self):
        """Valida los rangos admitidos por la simulación.

        Lanza:
            ValueError: Si λ, μ, T o la semilla están fuera de rango.
        """
        # λ y μ deben ser positivas y no superar 100 para evitar valores absurdos.
        if not 0 < self.arrival_rate <= 100 or not 0 < self.service_rate <= 100:
            raise ValueError('Las tasas λ y μ deben estar en (0, 100].')
        # El horizonte debe ser positivo y acotado.
        if not 1 <= self.duration <= 10000:
            raise ValueError('La duración debe estar entre 1 y 10000.')
        # La semilla debe caber en un entero sin signo de 32 bits.
        if not 0 <= self.seed <= 2**32 - 1:
            raise ValueError('La semilla debe ser un entero sin signo de 32 bits.')


@dataclass(frozen=True)
class Theory:
    """Resultados teóricos de M/M/1; None indica que no hay régimen estable."""

    rho: float  # Utilización del servidor: ρ = λ / μ.
    L: float | None  # Número medio de paquetes en el sistema.
    Lq: float | None  # Número medio de paquetes en cola.
    W: float | None  # Tiempo medio de permanencia en el sistema.
    Wq: float | None  # Tiempo medio de espera en cola.
    stable: bool  # True si λ < μ; False si el sistema es inestable.

    def to_dict(self):
        """Convierte la entidad a un diccionario serializable."""
        return asdict(self)
