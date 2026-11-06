# ------------------------------------------------------------
# Archivo: comparar.py  (segundo punto de entrada)
#
# Compara la secuencia generada por Python con la generada por Java
# y arma la tabla que pide la guia (seccion 6: Resultados esperados).
#
# Orden de ejecucion:
#   1) python3 main.py          (crea resultados/secuencia_python.csv)
#   2) programa Java            (crea resultados/secuencia_java.csv)
#   3) python3 comparar.py      (crea resultados/tabla_comparacion.csv)
# ------------------------------------------------------------

import os

from controlador.controlador_comparacion import ControladorComparacion
from modelo.comparador_secuencias import ComparadorSecuencias
from modelo.exportador_csv import ExportadorCSV
from vista.vista_comparacion import VistaComparacion
from vista.vista_consola import VistaConsola

CARPETA_BASE = os.path.dirname(os.path.abspath(__file__))
CARPETA_RESULTADOS = os.path.normpath(os.path.join(CARPETA_BASE, "..", "resultados"))


def main():
    controlador = ControladorComparacion(
        exportador=ExportadorCSV(),
        comparador=ComparadorSecuencias(),
        vista_consola=VistaConsola(),
        vista_comparacion=VistaComparacion(),
    )
    controlador.ejecutar(
        os.path.join(CARPETA_RESULTADOS, "secuencia_python.csv"),
        os.path.join(CARPETA_RESULTADOS, "secuencia_java.csv"),
        os.path.join(CARPETA_RESULTADOS, "tabla_comparacion.csv"),
        cantidad_tabla=20,
    )


if __name__ == "__main__":
    main()
