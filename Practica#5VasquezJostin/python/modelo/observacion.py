# ------------------------------------------------------------
# Archivo: observacion.py
# Responsabilidad unica (S de SOLID): guardar UN valor generado.
# ------------------------------------------------------------


class Observacion:
    """Representa un numero generado por el generador."""

    def __init__(self, indice, valor_x, valor_u):
        # indice  -> posicion del numero en la secuencia (1, 2, 3, ...)
        # valor_x -> numero entero X(n) producido por la formula
        # valor_u -> numero normalizado U(n) = X(n) / m, siempre entre 0 y 1
        self.indice = indice
        self.valor_x = valor_x
        self.valor_u = valor_u
