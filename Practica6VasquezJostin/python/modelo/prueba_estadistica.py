# ============================================================
# MODELO - Interfaz comun para las pruebas estadisticas
# ============================================================
#  - I (Segregacion de interfaces): la interfaz es pequena,
#    solo pide el metodo que todas las pruebas necesitan.
#  - O (Abierto/Cerrado): para agregar otra prueba (por ejemplo
#    "prueba de rachas") se crea otra clase hija; el controlador
#    no se modifica.
# ============================================================

from abc import ABC, abstractmethod


class PruebaEstadistica(ABC):
    """Contrato que deben cumplir todas las pruebas de bondad de ajuste."""

    @abstractmethod
    def aplicar(self, numeros):
        """Recibe la lista de numeros y devuelve un ResultadoPrueba."""
        pass
