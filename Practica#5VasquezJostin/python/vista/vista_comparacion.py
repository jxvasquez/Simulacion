# ------------------------------------------------------------
# Archivo: vista_comparacion.py
# Responsabilidad unica: mostrar la tabla Python vs Java.
#
# Se puso en un archivo aparte (y no dentro de VistaConsola) para que
# cada vista tenga una sola razon para cambiar (S de SOLID).
# ------------------------------------------------------------


class VistaComparacion:
    """Muestra en consola el resultado de comparar Python con Java."""

    def mostrar_tabla_lenguajes(self, filas, cantidad):
        print(f"{'n':>4} | {'X Python':>11} | {'X Java':>11} | {'U Python':>12} | {'U Java':>12} | Igual")
        print("-" * 72)
        for fila in filas[:cantidad]:
            n, x_py, x_java, u_py, u_java, coinciden = fila
            igual = "SI" if coinciden else "NO"
            print(f"{n:>4} | {x_py:>11} | {x_java:>11} | {u_py:>12.10f} | {u_java:>12.10f} | {igual}")
