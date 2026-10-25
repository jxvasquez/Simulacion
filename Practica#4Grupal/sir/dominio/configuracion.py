# ==============================================================================
# ARCHIVO : sir/dominio/configuracion.py
# CAPA    : Dominio
# OBJETIVO: guardar los parametros del modelo SIR y comprobar que sean validos.
# ==============================================================================


# Una CLASE es un molde para crear objetos. Esta clase es el molde de la configuracion.
class ConfiguracionSIR:

    # __init__ se ejecuta automaticamente cada vez que se crea una configuracion nueva.
    # Los valores que aparecen despues del signo "=" son los valores por defecto de la guia.
    # "self" representa al propio objeto que se esta creando.
    def __init__(self, poblacion=100, infectados_iniciales=5, beta=0.30, gamma=0.10,
                 pasos=100, semilla=42):

        # Regla 1: tiene que existir al menos una persona en la poblacion.
        if poblacion < 1:
            # Si la regla se rompe, detenemos el programa avisando cual fue el error.
            raise ValueError("La poblacion debe ser como minimo 1")

        # Regla 2: no puede haber una cantidad negativa de infectados iniciales.
        if infectados_iniciales < 0:
            # Avisamos del error de la regla 2.
            raise ValueError("Los infectados iniciales no pueden ser negativos")

        # Regla 3: no puede haber mas infectados que personas en total.
        if infectados_iniciales > poblacion:
            # Avisamos del error de la regla 3.
            raise ValueError("Los infectados iniciales no pueden superar a la poblacion")

        # Regla 4: beta es una probabilidad, por eso debe estar entre 0 y 1.
        if beta < 0 or beta > 1:
            # Avisamos del error de la regla 4.
            raise ValueError("Beta (tasa de contagio) debe estar entre 0 y 1")

        # Regla 5: gamma tambien es una probabilidad, entre 0 y 1.
        if gamma < 0 or gamma > 1:
            # Avisamos del error de la regla 5.
            raise ValueError("Gamma (tasa de recuperacion) debe estar entre 0 y 1")

        # Regla 6: la cantidad de pasos de tiempo no puede ser negativa.
        if pasos < 0:
            # Avisamos del error de la regla 6.
            raise ValueError("La cantidad de pasos no puede ser negativa")

        # Si llegamos hasta aqui, todos los valores son validos y los guardamos.
        # N: cantidad total de personas.
        self.poblacion = poblacion

        # I(0): cantidad de personas infectadas al comenzar.
        self.infectados_iniciales = infectados_iniciales

        # beta: probabilidad de contagio.
        self.beta = beta

        # gamma: probabilidad de recuperacion en cada paso.
        self.gamma = gamma

        # Cantidad de pasos de tiempo que se van a simular.
        self.pasos = pasos

        # Semilla del generador de numeros aleatorios (misma semilla = mismos resultados).
        self.semilla = semilla

        # S(0) = N - I(0): los que no estan infectados al comenzar son susceptibles.
        self.susceptibles_iniciales = poblacion - infectados_iniciales

        # R(0) = 0: al comenzar nadie se ha recuperado todavia.
        self.recuperados_iniciales = 0
