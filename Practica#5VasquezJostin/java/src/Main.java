// ------------------------------------------------------------
// Archivo: Main.java  (punto de entrada del programa en Java)
//
// Aqui solo se CREAN los objetos y se conectan entre si.
// Toda la logica esta en el modelo, la vista y el controlador.
//
// Compilar y ejecutar desde la carpeta "java":
//   javac -d bin src/Main.java src/modelo/*.java src/vista/*.java src/controlador/*.java
//   java -cp bin Main
// ------------------------------------------------------------

import java.io.IOException;
import java.util.List;

import controlador.ControladorLCG;
import modelo.AnalizadorPeriodo;
import modelo.Estadisticas;
import modelo.ExportadorCSV;
import modelo.GeneradorLCG;
import modelo.Observacion;
import modelo.ParametrosLCG;
import vista.VistaConsola;
import vista.VistaGrafica;

public class Main {

    // Datos de la guia de practica
    private static final int CANTIDAD_VALORES = 10000;
    private static final int CANTIDAD_TABLA = 20;
    private static final long NUEVA_SEMILLA = 54321;
    private static final String CARPETA_RESULTADOS = "../resultados/";

    public static void main(String[] args) throws IOException {
        // 1. Modelo: parametros y generador (m = 2^32 = 4294967296)
        ParametrosLCG parametros = new ParametrosLCG(1664525L, 1013904223L, 4294967296L, 12345L);
        GeneradorLCG generador = new GeneradorLCG(parametros);

        // 2. Controlador: recibe todas sus dependencias ya creadas
        ControladorLCG controlador = new ControladorLCG(
                generador,
                parametros,
                new VistaConsola(),
                new VistaGrafica(),
                new ExportadorCSV(),
                new AnalizadorPeriodo(),
                new Estadisticas());

        // 3. Ejecutar los pasos de la practica
        List<Observacion> observaciones = controlador.generarSecuenciaPrincipal(
                CANTIDAD_VALORES, CANTIDAD_TABLA,
                CARPETA_RESULTADOS + "secuencia_java.csv",
                CARPETA_RESULTADOS + "grafico_java.png");

        controlador.analizarPeriodo(observaciones);

        controlador.compararConOtraSemilla(observaciones, NUEVA_SEMILLA,
                CANTIDAD_VALORES, CANTIDAD_TABLA);

        // 4. Extra: parametros inadecuados (m pequeno y c = 0)
        ParametrosLCG parametrosMalos = new ParametrosLCG(5, 0, 16, 3);
        controlador.demostrarParametrosInadecuados(
                new GeneradorLCG(parametrosMalos), parametrosMalos, 8);
    }
}
