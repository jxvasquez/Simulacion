# ============================================================
# MODELO - Estimacion de pi por Monte Carlo
# ============================================================
# Sirve para llenar la tabla de la seccion 6 de la guia
# (N, pi estimado, Error, Tiempo).
#
# Idea: se lanzan N puntos (x, y) al azar dentro de un cuadrado
# de lado 1. La proporcion de puntos que cae dentro del cuarto de
# circulo (x^2 + y^2 <= 1) es aproximadamente pi / 4.
#     pi estimado = 4 * (puntos dentro) / N
#     error       = | pi estimado - pi real |
#
# D (Inversion de dependencias): recibe cualquier GeneradorAleatorio.
# ============================================================

import math


class EstimadorPi:

    def __init__(self, generador):
        self.generador = generador

    def estimar(self, n):
        """Devuelve (pi_estimado, error) usando n puntos."""
        # Cada punto necesita 2 numeros: uno para x y otro para y
        numeros = self.generador.generar(2 * n)

        dentro = 0
        for i in range(n):
            x = numeros[2 * i]       # numeros en posicion par -> x
            y = numeros[2 * i + 1]   # numeros en posicion impar -> y
            if x * x + y * y <= 1.0:
                dentro += 1

        pi_estimado = 4.0 * dentro / n
        error = abs(pi_estimado - math.pi)
        return pi_estimado, error
