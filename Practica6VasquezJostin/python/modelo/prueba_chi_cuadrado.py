# ============================================================
# MODELO - Prueba Chi-cuadrado (Algoritmo 2 de la guia)
# ============================================================

from modelo.prueba_estadistica import PruebaEstadistica
from modelo.resultado_prueba import ResultadoPrueba
from modelo.distribuciones import valor_p_chi_cuadrado


class PruebaChiCuadrado(PruebaEstadistica):

    def __init__(self, numero_intervalos=10, alfa=0.05):
        # Paso 2: numero de intervalos en que se divide [0, 1]
        self.numero_intervalos = numero_intervalos
        self.alfa = alfa

    def aplicar(self, numeros):
        # Paso 1: recibir la secuencia
        n = len(numeros)
        k = self.numero_intervalos

        # Paso 4: frecuencia esperada = total de datos / numero de intervalos
        esperada = n / k

        # Pasos 3, 5 y 6: contar cuantos numeros caen en cada intervalo
        observadas = [0] * k
        for numero in numeros:
            indice = int(numero * k)   # ejemplo: 0.37 * 10 = 3.7 -> intervalo 3
            if indice >= k:            # por seguridad, si numero fuera 1.0
                indice = k - 1
            observadas[indice] += 1

        # Pasos 7 y 8: calcular el estadistico chi-cuadrado
        chi_cuadrado = 0.0
        for frecuencia in observadas:
            diferencia = frecuencia - esperada
            chi_cuadrado += (diferencia ** 2) / esperada

        # Paso 9: grados de libertad
        grados_libertad = k - 1

        # Paso 10: valor p con la distribucion chi-cuadrado
        valor_p = valor_p_chi_cuadrado(chi_cuadrado, grados_libertad)

        # Pasos 11 al 14: la decision la toma ResultadoPrueba y la muestra la Vista
        detalles = {
            "observadas": observadas,
            "esperada": esperada,
            "grados_libertad": grados_libertad,
        }
        return ResultadoPrueba("Chi-cuadrado", chi_cuadrado, valor_p, self.alfa, detalles)
