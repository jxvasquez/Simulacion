# ==============================================================================
# ARCHIVO : sir/presentacion/consola.py
# CAPA    : Presentacion
# OBJETIVO: interactuar con la persona por consola y coordinar todo el programa.
# ==============================================================================

# os: modulo de Python para armar rutas de archivos de forma correcta en cualquier sistema.
import os

# --- Importaciones de la capa de DOMINIO ---
# Importamos la clase que guarda los parametros del modelo.
from sir.dominio.configuracion import ConfiguracionSIR
# Importamos la funcion que calcula dS, dI y dR.
from sir.dominio.ecuaciones import calcular_derivadas
# Importamos la funcion que calcula R0.
from sir.dominio.ecuaciones import numero_reproductivo_basico

# --- Importaciones de la capa de APLICACION ---
# Importamos el simulador persona por persona.
from sir.aplicacion.simulador import SimuladorSIR
# Importamos la solucion matematica por el metodo de Euler.
from sir.aplicacion.solucion_euler import resolver_por_euler
# Importamos la funcion que revisa que los resultados sean coherentes.
from sir.aplicacion.verificador import verificar_historial

# --- Importaciones de la capa de INFRAESTRUCTURA ---
# Importamos la funcion que guarda el CSV principal (para NetLogo).
from sir.infraestructura.exportador_csv import exportar_csv
# Importamos la funcion que guarda el CSV adicional de Euler.
from sir.infraestructura.exportador_csv import exportar_csv_euler
# Importamos la funcion que guarda la grafica en PNG.
from sir.infraestructura.graficador import guardar_grafica


# Esta funcion pide a la persona un numero ENTERO. Si solo presiona Enter, usa el valor por defecto.
def pedir_entero(mensaje, valor_por_defecto):

    # Empezamos sin resultado. Mientras no haya un resultado valido, seguimos preguntando.
    resultado = None

    # Repetimos la pregunta mientras el resultado siga vacio (None).
    while resultado is None:

        # Mostramos la pregunta (con el valor por defecto entre corchetes) y leemos la respuesta.
        texto = input(mensaje + " [" + str(valor_por_defecto) + "]: ")

        # Quitamos los espacios sobrantes al inicio y al final.
        texto = texto.strip()

        # Si la persona no escribio nada...
        if texto == "":
            # ...usamos el valor por defecto.
            resultado = valor_por_defecto
        # Si escribio algo...
        else:
            # ...intentamos convertir el texto a numero entero.
            try:
                # int(...) convierte texto a entero; falla si el texto no es un numero entero.
                resultado = int(texto)
            # Si la conversion fallo, Python lanza un ValueError y entramos aqui.
            except ValueError:
                # Avisamos y volvemos a preguntar.
                print("Eso no es un numero entero valido. Intente de nuevo.")

    # Devolvemos el numero entero obtenido.
    return resultado


# Esta funcion pide a la persona un numero DECIMAL. Acepta tanto 0.3 como 0,3.
def pedir_decimal(mensaje, valor_por_defecto):

    # Empezamos sin resultado.
    resultado = None

    # Repetimos mientras no tengamos un resultado valido.
    while resultado is None:

        # Mostramos la pregunta y leemos la respuesta.
        texto = input(mensaje + " [" + str(valor_por_defecto) + "]: ")

        # Quitamos los espacios sobrantes.
        texto = texto.strip()

        # Cambiamos la coma decimal por punto, porque Python solo entiende el punto.
        texto = texto.replace(",", ".")

        # Si la persona no escribio nada...
        if texto == "":
            # ...usamos el valor por defecto.
            resultado = valor_por_defecto
        # Si escribio algo...
        else:
            # ...intentamos convertir el texto a numero decimal.
            try:
                # float(...) convierte texto a decimal; falla si el texto no es un numero.
                resultado = float(texto)
            # Si la conversion fallo...
            except ValueError:
                # ...avisamos y volvemos a preguntar.
                print("Eso no es un numero valido. Intente de nuevo.")

    # Devolvemos el numero decimal obtenido.
    return resultado


# Esta funcion obtiene la configuracion: o la de la guia, o la que escriba la persona.
def pedir_configuracion():

    # Empezamos sin configuracion. Repetiremos hasta tener una valida.
    configuracion = None

    # Mientras no haya configuracion valida, seguimos.
    while configuracion is None:

        # Preguntamos si desea usar los valores por defecto de la guia.
        respuesta = input("Desea usar los valores por defecto de la guia? (s/n) [s]: ")

        # Quitamos espacios sobrantes.
        respuesta = respuesta.strip()

        # Pasamos la respuesta a minusculas para aceptar "S" y "s" por igual.
        respuesta = respuesta.lower()

        # Caso 1: la persona presiono Enter o escribio "s".
        if respuesta == "" or respuesta == "s":
            # Creamos la configuracion con todos los valores por defecto.
            configuracion = ConfiguracionSIR()

        # Caso 2: la persona escribio "n" y quiere elegir sus propios valores.
        elif respuesta == "n":
            # Pedimos cada parametro, mostrando el valor por defecto como ayuda.
            poblacion = pedir_entero("Poblacion total (N)", 100)
            # Pedimos los infectados iniciales.
            infectados_iniciales = pedir_entero("Infectados iniciales I(0)", 5)
            # Pedimos beta.
            beta = pedir_decimal("Beta, tasa de contagio (entre 0 y 1)", 0.30)
            # Pedimos gamma.
            gamma = pedir_decimal("Gamma, tasa de recuperacion (entre 0 y 1)", 0.10)
            # Pedimos la cantidad de pasos.
            pasos = pedir_entero("Cantidad de pasos de tiempo", 100)
            # Pedimos la semilla del generador aleatorio.
            semilla = pedir_entero("Semilla aleatoria", 42)

            # Intentamos crear la configuracion con los valores escritos.
            try:
                # Si algun valor no cumple las reglas del dominio, se lanza un ValueError.
                configuracion = ConfiguracionSIR(poblacion, infectados_iniciales, beta, gamma,
                                                 pasos, semilla)
            # Si hubo un valor invalido...
            except ValueError as error:
                # ...mostramos cual fue el problema y se vuelve a preguntar desde el inicio.
                print("Configuracion invalida: " + str(error))
                # Avisamos que se repetira la pregunta.
                print("Vamos a intentarlo de nuevo.")

        # Caso 3: la persona escribio cualquier otra cosa.
        else:
            # Avisamos y volvemos a preguntar.
            print("Respuesta no reconocida. Escriba s o n.")

    # Devolvemos la configuracion valida.
    return configuracion


# Esta funcion muestra en pantalla los datos de partida y las ecuaciones evaluadas en t = 0.
def mostrar_datos_iniciales(configuracion):

    # Imprimimos una linea en blanco para separar visualmente.
    print("")
    # Imprimimos un titulo.
    print("=== DATOS INICIALES ===")
    # Mostramos la poblacion total.
    print("Poblacion total N = " + str(configuracion.poblacion))
    # Mostramos los valores iniciales de S, I y R.
    print("Valores iniciales: S = " + str(configuracion.susceptibles_iniciales)
          + ", I = " + str(configuracion.infectados_iniciales)
          + ", R = " + str(configuracion.recuperados_iniciales))
    # Mostramos beta, gamma y la semilla.
    print("Beta = " + str(configuracion.beta) + ", Gamma = " + str(configuracion.gamma)
          + ", Semilla = " + str(configuracion.semilla))

    # Calculamos dS, dI y dR en el instante inicial usando el dominio.
    derivadas = calcular_derivadas(configuracion.susceptibles_iniciales,
                                   configuracion.infectados_iniciales,
                                   configuracion.recuperados_iniciales,
                                   configuracion.beta, configuracion.gamma)

    # Convertimos cada derivada a texto con 3 decimales.
    texto_ds = format(derivadas.cambio_susceptibles, ".3f")
    # Texto de dI.
    texto_di = format(derivadas.cambio_infectados, ".3f")
    # Texto de dR.
    texto_dr = format(derivadas.cambio_recuperados, ".3f")

    # Mostramos las derivadas iniciales.
    print("Cambios esperados en t = 0: dS = " + texto_ds + ", dI = " + texto_di
          + ", dR = " + texto_dr)

    # Calculamos R0 (numero reproductivo basico) usando el dominio.
    r_cero = numero_reproductivo_basico(configuracion.beta, configuracion.gamma)

    # Mostramos R0 con 2 decimales.
    print("Numero reproductivo basico R0 = " + format(r_cero, ".2f"))


# Esta funcion muestra un resumen de los resultados de la simulacion.
def mostrar_resumen_final(historial, ruta_csv, ruta_csv_euler, ruta_grafica):

    # Tomamos la ultima fila del historial (la que esta en la posicion -1).
    ultimo = historial[-1]

    # Buscamos el momento con mayor cantidad de infectados (el "pico" de la epidemia).
    # Empezamos suponiendo que el pico esta en la primera fila.
    pico_infectados = historial[0].infectados
    # Tiempo en el que ocurre ese pico.
    tiempo_del_pico = historial[0].tiempo

    # Revisamos todas las filas.
    for registro in historial:
        # Si esta fila tiene mas infectados que el pico registrado hasta ahora...
        if registro.infectados > pico_infectados:
            # ...actualizamos el valor del pico.
            pico_infectados = registro.infectados
            # ...y guardamos en que tiempo ocurrio.
            tiempo_del_pico = registro.tiempo

    # Imprimimos una linea en blanco para separar visualmente.
    print("")
    # Imprimimos un titulo.
    print("=== RESULTADOS ===")
    # Mostramos cuantas filas tiene el historial.
    print("Filas generadas: " + str(len(historial)))
    # Mostramos el pico de infectados.
    print("Pico de infectados: " + str(pico_infectados) + " personas en el tiempo "
          + str(tiempo_del_pico))
    # Mostramos la ultima fila.
    print("Estado final -> " + ultimo.como_texto())
    # Mostramos donde quedaron los archivos.
    print("")
    # Titulo de la lista de archivos.
    print("=== ARCHIVOS GENERADOS ===")
    # Ruta del CSV principal.
    print("CSV para NetLogo : " + ruta_csv)
    # Ruta del CSV de Euler.
    print("CSV de Euler     : " + ruta_csv_euler)
    # Ruta de la grafica.
    print("Grafica PNG      : " + ruta_grafica)


# Esta es la funcion principal del programa: coordina todas las capas, paso a paso.
def ejecutar_aplicacion(carpeta_proyecto):

    # Mostramos el titulo del programa.
    print("==============================================")
    # Segunda linea del titulo.
    print("  SIMULACION DEL MODELO EPIDEMIOLOGICO SIR")
    # Tercera linea del titulo.
    print("==============================================")

    # Definimos las rutas de los archivos que vamos a generar.
    # os.path.join une las partes de la ruta usando el separador correcto del sistema.
    ruta_csv = os.path.join(carpeta_proyecto, "netlogo", "resultados_python.csv")
    # Ruta del CSV de Euler (queda junto al CSV principal).
    ruta_csv_euler = os.path.join(carpeta_proyecto, "netlogo", "resultados_euler_python.csv")
    # Ruta de la imagen con la grafica.
    ruta_grafica = os.path.join(carpeta_proyecto, "resultados", "grafica_python.png")

    # PASO 1 (Presentacion): pedimos la configuracion a la persona.
    configuracion = pedir_configuracion()

    # PASO 2 (Presentacion): mostramos los datos iniciales.
    mostrar_datos_iniciales(configuracion)

    # PASO 3 (Aplicacion): creamos el simulador con la configuracion.
    simulador = SimuladorSIR(configuracion)

    # Avisamos que empieza la simulacion.
    print("")
    # Mensaje de progreso.
    print("Ejecutando la simulacion...")

    # PASO 4 (Aplicacion): ejecutamos la simulacion y recibimos el historial.
    historial = simulador.ejecutar()

    # PASO 5 (Aplicacion): verificamos que los resultados sean coherentes.
    problemas = verificar_historial(historial, configuracion)

    # Si la lista de problemas NO esta vacia, hubo errores en la simulacion.
    if len(problemas) > 0:
        # Avisamos que algo salio mal.
        print("ERROR: los resultados no pasaron la verificacion:")
        # Mostramos cada problema encontrado.
        for problema in problemas:
            # Imprimimos el problema.
            print(" - " + problema)
        # Terminamos la funcion aqui; no se guarda ningun archivo.
        return

    # Avisamos que la verificacion fue exitosa.
    print("Verificacion correcta: en todas las filas S + I + R = " + str(configuracion.poblacion))

    # PASO 6 (Aplicacion): calculamos tambien la solucion matematica de Euler.
    historial_euler = resolver_por_euler(configuracion)

    # PASO 7 (Infraestructura): guardamos el CSV principal para NetLogo.
    exportar_csv(historial, ruta_csv)

    # PASO 8 (Infraestructura): guardamos el CSV adicional de Euler.
    exportar_csv_euler(historial_euler, ruta_csv_euler)

    # PASO 9 (Infraestructura): guardamos la grafica en un archivo PNG.
    guardar_grafica(historial, ruta_grafica)

    # PASO 10 (Presentacion): mostramos el resumen final.
    mostrar_resumen_final(historial, ruta_csv, ruta_csv_euler, ruta_grafica)
