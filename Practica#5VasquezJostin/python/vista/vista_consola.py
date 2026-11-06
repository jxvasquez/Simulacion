# ------------------------------------------------------------
# Archivo: vista_consola.py
# Responsabilidad unica: mostrar informacion en la consola.
# ------------------------------------------------------------


class VistaConsola:
    """Imprime titulos, tablas y resultados en la terminal."""

    def mostrar_titulo(self, texto):
        print()
        print("=" * 70)
        print(f" {texto}")
        print("=" * 70)

    def mostrar_mensaje(self, texto):
        print(texto)

    def mostrar_parametros(self, parametros):
        print(f"  a (multiplicador) = {parametros.a}")
        print(f"  c (incremento)    = {parametros.c}")
        print(f"  m (modulo)        = {parametros.m}")
        print(f"  semilla X(0)      = {parametros.semilla}")

    def mostrar_tabla(self, observaciones, cantidad):
        """Muestra las primeras 'cantidad' observaciones."""
        print(f"{'n':>5} | {'X(n)':>12} | {'U(n)':>14}")
        print("-" * 37)
        for obs in observaciones[:cantidad]:
            print(f"{obs.indice:>5} | {obs.valor_x:>12} | {obs.valor_u:>14.10f}")

    def mostrar_comparacion_semillas(self, obs_1, obs_2, semilla_1, semilla_2, cantidad):
        """Muestra lado a lado dos secuencias generadas con semillas distintas."""
        print(f"{'n':>5} | {'U(n) semilla ' + str(semilla_1):>22} | {'U(n) semilla ' + str(semilla_2):>22}")
        print("-" * 55)
        for i in range(cantidad):
            print(f"{obs_1[i].indice:>5} | {obs_1[i].valor_u:>22.10f} | {obs_2[i].valor_u:>22.10f}")

    def mostrar_hull_dobell(self, resultado):
        """Muestra si se cumplen las condiciones del teorema de Hull-Dobell."""
        for condicion, cumple in resultado.items():
            texto = "SI" if cumple else "NO"
            print(f"  {condicion:<45}: {texto}")

    def mostrar_estadisticas(self, nombre, media, varianza, minimo, maximo):
        """Muestra estadisticas basicas de los valores U(n)."""
        print(f"  [{nombre}]")
        print(f"    Media    = {media:.6f}   (esperado 0.5)")
        print(f"    Varianza = {varianza:.6f}   (esperado 1/12 = 0.083333)")
        print(f"    Minimo   = {minimo:.6f}")
        print(f"    Maximo   = {maximo:.6f}")
