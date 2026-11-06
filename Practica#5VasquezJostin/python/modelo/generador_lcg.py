# ------------------------------------------------------------
# Archivo: generador_lcg.py
# Implementacion del Generador Congruencial Lineal (LCG).
#
#   Formula:        X(n+1) = (a * X(n) + c) mod m
#   Normalizacion:  U(n)   = X(n) / m
# ------------------------------------------------------------

from modelo.generador_aleatorio import GeneradorAleatorio
from modelo.observacion import Observacion


class GeneradorLCG(GeneradorAleatorio):
    """Generador Congruencial Lineal. Hereda de GeneradorAleatorio."""

    def __init__(self, parametros):
        # Guardamos los parametros (objeto ParametrosLCG)
        self.parametros = parametros
        # El estado actual empieza siendo la semilla X(0)
        self.estado_actual = parametros.semilla

    def reiniciar(self, semilla):
        """Cambia la semilla y vuelve al inicio de la secuencia."""
        if semilla < 0 or semilla >= self.parametros.m:
            raise ValueError("La semilla debe cumplir 0 <= semilla < m")
        self.estado_actual = semilla

    def siguiente(self):
        """Aplica la formula del LCG una vez y devuelve el nuevo X."""
        a = self.parametros.a
        c = self.parametros.c
        m = self.parametros.m
        # En Python los enteros no se desbordan, asi que el calculo es exacto
        self.estado_actual = (a * self.estado_actual + c) % m
        return self.estado_actual

    def normalizar(self, valor_x):
        """Divide X entre m para obtener un numero en el intervalo [0, 1)."""
        return valor_x / self.parametros.m

    def generar_secuencia(self, cantidad):
        """Genera 'cantidad' numeros: X(1), X(2), ..., X(cantidad)."""
        observaciones = []
        for indice in range(1, cantidad + 1):
            valor_x = self.siguiente()
            valor_u = self.normalizar(valor_x)
            observaciones.append(Observacion(indice, valor_x, valor_u))
        return observaciones
