# ==============================================================================
# ARCHIVO : sir/infraestructura/graficador.py
# CAPA    : Infraestructura
# OBJETIVO: dibujar la evolucion de S, I y R y guardarla como imagen PNG.
# ==============================================================================

# os: modulo de Python para trabajar con carpetas y rutas de archivos.
import os

# matplotlib: libreria para hacer graficos.
import matplotlib

# Elegimos el modo "Agg": dibuja directamente en un archivo, sin abrir ninguna ventana.
# Esta linea debe ir ANTES de importar pyplot.
matplotlib.use("Agg")

# pyplot: la parte de matplotlib con las funciones para dibujar. Lo abreviamos "plt".
import matplotlib.pyplot as plt


# Esta funcion dibuja el historial y guarda la imagen en la ruta indicada.
def guardar_grafica(historial, ruta_archivo):

    # Obtenemos la carpeta donde se guardara la imagen.
    carpeta = os.path.dirname(ruta_archivo)

    # Si la carpeta tiene nombre y todavia no existe...
    if carpeta != "" and not os.path.exists(carpeta):
        # ...la creamos.
        os.makedirs(carpeta)

    # Preparamos tres listas vacias, una para cada serie de datos, y una para el tiempo.
    tiempos = []
    # Lista de susceptibles.
    lista_susceptibles = []
    # Lista de infectados.
    lista_infectados = []
    # Lista de recuperados.
    lista_recuperados = []

    # Recorremos el historial y repartimos cada dato en su lista.
    for registro in historial:
        # Guardamos el tiempo.
        tiempos.append(registro.tiempo)
        # Guardamos los susceptibles.
        lista_susceptibles.append(registro.susceptibles)
        # Guardamos los infectados.
        lista_infectados.append(registro.infectados)
        # Guardamos los recuperados.
        lista_recuperados.append(registro.recuperados)

    # Creamos una figura nueva y vacia.
    plt.figure()

    # Dibujamos la linea de los susceptibles.
    plt.plot(tiempos, lista_susceptibles, label="Susceptibles")

    # Dibujamos la linea de los infectados.
    plt.plot(tiempos, lista_infectados, label="Infectados")

    # Dibujamos la linea de los recuperados.
    plt.plot(tiempos, lista_recuperados, label="Recuperados")

    # Ponemos nombre al eje horizontal.
    plt.xlabel("Tiempo (pasos)")

    # Ponemos nombre al eje vertical.
    plt.ylabel("Numero de personas")

    # Ponemos el titulo del grafico.
    plt.title("Evolucion del modelo SIR - Python/SimPy")

    # Mostramos la leyenda que explica el color de cada linea.
    plt.legend()

    # Dibujamos una cuadricula suave de fondo.
    plt.grid(alpha=0.2)

    # Guardamos la figura como imagen PNG (dpi = calidad de la imagen).
    plt.savefig(ruta_archivo, dpi=160, bbox_inches="tight")

    # Cerramos la figura para liberar memoria.
    plt.close()
