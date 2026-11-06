package modelo;

// ============================================================
// MODELO - Generador congruencial lineal (Actividad 1)
// X(n+1) = (a * X(n) + c) mod m
// ============================================================
// S (Responsabilidad unica): esta clase solo genera numeros.
// Se usa 'long' para que a * X no se desborde (m = 2^32).
// ============================================================
public class GeneradorLCG implements GeneradorAleatorio {

    private final long semilla;
    private final long multiplicador;
    private final long incremento;
    private final long modulo;

    // Paso 2: definir los parametros del generador
    public GeneradorLCG(long semilla, long multiplicador, long incremento, long modulo) {
        this.semilla = semilla;
        this.multiplicador = multiplicador;
        this.incremento = incremento;
        this.modulo = modulo;
    }

    @Override
    public double[] generar(int cantidad) {
        double[] numeros = new double[cantidad]; // arreglo donde se guardan los numeros
        long valorActual = semilla;              // paso 3: la semilla es el valor inicial

        // Paso 4: repetir hasta completar la cantidad pedida
        for (int i = 0; i < cantidad; i++) {
            // Pasos 5, 6 y 7: multiplicar, sumar el incremento y sacar el residuo
            valorActual = (multiplicador * valorActual + incremento) % modulo;

            // Paso 8 y 9: dividir entre el modulo y almacenar
            numeros[i] = (double) valorActual / modulo;
            // Paso 10: valorActual ya quedo actualizado para la siguiente vuelta
        }
        return numeros;
    }

    @Override
    public String descripcion() {
        return "LCG(semilla=" + semilla + ", a=" + multiplicador
                + ", c=" + incremento + ", m=" + modulo + ")";
    }
}
