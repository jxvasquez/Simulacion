# ============================================================
# VISTA - Graficos con Matplotlib
# ============================================================
# Paso 14 del algoritmo KS: comparar graficamente la distribucion
# acumulada empirica con la teorica. Tambien se dibuja el
# histograma usado en la prueba Chi-cuadrado.
# ============================================================

import os
import matplotlib
matplotlib.use("Agg")  # permite guardar imagenes sin abrir ventanas
import matplotlib.pyplot as plt


class VistaGrafica:

    def __init__(self, carpeta_salida):
        self.carpeta_salida = carpeta_salida
        os.makedirs(carpeta_salida, exist_ok=True)

    def graficar(self, nombre, resultado_chi, resultado_ks):
        """Crea una imagen con el histograma y las dos funciones acumuladas."""
        figura, (eje1, eje2) = plt.subplots(1, 2, figsize=(12, 4.5))

        # ----- Grafico 1: frecuencias observadas vs esperadas -----
        observadas = resultado_chi.detalles["observadas"]
        esperada = resultado_chi.detalles["esperada"]
        k = len(observadas)
        etiquetas = [f"{i / k:.1f}" for i in range(k)]
        eje1.bar(etiquetas, observadas, color="#4C78A8", label="Observada")
        eje1.axhline(esperada, color="#E45756", linestyle="--", label="Esperada")
        eje1.set_title(f"Chi-cuadrado  (p = {resultado_chi.valor_p:.4f})")
        eje1.set_xlabel("Inicio del intervalo")
        eje1.set_ylabel("Frecuencia")
        eje1.legend()

        # ----- Grafico 2: acumulada empirica vs teorica -----
        ordenados = resultado_ks.detalles["ordenados"]
        n = len(ordenados)
        # Si hay muchos datos se toma uno de cada 'paso' para que el grafico sea rapido
        paso = max(1, n // 2000)
        x = ordenados[::paso]
        y_empirica = [(i * paso + 1) / n for i in range(len(x))]
        eje2.step(x, y_empirica, where="post", color="#4C78A8", label="Fn(x) empirica")
        eje2.plot([0, 1], [0, 1], color="#E45756", linestyle="--", label="F(x) = x teorica")
        eje2.set_title(f"Kolmogorov-Smirnov  (D = {resultado_ks.estadistico:.4f}, "
                       f"p = {resultado_ks.valor_p:.4f})")
        eje2.set_xlabel("x")
        eje2.set_ylabel("Probabilidad acumulada")
        eje2.legend()

        figura.suptitle(nombre)
        figura.tight_layout()

        ruta = os.path.join(self.carpeta_salida, f"grafico_{nombre}.png")
        figura.savefig(ruta, dpi=110)
        plt.close(figura)
        return ruta
