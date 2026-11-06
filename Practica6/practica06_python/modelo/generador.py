# ============================================================
# MODELO - Generadores de numeros pseudoaleatorios
# ============================================================
# Principios SOLID aplicados:
#  - S (Responsabilidad unica): esta clase SOLO genera numeros.
#  - O (Abierto/Cerrado): si se quiere otro generador se crea una
#    nueva clase que herede de GeneradorAleatorio, sin tocar esta.
#  - L (Sustitucion de Liskov): cualquier hijo de GeneradorAleatorio
#    puede usarse donde se espera un GeneradorAleatorio.
#  - D (Inversion de dependencias): el controlador depende de la
#    abstraccion GeneradorAleatorio, no de GeneradorLCG directamente.
# ============================================================

from abc import ABC, abstractmethod


class GeneradorAleatorio(ABC):
    """Abstraccion (interfaz) de cualquier generador pseudoaleatorio."""

    @abstractmethod
    def generar(self, cantidad):
        """Debe devolver una lista con 'cantidad' numeros en [0, 1)."""
        pass

    @abstractmethod
    def descripcion(self):
        """Devuelve un texto con los parametros del generador."""
        pass


class GeneradorLCG(GeneradorAleatorio):
    """Generador congruencial lineal: X(n+1) = (a * X(n) + c) mod m"""

    def __init__(self, semilla, multiplicador, incremento, modulo):
        # Paso 2 del algoritmo: definir los parametros del generador
        self.semilla = semilla
        self.multiplicador = multiplicador
        self.incremento = incremento
        self.modulo = modulo

    def generar(self, cantidad):
        numeros = []                 # lista donde se almacenan los resultados
        valor_actual = self.semilla  # paso 3: la semilla es el valor inicial

        # Paso 4: repetir hasta completar la cantidad pedida
        for _ in range(cantidad):
            # Pasos 5, 6 y 7: multiplicar, sumar el incremento y sacar el residuo
            valor_actual = (self.multiplicador * valor_actual + self.incremento) % self.modulo

            # Paso 8: dividir para obtener un numero entre 0 y 1
            numero = valor_actual / self.modulo

            # Paso 9: almacenar el numero obtenido
            numeros.append(numero)
            # Paso 10: valor_actual ya quedo actualizado para la siguiente vuelta

        return numeros

    def descripcion(self):
        return (f"LCG(semilla={self.semilla}, a={self.multiplicador}, "
                f"c={self.incremento}, m={self.modulo})")
