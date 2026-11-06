# Practica 06 - Version Java (MVC)

Validacion de numeros pseudoaleatorios (LCG) con Chi-cuadrado y Kolmogorov-Smirnov.
Solo usa Java estandar (sin librerias externas).

## Estructura

```
practica06_java/src/
├── Main.java                         # arma el programa (punto de entrada)
├── modelo/
│   ├── GeneradorAleatorio.java       # interfaz
│   ├── GeneradorLCG.java
│   ├── PruebaEstadistica.java        # interfaz
│   ├── PruebaChiCuadrado.java        # Algoritmo 2
│   ├── PruebaKolmogorovSmirnov.java  # Algoritmo 3
│   ├── Distribuciones.java           # calculo de valores p
│   ├── ResultadoPrueba.java          # datos + decision (p < 0.05)
│   ├── FilaResumen.java              # una fila de la tabla
│   └── RepositorioResultados.java    # guarda los CSV
├── vista/
│   ├── VistaConsola.java
│   └── VistaGrafica.java             # grafico Fn(x) vs F(x) en PNG
└── controlador/
    └── ControladorSimulacion.java
```

## Ejecutar (desde la carpeta practica06_java)

```bash
javac -d bin src/Main.java src/modelo/*.java src/vista/*.java src/controlador/*.java
java -cp bin Main
```

En IntelliJ / NetBeans / Eclipse: marcar `src` como carpeta de codigo fuente y ejecutar `Main`.

Los resultados quedan en la carpeta `resultados/`:
`resultados_java.csv`, `secuencia_java_*.csv` y los graficos `.png`.

## SOLID

- **S**: cada clase hace una sola cosa (generar, probar, guardar, mostrar, coordinar).
- **O**: una prueba o generador nuevo es una clase nueva; el controlador no cambia.
- **L**: cualquier GeneradorAleatorio / PruebaEstadistica puede reemplazar a otro.
- **I**: interfaces pequenas (`generar`, `descripcion`, `aplicar`).
- **D**: el controlador recibe las interfaces por su constructor (se crean en `Main`).
