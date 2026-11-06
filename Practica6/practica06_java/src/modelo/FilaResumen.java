package modelo;

// ============================================================
// MODELO - Una fila de la tabla resumen
// ============================================================
// Clase de datos sencilla (solo atributos y getters).
// ============================================================
public class FilaResumen {

    private final String configuracion;
    private final int n;
    private final ResultadoPrueba chi;
    private final ResultadoPrueba ks;
    private final double tiempoSegundos;

    public FilaResumen(String configuracion, int n, ResultadoPrueba chi,
                       ResultadoPrueba ks, double tiempoSegundos) {
        this.configuracion = configuracion;
        this.n = n;
        this.chi = chi;
        this.ks = ks;
        this.tiempoSegundos = tiempoSegundos;
    }

    public String getConfiguracion() { return configuracion; }
    public int getN() { return n; }
    public ResultadoPrueba getChi() { return chi; }
    public ResultadoPrueba getKs() { return ks; }
    public double getTiempoSegundos() { return tiempoSegundos; }
}
