// ------------------------------------------------------------
// Archivo: ControladorLCG.java
// El controlador coordina los pasos de la practica.
//
// Principio D (Inversion de dependencias): el controlador NO crea sus
// dependencias con 'new'; las recibe ya creadas en el constructor.
// Asi se puede cambiar el generador o la vista sin tocar esta clase.
// ------------------------------------------------------------
package controlador;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import modelo.AnalizadorPeriodo;
import modelo.Estadisticas;
import modelo.ExportadorCSV;
import modelo.GeneradorAleatorio;
import modelo.Observacion;
import modelo.ParametrosLCG;
import vista.VistaConsola;
import vista.VistaGrafica;

public class ControladorLCG {

    private final GeneradorAleatorio generador;  // depende de la INTERFAZ
    private final ParametrosLCG parametros;
    private final VistaConsola vista;
    private final VistaGrafica vistaGrafica;
    private final ExportadorCSV exportador;
    private final AnalizadorPeriodo analizador;
    private final Estadisticas estadisticas;

    public ControladorLCG(GeneradorAleatorio generador, ParametrosLCG parametros,
                          VistaConsola vista, VistaGrafica vistaGrafica,
                          ExportadorCSV exportador, AnalizadorPeriodo analizador,
                          Estadisticas estadisticas) {
        this.generador = generador;
        this.parametros = parametros;
        this.vista = vista;
        this.vistaGrafica = vistaGrafica;
        this.exportador = exportador;
        this.analizador = analizador;
        this.estadisticas = estadisticas;
    }

    // ---------- Pasos 1 al 5: generar, mostrar, exportar y graficar ----------
    public List<Observacion> generarSecuenciaPrincipal(int cantidad, int cantidadTabla,
                                                       String rutaCsv, String rutaGrafico)
            throws IOException {
        vista.mostrarTitulo("PASO 1: Parametros del generador LCG");
        vista.mostrarParametros(parametros);

        vista.mostrarTitulo("PASO 3: Generando " + cantidad + " valores en Java");
        generador.reiniciar(parametros.getSemilla());
        List<Observacion> observaciones = generador.generarSecuencia(cantidad);
        vista.mostrarMensaje("  Se generaron " + observaciones.size() + " valores.");

        vista.mostrarTitulo("PASO 4: Primeras " + cantidadTabla + " observaciones");
        vista.mostrarTabla(observaciones, cantidadTabla);

        exportador.exportar(observaciones, rutaCsv);
        vista.mostrarMensaje("\n  Secuencia guardada en: " + rutaCsv);

        vista.mostrarTitulo("PASO 5: Grafico de la secuencia");
        vistaGrafica.graficarSecuencia(observaciones, 200, rutaGrafico,
                "LCG en Java - semilla " + parametros.getSemilla() + " (primeros 200 valores)");
        vista.mostrarMensaje("  Grafico guardado en: " + rutaGrafico);

        mostrarEstadisticas("semilla " + parametros.getSemilla(), observaciones);
        return observaciones;
    }

    // ---------- Paso 6: analisis del periodo ----------
    public void analizarPeriodo(List<Observacion> observaciones) {
        vista.mostrarTitulo("PASO 6: Analisis del periodo");
        vista.mostrarMensaje("  Teorema de Hull-Dobell:");
        Map<String, Boolean> resultado = analizador.cumpleHullDobell(parametros);
        vista.mostrarHullDobell(resultado);

        if (resultado.get("periodo completo")) {
            vista.mostrarMensaje("\n  => El periodo es COMPLETO: " + parametros.getM()
                    + " valores antes de repetirse.");
        } else {
            vista.mostrarMensaje("\n  => El periodo NO es completo.");
        }

        int repeticion = analizador.buscarRepeticion(observaciones);
        if (repeticion == -1) {
            vista.mostrarMensaje("  En los " + observaciones.size()
                    + " valores generados no se repite ningun X(n).");
        } else {
            vista.mostrarMensaje("  Primer valor repetido en la posicion " + repeticion + ".");
        }
    }

    // ---------- Pasos 7 y 8: cambiar semilla y comparar ----------
    public void compararConOtraSemilla(List<Observacion> originales, long nuevaSemilla,
                                       int cantidad, int cantidadTabla) {
        vista.mostrarTitulo("PASO 7: Cambio de semilla a " + nuevaSemilla);
        generador.reiniciar(nuevaSemilla);
        List<Observacion> nuevas = generador.generarSecuencia(cantidad);

        vista.mostrarTitulo("PASO 8: Comparacion de resultados entre semillas");
        vista.mostrarComparacionSemillas(originales, nuevas,
                parametros.getSemilla(), nuevaSemilla, cantidadTabla);

        mostrarEstadisticas("semilla " + parametros.getSemilla(), originales);
        mostrarEstadisticas("semilla " + nuevaSemilla, nuevas);
    }

    // ---------- Extra: que pasa con parametros inadecuados ----------
    public void demostrarParametrosInadecuados(GeneradorAleatorio generadorMalo,
                                               ParametrosLCG parametrosMalos, int cantidadTabla) {
        vista.mostrarTitulo("EXTRA: Generador con parametros inadecuados");
        vista.mostrarParametros(parametrosMalos);
        vista.mostrarMensaje("");
        vista.mostrarHullDobell(analizador.cumpleHullDobell(parametrosMalos));

        long periodo = analizador.calcularPeriodo(generadorMalo,
                parametrosMalos.getSemilla(), parametrosMalos.getM() + 1);
        vista.mostrarMensaje("\n  Periodo real = " + periodo
                + " (el maximo posible seria " + parametrosMalos.getM() + ")");

        generadorMalo.reiniciar(parametrosMalos.getSemilla());
        vista.mostrarTabla(generadorMalo.generarSecuencia(cantidadTabla), cantidadTabla);
        vista.mostrarMensaje("  Observe como los valores se repiten muy rapido.");
    }

    // ---------- Metodo auxiliar privado ----------
    private void mostrarEstadisticas(String nombre, List<Observacion> observaciones) {
        List<Double> valores = new ArrayList<>();
        for (Observacion obs : observaciones) {
            valores.add(obs.getValorU());
        }
        vista.mostrarEstadisticas(nombre,
                estadisticas.media(valores),
                estadisticas.varianza(valores),
                estadisticas.minimo(valores),
                estadisticas.maximo(valores));
    }
}
