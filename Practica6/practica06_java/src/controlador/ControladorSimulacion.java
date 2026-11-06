package controlador;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import modelo.FilaResumen;
import modelo.GeneradorAleatorio;
import modelo.PruebaEstadistica;
import modelo.RepositorioResultados;
import modelo.ResultadoPrueba;
import vista.VistaConsola;
import vista.VistaGrafica;

// ============================================================
// CONTROLADOR - Coordina el Modelo y la Vista
// ============================================================
// D (Inversion de dependencias): recibe todo por el constructor
// y trabaja con las interfaces GeneradorAleatorio y PruebaEstadistica.
// ============================================================
public class ControladorSimulacion {

    private final List<PruebaEstadistica> pruebas;
    private final VistaConsola vista;
    private final VistaGrafica vistaGrafica;
    private final RepositorioResultados repositorio;

    public ControladorSimulacion(List<PruebaEstadistica> pruebas, VistaConsola vista,
                                 VistaGrafica vistaGrafica, RepositorioResultados repositorio) {
        this.pruebas = pruebas;
        this.vista = vista;
        this.vistaGrafica = vistaGrafica;
        this.repositorio = repositorio;
    }

    public void ejecutar(Map<String, GeneradorAleatorio> configuraciones,
                         int[] tamanos, int nDetalle) throws IOException {
        List<FilaResumen> filas = new ArrayList<>();

        for (Map.Entry<String, GeneradorAleatorio> entrada : configuraciones.entrySet()) {
            String nombre = entrada.getKey();
            GeneradorAleatorio generador = entrada.getValue();
            vista.mostrarTitulo("Configuracion '" + nombre + "': " + generador.descripcion());

            for (int n : tamanos) {
                // Se mide el tiempo de generar + aplicar las pruebas
                long inicio = System.nanoTime();
                double[] numeros = generador.generar(n);
                List<ResultadoPrueba> resultados = new ArrayList<>();
                for (PruebaEstadistica prueba : pruebas) {
                    resultados.add(prueba.aplicar(numeros));
                }
                double tiempo = (System.nanoTime() - inicio) / 1_000_000_000.0;

                ResultadoPrueba chi = buscar(resultados, "Chi-cuadrado");
                ResultadoPrueba ks = buscar(resultados, "Kolmogorov-Smirnov");

                // Detalle completo solo para el tamano elegido
                if (n == nDetalle) {
                    vista.mostrarMensaje("\n>> Detalle para N = " + n);
                    vista.mostrarSecuencia(numeros, 10);
                    vista.mostrarChiCuadrado(chi);
                    vista.mostrarKolmogorov(ks);
                    String ruta = vistaGrafica.graficar(nombre + "_N" + n, ks);
                    vista.mostrarMensaje("Grafico guardado en: " + ruta);
                    // Primeros 20 numeros para compararlos con Python
                    repositorio.guardarSecuencia("secuencia_java_" + nombre + ".csv", numeros, 20);
                }

                filas.add(new FilaResumen(nombre, n, chi, ks, tiempo));
            }
        }

        vista.mostrarTablaResumen(filas);
        String ruta = repositorio.guardarTabla("resultados_java.csv", filas);
        vista.mostrarMensaje("\nTabla guardada en: " + ruta);
    }

    // Devuelve el resultado cuyo nombre coincide
    private ResultadoPrueba buscar(List<ResultadoPrueba> resultados, String nombre) {
        for (ResultadoPrueba resultado : resultados) {
            if (resultado.getNombrePrueba().equals(nombre)) {
                return resultado;
            }
        }
        return null;
    }
}
