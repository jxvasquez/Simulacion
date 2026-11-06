package modelo;

// ============================================================
// MODELO - Interfaz (abstraccion) de un generador pseudoaleatorio
// ============================================================
// D (Inversion de dependencias): el controlador trabaja con esta
// interfaz, no con una clase concreta.
// O (Abierto/Cerrado): para otro generador se crea otra clase que
// implemente esta interfaz, sin modificar el resto del programa.
// ============================================================
public interface GeneradorAleatorio {

    // Devuelve un arreglo con 'cantidad' numeros en el intervalo [0, 1)
    double[] generar(int cantidad);

    // Devuelve un texto con los parametros del generador
    String descripcion();
}
