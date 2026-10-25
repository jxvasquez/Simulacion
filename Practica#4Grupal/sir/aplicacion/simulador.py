# ==============================================================================
# ARCHIVO : sir/aplicacion/simulador.py
# CAPA    : Aplicacion
# OBJETIVO: simular el modelo SIR persona por persona, paso de tiempo por paso de tiempo.
# ==============================================================================

# random: modulo de Python para generar numeros aleatorios.
import random

# simpy: libreria de simulacion. Aqui la usamos como "reloj" que avanza de 1 en 1.
import simpy

# Importamos los nombres de los tres estados desde la capa de dominio.
from sir.dominio.estados import ESTADO_SUSCEPTIBLE
# Importamos el estado infectado.
from sir.dominio.estados import ESTADO_INFECTADO
# Importamos el estado recuperado.
from sir.dominio.estados import ESTADO_RECUPERADO
# Importamos la clase que representa una fila de resultados.
from sir.dominio.registro_sir import RegistroSIR
# Importamos la regla matematica del contagio.
from sir.dominio.reglas import probabilidad_infeccion


# Esta clase es el simulador. Cada objeto SimuladorSIR representa UNA simulacion completa.
class SimuladorSIR:

    # El constructor prepara todo lo necesario ANTES de empezar a simular.
    def __init__(self, configuracion):

        # Guardamos la configuracion (poblacion, beta, gamma, pasos, semilla...).
        self.configuracion = configuracion

        # Creamos el generador de numeros aleatorios con la semilla indicada.
        # Con la misma semilla, la simulacion siempre da los mismos resultados.
        self.generador_aleatorio = random.Random(configuracion.semilla)

        # Creamos una lista vacia donde guardaremos el estado de cada persona.
        # La posicion 0 de la lista es la persona 0, la posicion 1 es la persona 1, etc.
        self.estados = []

        # Repetimos una vez por cada persona infectada al inicio.
        for contador in range(configuracion.infectados_iniciales):
            # Agregamos una persona infectada a la lista.
            self.estados.append(ESTADO_INFECTADO)

        # Repetimos una vez por cada persona susceptible al inicio.
        for contador in range(configuracion.susceptibles_iniciales):
            # Agregamos una persona susceptible a la lista.
            self.estados.append(ESTADO_SUSCEPTIBLE)

        # Mezclamos la lista para que los infectados queden en posiciones al azar.
        self.generador_aleatorio.shuffle(self.estados)

        # Creamos la lista vacia donde se guardara el historial (una fila por paso de tiempo).
        self.historial = []

    # Este metodo cuenta cuantas personas hay en cada estado y guarda una fila en el historial.
    def registrar_estado_actual(self, tiempo):

        # Contamos las personas susceptibles de la lista de estados.
        cantidad_susceptibles = self.estados.count(ESTADO_SUSCEPTIBLE)

        # Contamos las personas infectadas.
        cantidad_infectados = self.estados.count(ESTADO_INFECTADO)

        # Contamos las personas recuperadas.
        cantidad_recuperados = self.estados.count(ESTADO_RECUPERADO)

        # Creamos una fila de resultados con los tres conteos.
        registro = RegistroSIR(tiempo, cantidad_susceptibles, cantidad_infectados,
                               cantidad_recuperados)

        # Agregamos la fila al final del historial.
        self.historial.append(registro)

    # Este metodo avanza la simulacion UN paso de tiempo.
    # Los cambios son simultaneos: todos se deciden mirando la foto del paso anterior.
    def avanzar_un_paso(self):

        # Paso 1: sacamos una copia de la lista de estados (la "foto" del paso anterior).
        estados_anteriores = list(self.estados)

        # Paso 2: contamos cuantos infectados habia en esa foto.
        cantidad_infectados = estados_anteriores.count(ESTADO_INFECTADO)

        # Paso 3: calculamos la probabilidad de que un susceptible se contagie en este paso.
        probabilidad_contagio = probabilidad_infeccion(self.configuracion.beta,
                                                       cantidad_infectados,
                                                       self.configuracion.poblacion)

        # Paso 4: preparamos la lista de estados nuevos, empezando como copia de la anterior.
        estados_siguientes = list(estados_anteriores)

        # Paso 5: revisamos a las personas una por una, desde la posicion 0 hasta la ultima.
        for indice in range(len(estados_anteriores)):

            # Leemos el estado que tenia esta persona en el paso anterior.
            estado_actual = estados_anteriores[indice]

            # Caso A: la persona estaba susceptible.
            if estado_actual == ESTADO_SUSCEPTIBLE:

                # Sacamos un numero al azar entre 0 y 1.
                numero_al_azar = self.generador_aleatorio.random()

                # Si el numero es menor que la probabilidad de contagio, la persona se contagia.
                if numero_al_azar < probabilidad_contagio:
                    # Cambiamos su estado a infectado en la lista nueva.
                    estados_siguientes[indice] = ESTADO_INFECTADO

            # Caso B: la persona estaba infectada.
            elif estado_actual == ESTADO_INFECTADO:

                # Sacamos un numero al azar entre 0 y 1.
                numero_al_azar = self.generador_aleatorio.random()

                # Si el numero es menor que gamma, la persona se recupera.
                if numero_al_azar < self.configuracion.gamma:
                    # Cambiamos su estado a recuperado en la lista nueva.
                    estados_siguientes[indice] = ESTADO_RECUPERADO

            # Caso C: la persona estaba recuperada. No hacemos nada, sigue recuperada.

        # Paso 6: la lista nueva pasa a ser la lista oficial de estados.
        self.estados = estados_siguientes

    # Este metodo es el PROCESO de SimPy: la "historia" de la simulacion a lo largo del tiempo.
    # Tiene la palabra "yield", por eso Python lo trata como un generador:
    # cada vez que llega a un "yield", se pausa y le devuelve el control al reloj de SimPy.
    def proceso_simulacion(self, entorno):

        # Guardamos la foto del tiempo 0, antes de que ocurra cualquier contagio.
        self.registrar_estado_actual(0)

        # Repetimos para los tiempos 1, 2, 3, ... hasta el ultimo paso (inclusive).
        for tiempo in range(1, self.configuracion.pasos + 1):

            # Le pedimos al reloj de SimPy que avance 1 unidad de tiempo.
            # La simulacion se pausa aqui y continua cuando el reloj llega al nuevo instante.
            yield entorno.timeout(1)

            # Ya paso una unidad de tiempo: calculamos los cambios de este paso.
            self.avanzar_un_paso()

            # Guardamos la foto de este instante en el historial.
            self.registrar_estado_actual(tiempo)

    # Este metodo ejecuta la simulacion completa y devuelve el historial.
    def ejecutar(self):

        # Borramos cualquier historial anterior.
        self.historial = []

        # Creamos el entorno de SimPy (el reloj de la simulacion).
        entorno = simpy.Environment()

        # Registramos nuestro proceso dentro del entorno para que SimPy lo ejecute.
        entorno.process(self.proceso_simulacion(entorno))

        # Ponemos a correr el reloj hasta que el proceso termine.
        entorno.run()

        # Devolvemos la lista de filas (una por cada paso de tiempo).
        return self.historial
