package modelo;

import java.util.Arrays;

// ============================================================
// MODELO - Prueba Kolmogorov-Smirnov (Algoritmo 3 de la guia)
// ============================================================
public class PruebaKolmogorovSmirnov implements PruebaEstadistica {

    private final double alfa;

    public PruebaKolmogorovSmirnov(double alfa) {
        this.alfa = alfa;
    }

    @Override
    public ResultadoPrueba aplicar(double[] numeros) {
        // Paso 2: ordenar los numeros (se copia para no alterar el original)
        double[] ordenados = numeros.clone();
        Arrays.sort(ordenados);

        // Paso 3: cantidad total de numeros
        int n = ordenados.length;

        // Paso 4: inicializar las diferencias maximas
        double dPositivo = 0.0;
        double dNegativo = 0.0;

        // Pasos 5 y 6: recorrer los numeros ordenados
        for (int i = 0; i < n; i++) {
            int posicion = i + 1;                       // la posicion empieza en 1
            double empirica = (double) posicion / n;    // Fn(x) = i / n
            double teorica = ordenados[i];              // F(x) = x para U(0,1)

            // Diferencia positiva: Fn(x) - F(x)
            double difPositiva = empirica - teorica;
            // Diferencia negativa: F(x) - Fn(x) justo antes del salto
            double difNegativa = teorica - (double) (posicion - 1) / n;

            // Paso 7: quedarnos con la mayor de cada tipo
            if (difPositiva > dPositivo) dPositivo = difPositiva;
            if (difNegativa > dNegativo) dNegativo = difNegativa;
        }

        // Paso 8: el estadistico D es la mayor de las dos diferencias
        double d = Math.max(dPositivo, dNegativo);

        // Paso 9: valor p
        double valorP = Distribuciones.valorPKolmogorov(d, n);

        ResultadoPrueba resultado = new ResultadoPrueba("Kolmogorov-Smirnov", d, valorP, alfa);
        resultado.agregarDetalle("dPositivo", dPositivo);
        resultado.agregarDetalle("dNegativo", dNegativo);
        resultado.agregarDetalle("ordenados", ordenados); // para graficar (paso 14)
        return resultado;
    }
}
