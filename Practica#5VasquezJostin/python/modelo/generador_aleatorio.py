# ------------------------------------------------------------
# Archivo: generador_aleatorio.py
# Define la "interfaz" (contrato) que debe cumplir cualquier generador.
#
# Principios SOLID que se aplican aqui:
#  - O (Abierto/Cerrado): si manana queremos otro generador (por ejemplo
#    el de cuadrados medios) creamos una clase nueva que herede de esta,
#    sin modificar el controlador.
#  - L (Sustitucion de Liskov): cualquier clase hija puede usarse en lugar
#    de otra sin que el programa falle.
#  - D (Inversion de dependencias): el controlador depende de esta
#    abstraccion y no de una clase concreta.
# ------------------------------------------------------------

from abc import ABC, abstractmethod


class GeneradorAleatorio(ABC):
    """Clase abstracta: no se puede crear un objeto directamente de ella."""

    @abstractmethod
    def reiniciar(self, semilla):
        """Vuelve a empezar la secuencia usando una nueva semilla."""

    @abstractmethod
    def siguiente(self):
        """Calcula y devuelve el siguiente numero entero X(n+1)."""

    @abstractmethod
    def normalizar(self, valor_x):
        """Convierte X(n) en un numero entre 0 y 1."""

    @abstractmethod
    def generar_secuencia(self, cantidad):
        """Devuelve una lista con 'cantidad' observaciones."""
