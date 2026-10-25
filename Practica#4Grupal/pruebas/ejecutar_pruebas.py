# ==============================================================================
# ARCHIVO : pruebas/ejecutar_pruebas.py
# OBJETIVO: comprobar automaticamente que el proyecto funciona bien.
# USO     : desde la carpeta raiz del proyecto ejecute:  python pruebas/ejecutar_pruebas.py
#
# Cada prueba es una funcion que devuelve un texto:
#   - texto vacio ""  -> la prueba paso
#   - texto con algo  -> la prueba fallo, y el texto explica por que
# ==============================================================================

# os: modulo para trabajar con rutas y carpetas.
import os

# sys: modulo con informacion del sistema; lo usamos para agregar carpetas de busqueda.
import sys

# csv: modulo para leer archivos CSV.
import csv

# shutil: modulo para borrar carpetas completas.
import shutil

# tempfile: modulo para crear carpetas temporales.
import tempfile

# Obtenemos la carpeta donde esta este archivo de pruebas.
carpeta_pruebas = os.path.dirname(os.path.abspath(__file__))

# La carpeta raiz del proyecto es la carpeta que contiene a "pruebas".
carpeta_proyecto = os.path.dirname(carpeta_pruebas)

# Agregamos la carpeta raiz a la lista de busqueda de Python, para poder hacer "import sir".
sys.path.insert(0, carpeta_proyecto)

# Importamos lo que vamos a probar (una linea por cada pieza).
from sir.dominio.configuracion import ConfiguracionSIR
# Importamos las ecuaciones.
from sir.dominio.ecuaciones import calcular_derivadas
# Importamos el calculo de R0.
from sir.dominio.ecuaciones import numero_reproductivo_basico
# Importamos la clase de registro entero.
from sir.dominio.registro_sir import RegistroSIR
# Importamos el simulador.
from sir.aplicacion.simulador import SimuladorSIR
# Importamos la solucion de Euler.
from sir.aplicacion.solucion_euler import resolver_por_euler
# Importamos el verificador.
from sir.aplicacion.verificador import verificar_historial
# Importamos el exportador del CSV principal.
from sir.infraestructura.exportador_csv import exportar_csv
# Importamos el exportador del CSV de Euler.
from sir.infraestructura.exportador_csv import exportar_csv_euler
# Importamos el graficador.
from sir.infraestructura.graficador import guardar_grafica


# Prueba 1: los valores iniciales de la guia son N=100, S=95, I=5, R=0 y R0=3.
def prueba_valores_iniciales():
    # Creamos la configuracion por defecto.
    configuracion = ConfiguracionSIR()
    # Comprobamos S(0).
    if configuracion.susceptibles_iniciales != 95:
        # Si S(0) no es 95, devolvemos el motivo del fallo.
        return "S(0) deberia ser 95 y es " + str(configuracion.susceptibles_iniciales)
    # Comprobamos I(0).
    if configuracion.infectados_iniciales != 5:
        # Si I(0) no es 5, devolvemos el motivo del fallo.
        return "I(0) deberia ser 5"
    # Comprobamos R(0).
    if configuracion.recuperados_iniciales != 0:
        # Si R(0) no es 0, devolvemos el motivo del fallo.
        return "R(0) deberia ser 0"
    # Calculamos R0.
    r_cero = numero_reproductivo_basico(configuracion.beta, configuracion.gamma)
    # Comprobamos que R0 sea 3 (con un margen minimo por los decimales).
    if abs(r_cero - 3.0) > 0.000001:
        # Si R0 no es 3, devolvemos el motivo del fallo.
        return "R0 deberia ser 3 y es " + str(r_cero)
    # Si llegamos aqui, todo esta bien: devolvemos texto vacio.
    return ""


# Prueba 2: las derivadas en t=0 deben ser dS=-1.425, dI=0.925, dR=0.500.
def prueba_derivadas_iniciales():
    # Calculamos las derivadas con S=95, I=5, R=0, beta=0.30, gamma=0.10.
    derivadas = calcular_derivadas(95, 5, 0, 0.30, 0.10)
    # Comprobamos dS.
    if abs(derivadas.cambio_susceptibles - (-1.425)) > 0.000001:
        # Si dS es incorrecto, devolvemos el motivo del fallo.
        return "dS incorrecto: " + str(derivadas.cambio_susceptibles)
    # Comprobamos dI.
    if abs(derivadas.cambio_infectados - 0.925) > 0.000001:
        # Si dI es incorrecto, devolvemos el motivo del fallo.
        return "dI incorrecto: " + str(derivadas.cambio_infectados)
    # Comprobamos dR.
    if abs(derivadas.cambio_recuperados - 0.500) > 0.000001:
        # Si dR es incorrecto, devolvemos el motivo del fallo.
        return "dR incorrecto: " + str(derivadas.cambio_recuperados)
    # Todo correcto.
    return ""


# Prueba 3: una configuracion con valores imposibles debe ser rechazada.
def prueba_configuracion_invalida():
    # Lista de configuraciones malas: (poblacion, infectados, beta, gamma, pasos).
    casos_malos = [
        [0, 0, 0.3, 0.1, 10],
        [100, 200, 0.3, 0.1, 10],
        [100, 5, 1.5, 0.1, 10],
        [100, 5, 0.3, -0.1, 10],
        [100, 5, 0.3, 0.1, -1],
    ]
    # Probamos cada caso malo.
    for caso in casos_malos:
        # Marcamos que todavia no se detecto ningun error.
        error_detectado = False
        # Intentamos crear la configuracion.
        try:
            # Esta linea DEBERIA fallar con ValueError, porque el caso es invalido.
            ConfiguracionSIR(caso[0], caso[1], caso[2], caso[3], caso[4])
        # Si el dominio lanza ValueError, es lo que esperabamos.
        except ValueError:
            # Anotamos que el error fue detectado.
            error_detectado = True
        # Si no se detecto el error, la prueba falla.
        if not error_detectado:
            # Si el caso invalido fue aceptado, devolvemos el motivo del fallo.
            return "No se rechazo la configuracion invalida " + str(caso)
    # Todo correcto.
    return ""


# Prueba 4: la simulacion por defecto produce 101 filas, empieza en 0,95,5,0 y es coherente.
def prueba_simulacion_por_defecto():
    # Creamos la configuracion por defecto.
    configuracion = ConfiguracionSIR()
    # Ejecutamos la simulacion.
    historial = SimuladorSIR(configuracion).ejecutar()
    # Comprobamos la cantidad de filas.
    if len(historial) != 101:
        # Si la cantidad de filas no es 101, devolvemos el motivo del fallo.
        return "Se esperaban 101 filas y hay " + str(len(historial))
    # Tomamos la primera fila.
    primera = historial[0]
    # Comprobamos que sea 0,95,5,0.
    if (primera.tiempo != 0 or primera.susceptibles != 95
            or primera.infectados != 5 or primera.recuperados != 0):
        # Si la primera fila es incorrecta, devolvemos el motivo del fallo.
        return "La primera fila deberia ser 0,95,5,0 y es " + primera.como_texto()
    # Usamos el verificador para revisar todas las filas.
    problemas = verificar_historial(historial, configuracion)
    # Si hay problemas, los mostramos unidos en un solo texto.
    if len(problemas) > 0:
        # Unimos los problemas con " | " y devolvemos el motivo del fallo.
        return "El verificador encontro problemas: " + " | ".join(problemas)
    # Todo correcto.
    return ""


# Prueba 5: la misma semilla da los mismos resultados; otra semilla da resultados distintos.
def prueba_semillas():
    # Simulamos dos veces con la semilla 42.
    historial_a = SimuladorSIR(ConfiguracionSIR(semilla=42)).ejecutar()
    # Segunda simulacion con la misma semilla.
    historial_b = SimuladorSIR(ConfiguracionSIR(semilla=42)).ejecutar()
    # Simulamos con otra semilla.
    historial_c = SimuladorSIR(ConfiguracionSIR(semilla=7)).ejecutar()
    # Contadores de diferencias.
    diferencias_misma_semilla = 0
    # Diferencias con semilla distinta.
    diferencias_otra_semilla = 0
    # Recorremos las filas comparando.
    for posicion in range(len(historial_a)):
        # Comparamos las dos simulaciones con semilla 42.
        if historial_a[posicion].como_texto() != historial_b[posicion].como_texto():
            # Contamos una diferencia.
            diferencias_misma_semilla = diferencias_misma_semilla + 1
        # Comparamos la simulacion con semilla 42 contra la de semilla 7.
        if historial_a[posicion].como_texto() != historial_c[posicion].como_texto():
            # Contamos una diferencia.
            diferencias_otra_semilla = diferencias_otra_semilla + 1
    # La misma semilla no debe producir ninguna diferencia.
    if diferencias_misma_semilla != 0:
        # Si la misma semilla dio resultados distintos, devolvemos el fallo.
        return "La misma semilla produjo resultados distintos"
    # Otra semilla debe producir alguna diferencia.
    if diferencias_otra_semilla == 0:
        # Si otra semilla dio resultados iguales, devolvemos el fallo.
        return "Una semilla distinta produjo exactamente los mismos resultados"
    # Todo correcto.
    return ""


# Prueba 6: el CSV para NetLogo tiene el encabezado y las filas correctas.
def prueba_csv_para_netlogo():
    # Creamos una carpeta temporal para no ensuciar el proyecto.
    carpeta_temporal = tempfile.mkdtemp()
    # Guardamos el mensaje de resultado; vacio significa que todo va bien.
    mensaje = ""
    # Ejecutamos la simulacion por defecto.
    historial = SimuladorSIR(ConfiguracionSIR()).ejecutar()
    # Definimos la ruta del CSV temporal.
    ruta = os.path.join(carpeta_temporal, "resultados_python.csv")
    # Exportamos el CSV.
    exportar_csv(historial, ruta)
    # Abrimos el CSV recien creado para leerlo.
    with open(ruta, newline="", encoding="utf-8") as archivo:
        # Leemos todas las filas como listas de textos.
        filas = list(csv.reader(archivo))
    # Comprobamos el encabezado.
    if filas[0] != ["tiempo", "susceptibles", "infectados", "recuperados"]:
        # Guardamos el motivo del fallo en la variable mensaje.
        mensaje = "Encabezado incorrecto: " + str(filas[0])
    # Comprobamos la cantidad de filas: 1 encabezado + 101 datos.
    elif len(filas) != 102:
        # Guardamos el motivo del fallo en la variable mensaje.
        mensaje = "Se esperaban 102 lineas y hay " + str(len(filas))
    # Comprobamos la primera fila de datos.
    elif filas[1] != ["0", "95", "5", "0"]:
        # Guardamos el motivo del fallo en la variable mensaje.
        mensaje = "La primera fila de datos deberia ser 0,95,5,0 y es " + str(filas[1])
    # Si lo anterior esta bien, revisamos que cada fila sume 100 y use enteros.
    else:
        # Recorremos las filas de datos (sin el encabezado).
        for fila in filas[1:]:
            # Convertimos las tres ultimas columnas a enteros y las sumamos.
            suma = int(fila[1]) + int(fila[2]) + int(fila[3])
            # La suma debe ser igual a la poblacion.
            if suma != 100:
                # Guardamos el motivo del fallo en la variable mensaje.
                mensaje = "La fila " + str(fila) + " no suma 100"
    # Borramos la carpeta temporal.
    shutil.rmtree(carpeta_temporal)
    # Devolvemos el resultado.
    return mensaje


# Prueba 7: la solucion de Euler tiene 101 filas, parte de 95,5,0 y conserva la poblacion.
def prueba_euler():
    # Resolvemos con la configuracion por defecto.
    historial_euler = resolver_por_euler(ConfiguracionSIR())
    # Comprobamos la cantidad de filas.
    if len(historial_euler) != 101:
        # Si Euler no tiene 101 filas, devolvemos el motivo del fallo.
        return "Euler deberia tener 101 filas"
    # Comprobamos la fila inicial.
    primera = historial_euler[0]
    # S, I y R iniciales.
    if primera.susceptibles != 95.0 or primera.infectados != 5.0 or primera.recuperados != 0.0:
        # Si la fila inicial de Euler es incorrecta, devolvemos el fallo.
        return "La fila inicial de Euler es incorrecta"
    # Comprobamos que en cada fila la suma sea (casi) 100.
    for registro in historial_euler:
        # Sumamos S + I + R.
        suma = registro.susceptibles + registro.infectados + registro.recuperados
        # Aceptamos un error minimo por los decimales.
        if abs(suma - 100.0) > 0.000001:
            # Si la suma no es 100, devolvemos el motivo del fallo.
            return "Euler no conserva la poblacion en el tiempo " + str(registro.tiempo)
    # Probamos tambien la exportacion del CSV de Euler.
    carpeta_temporal = tempfile.mkdtemp()
    # Ruta del archivo temporal.
    ruta = os.path.join(carpeta_temporal, "euler.csv")
    # Exportamos.
    exportar_csv_euler(historial_euler, ruta)
    # Leemos el archivo creado.
    with open(ruta, newline="", encoding="utf-8") as archivo:
        # Leemos todas las filas.
        filas = list(csv.reader(archivo))
    # Borramos la carpeta temporal.
    shutil.rmtree(carpeta_temporal)
    # Comprobamos la cantidad de lineas.
    if len(filas) != 102:
        # Si el CSV de Euler no tiene 102 lineas, devolvemos el fallo.
        return "El CSV de Euler deberia tener 102 lineas"
    # Todo correcto.
    return ""


# Prueba 8: el verificador debe detectar resultados incorrectos.
def prueba_verificador_detecta_errores():
    # Configuracion pequena: 10 personas, 2 infectados, 2 pasos.
    configuracion = ConfiguracionSIR(poblacion=10, infectados_iniciales=2, pasos=2)
    # Historial inventado a proposito con errores.
    historial_malo = [
        RegistroSIR(0, 8, 2, 0),
        RegistroSIR(1, 7, 2, 2),
        RegistroSIR(2, 6, 3, 0),
    ]
    # Pedimos al verificador que lo revise.
    problemas = verificar_historial(historial_malo, configuracion)
    # Debe encontrar problemas (la suma del tiempo 1 es 11 y los recuperados bajan en el tiempo 2).
    if len(problemas) == 0:
        # Si el verificador no vio los errores, devolvemos el fallo.
        return "El verificador no detecto los errores del historial inventado"
    # Todo correcto.
    return ""


# Prueba 9: la grafica se guarda como un archivo PNG que no esta vacio.
def prueba_grafica():
    # Creamos una carpeta temporal.
    carpeta_temporal = tempfile.mkdtemp()
    # Ruta de la imagen temporal.
    ruta = os.path.join(carpeta_temporal, "subcarpeta", "grafica.png")
    # Simulamos y graficamos.
    historial = SimuladorSIR(ConfiguracionSIR()).ejecutar()
    # Guardamos la grafica (tambien debe crear la subcarpeta).
    guardar_grafica(historial, ruta)
    # Comprobamos que el archivo exista y tenga contenido.
    existe = os.path.exists(ruta)
    # Tamano del archivo (0 si no existe).
    tamano = 0
    # Si existe, medimos su tamano en bytes.
    if existe:
        # os.path.getsize devuelve el tamano del archivo en bytes.
        tamano = os.path.getsize(ruta)
    # Borramos la carpeta temporal.
    shutil.rmtree(carpeta_temporal)
    # Si no existe o esta vacio, la prueba falla.
    if not existe or tamano == 0:
        # Si la grafica no existe o esta vacia, devolvemos el fallo.
        return "La grafica no se creo correctamente"
    # Todo correcto.
    return ""


# ------------------------------------------------------------------------------
# PROGRAMA PRINCIPAL DE LAS PRUEBAS
# ------------------------------------------------------------------------------

# Lista con el nombre de cada prueba y la funcion que la ejecuta.
lista_de_pruebas = [
    ["Valores iniciales de la guia", prueba_valores_iniciales],
    ["Derivadas en t = 0", prueba_derivadas_iniciales],
    ["Configuracion invalida rechazada", prueba_configuracion_invalida],
    ["Simulacion por defecto", prueba_simulacion_por_defecto],
    ["Semillas aleatorias", prueba_semillas],
    ["CSV para NetLogo", prueba_csv_para_netlogo],
    ["Solucion de Euler", prueba_euler],
    ["Verificador detecta errores", prueba_verificador_detecta_errores],
    ["Grafica PNG", prueba_grafica],
]

# Contadores de pruebas correctas y fallidas.
cantidad_correctas = 0
# Cantidad de pruebas fallidas.
cantidad_fallidas = 0

# Recorremos la lista de pruebas.
for elemento in lista_de_pruebas:
    # El primer elemento es el nombre.
    nombre = elemento[0]
    # El segundo elemento es la funcion de la prueba.
    funcion_de_prueba = elemento[1]
    # Ejecutamos la prueba y guardamos el texto que devuelve.
    resultado = funcion_de_prueba()
    # Si el texto esta vacio, la prueba paso.
    if resultado == "":
        # Mostramos que paso.
        print("[OK]    " + nombre)
        # Sumamos una correcta.
        cantidad_correctas = cantidad_correctas + 1
    # Si el texto no esta vacio, la prueba fallo.
    else:
        # Mostramos que fallo y por que.
        print("[FALLO] " + nombre + " -> " + resultado)
        # Sumamos una fallida.
        cantidad_fallidas = cantidad_fallidas + 1

# Mostramos el resumen final.
print("")
# Totales.
print("Pruebas correctas: " + str(cantidad_correctas) + " | Pruebas fallidas: "
      + str(cantidad_fallidas))

# Si hubo fallos, terminamos con codigo 1 (convencion: distinto de 0 significa error).
if cantidad_fallidas > 0:
    # Terminamos el programa indicando error.
    sys.exit(1)
