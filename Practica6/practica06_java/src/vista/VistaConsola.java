package vista;

import java.util.List;
import java.util.Locale;
import modelo.FilaResumen;
import modelo.ResultadoPrueba;

// ============================================================
// VISTA - Mostrar resultados en la consola
// ============================================================
// La vista NO calcula, solo muestra lo que recibe.
// ============================================================
public class VistaConsola {

    public void mostrarTitulo(String texto) {
        String linea = "=".repeat(70);
        System.out.println();
        System.out.println(linea);
        System.out.println(texto);
        System.out.println(linea);
    }

    public void mostrarMensaje(String texto) {
        System.out.println(texto);
    }

    // Paso 11 de la Actividad 1: mostrar los numeros generados
    public void mostrarSecuencia(double[] numeros, int cantidadAMostrar) {
        System.out.println("Primeros " + cantidadAMostrar + " numeros generados:");
        for (int i = 0; i < Math.min(cantidadAMostrar, numeros.length); i++) {
            System.out.printf(Locale.US, "  r%-3d = %.10f%n", i + 1, numeros[i]);
        }
    }

    // Paso 14 del Algoritmo 2
    public void mostrarChiCuadrado(ResultadoPrueba resultado) {
        int[] observadas = (int[]) resultado.getDetalle("observadas");
        double esperada = (double) resultado.getDetalle("esperada");
        int k = observadas.length;

        System.out.println("\n--- Prueba Chi-cuadrado ---");
        System.out.printf("%-15s%12s%12s%14s%n", "Intervalo", "Observada", "Esperada", "(O-E)^2/E");
        for (int i = 0; i < k; i++) {
            double aporte = Math.pow(observadas[i] - esperada, 2) / esperada;
            System.out.printf(Locale.US, "[%.1f, %.1f)     %12d%12.1f%14.4f%n",
                    (double) i / k, (double) (i + 1) / k, observadas[i], esperada, aporte);
        }
        System.out.printf(Locale.US, "Estadistico chi2   = %.4f%n", resultado.getEstadistico());
        System.out.println("Grados de libertad = " + resultado.getDetalle("gradosLibertad"));
        System.out.printf(Locale.US, "Valor p            = %.4f%n", resultado.getValorP());
        System.out.println("Decision (alfa=" + resultado.getAlfa() + "): " + resultado.decision());
    }

    // Paso 13 del Algoritmo KS
    public void mostrarKolmogorov(ResultadoPrueba resultado) {
        System.out.println("\n--- Prueba Kolmogorov-Smirnov ---");
        System.out.printf(Locale.US, "D+ (mayor diferencia positiva) = %.6f%n", (double) resultado.getDetalle("dPositivo"));
        System.out.printf(Locale.US, "D- (mayor diferencia negativa) = %.6f%n", (double) resultado.getDetalle("dNegativo"));
        System.out.printf(Locale.US, "Estadistico D                  = %.6f%n", resultado.getEstadistico());
        System.out.printf(Locale.US, "Valor p                        = %.4f%n", resultado.getValorP());
        System.out.println("Decision (alfa=" + resultado.getAlfa() + "): " + resultado.decision());
    }

    // Tabla final con todos los tamanos y configuraciones
    public void mostrarTablaResumen(List<FilaResumen> filas) {
        mostrarTitulo("TABLA RESUMEN (Java)");
        System.out.printf("%-12s%10s%11s%9s%11s%9s%11s%n",
                "Config", "N", "chi2", "p chi2", "D", "p KS", "Tiempo(s)");
        for (FilaResumen fila : filas) {
            System.out.printf(Locale.US, "%-12s%10d%11.4f%9.4f%11.6f%9.4f%11.4f%n",
                    fila.getConfiguracion(), fila.getN(),
                    fila.getChi().getEstadistico(), fila.getChi().getValorP(),
                    fila.getKs().getEstadistico(), fila.getKs().getValorP(),
                    fila.getTiempoSegundos());
        }
    }

    // Tabla de la seccion 6 de la guia: N, pi estimado, error y tiempo
    public void mostrarTablaPi(double[][] filas) {
        mostrarTitulo("ESTIMACION DE PI CON EL LCG (Java)");
        System.out.printf("%10s%14s%12s%12s%n", "N", "pi estimado", "Error", "Tiempo(s)");
        for (double[] fila : filas) {
            System.out.printf(Locale.US, "%10d%14.6f%12.6f%12.4f%n",
                    (int) fila[0], fila[1], fila[2], fila[3]);
        }
    }
}
