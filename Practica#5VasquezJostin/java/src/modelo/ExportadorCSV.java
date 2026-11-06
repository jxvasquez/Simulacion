// ------------------------------------------------------------
// Archivo: ExportadorCSV.java
// Responsabilidad unica: guardar observaciones en un archivo CSV.
// El CSV luego se compara con el que genera el programa en Python.
// ------------------------------------------------------------
package modelo;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.List;
import java.util.Locale;

public class ExportadorCSV {

    public void exportar(List<Observacion> observaciones, String ruta) throws IOException {
        // Creamos la carpeta si todavia no existe
        File archivo = new File(ruta);
        File carpeta = archivo.getParentFile();
        if (carpeta != null && !carpeta.exists()) {
            carpeta.mkdirs();
        }

        // try-with-resources: cierra el archivo automaticamente al terminar
        try (PrintWriter escritor = new PrintWriter(new FileWriter(archivo))) {
            escritor.println("n,X,U");  // encabezado
            for (Observacion obs : observaciones) {
                // Locale.US asegura que el decimal sea con punto (0.5) y no con coma (0,5)
                escritor.println(obs.getIndice() + "," + obs.getValorX() + ","
                        + String.format(Locale.US, "%.10f", obs.getValorU()));
            }
        }
    }
}
