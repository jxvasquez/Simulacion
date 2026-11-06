package modelo;

import java.util.HashMap;
import java.util.Map;

// ============================================================
// MODELO - Guarda el resultado de cualquier prueba estadistica
// ============================================================
// S (Responsabilidad unica): solo almacena datos y toma la decision.
// ============================================================
public class ResultadoPrueba {

    private final String nombrePrueba;
    private final double estadistico;
    private final double valorP;
    private final double alfa;
    // Informacion extra (frecuencias, grados de libertad, etc.)
    private final Map<String, Object> detalles = new HashMap<>();

    public ResultadoPrueba(String nombrePrueba, double estadistico, double valorP, double alfa) {
        this.nombrePrueba = nombrePrueba;
        this.estadistico = estadistico;
        this.valorP = valorP;
        this.alfa = alfa;
    }

    // Criterio de decision: si p < alfa se rechaza H0
    public boolean seRechazaH0() {
        return valorP < alfa;
    }

    public String decision() {
        if (seRechazaH0()) {
            return "Se rechaza H0: los numeros NO siguen una distribucion uniforme";
        }
        return "No se rechaza H0: los numeros son compatibles con U(0,1)";
    }

    public void agregarDetalle(String clave, Object valor) {
        detalles.put(clave, valor);
    }

    public Object getDetalle(String clave) {
        return detalles.get(clave);
    }

    public String getNombrePrueba() { return nombrePrueba; }
    public double getEstadistico() { return estadistico; }
    public double getValorP() { return valorP; }
    public double getAlfa() { return alfa; }
}
