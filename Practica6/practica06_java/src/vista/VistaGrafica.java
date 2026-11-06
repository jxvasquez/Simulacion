package vista;

import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Font;
import java.awt.Graphics2D;
import java.awt.RenderingHints;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.Locale;
import javax.imageio.ImageIO;
import modelo.ResultadoPrueba;

// ============================================================
// VISTA - Grafico de la prueba KS (paso 14 del algoritmo)
// ============================================================
// Dibuja la distribucion acumulada empirica Fn(x) y la teorica
// F(x) = x usando solo Java estandar (sin librerias externas)
// y guarda la imagen como PNG.
// ============================================================
public class VistaGrafica {

    private static final int ANCHO = 700;
    private static final int ALTO = 500;
    private static final int MARGEN = 60;

    private final String carpetaSalida;

    public VistaGrafica(String carpetaSalida) {
        this.carpetaSalida = carpetaSalida;
        new File(carpetaSalida).mkdirs();
    }

    public String graficar(String nombre, ResultadoPrueba resultadoKs) throws IOException {
        double[] ordenados = (double[]) resultadoKs.getDetalle("ordenados");
        int n = ordenados.length;

        BufferedImage imagen = new BufferedImage(ANCHO, ALTO, BufferedImage.TYPE_INT_RGB);
        Graphics2D g = imagen.createGraphics();
        g.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);

        // Fondo blanco
        g.setColor(Color.WHITE);
        g.fillRect(0, 0, ANCHO, ALTO);

        // Ejes
        g.setColor(Color.BLACK);
        g.drawLine(MARGEN, ALTO - MARGEN, ANCHO - MARGEN, ALTO - MARGEN); // eje x
        g.drawLine(MARGEN, MARGEN, MARGEN, ALTO - MARGEN);                // eje y
        g.drawString("0", MARGEN - 15, ALTO - MARGEN + 15);
        g.drawString("1", ANCHO - MARGEN, ALTO - MARGEN + 15);
        g.drawString("1", MARGEN - 15, MARGEN + 5);
        g.drawString("x", ANCHO / 2, ALTO - 20);

        // Linea teorica F(x) = x (roja)
        g.setColor(new Color(228, 87, 86));
        g.setStroke(new BasicStroke(2f, BasicStroke.CAP_BUTT, BasicStroke.JOIN_MITER,
                10f, new float[]{8f, 6f}, 0f));
        g.drawLine(aPixelX(0), aPixelY(0), aPixelX(1), aPixelY(1));

        // Funcion empirica Fn(x) en escalones (azul)
        g.setColor(new Color(76, 120, 168));
        g.setStroke(new BasicStroke(1.5f));
        int paso = Math.max(1, n / 2000); // se dibujan como maximo ~2000 puntos
        double xAnterior = 0;
        double yAnterior = 0;
        for (int i = 0; i < n; i += paso) {
            double x = ordenados[i];
            double y = (double) (i + 1) / n;
            // escalon: horizontal y luego vertical
            g.drawLine(aPixelX(xAnterior), aPixelY(yAnterior), aPixelX(x), aPixelY(yAnterior));
            g.drawLine(aPixelX(x), aPixelY(yAnterior), aPixelX(x), aPixelY(y));
            xAnterior = x;
            yAnterior = y;
        }

        // Titulo y leyenda
        g.setColor(Color.BLACK);
        g.setFont(new Font("SansSerif", Font.BOLD, 14));
        g.drawString(String.format(Locale.US, "%s  |  D = %.4f  p = %.4f",
                nombre, resultadoKs.getEstadistico(), resultadoKs.getValorP()), MARGEN, 30);
        g.setFont(new Font("SansSerif", Font.PLAIN, 12));
        g.setColor(new Color(76, 120, 168));
        g.drawString("Fn(x) empirica", MARGEN + 20, MARGEN + 20);
        g.setColor(new Color(228, 87, 86));
        g.drawString("F(x) = x teorica", MARGEN + 20, MARGEN + 38);

        g.dispose();
        File archivo = new File(carpetaSalida, "grafico_java_" + nombre + ".png");
        ImageIO.write(imagen, "png", archivo);
        return archivo.getPath();
    }

    // Convierte un valor entre 0 y 1 a la posicion en pixeles
    private int aPixelX(double valor) {
        return (int) (MARGEN + valor * (ANCHO - 2 * MARGEN));
    }

    private int aPixelY(double valor) {
        return (int) (ALTO - MARGEN - valor * (ALTO - 2 * MARGEN));
    }
}
