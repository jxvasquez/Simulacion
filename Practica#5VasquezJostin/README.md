# Practica 05 - Generador Congruencial Lineal (LCG) en Python y Java

Patron de diseno: **MVC (Modelo - Vista - Controlador)**
Parametros de la guia: a = 1664525, c = 1013904223, m = 2^32, semilla = 12345

## Estructura del proyecto

```
practica_lcg/
|-- python/
|   |-- main.py                        <- punto de entrada (pasos 1 al 8)
|   |-- comparar.py                    <- arma la tabla Python vs Java
|   |-- modelo/
|   |   |-- observacion.py             <- un valor generado (n, X, U)
|   |   |-- parametros_lcg.py          <- a, c, m, semilla + validacion
|   |   |-- generador_aleatorio.py     <- interfaz (clase abstracta)
|   |   |-- generador_lcg.py           <- formula del LCG
|   |   |-- analizador_periodo.py      <- Hull-Dobell y calculo del periodo
|   |   |-- estadisticas.py            <- media, varianza, min, max
|   |   |-- exportador_csv.py          <- guardar / leer CSV
|   |   |-- comparador_secuencias.py   <- compara dos secuencias
|   |-- vista/
|   |   |-- vista_consola.py           <- tablas y mensajes en la terminal
|   |   |-- vista_grafica.py           <- graficos con matplotlib (PNG)
|   |   |-- vista_comparacion.py       <- tabla Python vs Java
|   |-- controlador/
|       |-- controlador_lcg.py         <- coordina los pasos de la practica
|       |-- controlador_comparacion.py <- coordina la comparacion
|-- java/
|   |-- src/
|       |-- Main.java
|       |-- modelo/      (Observacion, ParametrosLCG, GeneradorAleatorio,
|       |                 GeneradorLCG, AnalizadorPeriodo, Estadisticas, ExportadorCSV)
|       |-- vista/       (VistaConsola, VistaGrafica)
|       |-- controlador/ (ControladorLCG)
|-- resultados/          <- aqui se guardan los CSV y los graficos
```

## Como ejecutar (Linux o macOS)

```bash
# 1) Python  (necesita matplotlib:  pip install matplotlib)
cd python
python3 main.py

# 2) Java
cd ../java
javac -d bin src/Main.java src/modelo/*.java src/vista/*.java src/controlador/*.java
java -cp bin Main

# 3) Tabla comparativa Python vs Java
cd ../python
python3 comparar.py
```

Importante: el programa Java se debe ejecutar desde la carpeta `java/`
para que los archivos se guarden en `resultados/`.

Archivos que se generan en `resultados/`:

- `secuencia_python.csv` y `secuencia_java.csv` (los 10 000 valores: n, X, U)
- `tabla_comparacion.csv` (n, X_python, X_java, U_python, U_java, coinciden)
- `comparacion_semillas.csv` (semilla 12345 vs 54321, lado a lado)
- `grafico_semilla_12345.png`, `grafico_semilla_54321.png`, `grafico_java.png`

## Como se aplica MVC

| Capa        | Que hace                                    | Ejemplo                              |
|-------------|---------------------------------------------|--------------------------------------|
| Modelo      | Calculos y datos. No imprime nada.          | `GeneradorLCG`, `AnalizadorPeriodo`  |
| Vista       | Solo muestra informacion.                   | `VistaConsola`, `VistaGrafica`       |
| Controlador | Pide datos al modelo y se los da a la vista | `ControladorLCG`                     |

## Como se aplican los principios SOLID

- **S - Responsabilidad unica:** cada clase hace una sola cosa
  (una genera, otra analiza el periodo, otra exporta CSV, otra muestra en pantalla).
- **O - Abierto/Cerrado:** para agregar otro generador (por ejemplo cuadrados medios)
  se crea una clase nueva que implemente `GeneradorAleatorio`; el controlador no se modifica.
- **L - Sustitucion de Liskov:** cualquier clase que implemente `GeneradorAleatorio`
  puede reemplazar a `GeneradorLCG` y el programa sigue funcionando.
- **I - Segregacion de interfaces:** `GeneradorAleatorio` es pequena y solo tiene
  metodos de generacion; exportar o analizar estan en clases separadas.
- **D - Inversion de dependencias:** el controlador recibe sus objetos en el constructor
  (los crea `main`) y depende de la interfaz, no de la clase concreta.

## Resultado obtenido

Las dos implementaciones producen exactamente la misma secuencia
(10 000 de 10 000 valores iguales). Primeros valores:

| n | X(n)       | U(n)         |
|---|------------|--------------|
| 1 | 87628868   | 0.0204026857 |
| 2 | 71072467   | 0.0165478482 |
| 3 | 2332836374 | 0.5431557945 |
| 4 | 2726892157 | 0.6349040561 |
| 5 | 3908547000 | 0.9100295138 |

Los parametros cumplen el teorema de Hull-Dobell, por lo que el periodo es
completo: m = 4 294 967 296. Con 10 000 valores la media fue 0.4988 (esperado 0.5)
y la varianza 0.0830 (esperado 1/12 = 0.0833).

Con parametros inadecuados (a = 5, c = 0, m = 16) el periodo baja a solo 4.

Detalle importante en Java: se usa `long` y no `int`, porque con m = 2^32 los valores
de X no caben en un `int` (maximo 2 147 483 647).
