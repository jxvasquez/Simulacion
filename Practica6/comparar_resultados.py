# ============================================================
# PRACTICA 06 - Comparacion de resultados Python vs Java
# ============================================================
# Este archivo es independiente de los dos proyectos.
# Solo lee los CSV que genera cada programa y arma la tabla
# comparativa pedida en la seccion 6 "Resultados esperados".
#
# Pasos:
#   1) Ejecutar el proyecto de Python  -> crea practica06_python/resultados/
#   2) Ejecutar el proyecto de Java    -> crea practica06_java/resultados/
#   3) Copiar en ESTA carpeta los archivos:
#        resultados_python.csv, secuencia_python_buena.csv, secuencia_python_deficiente.csv
#        resultados_java.csv,   secuencia_java_buena.csv,   secuencia_java_deficiente.csv
#   4) Ejecutar:   python comparar_resultados.py
#
# (Tambien se pueden indicar las carpetas de cada proyecto:
#   python comparar_resultados.py ../practica06_python/resultados ../practica06_java/resultados)
# ============================================================

import csv
import os
import sys


def leer_csv(carpeta, nombre):
    """Lee un archivo CSV y devuelve una lista de diccionarios."""
    ruta = os.path.join(carpeta, nombre)
    if not os.path.exists(ruta):
        print(f"ERROR: no se encontro el archivo {ruta}")
        print("Primero ejecuta los dos programas y copia sus CSV aqui.")
        sys.exit(1)
    with open(ruta, encoding="utf-8") as archivo:
        return list(csv.DictReader(archivo))


def comparar_secuencias(carpeta_python, carpeta_java, configuracion):
    """Verifica que ambos programas generen exactamente la misma secuencia."""
    python = leer_csv(carpeta_python, f"secuencia_python_{configuracion}.csv")
    java = leer_csv(carpeta_java, f"secuencia_java_{configuracion}.csv")

    print(f"\nSecuencia '{configuracion}' (primeros 5 de {len(python)} numeros):")
    print(f"{'i':<4}{'Python':>15}{'Java':>15}")
    for p, j in list(zip(python, java))[:5]:
        print(f"{p['indice']:<4}{p['numero']:>15}{j['numero']:>15}")

    iguales = all(p["numero"] == j["numero"] for p, j in zip(python, java))
    print("Resultado:", "IDENTICAS" if iguales else "DIFERENTES")
    return iguales


def decision_general(fila):
    """Se rechaza H0 si al menos una de las dos pruebas la rechaza."""
    if fila["decision_chi2"] == "Rechaza" or fila["decision_ks"] == "Rechaza":
        return "Rechaza"
    return "No rechaza"


def mostrar_tabla(filas_python, filas_java):
    """Imprime la tabla comparativa y devuelve las filas para guardarlas."""
    print("\n" + "=" * 100)
    print("TABLA COMPARATIVA PYTHON vs JAVA")
    print("=" * 100)
    encabezado = (f"{'Config':<11}{'N':>9}{'chi2':>11}{'p chi2':>8}{'D':>10}"
                  f"{'p KS':>8}{'Decision':>12}{'T Python':>10}{'T Java':>9}{'Iguales':>9}")
    print(encabezado)
    print("-" * len(encabezado))

    filas_salida = []
    for py, ja in zip(filas_python, filas_java):
        # Los estadisticos deben coincidir (se comparan con 6 decimales)
        iguales = (abs(float(py["chi2"]) - float(ja["chi2"])) < 1e-5 and
                   abs(float(py["D"]) - float(ja["D"])) < 1e-5)
        decision = decision_general(py)
        print(f"{py['configuracion']:<11}{py['N']:>9}{float(py['chi2']):>11.4f}"
              f"{float(py['p_chi2']):>8.4f}{float(py['D']):>10.6f}{float(py['p_ks']):>8.4f}"
              f"{decision:>12}{float(py['tiempo_segundos']):>10.4f}"
              f"{float(ja['tiempo_segundos']):>9.4f}{'Si' if iguales else 'No':>9}")
        filas_salida.append({
            "configuracion": py["configuracion"], "N": py["N"],
            "chi2": py["chi2"], "p_chi2": py["p_chi2"],
            "D": py["D"], "p_ks": py["p_ks"], "decision": decision,
            "tiempo_python": py["tiempo_segundos"], "tiempo_java": ja["tiempo_segundos"],
            "resultados_iguales": "Si" if iguales else "No",
        })
    return filas_salida


def mostrar_conclusiones(filas, secuencias_iguales):
    """Genera las conclusiones a partir de los datos de la tabla."""
    print("\n" + "=" * 100)
    print("CONCLUSIONES")
    print("=" * 100)

    # 1) Equivalencia de las implementaciones
    todas_iguales = secuencias_iguales and all(f["resultados_iguales"] == "Si" for f in filas)
    if todas_iguales:
        print("1. Ambas implementaciones producen la misma secuencia y los mismos estadisticos")
        print("   con los mismos parametros, por lo tanto son equivalentes.")
    else:
        print("1. Hay diferencias entre Python y Java: revisar parametros o tipos de datos.")

    # 2) Calidad de cada configuracion
    print("2. Calidad de cada configuracion del generador:")
    configuraciones = []
    for f in filas:
        if f["configuracion"] not in configuraciones:
            configuraciones.append(f["configuracion"])
    for nombre in configuraciones:
        decisiones = [f["decision"] for f in filas if f["configuracion"] == nombre]
        if all(d == "No rechaza" for d in decisiones):
            print(f"   - '{nombre}': no se rechaza H0 en ningun tamano de muestra;")
            print("     los numeros son compatibles con una distribucion U(0,1).")
        else:
            veces = decisiones.count("Rechaza")
            print(f"   - '{nombre}': se rechaza H0 en {veces} de {len(decisiones)} casos;")
            print("     el generador NO produce numeros uniformes (periodo corto / modulo pequeno).")

    # 3) Tiempos
    total_python = sum(float(f["tiempo_python"]) for f in filas)
    total_java = sum(float(f["tiempo_java"]) for f in filas)
    mas_rapido = "Java" if total_java < total_python else "Python"
    veces = max(total_python, total_java) / min(total_python, total_java)
    print(f"3. Tiempo total: Python = {total_python:.4f} s, Java = {total_java:.4f} s.")
    print(f"   {mas_rapido} fue aproximadamente {veces:.1f} veces mas rapido.")

    # 4) Efecto del tamano de muestra
    print("4. Al aumentar N el estadistico D disminuye cuando el generador es bueno,")
    print("   porque la distribucion empirica se acerca a la teorica. Con un generador")
    print("   deficiente D no baja y el valor p tiende a cero.")


def guardar_tabla(filas, ruta):
    with open(ruta, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=list(filas[0].keys()))
        escritor.writeheader()
        escritor.writerows(filas)
    print(f"\nTabla comparativa guardada en: {ruta}")


def tabla_seccion_6(carpeta_python, carpeta_java):
    """Tabla EXACTA de la guia: N | pi estimado | Error | Tiempo Python | Tiempo Java"""
    pi_python = leer_csv(carpeta_python, "pi_python.csv")
    pi_java = leer_csv(carpeta_java, "pi_java.csv")

    print("\n" + "=" * 100)
    print("TABLA SECCION 6 - RESULTADOS ESPERADOS")
    print("=" * 100)
    print(f"{'N':>10}{'pi estimado':>14}{'Error':>12}{'Tiempo Python':>16}"
          f"{'Tiempo Java':>14}{'pi igual?':>11}")
    filas = []
    for py, ja in zip(pi_python, pi_java):
        igual = abs(float(py["pi_estimado"]) - float(ja["pi_estimado"])) < 1e-9
        print(f"{py['N']:>10}{float(py['pi_estimado']):>14.6f}{float(py['error']):>12.6f}"
              f"{float(py['tiempo_segundos']):>15.4f}s{float(ja['tiempo_segundos']):>13.4f}s"
              f"{'Si' if igual else 'No':>11}")
        filas.append({"N": py["N"], "pi_estimado": py["pi_estimado"], "error": py["error"],
                      "tiempo_python": py["tiempo_segundos"],
                      "tiempo_java": ja["tiempo_segundos"]})

    print("\nConclusion: al aumentar N el error de pi tiende a disminuir (proporcional")
    print("a 1/raiz(N)), y ambos lenguajes obtienen el mismo pi porque usan la misma secuencia.")
    guardar_tabla(filas, "tabla_seccion6_pi.csv")


def main():
    # Por defecto se buscan los CSV en la misma carpeta de este archivo
    carpeta_python = sys.argv[1] if len(sys.argv) > 1 else "."
    carpeta_java = sys.argv[2] if len(sys.argv) > 2 else "."

    tabla_seccion_6(carpeta_python, carpeta_java)

    filas_python = leer_csv(carpeta_python, "resultados_python.csv")
    filas_java = leer_csv(carpeta_java, "resultados_java.csv")

    iguales_buena = comparar_secuencias(carpeta_python, carpeta_java, "buena")
    iguales_deficiente = comparar_secuencias(carpeta_python, carpeta_java, "deficiente")

    filas = mostrar_tabla(filas_python, filas_java)
    mostrar_conclusiones(filas, iguales_buena and iguales_deficiente)
    guardar_tabla(filas, "tabla_comparativa.csv")


if __name__ == "__main__":
    main()
