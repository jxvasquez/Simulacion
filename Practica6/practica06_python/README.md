# Practica 06 - Version Python (MVC)

Validacion de numeros pseudoaleatorios (LCG) con Chi-cuadrado y Kolmogorov-Smirnov.

## Estructura

```
practica06_python/
├── main.py                          # arma el programa (punto de entrada)
├── modelo/
│   ├── generador.py                 # GeneradorAleatorio (abstracta) + GeneradorLCG
│   ├── prueba_estadistica.py        # interfaz PruebaEstadistica
│   ├── prueba_chi_cuadrado.py       # Algoritmo 2
│   ├── prueba_kolmogorov_smirnov.py # Algoritmo 3
│   ├── distribuciones.py            # calculo de valores p
│   ├── resultado_prueba.py          # datos + decision (p < 0.05)
│   └── repositorio_resultados.py    # guarda los CSV
├── vista/
│   ├── vista_consola.py             # tablas y decisiones en consola
│   └── vista_grafica.py             # histograma + Fn(x) vs F(x)
└── controlador/
    └── controlador_simulacion.py    # une modelo y vista, mide tiempos
```

## Ejecutar

```bash
pip install matplotlib
python main.py
```

Los resultados quedan en la carpeta `resultados/`:
`resultados_python.csv`, `secuencia_python_*.csv` y los graficos `.png`.

## SOLID

- **S**: cada clase hace una sola cosa (generar, probar, guardar, mostrar, coordinar).
- **O**: una prueba o generador nuevo es una clase nueva; el controlador no cambia.
- **L**: cualquier GeneradorAleatorio / PruebaEstadistica puede reemplazar a otro.
- **I**: interfaces pequenas (`generar`, `descripcion`, `aplicar`).
- **D**: el controlador recibe las abstracciones por su constructor (se crean en `main.py`).
