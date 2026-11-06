// ------------------------------------------------------------
// Archivo: GeneradorAleatorio.java
// Interfaz (contrato) que debe cumplir cualquier generador.
//
// Principios SOLID que se aplican aqui:
//  - O (Abierto/Cerrado): para agregar otro generador se crea una clase
//    nueva que implemente esta interfaz, sin modificar el controlador.
//  - L (Sustitucion de Liskov): cualquier implementacion puede usarse
//    en lugar de otra sin que el programa falle.
//  - I (Segregacion de interfaces): la interfaz es pequena, solo tiene
//    lo necesario para generar numeros.
//  - D (Inversion de dependencias): el controlador depende de esta
//    interfaz y no de la clase concreta GeneradorLCG.
// ------------------------------------------------------------
package modelo;

import java.util.List;

public interface GeneradorAleatorio {

    // Vuelve a empezar la secuencia usando una nueva semilla
    void reiniciar(long semilla);

    // Calcula y devuelve el siguiente numero entero X(n+1)
    long siguiente();

    // Convierte X(n) en un numero entre 0 y 1
    double normalizar(long valorX);

    // Devuelve una lista con 'cantidad' observaciones
    List<Observacion> generarSecuencia(int cantidad);
}
