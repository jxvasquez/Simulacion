# ==============================================================================
# ARCHIVO : sir/aplicacion/solucion_euler.py
# CAPA    : Aplicacion
# OBJETIVO: resolver las ecuaciones del modelo SIR con el metodo de Euler (paso = 1).
#           Es una referencia determinista (sin azar) para comparar con la simulacion.
# ==============================================================================

# Importamos la clase de registro con decimales desde el dominio.
from sir.dominio.registro_sir import RegistroEuler
# Importamos las ecuaciones del modelo desde el dominio.
from sir.dominio.ecuaciones import calcular_derivadas


# Esta funcion aplica el metodo de Euler: nuevo valor = valor anterior + cambio.
def resolver_por_euler(configuracion):

    # Convertimos los valores iniciales a decimales (float).
    susceptibles = float(configuracion.susceptibles_iniciales)

    # Infectados iniciales como decimal.
    infectados = float(configuracion.infectados_iniciales)

    # Recuperados iniciales como decimal.
    recuperados = float(configuracion.recuperados_iniciales)

    # Creamos el historial vacio.
    historial = []

    # Guardamos la fila del tiempo 0 con los valores iniciales.
    fila_inicial = RegistroEuler(0, susceptibles, infectados, recuperados)

    # Agregamos la fila inicial al historial.
    historial.append(fila_inicial)

    # Repetimos para los tiempos 1, 2, 3, ... hasta el ultimo paso (inclusive).
    for tiempo in range(1, configuracion.pasos + 1):

        # Calculamos cuanto cambia cada grupo usando las ecuaciones del dominio.
        cambio = calcular_derivadas(susceptibles, infectados, recuperados,
                                    configuracion.beta, configuracion.gamma)

        # Sumamos el cambio de los susceptibles al valor anterior.
        susceptibles = susceptibles + cambio.cambio_susceptibles

        # Sumamos el cambio de los infectados al valor anterior.
        infectados = infectados + cambio.cambio_infectados

        # Sumamos el cambio de los recuperados al valor anterior.
        recuperados = recuperados + cambio.cambio_recuperados

        # Creamos la fila de este tiempo con los valores nuevos.
        fila_nueva = RegistroEuler(tiempo, susceptibles, infectados, recuperados)

        # Agregamos la fila nueva al historial.
        historial.append(fila_nueva)

    # Devolvemos el historial completo.
    return historial
