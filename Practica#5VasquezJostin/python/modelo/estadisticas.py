# ------------------------------------------------------------
# Archivo: estadisticas.py
# Responsabilidad unica: calcular estadisticas basicas de U(n).
# Para una distribucion uniforme en [0, 1):
#   media esperada    = 0.5
#   varianza esperada = 1/12 = 0.0833...
# ------------------------------------------------------------


class Estadisticas:
    """Calcula media, varianza, minimo y maximo de una lista de numeros."""

    def media(self, valores):
        return sum(valores) / len(valores)

    def varianza(self, valores):
        promedio = self.media(valores)
        suma_cuadrados = 0
        for valor in valores:
            suma_cuadrados = suma_cuadrados + (valor - promedio) ** 2
        return suma_cuadrados / len(valores)

    def minimo(self, valores):
        return min(valores)

    def maximo(self, valores):
        return max(valores)
