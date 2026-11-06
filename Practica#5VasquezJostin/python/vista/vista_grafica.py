# ------------------------------------------------------------
# Archivo: vista_grafica.py
# Responsabilidad unica: dibujar graficos de la secuencia.
# Usa la libreria matplotlib (instalar con: pip install matplotlib)
# ------------------------------------------------------------

import os

import matplotlib

# "Agg" permite guardar imagenes sin abrir ventanas
# (funciona en cualquier computador, incluso sin entorno grafico)
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402


class VistaGrafica:
    """Genera y guarda graficos de la secuencia en archivos PNG."""

    def graficar_secuencia(self, observaciones, ruta, titulo):
        """
        Crea una imagen con 3 graficos:
          1) U(n) en el orden en que se generaron (primeros 200 valores)
          2) Histograma de U(n) (deberia verse casi plano = uniforme)
          3) Dispersion U(n) vs U(n+1) (no deberia verse ningun patron)
        """
        valores_u = [obs.valor_u for obs in observaciones]
        indices = [obs.indice for obs in observaciones]

        figura, ejes = plt.subplots(1, 3, figsize=(16, 4.5))
        figura.suptitle(titulo)

        # Grafico 1: secuencia en el tiempo
        cantidad = min(200, len(valores_u))
        ejes[0].plot(indices[:cantidad], valores_u[:cantidad], marker="o", markersize=3, linewidth=0.8)
        ejes[0].set_title(f"Secuencia U(n) - primeros {cantidad}")
        ejes[0].set_xlabel("n")
        ejes[0].set_ylabel("U(n)")

        # Grafico 2: histograma
        ejes[1].hist(valores_u, bins=20, edgecolor="black")
        ejes[1].set_title("Histograma de U(n)")
        ejes[1].set_xlabel("U(n)")
        ejes[1].set_ylabel("Frecuencia")

        # Grafico 3: cada valor contra el siguiente
        ejes[2].scatter(valores_u[:-1], valores_u[1:], s=1)
        ejes[2].set_title("U(n) vs U(n+1)")
        ejes[2].set_xlabel("U(n)")
        ejes[2].set_ylabel("U(n+1)")

        figura.tight_layout()
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        figura.savefig(ruta, dpi=110)
        plt.close(figura)
