# ==============================================================================
# ARCHIVO : sir/infraestructura/exportador_csv.py
# CAPA    : Infraestructura
# OBJETIVO: guardar los resultados en archivos CSV listos para importar en NetLogo.
#
# Formato del CSV principal (una fila por paso de tiempo):
#   tiempo,susceptibles,infectados,recuperados
#   0,95,5,0
#   1,93,7,0
#   ...
# ==============================================================================

# csv: modulo de Python que sabe escribir archivos separados por comas.
import csv

# os: modulo de Python para trabajar con carpetas y rutas de archivos.
import os

# Lista con los nombres de las columnas. NetLogo espera exactamente estos nombres.
COLUMNAS_CSV = ["tiempo", "susceptibles", "infectados", "recuperados"]


# Esta funcion crea la carpeta donde se guardara un archivo, si todavia no existe.
def crear_carpeta_si_no_existe(ruta_archivo):

    # Obtenemos solo la parte de la carpeta de la ruta (sin el nombre del archivo).
    carpeta = os.path.dirname(ruta_archivo)

    # Si la ruta tiene carpeta y esa carpeta todavia no existe...
    if carpeta != "" and not os.path.exists(carpeta):
        # ...la creamos (incluyendo las carpetas intermedias si hicieran falta).
        os.makedirs(carpeta)


# Esta funcion guarda el historial de la simulacion (numeros ENTEROS) en un archivo CSV.
def exportar_csv(historial, ruta_archivo):

    # Primero nos aseguramos de que la carpeta de destino exista.
    crear_carpeta_si_no_existe(ruta_archivo)

    # Abrimos el archivo en modo escritura ("w"). Si ya existia, se reemplaza.
    # "with" cierra el archivo automaticamente al terminar el bloque.
    # newline="" evita lineas en blanco extra en Windows.
    with open(ruta_archivo, "w", newline="", encoding="utf-8") as archivo:

        # Creamos el escritor de CSV. Cada fila termina con un salto de linea simple.
        escritor = csv.writer(archivo, lineterminator="\n")

        # Escribimos la primera fila: los nombres de las columnas.
        escritor.writerow(COLUMNAS_CSV)

        # Recorremos el historial, un registro a la vez.
        for registro in historial:

            # Armamos una fila con los cuatro datos del registro.
            fila = [registro.tiempo, registro.susceptibles, registro.infectados,
                    registro.recuperados]

            # Escribimos la fila en el archivo.
            escritor.writerow(fila)


# Esta funcion guarda la solucion de Euler (numeros DECIMALES) en un archivo CSV adicional.
def exportar_csv_euler(historial_euler, ruta_archivo):

    # Primero nos aseguramos de que la carpeta de destino exista.
    crear_carpeta_si_no_existe(ruta_archivo)

    # Abrimos el archivo en modo escritura.
    with open(ruta_archivo, "w", newline="", encoding="utf-8") as archivo:

        # Creamos el escritor de CSV.
        escritor = csv.writer(archivo, lineterminator="\n")

        # Escribimos los nombres de las columnas.
        escritor.writerow(COLUMNAS_CSV)

        # Recorremos el historial de Euler, un registro a la vez.
        for registro in historial_euler:

            # Convertimos cada valor a texto con exactamente 8 decimales.
            susceptibles_texto = format(registro.susceptibles, ".8f")

            # Infectados con 8 decimales.
            infectados_texto = format(registro.infectados, ".8f")

            # Recuperados con 8 decimales.
            recuperados_texto = format(registro.recuperados, ".8f")

            # Armamos la fila (el tiempo sigue siendo un numero entero).
            fila = [registro.tiempo, susceptibles_texto, infectados_texto, recuperados_texto]

            # Escribimos la fila en el archivo.
            escritor.writerow(fila)
