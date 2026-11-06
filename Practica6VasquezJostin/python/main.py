# ============================================================
# PRACTICA 06 - Validacion estadistica de numeros pseudoaleatorios
# Chi-cuadrado y Kolmogorov-Smirnov  |  Patron MVC  |  Python
# ============================================================
# Este archivo solo "arma" el programa: crea los objetos y se los
# entrega al controlador (punto de composicion). Para cambiar los
# parametros del generador solo se edita este archivo.
#
# Ejecutar desde la carpeta 'python':   python main.py
# ============================================================

from modelo.generador import GeneradorLCG
from modelo.prueba_chi_cuadrado import PruebaChiCuadrado
from modelo.prueba_kolmogorov_smirnov import PruebaKolmogorovSmirnov
from modelo.repositorio_resultados import RepositorioResultados
from vista.vista_consola import VistaConsola
from vista.vista_grafica import VistaGrafica
from controlador.controlador_simulacion import ControladorSimulacion

CARPETA_SALIDA = "../resultados"
ALFA = 0.05
INTERVALOS = 10


def main():
    # ---------- MODELO: configuraciones del generador ----------
    # IMPORTANTE: usar los MISMOS parametros en Java para obtener la misma secuencia
    configuraciones = {
        # Parametros conocidos (Numerical Recipes): buena calidad, m = 2^32
        "buena": GeneradorLCG(semilla=12345, multiplicador=1664525,
                              incremento=1013904223, modulo=2 ** 32),
        # Parametros pobres: modulo pequeno y periodo corto
        "deficiente": GeneradorLCG(semilla=7, multiplicador=13,
                                   incremento=0, modulo=64),
    }

    # Lista de pruebas: para agregar una nueva prueba solo se anade aqui
    pruebas = [
        PruebaChiCuadrado(numero_intervalos=INTERVALOS, alfa=ALFA),
        PruebaKolmogorovSmirnov(alfa=ALFA),
    ]

    # ---------- VISTA ----------
    vista_consola = VistaConsola()
    vista_grafica = VistaGrafica(CARPETA_SALIDA)

    # ---------- CONTROLADOR ----------
    repositorio = RepositorioResultados(CARPETA_SALIDA)
    controlador = ControladorSimulacion(pruebas, vista_consola, vista_grafica, repositorio)

    tamanos = [1_000, 10_000, 100_000, 1_000_000]
    controlador.ejecutar(configuraciones, tamanos, n_detalle=10_000)


if __name__ == "__main__":
    main()
