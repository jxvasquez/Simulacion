# ------------------------------------------------------------
# Archivo: controlador_lcg.py
# El controlador coordina los pasos de la practica.
#
# Principio D (Inversion de dependencias): el controlador NO crea sus
# dependencias; las recibe ya creadas en el constructor (desde main.py).
# Asi podemos cambiar el generador, la vista o el exportador sin tocar
# este archivo.
# ------------------------------------------------------------


class ControladorLCG:
    """Ejecuta los pasos 1 al 8 de la guia de practica."""

    def __init__(self, generador, parametros, vista_consola, vista_grafica,
                 exportador, analizador, estadisticas):
        self.generador = generador          # cualquier GeneradorAleatorio
        self.parametros = parametros        # ParametrosLCG
        self.vista = vista_consola          # VistaConsola
        self.vista_grafica = vista_grafica  # VistaGrafica
        self.exportador = exportador        # ExportadorCSV
        self.analizador = analizador        # AnalizadorPeriodo
        self.estadisticas = estadisticas    # Estadisticas

    # ---------- Pasos 1 al 5: generar, mostrar, exportar y graficar ----------
    def generar_secuencia_principal(self, cantidad, cantidad_tabla, ruta_csv, ruta_grafico):
        self.vista.mostrar_titulo("PASO 1: Parametros del generador LCG")
        self.vista.mostrar_parametros(self.parametros)

        self.vista.mostrar_titulo(f"PASO 2: Generando {cantidad} valores")
        self.generador.reiniciar(self.parametros.semilla)
        observaciones = self.generador.generar_secuencia(cantidad)
        self.vista.mostrar_mensaje(f"  Se generaron {len(observaciones)} valores.")

        self.vista.mostrar_titulo(f"PASO 4: Primeras {cantidad_tabla} observaciones")
        self.vista.mostrar_tabla(observaciones, cantidad_tabla)

        self.exportador.exportar(observaciones, ruta_csv)
        self.vista.mostrar_mensaje(f"\n  Secuencia guardada en: {ruta_csv}")

        self.vista.mostrar_titulo("PASO 5: Grafico de la secuencia")
        titulo = f"LCG semilla = {self.parametros.semilla}"
        self.vista_grafica.graficar_secuencia(observaciones, ruta_grafico, titulo)
        self.vista.mostrar_mensaje(f"  Grafico guardado en: {ruta_grafico}")

        self._mostrar_estadisticas(f"semilla {self.parametros.semilla}", observaciones)
        return observaciones

    # ---------- Paso 6: analisis del periodo ----------
    def analizar_periodo(self, observaciones):
        self.vista.mostrar_titulo("PASO 6: Analisis del periodo")
        self.vista.mostrar_mensaje("  Teorema de Hull-Dobell:")
        resultado = self.analizador.cumple_hull_dobell(self.parametros)
        self.vista.mostrar_hull_dobell(resultado)

        if resultado["periodo completo"]:
            self.vista.mostrar_mensaje(
                f"\n  => El periodo es COMPLETO: {self.parametros.m} valores antes de repetirse.")
        else:
            self.vista.mostrar_mensaje("\n  => El periodo NO es completo.")

        repeticion = self.analizador.buscar_repeticion(observaciones)
        if repeticion is None:
            self.vista.mostrar_mensaje(
                f"  En los {len(observaciones)} valores generados no se repite ningun X(n).")
        else:
            self.vista.mostrar_mensaje(f"  Primer valor repetido en la posicion {repeticion}.")

    # ---------- Pasos 7 y 8: cambiar semilla y comparar ----------
    def comparar_con_otra_semilla(self, observaciones_originales, nueva_semilla,
                                  cantidad, cantidad_tabla, ruta_grafico):
        self.vista.mostrar_titulo(f"PASO 7: Cambio de semilla a {nueva_semilla}")
        self.generador.reiniciar(nueva_semilla)
        nuevas = self.generador.generar_secuencia(cantidad)

        self.vista.mostrar_titulo("PASO 8: Comparacion de resultados entre semillas")
        self.vista.mostrar_comparacion_semillas(
            observaciones_originales, nuevas,
            self.parametros.semilla, nueva_semilla, cantidad_tabla)

        self._mostrar_estadisticas(f"semilla {self.parametros.semilla}", observaciones_originales)
        self._mostrar_estadisticas(f"semilla {nueva_semilla}", nuevas)

        titulo = f"LCG semilla = {nueva_semilla}"
        self.vista_grafica.graficar_secuencia(nuevas, ruta_grafico, titulo)
        self.vista.mostrar_mensaje(f"\n  Grafico guardado en: {ruta_grafico}")

    # ---------- Extra: que pasa con parametros inadecuados ----------
    def demostrar_parametros_inadecuados(self, generador_malo, parametros_malos, cantidad_tabla):
        self.vista.mostrar_titulo("EXTRA: Generador con parametros inadecuados")
        self.vista.mostrar_parametros(parametros_malos)
        self.vista.mostrar_mensaje("")
        self.vista.mostrar_hull_dobell(self.analizador.cumple_hull_dobell(parametros_malos))

        periodo = self.analizador.calcular_periodo(
            generador_malo, parametros_malos.semilla, parametros_malos.m + 1)
        self.vista.mostrar_mensaje(
            f"\n  Periodo real = {periodo} (el maximo posible seria {parametros_malos.m})")

        generador_malo.reiniciar(parametros_malos.semilla)
        observaciones = generador_malo.generar_secuencia(cantidad_tabla)
        self.vista.mostrar_tabla(observaciones, cantidad_tabla)
        self.vista.mostrar_mensaje("  Observe como los valores se repiten muy rapido.")

    # ---------- Metodo auxiliar privado ----------
    def _mostrar_estadisticas(self, nombre, observaciones):
        valores = [obs.valor_u for obs in observaciones]
        self.vista.mostrar_estadisticas(
            nombre,
            self.estadisticas.media(valores),
            self.estadisticas.varianza(valores),
            self.estadisticas.minimo(valores),
            self.estadisticas.maximo(valores))
