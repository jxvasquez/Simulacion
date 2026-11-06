# Practica 06 - Validacion estadistica con Chi-cuadrado y Kolmogorov-Smirnov

Dos implementaciones (Python y Java) con patron MVC que generan la MISMA secuencia
cuando usan los mismos parametros del LCG.

## Estructura

```
practica06/
├── python/
│   ├── main.py                         # arma el programa (punto de entrada)
│   ├── modelo/
│   │   ├── generador.py                # GeneradorAleatorio (abstracta) + GeneradorLCG
│   │   ├── prueba_estadistica.py       # interfaz PruebaEstadistica
│   │   ├── prueba_chi_cuadrado.py      # Algoritmo 2
│   │   ├── prueba_kolmogorov_smirnov.py# Algoritmo 3
│   │   ├── distribuciones.py           # calculo de valores p (sin scipy)
│   │   ├── resultado_prueba.py         # datos + decision (p < 0.05)
│   │   └── repositorio_resultados.py   # guarda CSV
│   ├── vista/
│   │   ├── vista_consola.py            # imprime tablas y decisiones
│   │   └── vista_grafica.py            # histograma + Fn(x) vs F(x) (matplotlib)
│   └── controlador/
│       └── controlador_simulacion.py   # une modelo y vista, mide tiempos
├── java/src/
│   ├── Main.java
│   ├── modelo/   (GeneradorAleatorio, GeneradorLCG, PruebaEstadistica,
│   │              PruebaChiCuadrado, PruebaKolmogorovSmirnov, Distribuciones,
│   │              ResultadoPrueba, FilaResumen, RepositorioResultados)
│   ├── vista/    (VistaConsola, VistaGrafica)
│   └── controlador/ (ControladorSimulacion)
├── comparar_resultados.py              # arma la tabla Python vs Java
└── resultados/                         # CSV y graficos generados
```

## Como ejecutar

```bash
# 1) Python (requiere matplotlib)
cd python
python main.py

# 2) Java (JDK 11 o superior)
cd ../java
javac -d bin src/Main.java src/modelo/*.java src/vista/*.java src/controlador/*.java
java -cp bin Main

# 3) Tabla comparativa
cd ..
python comparar_resultados.py
```

## Principios SOLID aplicados

| Principio | Donde se aplica |
|---|---|
| S - Responsabilidad unica | Cada clase hace una sola cosa: generar, probar, guardar, mostrar o coordinar. |
| O - Abierto/Cerrado | Para agregar otra prueba o generador se crea una clase nueva; el controlador no cambia. |
| L - Sustitucion de Liskov | Cualquier `GeneradorAleatorio` o `PruebaEstadistica` puede reemplazar a otro. |
| I - Segregacion de interfaces | Interfaces pequenas: `generar()`/`descripcion()` y `aplicar()`. |
| D - Inversion de dependencias | El controlador recibe las abstracciones por su constructor (se arman en `main`). |

## Parametros usados

| Configuracion | semilla | a | c | m |
|---|---|---|---|---|
| buena | 12345 | 1664525 | 1013904223 | 2^32 |
| deficiente | 7 | 13 | 0 | 64 |

Nivel de significancia: alfa = 0.05, k = 10 intervalos (gl = 9).
