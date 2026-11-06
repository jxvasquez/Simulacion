// ------------------------------------------------------------
// Archivo: AnalizadorPeriodo.java
// Responsabilidad unica: analizar el PERIODO de un generador.
//
// Periodo = cantidad de numeros distintos que salen antes de que la
//           secuencia empiece a repetirse.
// ------------------------------------------------------------
package modelo;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

public class AnalizadorPeriodo {

    // Teorema de Hull-Dobell: el LCG tiene periodo completo (igual a m)
    // si y solo si se cumplen las 3 condiciones.
    // Devuelve un mapa: nombre de la condicion -> si se cumple o no.
    public Map<String, Boolean> cumpleHullDobell(ParametrosLCG parametros) {
        long a = parametros.getA();
        long c = parametros.getC();
        long m = parametros.getM();

        // Condicion 1: c y m deben ser primos relativos (mcd = 1)
        boolean condicion1 = mcd(c, m) == 1;

        // Condicion 2: (a - 1) divisible por TODOS los factores primos de m
        boolean condicion2 = true;
        for (long factor : factoresPrimos(m)) {
            if ((a - 1) % factor != 0) {
                condicion2 = false;
            }
        }

        // Condicion 3: si m es multiplo de 4, (a - 1) tambien debe serlo
        boolean condicion3 = true;
        if (m % 4 == 0) {
            condicion3 = (a - 1) % 4 == 0;
        }

        // LinkedHashMap mantiene el orden en que se insertan los datos
        Map<String, Boolean> resultado = new LinkedHashMap<>();
        resultado.put("mcd(c, m) = 1", condicion1);
        resultado.put("(a-1) divisible por factores primos de m", condicion2);
        resultado.put("si 4 divide a m, 4 divide a (a-1)", condicion3);
        resultado.put("periodo completo", condicion1 && condicion2 && condicion3);
        return resultado;
    }

    // Calcula el periodo generando numeros hasta que uno se repite.
    // Solo sirve para modulos pequenos. Devuelve -1 si no lo encuentra.
    public long calcularPeriodo(GeneradorAleatorio generador, long semilla, long limite) {
        generador.reiniciar(semilla);
        Map<Long, Long> vistos = new HashMap<>();  // valor -> posicion
        vistos.put(semilla, 0L);
        for (long paso = 1; paso <= limite; paso++) {
            long valor = generador.siguiente();
            if (vistos.containsKey(valor)) {
                return paso - vistos.get(valor);
            }
            vistos.put(valor, paso);
        }
        return -1;
    }

    // Revisa si algun X se repite dentro de una lista ya generada.
    // Devuelve la posicion de la primera repeticion o -1 si no hay.
    public int buscarRepeticion(List<Observacion> observaciones) {
        Set<Long> vistos = new HashSet<>();
        for (Observacion obs : observaciones) {
            if (vistos.contains(obs.getValorX())) {
                return obs.getIndice();
            }
            vistos.add(obs.getValorX());
        }
        return -1;
    }

    // Maximo comun divisor (algoritmo de Euclides)
    private long mcd(long x, long y) {
        while (y != 0) {
            long temporal = y;
            y = x % y;
            x = temporal;
        }
        return x;
    }

    // Lista de factores primos distintos de un numero
    private List<Long> factoresPrimos(long numero) {
        List<Long> factores = new ArrayList<>();
        long divisor = 2;
        while (divisor * divisor <= numero) {
            if (numero % divisor == 0) {
                factores.add(divisor);
                while (numero % divisor == 0) {
                    numero = numero / divisor;
                }
            }
            divisor++;
        }
        if (numero > 1) {
            factores.add(numero);
        }
        return factores;
    }
}
