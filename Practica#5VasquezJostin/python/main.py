# ------------------------------------------------------------
# Archivo: main.py  (punto de entrada del programa en Python)
#
# Aqui solo se CREAN los objetos y se conectan entre si.
# Toda la logica esta en el modelo, la vista y el controlador.
#
# Ejecutar desde la carpeta "python":   python3 main.py
# ------------------------------------------------------------

import os

from controlador.controlador_lcg import ControladorLCG
from modelo.analizador_periodo import AnalizadorPeriodo
from modelo.estadisticas import Estadisticas
from modelo.exportador_csv import ExportadorCSV
from modelo.generador_lcg import GeneradorLCG
from modelo.parametros_lcg import ParametrosLCG
from vista.vista_consola import VistaConsola
from vista.vista_grafica import VistaGrafica

# Carpeta donde se guardan los resultados (una carpeta arriba de "python")
CARPETA_BASE = os.path.dirname(os.path.abspath(__file__))
CARPETA_RESULTADOS = os.path.normpath(os.path.join(CARPETA_BASE, "..", "resultados"))

# Datos de la guia de practica
CANTIDAD_VALORES = 10000
CANTIDAD_TABLA = 20
NUEVA_SEMILLA = 54321


def main():
    # 1. Modelo: parametros y generador (paso 1 de la guia)
    parametros = ParametrosLCG(a=1664525, c=1013904223, m=2 ** 32, semilla=12345)
    generador = GeneradorLCG(parametros)

    # 2. Controlador: recibe todas sus dependencias ya creadas
    controlador = ControladorLCG(
        generador=generador,
        parametros=parametros,
        vista_consola=VistaConsola(),
        vista_grafica=VistaGrafica(),
        exportador=ExportadorCSV(),
        analizador=AnalizadorPeriodo(),
        estadisticas=Estadisticas(),
    )

    # 3. Ejecutar los pasos de la practica
    observaciones = controlador.generar_secuencia_principal(
        CANTIDAD_VALORES, CANTIDAD_TABLA,
        os.path.join(CARPETA_RESULTADOS, "secuencia_python.csv"),
        os.path.join(CARPETA_RESULTADOS, "grafico_semilla_12345.png"))

    controlador.analizar_periodo(observaciones)

    controlador.comparar_con_otra_semilla(
        observaciones, NUEVA_SEMILLA, CANTIDAD_VALORES, CANTIDAD_TABLA,
        os.path.join(CARPETA_RESULTADOS, f"grafico_semilla_{NUEVA_SEMILLA}.png"),
        os.path.join(CARPETA_RESULTADOS, "comparacion_semillas.csv"))

    # 4. Extra: parametros inadecuados (m pequeno y c = 0)
    parametros_malos = ParametrosLCG(a=5, c=0, m=16, semilla=3)
    controlador.demostrar_parametros_inadecuados(
        GeneradorLCG(parametros_malos), parametros_malos, 8)


if __name__ == "__main__":
    main()
