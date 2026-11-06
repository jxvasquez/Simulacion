# ============================================================
# MODELO - Resultado de una prueba estadistica
# ============================================================
# Clase sencilla que solo guarda datos (S: responsabilidad unica).
# Asi las pruebas calculan y la vista muestra, sin mezclarse.
# ============================================================


class ResultadoPrueba:
    """Guarda lo que devuelve cualquier prueba de bondad de ajuste."""

    def __init__(self, nombre_prueba, estadistico, valor_p, alfa, detalles=None):
        self.nombre_prueba = nombre_prueba  # "Chi-cuadrado" o "Kolmogorov-Smirnov"
        self.estadistico = estadistico      # valor de chi2 o de D
        self.valor_p = valor_p              # probabilidad asociada
        self.alfa = alfa                    # nivel de significancia (0.05)
        # Diccionario con informacion extra (frecuencias, grados de libertad, etc.)
        self.detalles = detalles if detalles is not None else {}

    def se_rechaza_h0(self):
        """Criterio de decision: si p < alfa se rechaza H0."""
        return self.valor_p < self.alfa

    def decision(self):
        """Devuelve la decision en texto."""
        if self.se_rechaza_h0():
            return "Se rechaza H0: los numeros NO siguen una distribucion uniforme"
        return "No se rechaza H0: los numeros son compatibles con U(0,1)"
