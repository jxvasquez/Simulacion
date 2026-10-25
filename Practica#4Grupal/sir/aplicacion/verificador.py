# ==============================================================================
# ARCHIVO : sir/aplicacion/verificador.py
# CAPA    : Aplicacion
# OBJETIVO: comprobar que los resultados de la simulacion sean coherentes.
# NOTA    : esta capa NO imprime nada; solo DEVUELVE una lista de problemas.
#           Mostrar mensajes en pantalla es trabajo de la capa de presentacion.
# ==============================================================================


# Esta funcion revisa el historial y devuelve una lista de textos con los problemas hallados.
# Si la lista devuelta esta vacia, significa que todo esta correcto.
def verificar_historial(historial, configuracion):

    # Creamos la lista donde iremos anotando los problemas encontrados.
    problemas = []

    # Calculamos cuantas filas deberiamos tener: pasos + 1 (porque tambien existe el tiempo 0).
    filas_esperadas = configuracion.pasos + 1

    # Revision 1: la cantidad de filas debe ser la esperada.
    if len(historial) != filas_esperadas:
        # Anotamos el problema en la lista.
        problemas.append("Se esperaban " + str(filas_esperadas) + " filas y hay "
                         + str(len(historial)))

    # Guardamos el valor de recuperados de la fila anterior (empezamos con un valor imposible).
    recuperados_anteriores = -1

    # Revisamos las filas una por una, de la primera a la ultima.
    for posicion in range(len(historial)):

        # Tomamos la fila que esta en esta posicion.
        registro = historial[posicion]

        # Revision 2: el tiempo de la fila debe coincidir con su posicion (0, 1, 2, ...).
        if registro.tiempo != posicion:
            # Anotamos el problema.
            problemas.append("La fila " + str(posicion) + " tiene tiempo " + str(registro.tiempo))

        # Revision 3: S + I + R debe ser igual a la poblacion total (nadie aparece ni desaparece).
        if registro.total() != configuracion.poblacion:
            # Anotamos el problema.
            problemas.append("En el tiempo " + str(registro.tiempo)
                             + " la suma S+I+R es " + str(registro.total())
                             + " y deberia ser " + str(configuracion.poblacion))

        # Revision 4: los recuperados nunca pueden disminuir (nadie deja de estar recuperado).
        if registro.recuperados < recuperados_anteriores:
            # Anotamos el problema.
            problemas.append("En el tiempo " + str(registro.tiempo)
                             + " los recuperados disminuyeron")

        # Actualizamos el valor "anterior" para comparar con la fila siguiente.
        recuperados_anteriores = registro.recuperados

    # Revision 5: la primera fila debe coincidir con los valores iniciales de la configuracion.
    if len(historial) > 0:

        # Tomamos la primera fila.
        primera = historial[0]

        # Comparamos S, I y R de la primera fila con los valores iniciales.
        if (primera.susceptibles != configuracion.susceptibles_iniciales
                or primera.infectados != configuracion.infectados_iniciales
                or primera.recuperados != configuracion.recuperados_iniciales):
            # Anotamos el problema.
            problemas.append("La primera fila no coincide con los valores iniciales")

    # Devolvemos la lista de problemas (vacia si todo esta bien).
    return problemas
