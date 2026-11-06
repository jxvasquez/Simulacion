# ============================================================
# MODELO - Guardar resultados en archivos CSV
# ============================================================
# Responsabilidad unica: esta clase solo se encarga de escribir
# archivos. Asi Python y Java dejan sus resultados en el mismo
# formato y luego se pueden comparar.
# ============================================================

import csv
import os


class RepositorioResultados:

    def __init__(self, carpeta_salida):
        self.carpeta_salida = carpeta_salida
        os.makedirs(carpeta_salida, exist_ok=True)  # crea la carpeta si no existe

    def guardar_tabla(self, nombre_archivo, filas):
        """Guarda la tabla resumen. 'filas' es una lista de diccionarios."""
        ruta = os.path.join(self.carpeta_salida, nombre_archivo)
        columnas = ["configuracion", "N", "chi2", "p_chi2", "decision_chi2",
                    "D", "p_ks", "decision_ks", "tiempo_segundos"]
        with open(ruta, "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=columnas)
            escritor.writeheader()
            for fila in filas:
                escritor.writerow(fila)
        return ruta

    def guardar_secuencia(self, nombre_archivo, numeros):
        """Guarda los primeros numeros generados (uno por linea)."""
        ruta = os.path.join(self.carpeta_salida, nombre_archivo)
        with open(ruta, "w", encoding="utf-8") as archivo:
            archivo.write("indice,numero\n")
            for i, numero in enumerate(numeros):
                archivo.write(f"{i + 1},{numero:.10f}\n")
        return ruta

    def guardar_tabla_pi(self, nombre_archivo, filas):
        """Guarda la tabla de pi estimado (N, pi, error, tiempo)."""
        ruta = os.path.join(self.carpeta_salida, nombre_archivo)
        columnas = ["N", "pi_estimado", "error", "tiempo_segundos"]
        with open(ruta, "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=columnas)
            escritor.writeheader()
            for fila in filas:
                escritor.writerow(fila)
        return ruta
