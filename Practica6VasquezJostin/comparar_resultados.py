# ============================================================
# Comparacion Python vs Java (seccion 6 "Resultados esperados")
# ============================================================
# Ejecutar DESPUES de correr los dos programas:
#   python comparar_resultados.py
# Lee los CSV de la carpeta 'resultados' y arma la tabla comparativa.
# ============================================================

import csv
import os

CARPETA = "resultados"


def leer_csv(nombre):
    with open(os.path.join(CARPETA, nombre), encoding="utf-8") as archivo:
        return list(csv.DictReader(archivo))


def comparar_secuencias(configuracion):
    """Verifica que ambos programas generen exactamente la misma secuencia."""
    python = leer_csv(f"secuencia_python_{configuracion}.csv")
    java = leer_csv(f"secuencia_java_{configuracion}.csv")
    iguales = all(p["numero"] == j["numero"] for p, j in zip(python, java))
    print(f"Secuencia '{configuracion}': "
          f"{'IDENTICA en Python y Java' if iguales else 'DIFERENTE'} "
          f"(primeros {len(python)} numeros)")


def main():
    filas_python = leer_csv("resultados_python.csv")
    filas_java = leer_csv("resultados_java.csv")

    comparar_secuencias("buena")
    comparar_secuencias("deficiente")

    print()
    encabezado = (f"{'Config':<11}{'N':>9}{'chi2':>11}{'p chi2':>8}{'D':>10}"
                  f"{'p KS':>8}{'Decision':>12}{'T Python':>10}{'T Java':>9}{'Iguales':>9}")
    print(encabezado)
    print("-" * len(encabezado))

    lineas_csv = []
    for py, ja in zip(filas_python, filas_java):
        # Los estadisticos deben coincidir (se comparan con 6 decimales)
        iguales = (abs(float(py["chi2"]) - float(ja["chi2"])) < 1e-5 and
                   abs(float(py["D"]) - float(ja["D"])) < 1e-5)
        decision = "Rechaza" if "Rechaza" == py["decision_chi2"] or "Rechaza" == py["decision_ks"] else "No rechaza"
        print(f"{py['configuracion']:<11}{py['N']:>9}{float(py['chi2']):>11.4f}"
              f"{float(py['p_chi2']):>8.4f}{float(py['D']):>10.6f}{float(py['p_ks']):>8.4f}"
              f"{decision:>12}{float(py['tiempo_segundos']):>10.4f}"
              f"{float(ja['tiempo_segundos']):>9.4f}{'Si' if iguales else 'No':>9}")
        lineas_csv.append([py["configuracion"], py["N"], py["chi2"], py["p_chi2"],
                           py["D"], py["p_ks"], decision,
                           py["tiempo_segundos"], ja["tiempo_segundos"],
                           "Si" if iguales else "No"])

    ruta = os.path.join(CARPETA, "tabla_comparativa.csv")
    with open(ruta, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["configuracion", "N", "chi2", "p_chi2", "D", "p_ks",
                           "decision", "tiempo_python", "tiempo_java", "resultados_iguales"])
        escritor.writerows(lineas_csv)
    print(f"\nTabla comparativa guardada en: {ruta}")


if __name__ == "__main__":
    main()
