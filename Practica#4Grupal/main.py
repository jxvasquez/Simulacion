# ==============================================================================
# ARCHIVO : main.py
# OBJETIVO: es la "puerta de entrada" del programa. Se ejecuta con:  python main.py
# ==============================================================================

# os: modulo de Python para trabajar con rutas de archivos.
import os

# Importamos la funcion que arranca todo el programa, desde la capa de presentacion.
from sir.presentacion.consola import ejecutar_aplicacion

# __file__ es la ruta de este archivo; abspath la convierte en ruta completa;
# dirname se queda solo con la carpeta. Asi obtenemos la carpeta raiz del proyecto.
carpeta_proyecto = os.path.dirname(os.path.abspath(__file__))

# Esta condicion es verdadera solo cuando ejecutamos ESTE archivo directamente.
if __name__ == "__main__":
    # Arrancamos el programa indicando cual es la carpeta del proyecto.
    ejecutar_aplicacion(carpeta_proyecto)
