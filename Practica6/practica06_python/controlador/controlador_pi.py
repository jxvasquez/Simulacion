# ============================================================
# CONTROLADOR - Tabla de la seccion 6 (pi estimado, error, tiempo)
# ============================================================
# Es un controlador aparte (S: responsabilidad unica), asi no se
# modifica el controlador de las pruebas estadisticas (O: abierto/cerrado).
# ============================================================

import time


class ControladorPi:

    def __init__(self, estimador, vista_consola, repositorio):
        self.estimador = estimador
        self.vista = vista_consola
        self.repositorio = repositorio

    def ejecutar(self, tamanos):
        filas = []
        for n in tamanos:
            inicio = time.perf_counter()
            pi_estimado, error = self.estimador.estimar(n)
            tiempo = time.perf_counter() - inicio

            filas.append({
                "N": n,
                "pi_estimado": round(pi_estimado, 6),
                "error": round(error, 6),
                "tiempo_segundos": round(tiempo, 6),
            })

        self.vista.mostrar_tabla_pi(filas)
        ruta = self.repositorio.guardar_tabla_pi("pi_python.csv", filas)
        self.vista.mostrar_mensaje(f"\nTabla de pi guardada en: {ruta}")
