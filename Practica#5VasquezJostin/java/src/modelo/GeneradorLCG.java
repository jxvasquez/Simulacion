// ------------------------------------------------------------
// Archivo: GeneradorLCG.java
// Implementacion del Generador Congruencial Lineal (LCG).
//
//   Formula:        X(n+1) = (a * X(n) + c) mod m
//   Normalizacion:  U(n)   = X(n) / m
//
// NOTA IMPORTANTE: usamos 'long' (64 bits) y no 'int' (32 bits).
// Con m = 2^32 el valor X puede llegar a 4 294 967 295, que NO cabe en
// un int. Ademas a * X es como maximo 1664525 * 2^32 (aprox. 7.1e15),
// que si cabe en un long (maximo 9.2e18), asi que no hay desbordamiento.
// ------------------------------------------------------------
package modelo;

import java.util.ArrayList;
import java.util.List;

public class GeneradorLCG implements GeneradorAleatorio {

    private final ParametrosLCG parametros;
    private long estadoActual;  // ultimo X calculado

    public GeneradorLCG(ParametrosLCG parametros) {
        this.parametros = parametros;
        this.estadoActual = parametros.getSemilla();
    }

    @Override
    public void reiniciar(long semilla) {
        if (semilla < 0 || semilla >= parametros.getM()) {
            throw new IllegalArgumentException("La semilla debe cumplir 0 <= semilla < m");
        }
        this.estadoActual = semilla;
    }

    @Override
    public long siguiente() {
        long a = parametros.getA();
        long c = parametros.getC();
        long m = parametros.getM();
        estadoActual = (a * estadoActual + c) % m;
        return estadoActual;
    }

    @Override
    public double normalizar(long valorX) {
        // Convertimos a double para que la division tenga decimales
        return (double) valorX / parametros.getM();
    }

    @Override
    public List<Observacion> generarSecuencia(int cantidad) {
        List<Observacion> observaciones = new ArrayList<>();
        for (int indice = 1; indice <= cantidad; indice++) {
            long valorX = siguiente();
            double valorU = normalizar(valorX);
            observaciones.add(new Observacion(indice, valorX, valorU));
        }
        return observaciones;
    }
}
