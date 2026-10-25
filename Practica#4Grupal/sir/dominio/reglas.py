# ==============================================================================
# ARCHIVO : sir/dominio/reglas.py
# CAPA    : Dominio
# OBJETIVO: guardar la regla matematica del contagio para una simulacion por personas.
# ==============================================================================


# Esta funcion calcula la probabilidad de que UNA persona susceptible se contagie en un paso.
# Idea: cada infectado contagia a esa persona con probabilidad beta / N.
# La persona se salva solo si se salva de TODOS los infectados: (1 - beta/N) elevado a I.
# Por eso la probabilidad de contagio es: 1 - (1 - beta/N) ** I
def probabilidad_infeccion(beta, infectados, poblacion):

    # Paso 1: probabilidad de que UN infectado contagie a esta persona.
    probabilidad_un_infectado = beta / poblacion

    # Paso 2: probabilidad de que UN infectado NO la contagie.
    probabilidad_no_contagio_uno = 1 - probabilidad_un_infectado

    # Paso 3: probabilidad de que NINGUNO de los infectados la contagie.
    # El operador ** significa "elevado a la potencia".
    probabilidad_no_contagio_todos = probabilidad_no_contagio_uno ** infectados

    # Paso 4: la probabilidad de contagio es lo contrario de que nadie la contagie.
    probabilidad_contagio = 1 - probabilidad_no_contagio_todos

    # Paso 5: devolvemos la probabilidad calculada.
    return probabilidad_contagio
