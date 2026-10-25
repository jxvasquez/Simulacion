# Práctica #1: Simulación de Probabilidad de Lluvia

**Autor:** Jostin Xavier Vasquez Calderón  
**Institución:** Universidad Nacional de Loja — Carrera de Computación  
**Asignatura:** Simulación  
**Reporte técnico:** [APE1_Simulacion.pdf](APE1_Simulacion.pdf)

## Descripción general

Este proyecto implementa un modelo de simulación climática en Python que estima la probabilidad de lluvia a partir de datos horarios de **humedad relativa**, **nubosidad** y **temperatura**. Para cada registro, el programa calcula un índice de lluvia normalizado, lo clasifica en una de cuatro categorías y presenta los resultados mediante tablas en consola y gráficas de Matplotlib.

La simulación compara dos variantes del modelo:

- **Modelo original:** asigna mayor peso a la humedad.
- **Modelo ajustado:** asigna mayor peso a la nubosidad.

El código sigue el patrón de diseño **MVC (Modelo-Vista-Controlador)**, lo que separa la lógica matemática, la presentación de resultados y la coordinación del flujo de ejecución.

## Estructura del proyecto

```text
Practica#1VasquezJostin/
├── main.py               # Punto de entrada y datos de la simulación
├── modeloClima.py        # Fórmulas, cálculos y clasificación de estados
├── vistaClima.py         # Tablas en consola y gráficas con Matplotlib
├── controladorClima.py   # Orquesta modelo y vista
├── requirements.txt      # Dependencias con versiones fijadas
├── pyproject.toml        # Metadatos del proyecto
├── APE1_Simulacion.pdf   # Reporte técnico de la práctica
└── README.md
```

| Archivo | Responsabilidad |
| --- | --- |
| `main.py` | Define los datos meteorológicos e inicia la simulación. |
| `modeloClima.py` | Normaliza variables, calcula el factor de temperatura y el índice, y determina el estado del clima. |
| `vistaClima.py` | Imprime las tablas y genera las gráficas del índice frente al tiempo. |
| `controladorClima.py` | Ejecuta ambos modelos y coordina las salidas de la vista. |

## Modelo matemático

### 1. Normalización de variables

La humedad y la nubosidad se reciben como porcentajes y se transforman a una escala entre 0 y 1:

$$
H = \frac{\text{humedad}}{100}, \qquad N = \frac{\text{nubosidad}}{100}
$$

donde:

- $H$ es la humedad normalizada.
- $N$ es la nubosidad normalizada.

### 2. Factor de temperatura

La temperatura se transforma en un factor $T_f$ mediante una función lineal por tramos:

$$
T_f(T) =
\begin{cases}
1.00, & T \leq 10^\circ\text{C} \\[4pt]
\operatorname{round}\left(1 - 0.05\,(T - 10),\; 2\right), & 10 < T < 28^\circ\text{C} \\[4pt]
0.10, & T \geq 28^\circ\text{C}
\end{cases}
$$

El factor disminuye 0.05 por cada grado centígrado que aumenta la temperatura dentro del tramo intermedio. En el código, el resultado de ese tramo se redondea a dos decimales.

### 3. Índice de lluvia

El índice se obtiene mediante una combinación lineal ponderada de las tres variables normalizadas.

**Modelo original:**

$$
I = 0.50H + 0.30N + 0.20T_f
$$

**Modelo ajustado:**

$$
I = 0.20H + 0.70N + 0.10T_f
$$

En ambos casos los pesos suman 1, por lo que el índice queda en el intervalo $[0, 1]$. El valor final se redondea a dos decimales.

| Modelo | Peso de $H$ | Peso de $N$ | Peso de $T_f$ | Interpretación |
| --- | ---: | ---: | ---: | --- |
| Original | 0.50 | 0.30 | 0.20 | La humedad tiene la mayor influencia. |
| Ajustado | 0.20 | 0.70 | 0.10 | La nubosidad tiene la mayor influencia. |

### 4. Clasificación del estado del clima

El índice calculado se interpreta según los siguientes rangos:

| Rango del índice | Estado |
| --- | --- |
| $I < 0.40$ | Sin lluvia |
| $0.40 \leq I < 0.60$ | Baja posibilidad |
| $0.60 \leq I < 0.75$ | Lluvia probable |
| $I \geq 0.75$ | Lluvia |

En las gráficas se dibujan dos líneas de referencia: **0.40** (límite de "Sin lluvia") y **0.75** (umbral de lluvia, identificado como $K = 0.75$).

## Requisitos previos

- **Python 3.12 o superior** (el proyecto fue probado con Python 3.12.3).
- **pip**, incluido normalmente con Python.
- **Git**, si se desea clonar el repositorio (también es posible descargar el código en ZIP).
- **Entorno gráfico** o backend interactivo de Matplotlib para visualizar las ventanas de las gráficas.
- Dependencias de Python: Matplotlib y sus librerías asociadas, especificadas con versiones fijadas en `requirements.txt`.

## Instalación

1. Clonar el repositorio y entrar en la carpeta del proyecto:

   ```bash
   git clone https://github.com/xDylok/Simulacion.git
   cd "Simulacion/Practica#1VasquezJostin"
   ```

2. Crear un entorno virtual:

   ```bash
   python3 -m venv .venv
   ```

   > En Windows, use `py -3 -m venv .venv` o `python -m venv .venv` si el comando `python3` no está disponible.

3. Activar el entorno virtual:

   **Linux/macOS:**

   ```bash
   source .venv/bin/activate
   ```

   **Windows (CMD):**

   ```bat
   .venv\Scripts\activate.bat
   ```

   **Windows (PowerShell):**

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

4. Instalar las dependencias:

   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

## Instrucciones de uso

Con el entorno virtual activado y ubicado en la carpeta del proyecto, ejecutar:

```bash
python main.py
```

El programa realiza las siguientes acciones:

1. Calcula el índice de lluvia para cada hora con el **modelo original**.
2. Imprime la tabla de resultados en la consola.
3. Calcula y muestra la tabla del **modelo ajustado**.
4. Genera dos gráficas: una por cada modelo, con el índice a lo largo del tiempo y las líneas de referencia en 0.40 y 0.75.

Las tablas incluyen las columnas: hora, humedad, nubosidad, temperatura, humedad normalizada ($H$), nubosidad normalizada ($N$), factor de temperatura ($T_f$), índice calculado y estado.

### Modificar los datos de entrada

Los datos de la simulación se encuentran en `main.py`, dentro de la lista `datos_clima`. Cada elemento sigue el formato:

```python
# (hora, humedad_%, nubosidad_%, temperatura_°C)
datos_clima = [
    ("06:00", 65, 40, 14),
    ("08:00", 70, 50, 16),
    ("10:00", 68, 45, 18),
    # ...
]
```

- **Hora:** etiqueta de tiempo que se usa como eje horizontal en las gráficas.
- **Humedad:** porcentaje entre 0 y 100.
- **Nubosidad:** porcentaje entre 0 y 100.
- **Temperatura:** valor en grados centígrados.

Para simular otro escenario, basta con editar o ampliar esta lista y volver a ejecutar `python main.py`.

### Personalizar el modelo

- Los pesos de las fórmulas se definen en `modeloClima.py`, en el método `calcularIndice`.
- El factor de temperatura se calcula en el método `obtenerTf`.
- Los umbrales de clasificación se encuentran en el método `determinarEstado`.
- La línea de referencia $K = 0.75$ y los títulos de las gráficas se configuran en `vistaClima.py` y `controladorClima.py`, respectivamente.

## Notas

- Las ventanas de Matplotlib deben cerrarse para finalizar la ejecución del programa.
- En entornos sin interfaz gráfica (por ejemplo, servidores o SSH), las tablas se imprimen correctamente, pero las ventanas de las gráficas no podrán mostrarse. En ese caso, ejecute el proyecto en un entorno de escritorio o utilice un backend interactivo de Matplotlib.
- Si aparece un error de importación de `matplotlib`, verifique que el entorno virtual esté activado y que las dependencias se hayan instalado con `pip install -r requirements.txt`.
