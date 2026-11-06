# ============================================================
# VISTA - Mostrar resultados en la consola
# ============================================================
# La vista NO calcula nada, solo imprime lo que le entregan.
# (S: responsabilidad unica)
# ============================================================


class VistaConsola:

    def mostrar_titulo(self, texto):
        print()
        print("=" * 70)
        print(texto)
        print("=" * 70)

    def mostrar_mensaje(self, texto):
        print(texto)

    def mostrar_secuencia(self, numeros, cantidad_a_mostrar=10):
        """Paso 11 de la Actividad 1: mostrar los numeros generados."""
        print(f"Primeros {cantidad_a_mostrar} numeros generados:")
        for i in range(min(cantidad_a_mostrar, len(numeros))):
            print(f"  r{i + 1:<3} = {numeros[i]:.10f}")

    def mostrar_chi_cuadrado(self, resultado):
        """Paso 14 del Algoritmo 2."""
        detalles = resultado.detalles
        observadas = detalles["observadas"]
        esperada = detalles["esperada"]
        k = len(observadas)

        print("\n--- Prueba Chi-cuadrado ---")
        print(f"{'Intervalo':<15}{'Observada':>12}{'Esperada':>12}{'(O-E)^2/E':>14}")
        for i in range(k):
            inicio = i / k
            fin = (i + 1) / k
            aporte = (observadas[i] - esperada) ** 2 / esperada
            print(f"[{inicio:.1f}, {fin:.1f}){'':<5}{observadas[i]:>12}"
                  f"{esperada:>12.1f}{aporte:>14.4f}")
        print(f"Estadistico chi2   = {resultado.estadistico:.4f}")
        print(f"Grados de libertad = {detalles['grados_libertad']}")
        print(f"Valor p            = {resultado.valor_p:.4f}")
        print(f"Decision (alfa={resultado.alfa}): {resultado.decision()}")

    def mostrar_kolmogorov(self, resultado):
        """Paso 13 del Algoritmo KS."""
        detalles = resultado.detalles
        print("\n--- Prueba Kolmogorov-Smirnov ---")
        print(f"D+ (mayor diferencia positiva) = {detalles['d_positivo']:.6f}")
        print(f"D- (mayor diferencia negativa) = {detalles['d_negativo']:.6f}")
        print(f"Estadistico D                  = {resultado.estadistico:.6f}")
        print(f"Valor p                        = {resultado.valor_p:.4f}")
        print(f"Decision (alfa={resultado.alfa}): {resultado.decision()}")

    def mostrar_tabla_resumen(self, filas):
        """Tabla final con todos los tamanos de muestra y configuraciones."""
        self.mostrar_titulo("TABLA RESUMEN (Python)")
        print(f"{'Config':<12}{'N':>10}{'chi2':>11}{'p chi2':>9}"
              f"{'D':>11}{'p KS':>9}{'Tiempo(s)':>11}")
        for fila in filas:
            print(f"{fila['configuracion']:<12}{fila['N']:>10}{fila['chi2']:>11.4f}"
                  f"{fila['p_chi2']:>9.4f}{fila['D']:>11.6f}{fila['p_ks']:>9.4f}"
                  f"{fila['tiempo_segundos']:>11.4f}")
