// ------------------------------------------------------------
// Archivo: VistaConsola.java
// Responsabilidad unica: mostrar informacion en la consola.
// La vista NO hace calculos; solo muestra lo que le da el controlador.
// ------------------------------------------------------------
package vista;

import java.util.List;
import java.util.Locale;
import java.util.Map;

import modelo.Observacion;
import modelo.ParametrosLCG;

public class VistaConsola {

    public void mostrarTitulo(String texto) {
        System.out.println();
        System.out.println("=".repeat(70));
        System.out.println(" " + texto);
        System.out.println("=".repeat(70));
    }

    public void mostrarMensaje(String texto) {
        System.out.println(texto);
    }

    public void mostrarParametros(ParametrosLCG parametros) {
        System.out.println("  a (multiplicador) = " + parametros.getA());
        System.out.println("  c (incremento)    = " + parametros.getC());
        System.out.println("  m (modulo)        = " + parametros.getM());
        System.out.println("  semilla X(0)      = " + parametros.getSemilla());
    }

    public void mostrarTabla(List<Observacion> observaciones, int cantidad) {
        System.out.printf("%5s | %12s | %14s%n", "n", "X(n)", "U(n)");
        System.out.println("-".repeat(37));
        for (int i = 0; i < cantidad && i < observaciones.size(); i++) {
            Observacion obs = observaciones.get(i);
            System.out.printf(Locale.US, "%5d | %12d | %14.10f%n",
                    obs.getIndice(), obs.getValorX(), obs.getValorU());
        }
    }

    public void mostrarComparacionSemillas(List<Observacion> obs1, List<Observacion> obs2,
                                           long semilla1, long semilla2, int cantidad) {
        System.out.printf("%5s | %22s | %22s%n", "n",
                "U(n) semilla " + semilla1, "U(n) semilla " + semilla2);
        System.out.println("-".repeat(55));
        for (int i = 0; i < cantidad; i++) {
            System.out.printf(Locale.US, "%5d | %22.10f | %22.10f%n",
                    obs1.get(i).getIndice(), obs1.get(i).getValorU(), obs2.get(i).getValorU());
        }
    }

    public void mostrarHullDobell(Map<String, Boolean> resultado) {
        for (Map.Entry<String, Boolean> entrada : resultado.entrySet()) {
            String texto = entrada.getValue() ? "SI" : "NO";
            System.out.printf("  %-45s: %s%n", entrada.getKey(), texto);
        }
    }

    public void mostrarEstadisticas(String nombre, double media, double varianza,
                                    double minimo, double maximo) {
        System.out.println("  [" + nombre + "]");
        System.out.printf(Locale.US, "    Media    = %.6f   (esperado 0.5)%n", media);
        System.out.printf(Locale.US, "    Varianza = %.6f   (esperado 1/12 = 0.083333)%n", varianza);
        System.out.printf(Locale.US, "    Minimo   = %.6f%n", minimo);
        System.out.printf(Locale.US, "    Maximo   = %.6f%n", maximo);
    }
}
