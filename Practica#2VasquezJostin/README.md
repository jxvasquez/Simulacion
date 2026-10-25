# Simulación de Crecimiento Poblacional

![Python](https://img.shields.io/badge/Python-3.12%2B-blue.svg)
![NumPy](https://img.shields.io/badge/NumPy-2.5.3-lightblue.svg)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.11.2-orange.svg)

Comparación de cuatro paradigmas de simulación —determinístico, discreto, estocástico y continuo— aplicados al crecimiento de una población, con una arquitectura Modelo-Vista-Controlador (MVC).

---

## Tabla de contenido

- [Descripción general](#descripción-general)
- [Modelos y fórmulas](#modelos-y-fórmulas)
- [Parámetros de entrada](#parámetros-de-entrada)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Requisitos previos](#requisitos-previos)
- [Instalación](#instalación)
- [Instrucciones de uso](#instrucciones-de-uso)
- [Resultados](#resultados)
- [Consideraciones y limitaciones](#consideraciones-y-limitaciones)
- [Autor](#autor)

---

## Descripción general

Este proyecto implementa una simulación computacional del crecimiento poblacional a partir de una serie base de 7 registros (de 1000 a 2100 individuos). El sistema proyecta la evolución de la población con cuatro enfoques matemáticos y los compara gráficamente con los datos originales y con una capacidad máxima ambiental `K`:

| Modelo | Enfoque | Característica principal |
|---|---|---|
| Determinístico | Tiempo continuo | Crecimiento exponencial sin aleatoriedad |
| Discreto | Tiempo discreto | Actualización paso a paso de la población |
| Estocástico | Tiempo discreto con ruido | Incorpora incertidumbre mediante una distribución normal |
| Continuo | Integración numérica | Aproxima la EDO con el método de Euler |

El desarrollo sigue el patrón **Modelo-Vista-Controlador (MVC)**: `modelo.py` contiene la lógica matemática, `vista.py` la representación gráfica y `main.py` la configuración y coordinación de la simulación.

## Modelos y fórmulas

Sea:

- $P_0$: población inicial.
- $r$: tasa de crecimiento.
- $T$: horizonte de simulación (número de periodos).
- $\sigma$: desviación estándar del ruido.
- $\Delta t$: paso de tiempo del modelo continuo.

### 1. Modelo determinístico

Crecimiento exponencial continuo, evaluado en instantes enteros:

$$
P(t) = P_0 \, e^{rt}, \qquad t = 0, 1, \dots, T
$$

### 2. Modelo discreto

Actualización discreta con incremento proporcional a la población actual:

$$
P_{t+1} = P_t + rP_t = (1 + r)P_t, \qquad P_0 \text{ dado}
$$

### 3. Modelo estocástico

Modelo discreto con un término de ruido aleatorio independiente en cada periodo:

$$
P_{t+1} = \max\left(0,\; P_t + rP_t + \varepsilon_t\right),
\qquad \varepsilon_t \sim \mathcal{N}(0, \sigma^2)
$$

El valor se trunca a cero para evitar poblaciones negativas.

### 4. Modelo continuo (Euler)

Aproximación numérica de la ecuación diferencial $\frac{dP}{dt} = rP$ mediante el método explícito de Euler:

$$
P_{t+\Delta t} = P_t + \Delta t \, rP_t
$$

La malla temporal se genera con `np.arange(0, T + dt, dt)`.

## Parámetros de entrada

Los valores se definen en `main.py` y pueden modificarse antes de ejecutar:

| Parámetro | Variable | Valor por defecto | Descripción |
|---|---|---:|---|
| Población inicial | `p0` | `1000` | Primer dato de la serie |
| Tasa de crecimiento | `r` | `0.11` | Crecimiento proporcional por periodo |
| Horizonte | `tiempo` | `6` | Número de periodos simulados |
| Ruido | `sigma` | `40.0` | Desviación estándar del ruido (individuos) |
| Paso continuo | `dt` | `0.1` | Incremento temporal del método de Euler |
| Capacidad máxima | `K` | `2500` | Línea de referencia ambiental en la gráfica |
| Datos originales | `datos` | `[1000, 1100, 1250, 1400, 1600, 1850, 2100]` | Serie observada |

> **Nota:** `K` solo se dibuja como línea de referencia; no interviene en las ecuaciones de los modelos.

## Estructura del proyecto

```text
Practica#2VasquezJostin/
├── main.py                 # Controlador: parámetros, instancias y ejecución
├── modelo.py               # Modelo: algoritmos de los cuatro paradigmas
├── vista.py                # Vista: gráfica comparativa con Matplotlib
├── requirements.txt        # Dependencias con versiones fijadas
├── APE2_Simulacion.pdf     # Informe técnico de la práctica
└── README.md               # Documentación del proyecto
```

## Requisitos previos

- **Python 3.12 o superior** (el proyecto se desarrolló con Python 3.12).
- **pip** (incluido con Python).
- **Git** para clonar el repositorio.
- Entorno con interfaz gráfica o backend de Matplotlib compatible, ya que el resultado se muestra en una ventana con `plt.show()`.
- Dependencias principales:
  - `numpy==2.5.3` — cálculos vectoriales y generación de ruido normal.
  - `matplotlib==3.11.2` — gráfica comparativa.
- Sistema recomendado: Linux o macOS (también funciona en Windows).

## Instalación

1. Clonar el repositorio e ingresar al directorio del proyecto:

   ```bash
   git clone https://github.com/xDylok/Simulacion.git
   cd "Simulacion/Practica#2VasquezJostin"
   ```

2. Crear un entorno virtual:

   ```bash
   python3 -m venv .venv
   ```

3. Activar el entorno virtual:

   - Linux / macOS:

     ```bash
     source .venv/bin/activate
     ```

   - Windows (PowerShell):

     ```powershell
     .venv\Scripts\Activate.ps1
     ```

   - Windows (CMD):

     ```bat
     .venv\Scripts\activate.bat
     ```

4. Instalar las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

## Instrucciones de uso

1. Verificar que el entorno virtual esté activo.
2. Ejecutar el programa desde la raíz del proyecto:

   ```bash
   python main.py
   ```

3. Se abrirá una ventana de Matplotlib con:

   - La curva **determinística** (línea continua).
   - La curva **discreta** (línea discontinua).
   - La curva **estocástica** (puntos).
   - La curva **continua** (línea de punto y raya).
   - Los **datos originales** (marcadores negros).
   - La **capacidad máxima `K`** (línea roja discontinua).

4. Cerrar la ventana para finalizar el programa.

### Personalizar la simulación

Editar los valores en `Controlador.__init__` (`main.py`):

```python
self.datos = [1000, 1100, 1250, 1400, 1600, 1850, 2100]
self.p0 = self.datos[0]
self.tiempo = len(self.datos) - 1
self.r = 0.11
self.sigma = 40.0
self.dt = 0.1
self.K = 2500
```

Para reproducir una corrida estocástica específica, fijar una semilla antes de ejecutar el modelo:

```python
import numpy as np
np.random.seed(42)
```

## Resultados

La ejecución genera una gráfica comparativa titulada **"Comparación de modelos de crecimiento poblacional"**. En la práctica, el modelo estocástico suele aproximarse mejor a la serie observada, mientras que los modelos determinístico y continuo quedan por debajo y el discreto subestima el crecimiento final. Al no fijarse una semilla, la curva estocástica cambia en cada ejecución.

## Consideraciones y limitaciones

- Los modelos determinístico, discreto y continuo son variantes del mismo crecimiento proporcional; la diferencia radica en la discretización y en la aleatoriedad.
- `K` es solo una referencia visual: no se implementa un modelo logístico con saturación.
- La serie de datos es pequeña (7 puntos), por lo que las proyecciones son ilustrativas y no predictivas.
- El modelo estocástico añade ruido absoluto en individuos, no ruido proporcional a la población.
- El método de Euler con `dt = 0.1` es una aproximación; pasos menores aumentan la precisión.
- No se guardan resultados en disco ni se incluyen pruebas automatizadas.

## Autor

**Jostin Xavier Vasquez Calderón**

Universidad Nacional de Loja (UNL) — Carrera de Computación

Asignatura: Simulación — Práctica Nro. 002
