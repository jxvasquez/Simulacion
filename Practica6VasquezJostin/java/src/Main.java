// ============================================================
// PRACTICA 06 - Validacion estadistica de numeros pseudoaleatorios
// Chi-cuadrado y Kolmogorov-Smirnov  |  Patron MVC  |  Java
// ============================================================
// Esta clase solo "arma" el programa: crea los objetos y se los
// entrega al controlador. Para cambiar parametros, editar aqui.
//
// Compilar y ejecutar desde la carpeta 'java':
//   javac -d bin src/Main.java src/modelo/*.java src/vista/*.java src/controlador/*.java
//   java -cp bin Main
// ============================================================

import controlador.ControladorSimulacion;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import modelo.GeneradorAleatorio;
import modelo.GeneradorLCG;
import modelo.PruebaChiCuadrado;
import modelo.PruebaEstadistica;
import modelo.PruebaKolmogorovSmirnov;
import modelo.RepositorioResultados;
import vista.VistaConsola;
import vista.VistaGrafica;

public class Main {

    private static final String CARPETA_SALIDA = "../resultados";
    private static final double ALFA = 0.05;
    private static final int INTERVALOS = 10;

    public static void main(String[] args) throws Exception {
        // ---------- MODELO: configuraciones del generador ----------
        // IMPORTANTE: son los MISMOS parametros que en Python
        // LinkedHashMap mantiene el orden en que se agregan
        Map<String, GeneradorAleatorio> configuraciones = new LinkedHashMap<>();
        // Parametros conocidos (Numerical Recipes): buena calidad, m = 2^32
        configuraciones.put("buena", new GeneradorLCG(12345L, 1664525L, 1013904223L, 4294967296L));
        // Parametros pobres: modulo pequeno y periodo corto
        configuraciones.put("deficiente", new GeneradorLCG(7L, 13L, 0L, 64L));

        // Lista de pruebas: para agregar una nueva solo se anade aqui
        List<PruebaEstadistica> pruebas = new ArrayList<>();
        pruebas.add(new PruebaChiCuadrado(INTERVALOS, ALFA));
        pruebas.add(new PruebaKolmogorovSmirnov(ALFA));

        // ---------- VISTA ----------
        VistaConsola vistaConsola = new VistaConsola();
        VistaGrafica vistaGrafica = new VistaGrafica(CARPETA_SALIDA);

        // ---------- CONTROLADOR ----------
        RepositorioResultados repositorio = new RepositorioResultados(CARPETA_SALIDA);
        ControladorSimulacion controlador =
                new ControladorSimulacion(pruebas, vistaConsola, vistaGrafica, repositorio);

        int[] tamanos = {1_000, 10_000, 100_000, 1_000_000};
        controlador.ejecutar(configuraciones, tamanos, 10_000);
    }
}
