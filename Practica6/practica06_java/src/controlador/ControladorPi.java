package controlador;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.Locale;
import modelo.EstimadorPi;
import vista.VistaConsola;

// ============================================================
// CONTROLADOR - Tabla de la seccion 6 (pi estimado, error, tiempo)
// ============================================================
// Controlador aparte (S): no se modifica el de las pruebas (O).
// ============================================================
public class ControladorPi {

    private final EstimadorPi estimador;
    private final VistaConsola vista;
    private final String carpetaSalida;

    public ControladorPi(EstimadorPi estimador, VistaConsola vista, String carpetaSalida) {
        this.estimador = estimador;
        this.vista = vista;
        this.carpetaSalida = carpetaSalida;
    }

    public void ejecutar(int[] tamanos) throws IOException {
        // Matriz con una fila por cada N: {N, pi, error, tiempo}
        double[][] filas = new double[tamanos.length][4];

        for (int i = 0; i < tamanos.length; i++) {
            int n = tamanos[i];
            long inicio = System.nanoTime();
            double[] resultado = estimador.estimar(n);
            double tiempo = (System.nanoTime() - inicio) / 1_000_000_000.0;

            filas[i][0] = n;
            filas[i][1] = resultado[0];
            filas[i][2] = resultado[1];
            filas[i][3] = tiempo;
        }

        vista.mostrarTablaPi(filas);
        String ruta = guardar(filas);
        vista.mostrarMensaje("\nTabla de pi guardada en: " + ruta);
    }

    // Guarda la tabla en CSV con el mismo formato que Python
    private String guardar(double[][] filas) throws IOException {
        new File(carpetaSalida).mkdirs();
        File archivo = new File(carpetaSalida, "pi_java.csv");
        try (PrintWriter escritor = new PrintWriter(new FileWriter(archivo))) {
            escritor.println("N,pi_estimado,error,tiempo_segundos");
            for (double[] fila : filas) {
                escritor.println(String.format(Locale.US, "%d,%.6f,%.6f,%.6f",
                        (int) fila[0], fila[1], fila[2], fila[3]));
            }
        }
        return archivo.getPath();
    }
}
