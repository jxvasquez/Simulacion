# ------------------------------------------------------------
# Archivo: parametros_lcg.py
# Responsabilidad unica: guardar y validar los parametros del LCG.
# ------------------------------------------------------------


class ParametrosLCG:
    """Agrupa los parametros a, c, m y la semilla del generador."""

    def __init__(self, a, c, m, semilla):
        # Antes de guardar los datos verificamos que sean correctos
        self._validar(a, c, m, semilla)
        self.a = a              # multiplicador
        self.c = c              # incremento
        self.m = m              # modulo
        self.semilla = semilla  # valor inicial X(0)

    def _validar(self, a, c, m, semilla):
        """Lanza un error si algun parametro no tiene sentido."""
        if m <= 0:
            raise ValueError("El modulo m debe ser mayor que 0")
        if a <= 0 or a >= m:
            raise ValueError("El multiplicador a debe cumplir 0 < a < m")
        if c < 0 or c >= m:
            raise ValueError("El incremento c debe cumplir 0 <= c < m")
        if semilla < 0 or semilla >= m:
            raise ValueError("La semilla debe cumplir 0 <= semilla < m")
