# ------------------------------------------------------------
# Archivo: analizador_periodo.py
# Responsabilidad unica: analizar el PERIODO de un generador.
#
# Periodo = cantidad de numeros distintos que salen antes de que la
#           secuencia empiece a repetirse.
# ------------------------------------------------------------

import math


class AnalizadorPeriodo:
    """Contiene metodos para estudiar el periodo de un LCG."""

    def cumple_hull_dobell(self, parametros):
        """
        Teorema de Hull-Dobell: el LCG tiene periodo completo (igual a m)
        si y solo si se cumplen las 3 condiciones siguientes.
        Devuelve un diccionario con el resultado de cada condicion.
        """
        a = parametros.a
        c = parametros.c
        m = parametros.m

        # Condicion 1: c y m deben ser primos relativos (mcd = 1)
        condicion_1 = math.gcd(c, m) == 1

        # Condicion 2: (a - 1) debe ser divisible por TODOS los factores
        # primos de m
        factores = self._factores_primos(m)
        condicion_2 = True
        for factor in factores:
            if (a - 1) % factor != 0:
                condicion_2 = False

        # Condicion 3: si m es multiplo de 4, (a - 1) tambien debe serlo
        if m % 4 == 0:
            condicion_3 = (a - 1) % 4 == 0
        else:
            condicion_3 = True

        return {
            "mcd(c, m) = 1": condicion_1,
            "(a-1) divisible por factores primos de m": condicion_2,
            "si 4 divide a m, 4 divide a (a-1)": condicion_3,
            "periodo completo": condicion_1 and condicion_2 and condicion_3,
        }

    def calcular_periodo(self, generador, semilla, limite):
        """
        Calcula el periodo generando numeros hasta que uno se repite.
        Solo sirve para modulos pequenos (por eso usamos un limite).
        Devuelve el periodo, o None si no se encontro dentro del limite.
        """
        generador.reiniciar(semilla)
        # Diccionario: valor -> posicion en la que aparecio por primera vez
        vistos = {semilla: 0}
        for paso in range(1, limite + 1):
            valor = generador.siguiente()
            if valor in vistos:
                # La distancia entre las dos apariciones es el periodo
                return paso - vistos[valor]
            vistos[valor] = paso
        return None

    def buscar_repeticion(self, observaciones):
        """
        Revisa si algun valor X se repite dentro de una lista ya generada.
        Devuelve la posicion de la primera repeticion o None si no hay.
        """
        vistos = set()
        for observacion in observaciones:
            if observacion.valor_x in vistos:
                return observacion.indice
            vistos.add(observacion.valor_x)
        return None

    def _factores_primos(self, numero):
        """Devuelve la lista de factores primos distintos de 'numero'."""
        factores = []
        divisor = 2
        while divisor * divisor <= numero:
            if numero % divisor == 0:
                factores.append(divisor)
                while numero % divisor == 0:
                    numero = numero // divisor
            divisor = divisor + 1
        if numero > 1:
            factores.append(numero)
        return factores
