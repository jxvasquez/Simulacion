# ==============================================================================
# ARCHIVO : sir/dominio/ecuaciones.py
# CAPA    : Dominio
# OBJETIVO: escribir las ecuaciones diferenciales del modelo SIR en codigo Python.
#
#   dS/dt = -beta * S * I / N                  (los susceptibles disminuyen)
#   dI/dt =  beta * S * I / N - gamma * I      (los infectados suben y bajan)
#   dR/dt =  gamma * I                         (los recuperados aumentan)
# ==============================================================================


# Esta clase guarda el resultado de las tres ecuaciones: cuanto cambia cada grupo.
class DerivadasSIR:

    # El constructor recibe los tres cambios calculados.
    def __init__(self, cambio_susceptibles, cambio_infectados, cambio_recuperados):
        # Cambio de los susceptibles (dS): siempre es cero o negativo.
        self.cambio_susceptibles = cambio_susceptibles
        # Cambio de los infectados (dI): puede ser positivo o negativo.
        self.cambio_infectados = cambio_infectados
        # Cambio de los recuperados (dR): siempre es cero o positivo.
        self.cambio_recuperados = cambio_recuperados


# Esta funcion calcula dS, dI y dR para unos valores dados de S, I y R.
def calcular_derivadas(susceptibles, infectados, recuperados, beta, gamma):

    # Paso 1: calculamos la poblacion total N = S + I + R.
    poblacion = susceptibles + infectados + recuperados

    # Paso 2: si la poblacion no es positiva, no podemos dividir. Avisamos del error.
    if poblacion <= 0:
        # Detenemos el calculo con un mensaje claro.
        raise ValueError("La poblacion total debe ser positiva")

    # Paso 3: contagios esperados = beta * S * I / N.
    contagios = beta * susceptibles * infectados / poblacion

    # Paso 4: recuperaciones esperadas = gamma * I.
    recuperaciones = gamma * infectados

    # Paso 5: dS = -contagios (los contagiados dejan de ser susceptibles).
    cambio_susceptibles = -contagios

    # Paso 6: dI = contagios - recuperaciones (entran los contagiados y salen los recuperados).
    cambio_infectados = contagios - recuperaciones

    # Paso 7: dR = recuperaciones (los que se recuperan pasan al grupo R).
    cambio_recuperados = recuperaciones

    # Paso 8: empaquetamos los tres resultados en un objeto DerivadasSIR.
    resultado = DerivadasSIR(cambio_susceptibles, cambio_infectados, cambio_recuperados)

    # Paso 9: devolvemos el objeto con los tres cambios.
    return resultado


# Esta funcion calcula R0, el numero reproductivo basico = beta / gamma.
# R0 indica a cuantas personas contagia, en promedio, una persona infectada.
def numero_reproductivo_basico(beta, gamma):

    # Si gamma es cero o negativo, la division no tiene sentido. Avisamos del error.
    if gamma <= 0:
        # Detenemos el calculo con un mensaje claro.
        raise ValueError("Gamma debe ser positiva")

    # Dividimos beta entre gamma.
    r_cero = beta / gamma

    # Devolvemos el valor de R0.
    return r_cero
