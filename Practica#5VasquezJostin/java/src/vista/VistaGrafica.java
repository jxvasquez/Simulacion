// ------------------------------------------------------------
// Archivo: VistaGrafica.java
// Responsabilidad unica: dibujar la secuencia y guardarla como PNG.
//
// Se usan solo librerias que ya vienen con Java (java.awt e ImageIO),
// asi que no hace falta instalar nada extra.
// ------------------------------------------------------------
package vista;

import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Font;
import java.awt.Graphics2D;
import java.awt.RenderingHints;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.List;

import javax.imageio.ImageIO;

import modelo.Observacion;

public class VistaGrafica {

    private static final int ANCHO = 900;
    private static final int ALTO = 450;
    private static final int MARGEN = 60;

    // Dibuja U(n) de los primeros 'cantidad' valores y guarda la imagen
    public void graficarSecuencia(List<Observacion> observaciones, int cantidad,
                                  String ruta, String titulo) throws IOException {
        cantidad = Math.min(cantidad, observaciones.size());

        // 1. Creamos una imagen en blanco
        BufferedImage imagen = new BufferedImage(ANCHO, ALTO, BufferedImage.TYPE_INT_RGB);
        Graphics2D lapiz = imagen.createGraphics();
        lapiz.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        lapiz.setColor(Color.WHITE);
        lapiz.fillRect(0, 0, ANCHO, ALTO);

        // 2. Dibujamos los ejes
        int anchoUtil = ANCHO - 2 * MARGEN;
        int altoUtil = ALTO - 2 * MARGEN;
        lapiz.setColor(Color.BLACK);
        lapiz.drawLine(MARGEN, ALTO - MARGEN, ANCHO - MARGEN, ALTO - MARGEN); // eje X
        lapiz.drawLine(MARGEN, MARGEN, MARGEN, ALTO - MARGEN);                // eje Y

        // 3. Textos: titulo y etiquetas
        lapiz.setFont(new Font("SansSerif", Font.BOLD, 16));
        lapiz.drawString(titulo, MARGEN, 35);
        lapiz.setFont(new Font("SansSerif", Font.PLAIN, 12));
        lapiz.drawString("n", ANCHO - MARGEN + 10, ALTO - MARGEN + 5);
        lapiz.drawString("U(n)", 15, MARGEN - 10);
        lapiz.drawString("0", MARGEN - 15, ALTO - MARGEN + 5);
        lapiz.drawString("1", MARGEN - 15, MARGEN + 5);
        lapiz.drawString(String.valueOf(cantidad), ANCHO - MARGEN - 10, ALTO - MARGEN + 20);

        // 4. Dibujamos los puntos unidos por lineas
        lapiz.setColor(new Color(31, 119, 180));
        lapiz.setStroke(new BasicStroke(1.2f));
        int xAnterior = -1;
        int yAnterior = -1;
        for (int i = 0; i < cantidad; i++) {
            // Convertimos (n, U) a coordenadas de pixeles
            int x = MARGEN + (int) ((double) i / (cantidad - 1) * anchoUtil);
            int y = ALTO - MARGEN - (int) (observaciones.get(i).getValorU() * altoUtil);
            lapiz.fillOval(x - 2, y - 2, 5, 5);
            if (xAnterior >= 0) {
                lapiz.drawLine(xAnterior, yAnterior, x, y);
            }
            xAnterior = x;
            yAnterior = y;
        }
        lapiz.dispose();

        // 5. Guardamos la imagen en disco
        File archivo = new File(ruta);
        if (archivo.getParentFile() != null) {
            archivo.getParentFile().mkdirs();
        }
        ImageIO.write(imagen, "png", archivo);
    }
}
