# ============================================================
# CONTROLADOR - Coordina el Modelo y la Vista
# ============================================================
# D (Inversion de dependencias): el controlador recibe todo desde
# afuera (generadores, pruebas, vistas, repositorio). No crea nada
# con "new"/constructores propios, solo usa las abstracciones.
# ============================================================

import time


class ControladorSimulacion:

    def __init__(self, pruebas, vista_consola, vista_grafica, repositorio):
        self.pruebas = pruebas              # lista de PruebaEstadistica
        self.vista = vista_consola
        self.vista_grafica = vista_grafica
        self.repositorio = repositorio

    def ejecutar(self, configuraciones, tamanos, n_detalle):
        """
        configuraciones: diccionario {nombre: GeneradorAleatorio}
        tamanos: lista de cantidades N a probar (1000, 10000, ...)
        n_detalle: tamano para el cual se muestra el detalle y el grafico
        """
        filas = []

        for nombre, generador in configuraciones.items():
            self.vista.mostrar_titulo(f"Configuracion '{nombre}': {generador.descripcion()}")

            for n in tamanos:
                # Se mide el tiempo de generar + aplicar las pruebas
                inicio = time.perf_counter()
                numeros = generador.generar(n)
                resultados = [prueba.aplicar(numeros) for prueba in self.pruebas]
                tiempo = time.perf_counter() - inicio

                # Se busca cada resultado por su nombre
                chi = self._buscar(resultados, "Chi-cuadrado")
                ks = self._buscar(resultados, "Kolmogorov-Smirnov")

                # Detalle completo solo para el tamano elegido
                if n == n_detalle:
                    self.vista.mostrar_mensaje(f"\n>> Detalle para N = {n}")
                    self.vista.mostrar_secuencia(numeros, 10)
                    self.vista.mostrar_chi_cuadrado(chi)
                    self.vista.mostrar_kolmogorov(ks)
                    ruta = self.vista_grafica.graficar(f"{nombre}_N{n}", chi, ks)
                    self.vista.mostrar_mensaje(f"Grafico guardado en: {ruta}")
                    # Se guardan los primeros 20 numeros para compararlos con Java
                    self.repositorio.guardar_secuencia(
                        f"secuencia_python_{nombre}.csv", numeros[:20])

                filas.append({
                    "configuracion": nombre,
                    "N": n,
                    "chi2": round(chi.estadistico, 6),
                    "p_chi2": round(chi.valor_p, 6),
                    "decision_chi2": "Rechaza" if chi.se_rechaza_h0() else "No rechaza",
                    "D": round(ks.estadistico, 6),
                    "p_ks": round(ks.valor_p, 6),
                    "decision_ks": "Rechaza" if ks.se_rechaza_h0() else "No rechaza",
                    "tiempo_segundos": round(tiempo, 6),
                })

        self.vista.mostrar_tabla_resumen(filas)
        ruta = self.repositorio.guardar_tabla("resultados_python.csv", filas)
        self.vista.mostrar_mensaje(f"\nTabla guardada en: {ruta}")

    def _buscar(self, resultados, nombre):
        """Devuelve el resultado cuyo nombre coincide."""
        for resultado in resultados:
            if resultado.nombre_prueba == nombre:
                return resultado
        return None
