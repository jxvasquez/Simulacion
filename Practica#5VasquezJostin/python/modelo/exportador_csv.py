# ------------------------------------------------------------
# Archivo: exportador_csv.py
# Responsabilidad unica: guardar y leer secuencias en archivos CSV.
# El CSV de Python luego se compara con el que genera Java.
# ------------------------------------------------------------

import csv
import os


class ExportadorCSV:
    """Escribe y lee secuencias en formato CSV."""

    def exportar(self, observaciones, ruta):
        """Guarda la lista de observaciones en la ruta indicada (n, X, U)."""
        # Creamos la carpeta si todavia no existe
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(["n", "X", "U"])  # encabezado
            for obs in observaciones:
                escritor.writerow([obs.indice, obs.valor_x, f"{obs.valor_u:.10f}"])

    def exportar_comparacion(self, obs_1, obs_2, semilla_1, semilla_2, ruta):
        """Guarda lado a lado dos secuencias generadas con semillas distintas."""
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(["n",
                               f"X_semilla_{semilla_1}", f"U_semilla_{semilla_1}",
                               f"X_semilla_{semilla_2}", f"U_semilla_{semilla_2}"])
            for a, b in zip(obs_1, obs_2):
                escritor.writerow([a.indice,
                                   a.valor_x, f"{a.valor_u:.10f}",
                                   b.valor_x, f"{b.valor_u:.10f}"])

    def leer(self, ruta):
        """Lee un CSV (n, X, U) y devuelve una lista de tuplas."""
        filas = []
        with open(ruta, "r", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                filas.append((int(fila["n"]), int(fila["X"]), float(fila["U"])))
        return filas
