package modelo;

// ============================================================
// MODELO - Interfaz comun de las pruebas de bondad de ajuste
// ============================================================
// I (Segregacion de interfaces): interfaz pequena con un solo metodo.
// O (Abierto/Cerrado): una prueba nueva = una clase nueva que
// implemente esta interfaz; el controlador no cambia.
// ============================================================
public interface PruebaEstadistica {

    // Recibe los numeros y devuelve el resultado de la prueba
    ResultadoPrueba aplicar(double[] numeros);
}
