package modelo;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.List;
import java.util.Locale;

// ============================================================
// MODELO - Guardar resultados en archivos CSV
// ============================================================
// S (Responsabilidad unica): solo escribe archivos.
// Usa el mismo formato que la version de Python para compararlos.
// ============================================================
public class RepositorioResultados {

    private final String carpetaSalida;

    public RepositorioResultados(String carpetaSalida) {
        this.carpetaSalida = carpetaSalida;
        new File(carpetaSalida).mkdirs(); // crea la carpeta si no existe
    }

    public String guardarTabla(String nombreArchivo, List<FilaResumen> filas) throws IOException {
        File archivo = new File(carpetaSalida, nombreArchivo);
        try (PrintWriter escritor = new PrintWriter(new FileWriter(archivo))) {
            escritor.println("configuracion,N,chi2,p_chi2,decision_chi2,D,p_ks,decision_ks,tiempo_segundos");
            for (FilaResumen fila : filas) {
                // Locale.US para usar punto decimal y no coma
                escritor.println(String.format(Locale.US, "%s,%d,%.6f,%.6f,%s,%.6f,%.6f,%s,%.6f",
                        fila.getConfiguracion(),
                        fila.getN(),
                        fila.getChi().getEstadistico(),
                        fila.getChi().getValorP(),
                        fila.getChi().seRechazaH0() ? "Rechaza" : "No rechaza",
                        fila.getKs().getEstadistico(),
                        fila.getKs().getValorP(),
                        fila.getKs().seRechazaH0() ? "Rechaza" : "No rechaza",
                        fila.getTiempoSegundos()));
            }
        }
        return archivo.getPath();
    }

    public String guardarSecuencia(String nombreArchivo, double[] numeros, int cantidad) throws IOException {
        File archivo = new File(carpetaSalida, nombreArchivo);
        try (PrintWriter escritor = new PrintWriter(new FileWriter(archivo))) {
            escritor.println("indice,numero");
            for (int i = 0; i < Math.min(cantidad, numeros.length); i++) {
                escritor.println(String.format(Locale.US, "%d,%.10f", i + 1, numeros[i]));
            }
        }
        return archivo.getPath();
    }
}
