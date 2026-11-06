# ------------------------------------------------------------
# Archivo: exportador_csv.py
# Responsabilidad unica: guardar observaciones en un archivo CSV.
# El CSV luego se compara con el que genera el programa en Java.
# ------------------------------------------------------------

import csv
import os


class ExportadorCSV:
    """Escribe y lee secuencias en formato CSV (n, X, U)."""

    def exportar(self, observaciones, ruta):
        """Guarda la lista de observaciones en la ruta indicada."""
        # Creamos la carpeta si todavia no existe
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(["n", "X", "U"])  # encabezado
            for obs in observaciones:
                escritor.writerow([obs.indice, obs.valor_x, f"{obs.valor_u:.10f}"])

    def leer(self, ruta):
        """Lee un CSV y devuelve una lista de tuplas (n, X, U)."""
        filas = []
        with open(ruta, "r", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                filas.append((int(fila["n"]), int(fila["X"]), float(fila["U"])))
        return filas
