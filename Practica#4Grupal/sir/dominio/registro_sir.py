# ==============================================================================
# ARCHIVO : sir/dominio/registro_sir.py
# CAPA    : Dominio
# OBJETIVO: representar una "fila" de resultados: cuantos S, I y R hay en un instante.
# ==============================================================================


# Registro con numeros ENTEROS: cuenta personas reales (no se puede tener 2.5 personas).
class RegistroSIR:

    # El constructor recibe los cuatro datos de una fila de la tabla de resultados.
    def __init__(self, tiempo, susceptibles, infectados, recuperados):
        # Paso de tiempo al que pertenece esta fila (0, 1, 2, ...).
        self.tiempo = tiempo
        # Cantidad de personas susceptibles en ese instante.
        self.susceptibles = susceptibles
        # Cantidad de personas infectadas en ese instante.
        self.infectados = infectados
        # Cantidad de personas recuperadas en ese instante.
        self.recuperados = recuperados

    # Este metodo suma las tres categorias. Siempre debe dar igual a la poblacion total.
    def total(self):
        # Sumamos S + I + R.
        suma = self.susceptibles + self.infectados + self.recuperados
        # Devolvemos el resultado de la suma.
        return suma

    # Este metodo devuelve el registro escrito como texto, para poder mostrarlo en pantalla.
    def como_texto(self):
        # Armamos el texto uniendo piezas con el signo "+".
        # str(...) convierte un numero en texto.
        texto = ("tiempo=" + str(self.tiempo)
                 + " S=" + str(self.susceptibles)
                 + " I=" + str(self.infectados)
                 + " R=" + str(self.recuperados))
        # Devolvemos el texto armado.
        return texto


# Registro con numeros DECIMALES: lo usa la solucion matematica (metodo de Euler).
# Aqui se permiten decimales porque las ecuaciones trabajan con "cantidades esperadas".
class RegistroEuler:

    # El constructor recibe los cuatro datos de una fila de la tabla de Euler.
    def __init__(self, tiempo, susceptibles, infectados, recuperados):
        # Paso de tiempo al que pertenece esta fila.
        self.tiempo = tiempo
        # Susceptibles (puede tener decimales).
        self.susceptibles = susceptibles
        # Infectados (puede tener decimales).
        self.infectados = infectados
        # Recuperados (puede tener decimales).
        self.recuperados = recuperados
