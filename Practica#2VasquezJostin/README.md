# Simulación de Crecimiento Poblacional - Arquitectura MVC

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![NumPy](https://img.shields.io/badge/NumPy-Cálculo-lightblue.svg)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Gráficas-orange.svg)
## Descripción del Proyecto
___
Este proyecto implementa una simulación computacional orientada a analizar 
el crecimiento poblacional, comparando el comportamiento de cuatro paradigmas 
matemáticos fundamentales: determinístico, discreto, estocástico y continuo. 
A partir de un conjunto de  datos base, el sistema proyecta la evolución de la 
población para demostrar cómo la discretización del tiempo y la introducción de 
aleatoriedad (ruido) impactan en los resultados. Todo el desarrollo está estructurado 
bajo el patrón arquitectónico Modelo-Vista-Controlador (MVC), asegurando un código 
modular que separa estrictamente la lógica matemática de la representación gráfica 
final.

## Tecnologías
___
* **Python 3.x:** Lenguaje principal de desarrollo.
* **NumPy:** Operaciones con vectores, constantes matemáticas ($e$) y generación de variables aleatorias mediante distribución normal.
* **Matplotlib:** Generación de la gráfica comparativa y configuración de ejes, leyendas y cuadrículas.

## Estructura del Proyecto
___
```
Practica#2VasquezJostin/
├── main.py          # Controlador: Define variables (P0, r, sigma, dt), instancia las clases y orquesta el flujo.
├── modelo.py        # Modelo: Contiene los algoritmos iterativos paso a paso para cada paradigma de simulación.
├── vista.py         # Vista: Dibuja las curvas de población, los datos reales y la capacidad máxima K.
└── README.md        # Documentación técnica del proyecto.
```

## Requisitos previos
___
Python 3.12 o superior.
Instalador de paquetes pip (incluido por defecto con Python).

## Instalación y Ejecución
___

1. Clonar el repositorio:
   ```
   git clone "https://github.com/xDylok/Simulacion.git"
   cd Practica#2VasquezJostin

2. Crear el entorno virtual
   ```
   python3 -m venv .venv

3. Activar el entorno virtual
   
   - Linux/MacOS:
   ``` 
   source .venv/bin/activate 
   ```
   - Windows:
   ```
   .venv/Scripts/activate
   ```
4. Instalar los requerimientos
   ```
   pip install -r requirements.txt
   ```
5. Ejecutar la simulacion
   ```
   python main.py
   ```
   
## Autor(es)
___
* **Jostin Xavier Vasquez Calderón**
* Universidad Nacional de Loja (UNL) - Carrera de Computación