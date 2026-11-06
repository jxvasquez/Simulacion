# ------------------------------------------------------------
# Archivo: controlador_comparacion.py
# Coordina la comparacion de la secuencia de Python con la de Java.
# ------------------------------------------------------------

import csv
import os


class ControladorComparacion:
    """Lee los dos CSV, los compara y muestra la tabla resultante."""

    def __init__(self, exportador, comparador, vista_consola):
        self.exportador = exportador    # ExportadorCSV (sabe leer CSV)
        self.comparador = comparador    # ComparadorSecuencias
        self.vista = vista_consola      # VistaConsola

    def ejecutar(self, ruta_python, ruta_java, ruta_salida, cantidad_tabla):
        # Verificamos que existan los dos archivos antes de continuar
        for ruta in (ruta_python, ruta_java):
            if not os.path.exists(ruta):
                self.vista.mostrar_mensaje(f"No se encontro el archivo: {ruta}")
                self.vista.mostrar_mensaje("Ejecute primero main.py (Python) y Main.java (Java).")
                return

        secuencia_python = self.exportador.leer(ruta_python)
        secuencia_java = self.exportador.leer(ruta_java)
        filas = self.comparador.comparar(secuencia_python, secuencia_java)

        self.vista.mostrar_titulo(f"Tabla comparativa Python vs Java (primeras {cantidad_tabla})")
        self.vista.mostrar_tabla_lenguajes(filas, cantidad_tabla)

        diferencias = self.comparador.contar_diferencias(filas)
        self.vista.mostrar_titulo("Resultado de la comparacion completa")
        self.vista.mostrar_mensaje(f"  Valores comparados : {len(filas)}")
        self.vista.mostrar_mensaje(f"  Diferencias        : {diferencias}")
        if diferencias == 0:
            self.vista.mostrar_mensaje("  => Ambas implementaciones producen EXACTAMENTE la misma secuencia.")
        else:
            self.vista.mostrar_mensaje("  => Hay diferencias: revise los parametros o el codigo.")

        self._guardar_tabla(filas, ruta_salida)
        self.vista.mostrar_mensaje(f"\n  Tabla completa guardada en: {ruta_salida}")

    def _guardar_tabla(self, filas, ruta):
        with open(ruta, "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(["n", "X_python", "X_java", "U_python", "U_java", "coinciden"])
            for n, x_py, x_java, u_py, u_java, coinciden in filas:
                escritor.writerow([n, x_py, x_java, f"{u_py:.10f}", f"{u_java:.10f}",
                                   "SI" if coinciden else "NO"])
