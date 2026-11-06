// ------------------------------------------------------------
// Archivo: ParametrosLCG.java
// Responsabilidad unica: guardar y validar los parametros del LCG.
// ------------------------------------------------------------
package modelo;

public class ParametrosLCG {

    private final long a;        // multiplicador
    private final long c;        // incremento
    private final long m;        // modulo
    private final long semilla;  // valor inicial X(0)

    public ParametrosLCG(long a, long c, long m, long semilla) {
        // Antes de guardar los datos verificamos que sean correctos
        validar(a, c, m, semilla);
        this.a = a;
        this.c = c;
        this.m = m;
        this.semilla = semilla;
    }

    private void validar(long a, long c, long m, long semilla) {
        if (m <= 0) {
            throw new IllegalArgumentException("El modulo m debe ser mayor que 0");
        }
        if (a <= 0 || a >= m) {
            throw new IllegalArgumentException("El multiplicador a debe cumplir 0 < a < m");
        }
        if (c < 0 || c >= m) {
            throw new IllegalArgumentException("El incremento c debe cumplir 0 <= c < m");
        }
        if (semilla < 0 || semilla >= m) {
            throw new IllegalArgumentException("La semilla debe cumplir 0 <= semilla < m");
        }
    }

    public long getA() {
        return a;
    }

    public long getC() {
        return c;
    }

    public long getM() {
        return m;
    }

    public long getSemilla() {
        return semilla;
    }
}
