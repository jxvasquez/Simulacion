# ------------------------------------------------------------
# Archivo: comparador_secuencias.py
# Responsabilidad unica: comparar dos secuencias (Python vs Java).
# ------------------------------------------------------------


class ComparadorSecuencias:
    """Compara fila por fila dos listas de tuplas (n, X, U)."""

    def __init__(self, tolerancia=1e-9):
        # Tolerancia para comparar numeros decimales (U)
        self.tolerancia = tolerancia

    def comparar(self, secuencia_a, secuencia_b):
        """
        Devuelve una lista de filas con el resultado de la comparacion:
        (n, X_a, X_b, U_a, U_b, coinciden)
        """
        resultado = []
        cantidad = min(len(secuencia_a), len(secuencia_b))
        for i in range(cantidad):
            n, x_a, u_a = secuencia_a[i]
            _, x_b, u_b = secuencia_b[i]
            coinciden = x_a == x_b and abs(u_a - u_b) <= self.tolerancia
            resultado.append((n, x_a, x_b, u_a, u_b, coinciden))
        return resultado

    def contar_diferencias(self, filas_comparadas):
        """Cuenta cuantas filas NO coinciden."""
        diferencias = 0
        for fila in filas_comparadas:
            if not fila[5]:
                diferencias = diferencias + 1
        return diferencias
