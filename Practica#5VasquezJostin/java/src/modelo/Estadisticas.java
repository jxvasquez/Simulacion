// ------------------------------------------------------------
// Archivo: Estadisticas.java
// Responsabilidad unica: calcular estadisticas basicas de U(n).
// Para una distribucion uniforme en [0, 1):
//   media esperada    = 0.5
//   varianza esperada = 1/12 = 0.0833...
// ------------------------------------------------------------
package modelo;

import java.util.List;

public class Estadisticas {

    public double media(List<Double> valores) {
        double suma = 0;
        for (double valor : valores) {
            suma += valor;
        }
        return suma / valores.size();
    }

    public double varianza(List<Double> valores) {
        double promedio = media(valores);
        double sumaCuadrados = 0;
        for (double valor : valores) {
            sumaCuadrados += (valor - promedio) * (valor - promedio);
        }
        return sumaCuadrados / valores.size();
    }

    public double minimo(List<Double> valores) {
        double menor = valores.get(0);
        for (double valor : valores) {
            if (valor < menor) {
                menor = valor;
            }
        }
        return menor;
    }

    public double maximo(List<Double> valores) {
        double mayor = valores.get(0);
        for (double valor : valores) {
            if (valor > mayor) {
                mayor = valor;
            }
        }
        return mayor;
    }
}
