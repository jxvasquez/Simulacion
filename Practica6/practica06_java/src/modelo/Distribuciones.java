package modelo;

// ============================================================
// MODELO - Funciones matematicas para calcular valores p
// ============================================================
// Son las MISMAS formulas que en Python (distribuciones.py),
// asi ambos programas dan los mismos resultados.
// La clase es "utilitaria": solo tiene metodos estaticos.
// ============================================================
public final class Distribuciones {

    // Constructor privado: no se necesita crear objetos de esta clase
    private Distribuciones() { }

    // Logaritmo de la funcion Gamma (aproximacion de Lanczos)
    public static double logGamma(double x) {
        double[] coeficientes = {76.18009172947146, -86.50532032941677,
                24.01409824083091, -1.231739572450155,
                0.1208650973866179e-2, -0.5395239384953e-5};
        double y = x;
        double tmp = x + 5.5;
        tmp -= (x + 0.5) * Math.log(tmp);
        double serie = 1.000000000190015;
        for (double c : coeficientes) {
            y += 1;
            serie += c / y;
        }
        return -tmp + Math.log(2.5066282746310005 * serie / x);
    }

    // Gamma incompleta regularizada inferior P(a, x) usando una serie
    private static double gammaInferiorPorSerie(double a, double x) {
        double suma = 1.0 / a;
        double termino = suma;
        double n = a;
        for (int i = 0; i < 1000; i++) {
            n += 1;
            termino *= x / n;
            suma += termino;
            if (Math.abs(termino) < Math.abs(suma) * 1e-15) {
                break;
            }
        }
        return suma * Math.exp(-x + a * Math.log(x) - logGamma(a));
    }

    // Gamma incompleta regularizada superior Q(a, x) usando fraccion continua
    private static double gammaSuperiorPorFraccion(double a, double x) {
        double minimo = 1e-300;
        double b = x + 1 - a;
        double c = 1.0 / minimo;
        double d = 1.0 / b;
        double h = d;
        for (int i = 1; i < 1000; i++) {
            double an = -i * (i - a);
            b += 2;
            d = an * d + b;
            if (Math.abs(d) < minimo) d = minimo;
            c = b + an / c;
            if (Math.abs(c) < minimo) c = minimo;
            d = 1.0 / d;
            double delta = d * c;
            h *= delta;
            if (Math.abs(delta - 1) < 1e-15) {
                break;
            }
        }
        return Math.exp(-x + a * Math.log(x) - logGamma(a)) * h;
    }

    // Probabilidad de obtener un chi2 mayor o igual al calculado
    public static double valorPChiCuadrado(double estadistico, int gradosLibertad) {
        if (estadistico <= 0) {
            return 1.0;
        }
        double a = gradosLibertad / 2.0;
        double x = estadistico / 2.0;
        if (x < a + 1) {
            return 1.0 - gammaInferiorPorSerie(a, x);
        }
        return gammaSuperiorPorFraccion(a, x);
    }

    // Valor p aproximado de la prueba KS (distribucion de Kolmogorov)
    public static double valorPKolmogorov(double d, int n) {
        double raizN = Math.sqrt(n);
        // Correccion de Stephens para muestras finitas
        double lambda = (raizN + 0.12 + 0.11 / raizN) * d;
        if (lambda < 1e-10) {
            return 1.0;
        }
        double suma = 0.0;
        double signo = 1.0;
        for (int j = 1; j <= 100; j++) {
            double termino = signo * Math.exp(-2.0 * j * j * lambda * lambda);
            suma += termino;
            if (Math.abs(termino) < 1e-12) {
                break;
            }
            signo = -signo;
        }
        double p = 2.0 * suma;
        // El valor p siempre debe estar entre 0 y 1
        return Math.max(0.0, Math.min(1.0, p));
    }
}
