package modelo;

// ============================================================
// MODELO - Estimacion de pi por Monte Carlo
// ============================================================
// Sirve para llenar la tabla de la seccion 6 de la guia.
// Se lanzan N puntos (x, y) en un cuadrado de lado 1 y se cuenta
// cuantos caen dentro del cuarto de circulo (x^2 + y^2 <= 1).
//     pi estimado = 4 * (puntos dentro) / N
//     error       = | pi estimado - pi real |
// D (Inversion de dependencias): recibe cualquier GeneradorAleatorio.
// ============================================================
public class EstimadorPi {

    private final GeneradorAleatorio generador;

    public EstimadorPi(GeneradorAleatorio generador) {
        this.generador = generador;
    }

    // Devuelve un arreglo: [0] = pi estimado, [1] = error
    public double[] estimar(int n) {
        // Cada punto necesita 2 numeros: uno para x y otro para y
        double[] numeros = generador.generar(2 * n);

        int dentro = 0;
        for (int i = 0; i < n; i++) {
            double x = numeros[2 * i];      // posicion par -> x
            double y = numeros[2 * i + 1];  // posicion impar -> y
            if (x * x + y * y <= 1.0) {
                dentro++;
            }
        }

        double piEstimado = 4.0 * dentro / n;
        double error = Math.abs(piEstimado - Math.PI);
        return new double[]{piEstimado, error};
    }
}
