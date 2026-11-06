# ============================================================
# MODELO - Prueba Kolmogorov-Smirnov (Algoritmo 3 de la guia)
# ============================================================

from modelo.prueba_estadistica import PruebaEstadistica
from modelo.resultado_prueba import ResultadoPrueba
from modelo.distribuciones import valor_p_kolmogorov


class PruebaKolmogorovSmirnov(PruebaEstadistica):

    def __init__(self, alfa=0.05):
        self.alfa = alfa

    def aplicar(self, numeros):
        # Paso 2: ordenar los numeros de menor a mayor
        ordenados = sorted(numeros)

        # Paso 3: cantidad total de numeros
        n = len(ordenados)

        # Paso 4: inicializar las diferencias maximas
        d_positivo = 0.0
        d_negativo = 0.0

        # Pasos 5 y 6: recorrer los numeros ordenados
        for i in range(n):
            posicion = i + 1                 # la posicion empieza en 1
            empirica = posicion / n          # Fn(x) = i / n
            teorica = ordenados[i]           # F(x) = x para U(0,1)

            # Diferencia positiva: Fn(x) - F(x)
            dif_positiva = empirica - teorica
            # Diferencia negativa: F(x) - Fn(x) justo antes del salto
            dif_negativa = teorica - (posicion - 1) / n

            # Paso 7: quedarnos con la mayor de cada tipo
            if dif_positiva > d_positivo:
                d_positivo = dif_positiva
            if dif_negativa > d_negativo:
                d_negativo = dif_negativa

        # Paso 8: el estadistico D es la mayor de las dos diferencias
        d = max(d_positivo, d_negativo)

        # Paso 9: valor p
        valor_p = valor_p_kolmogorov(d, n)

        detalles = {
            "d_positivo": d_positivo,
            "d_negativo": d_negativo,
            "ordenados": ordenados,  # se guardan para poder graficar (paso 14)
        }
        return ResultadoPrueba("Kolmogorov-Smirnov", d, valor_p, self.alfa, detalles)
