// ------------------------------------------------------------
// Archivo: Observacion.java
// Responsabilidad unica (S de SOLID): guardar UN valor generado.
// ------------------------------------------------------------
package modelo;

public class Observacion {

    private final int indice;     // posicion en la secuencia (1, 2, 3, ...)
    private final long valorX;    // numero entero X(n)
    private final double valorU;  // numero normalizado U(n) = X(n) / m

    public Observacion(int indice, long valorX, double valorU) {
        this.indice = indice;
        this.valorX = valorX;
        this.valorU = valorU;
    }

    public int getIndice() {
        return indice;
    }

    public long getValorX() {
        return valorX;
    }

    public double getValorU() {
        return valorU;
    }
}
