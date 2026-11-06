package modelo;

// ============================================================
// MODELO - Prueba Chi-cuadrado (Algoritmo 2 de la guia)
// ============================================================
public class PruebaChiCuadrado implements PruebaEstadistica {

    private final int numeroIntervalos;
    private final double alfa;

    public PruebaChiCuadrado(int numeroIntervalos, double alfa) {
        // Paso 2: numero de intervalos en que se divide [0, 1]
        this.numeroIntervalos = numeroIntervalos;
        this.alfa = alfa;
    }

    @Override
    public ResultadoPrueba aplicar(double[] numeros) {
        // Paso 1: recibir la secuencia
        int n = numeros.length;
        int k = numeroIntervalos;

        // Paso 4: frecuencia esperada = total de datos / numero de intervalos
        double esperada = (double) n / k;

        // Pasos 3, 5 y 6: contar cuantos numeros caen en cada intervalo
        int[] observadas = new int[k];
        for (double numero : numeros) {
            int indice = (int) (numero * k); // ejemplo: 0.37 * 10 = 3.7 -> intervalo 3
            if (indice >= k) {               // por seguridad, si numero fuera 1.0
                indice = k - 1;
            }
            observadas[indice]++;
        }

        // Pasos 7 y 8: calcular el estadistico chi-cuadrado
        double chiCuadrado = 0.0;
        for (int frecuencia : observadas) {
            double diferencia = frecuencia - esperada;
            chiCuadrado += (diferencia * diferencia) / esperada;
        }

        // Paso 9: grados de libertad
        int gradosLibertad = k - 1;

        // Paso 10: valor p
        double valorP = Distribuciones.valorPChiCuadrado(chiCuadrado, gradosLibertad);

        // Pasos 11 al 14: la decision la toma ResultadoPrueba y la muestra la Vista
        ResultadoPrueba resultado = new ResultadoPrueba("Chi-cuadrado", chiCuadrado, valorP, alfa);
        resultado.agregarDetalle("observadas", observadas);
        resultado.agregarDetalle("esperada", esperada);
        resultado.agregarDetalle("gradosLibertad", gradosLibertad);
        return resultado;
    }
}
