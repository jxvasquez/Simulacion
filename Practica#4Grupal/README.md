# Simulacion del modelo epidemiologico SIR (Python + SimPy + NetLogo)

Proyecto didactico que simula una epidemia con el modelo **SIR** y guarda los resultados en un
archivo **CSV** que se puede importar directamente en **NetLogo**.


---

## Tabla de contenidos

1. [Que hace el proyecto](#1-que-hace-el-proyecto)
2. [Requisitos previos](#2-requisitos-previos)
3. [Estructura de carpetas](#3-estructura-de-carpetas)
4. [Conceptos basicos](#4-conceptos-basicos)
5. [Instalacion y ejecucion paso a paso](#5-instalacion-y-ejecucion-paso-a-paso)
6. [Que archivos genera el programa](#6-que-archivos-genera-el-programa)
7. [Como importar el CSV en NetLogo](#7-como-importar-el-csv-en-netlogo)
8. [Como leer el codigo (orden recomendado)](#8-como-leer-el-codigo-orden-recomendado)
9. [Problemas frecuentes](#9-problemas-frecuentes)
10. [Ejercicios sugeridos](#10-ejercicios-sugeridos)

---

## 1. Que hace el proyecto

1. Le pregunta (por consola) los parametros de la epidemia, o usa los de la guia.
2. Simula **persona por persona** como se contagian y se recuperan durante 100 pasos de tiempo.
3. Verifica que los resultados sean coherentes (por ejemplo, que nadie desaparezca).
4. Guarda automaticamente:
   - `netlogo/resultados_python.csv` : la tabla `tiempo, susceptibles, infectados, recuperados`
     lista para NetLogo.
   - `netlogo/resultados_euler_python.csv` : una referencia matematica (con decimales).
   - `resultados/grafica_python.png` : la grafica de S, I y R.

Valores por defecto de la guia: N = 100, I(0) = 5, S(0) = 95, R(0) = 0, beta = 0.30,
gamma = 0.10, 100 pasos y semilla aleatoria 42.

---

## 2. Requisitos previos

- **Python 3.9 o superior** (se recomienda 3.11 o mas nuevo).
- Una **terminal**:
  - Windows: *PowerShell* o *Simbolo del sistema (CMD)*.
  - macOS: la aplicacion *Terminal*.
  - Linux: cualquier terminal.
- Conexion a internet **solo una vez**, para instalar las dependencias.
- (Opcional) **NetLogo 6.x o 7.x** para importar el CSV: https://ccl.northwestern.edu/netlogo/

### Como saber si ya tiene Python

Abra la terminal y escriba:

```bash
python --version
```

- Si muestra algo como `Python 3.12.3`, ya esta listo.
- Si dice que el comando no existe, pruebe `python3 --version` (macOS/Linux) o `py --version`
  (Windows).
- Si ninguno funciona, instale Python desde https://www.python.org/downloads/ .
  **En Windows, marque la casilla "Add python.exe to PATH" durante la instalacion.**

> En el resto de este README se escribe `python`. Si en su equipo el comando que funciono fue
> `python3` o `py`, use ese en su lugar.

---

## 3. Estructura de carpetas

```
proyecto_sir/
|-- main.py                 <- puerta de entrada: se ejecuta este archivo
|-- requirements.txt             <- lista de librerias que hay que instalar
|-- README.md                    <- este documento
|
|-- sir/                         <- paquete con las 4 capas
|   |-- dominio/                 <- CAPA 1: ideas matematicas
|   |   |-- estados.py           <- los estados S, I y R
|   |   |-- configuracion.py     <- parametros del modelo y sus reglas de validez
|   |   |-- registro_sir.py      <- una fila de resultados (S, I, R en un instante)
|   |   |-- ecuaciones.py        <- ecuaciones diferenciales y R0
|   |   `-- reglas.py            <- probabilidad de contagio de una persona
|   |
|   |-- aplicacion/              <- CAPA 2: logica de la simulacion
|   |   |-- simulador.py         <- simulacion persona por persona (con SimPy)
|   |   |-- solucion_euler.py    <- solucion matematica por el metodo de Euler
|   |   `-- verificador.py       <- comprueba que los resultados sean coherentes
|   |
|   |-- infraestructura/         <- CAPA 3: archivos y graficos
|   |   |-- exportador_csv.py    <- escribe los CSV (para NetLogo)
|   |   `-- graficador.py        <- dibuja y guarda la grafica PNG
|   |
|   `-- presentacion/            <- CAPA 4: interaccion con la persona
|       `-- consola.py           <- preguntas, mensajes y coordinacion general
|
|-- netlogo/
|   `-- modelo_sir_netlogo.nls   <- codigo NetLogo (aqui tambien se guardan los CSV)
|
|-- resultados/                  <- aqui se guarda la grafica PNG
`-- pruebas/
    `-- ejecutar_pruebas.py      <- pruebas automaticas
```

---

## 4. Conceptos basicos

### 4.1 El modelo SIR

Divide a la poblacion en tres grupos:

| Letra | Nombre       | Significado                                  |
|-------|--------------|----------------------------------------------|
| S     | Susceptibles | Personas sanas que se pueden contagiar       |
| I     | Infectados   | Personas enfermas que pueden contagiar       |
| R     | Recuperados  | Personas curadas (ya no se vuelven a enfermar) |

Parametros:

- **N**: poblacion total (siempre se cumple S + I + R = N).
- **beta**: tasa de contagio (entre 0 y 1).
- **gamma**: tasa de recuperacion (entre 0 y 1).
- **R0 = beta / gamma**: a cuantas personas contagia, en promedio, un infectado.
  Con los valores de la guia, R0 = 0.30 / 0.10 = 3.

Ecuaciones diferenciales (estan en `sir/dominio/ecuaciones.py`):

```
dS/dt = -beta * S * I / N
dI/dt =  beta * S * I / N  -  gamma * I
dR/dt =  gamma * I
```

En el instante inicial: dS = -1.425, dI = 0.925, dR = 0.500.

### 4.2 Dos formas de resolver el mismo modelo

| Forma                         | Donde esta                         | Resultado                      |
|-------------------------------|------------------------------------|--------------------------------|
| **Simulacion por personas** (con azar) | `aplicacion/simulador.py`  | Numeros **enteros** (personas reales) |
| **Metodo de Euler** (sin azar)         | `aplicacion/solucion_euler.py` | Numeros **decimales** (valores esperados) |

El CSV principal para NetLogo (`resultados_python.csv`) viene de la **simulacion por personas**.
El CSV de Euler es una referencia adicional y **no reemplaza** al principal.

Regla usada en la simulacion: en cada paso, un susceptible se contagia con probabilidad
`1 - (1 - beta/N)^I` y un infectado se recupera con probabilidad `gamma`. Todos los cambios de un
paso se deciden mirando el estado del paso anterior (cambios simultaneos).

### 4.3 Arquitectura por capas

Cada capa tiene **una responsabilidad** y solo puede "mirar hacia abajo":

```
        +--------------------------------------------+
        |  PRESENTACION   (consola.py)               |  habla con la persona
        +--------------------------------------------+
              |                         |
              v                         v
   +----------------------+   +-------------------------+
   |  APLICACION          |   |  INFRAESTRUCTURA        |
   |  simula y verifica   |   |  escribe CSV y graficos |
   +----------------------+   +-------------------------+
              |                         |
              v                         v
        +--------------------------------------------+
        |  DOMINIO  (ecuaciones, reglas, entidades)  |  no depende de nadie
        +--------------------------------------------+
```

| Capa             | Carpeta                | Responsabilidad                           | Puede importar               |
|------------------|------------------------|-------------------------------------------|------------------------------|
| Dominio          | `sir/dominio`          | Ideas matematicas puras del modelo        | Nada del proyecto            |
| Aplicacion       | `sir/aplicacion`       | Logica de la simulacion                   | Dominio                      |
| Infraestructura  | `sir/infraestructura`  | Crear archivos CSV y graficos             | Dominio                      |
| Presentacion     | `sir/presentacion`     | Preguntar, mostrar mensajes, coordinar    | Las otras tres capas         |

Ejemplos de la regla en este proyecto:

- `verificador.py` (Aplicacion) **no usa `print`**: devuelve una lista de problemas y es
  `consola.py` (Presentacion) quien los muestra.
- `simulador.py` (Aplicacion) **no escribe archivos**: solo devuelve el historial. Guardar el
  CSV es trabajo de `exportador_csv.py` (Infraestructura).
- `ecuaciones.py` (Dominio) funciona sin saber que existen simulador, CSV o consola.

---

## 5. Instalacion y ejecucion paso a paso

### Paso 1. Abrir la terminal dentro de la carpeta del proyecto

- **Windows**: abra la carpeta `proyecto_sir` en el Explorador, haga clic en la barra de
  direcciones, escriba `powershell` y presione Enter. (O abra PowerShell y use `cd`.)
- **macOS / Linux**: abra la terminal y use `cd`:

```bash
cd ruta/hacia/proyecto_sir
```

Compruebe que esta en el lugar correcto listando los archivos:

```bash
# Windows (PowerShell o CMD)
dir

# macOS / Linux
ls
```

Debe ver, entre otros, `main.py` y `requirements.txt`.

### Paso 2. Crear el entorno virtual

Un **entorno virtual** es una carpeta aislada donde se instalan las librerias de ESTE proyecto,
sin mezclarlas con las de otros proyectos ni con las del sistema. Se crea una sola vez.

```bash
# Windows
python -m venv entorno_sir

# macOS / Linux
python3 -m venv entorno_sir
```

Esto crea una carpeta nueva llamada `entorno_sir` (puede tardar unos segundos).

> En algunas distribuciones de Linux (Ubuntu/Debian) puede aparecer un error pidiendo instalar
> `python3-venv`. En ese caso ejecute: `sudo apt install python3-venv` y repita el comando.

### Paso 3. Activar el entorno virtual

Hay que activarlo **cada vez** que se abre una terminal nueva para trabajar con el proyecto.

```bash
# Windows - PowerShell
entorno_sir\Scripts\Activate.ps1

# Windows - Simbolo del sistema (CMD)
entorno_sir\Scripts\activate.bat

# macOS / Linux
source entorno_sir/bin/activate
```

Sabra que funciono porque el inicio de la linea de la terminal muestra `(entorno_sir)`.

> **Windows PowerShell** puede mostrar el error *"la ejecucion de scripts esta deshabilitada en
> este sistema"*. Solucion: ejecute una sola vez
> `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`, responda `S` y repita
> el comando de activacion. Tambien puede usar CMD con `activate.bat`.

### Paso 4. Instalar las dependencias

Con el entorno activado, primero actualice `pip` (el instalador de librerias) y luego instale
lo que indica `requirements.txt`:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Se instalaran `simpy` (reloj de la simulacion) y `matplotlib` (graficas), junto con las
librerias que ellas necesitan. Para comprobarlo:

```bash
python -m pip list
```

Deben aparecer `simpy` y `matplotlib` en la lista.

### Paso 5. Ejecutar la simulacion

```bash
python main.py
```

El programa pregunta:

```
Desea usar los valores por defecto de la guia? (s/n) [s]:
```

- Presione **Enter** (o escriba `s`) para usar los valores de la guia.
- Escriba `n` para elegir sus propios valores. Cada pregunta muestra el valor por defecto entre
  corchetes; si presiona Enter sin escribir nada, se usa ese valor. Puede escribir decimales con
  punto (`0.3`) o con coma (`0,3`).

Si algun valor no es valido (por ejemplo, beta = 1.5), el programa explica el problema y vuelve
a preguntar.

#### Ejemplo de salida con los valores por defecto

```
==============================================
  SIMULACION DEL MODELO EPIDEMIOLOGICO SIR
==============================================
Desea usar los valores por defecto de la guia? (s/n) [s]:

=== DATOS INICIALES ===
Poblacion total N = 100
Valores iniciales: S = 95, I = 5, R = 0
Beta = 0.3, Gamma = 0.1, Semilla = 42
Cambios esperados en t = 0: dS = -1.425, dI = 0.925, dR = 0.500
Numero reproductivo basico R0 = 3.00

Ejecutando la simulacion...
Verificacion correcta: en todas las filas S + I + R = 100

=== RESULTADOS ===
Filas generadas: 101
Pico de infectados: 19 personas en el tiempo 33
Estado final -> tiempo=100 S=16 I=0 R=84

=== ARCHIVOS GENERADOS ===
CSV para NetLogo : .../proyecto_sir/netlogo/resultados_python.csv
CSV de Euler     : .../proyecto_sir/netlogo/resultados_euler_python.csv
Grafica PNG      : .../proyecto_sir/resultados/grafica_python.png
```

Como la semilla es 42, **siempre obtendra exactamente estos mismos numeros** con los valores por
defecto. Cambie la semilla para obtener otra epidemia distinta.

### Paso 6. Ejecutar las pruebas (opcional pero recomendado)

```bash
python pruebas/ejecutar_pruebas.py
```

Cada prueba muestra `[OK]` o `[FALLO]`. Al final debe decir `Pruebas fallidas: 0`.

### Paso 7. Desactivar el entorno virtual

Cuando termine de trabajar:

```bash
deactivate
```

La proxima vez que quiera ejecutar el proyecto, solo repita el **Paso 4** (activar) y el
**Paso 6** (ejecutar). No hace falta crear el entorno ni instalar de nuevo.

---

## 6. Que archivos genera el programa

| Archivo                               | Contenido                                        | Valores          |
|---------------------------------------|--------------------------------------------------|------------------|
| `netlogo/resultados_python.csv`       | Simulacion por personas. **Es el que usa NetLogo.** | Enteros       |
| `netlogo/resultados_euler_python.csv` | Solucion matematica de referencia (Euler)        | Decimales        |
| `resultados/grafica_python.png`       | Grafica de S, I y R en el tiempo                 | Imagen           |

Cada ejecucion **reemplaza** estos archivos.

### Formato del CSV para NetLogo

```
tiempo,susceptibles,infectados,recuperados
0,95,5,0
1,93,7,0
2,92,6,2
...
100,16,0,84
```

- La primera linea es el **encabezado** con los cuatro nombres exactos (NetLogo lo comprueba).
- Hay **una fila por paso de tiempo**: 101 filas de datos para 100 pasos (del tiempo 0 al 100).
- Los separadores son comas, los numeros no llevan comillas y el punto decimal es un punto.
- En cada fila, `susceptibles + infectados + recuperados` es igual a la poblacion total.

---

## 7. Como importar el CSV en NetLogo

El archivo `netlogo/modelo_sir_netlogo.nls` contiene el codigo NetLogo (con comentarios linea
por linea). Ya trae los procedimientos que **leen** el CSV y dibujan las graficas.

> **Idea clave:** NetLogo busca los archivos CSV en la **misma carpeta donde se guardo el modelo
> `.nlogo`**. Por eso el programa de Python guarda los CSV en la carpeta `netlogo/`.

### Paso 1. Crear el modelo y pegar el codigo

1. Ejecute primero `python main.py` para que exista `netlogo/resultados_python.csv`.
2. Abra NetLogo y cree un modelo nuevo (*File > New*).
3. Guardelo (*File > Save*) con el nombre `modelo_sir_netlogo.nlogo` **dentro de la carpeta
   `netlogo/` del proyecto**, junto al CSV.
4. Abra el archivo `modelo_sir_netlogo.nls` con cualquier editor de texto, copie TODO su
   contenido y peguelo en la pestana **Code** de NetLogo (reemplazando lo que haya).
5. Presione el boton **Check** para comprobar que no haya errores.

### Paso 2. Crear los botones (pestana Interface)

Cree cada boton con *Button* y escriba en el campo **Commands** el nombre indicado:

| Nombre del boton / comando         | Opcion especial                    |
|------------------------------------|------------------------------------|
| `preparar`                         | ninguna                            |
| `avanzar`                          | marque la casilla **Forever**      |
| `exportar-netlogo`                 | ninguna                            |
| `cargar-python`                    | ninguna                            |
| `actualizar-graficas-importadas`   | ninguna                            |
| `cargar-java` (opcional)           | ninguna (solo si tiene un CSV de Java) |

### Paso 3. Crear las graficas (pestana Interface)

Cree **seis graficas** con *Plot*. Los nombres deben ser **exactamente** estos (el codigo los
busca por nombre):

| Nombre de la grafica        | Lapices (pens) que debe tener |
|-----------------------------|-------------------------------|
| `SIR NetLogo`               | `S`, `I`, `R`                 |
| `SIR Python`                | `S`, `I`, `R`                 |
| `SIR Java`                  | `S`, `I`, `R`                 |
| `Comparacion infectados`    | `Python`, `Java`, `NetLogo`   |
| `Comparacion susceptibles`  | `Python`, `Java`, `NetLogo`   |
| `Comparacion recuperados`   | `Python`, `Java`, `NetLogo`   |

Para cada lapiz: modo **Line** y deje **vacios** los comandos de actualizacion
(*update commands*), porque el codigo dibuja los puntos por si mismo.

### Paso 4. Usar el modelo

1. Presione `preparar` y luego `avanzar` (se detiene solo a los 100 pasos). Esto genera la serie
   propia de NetLogo.
2. Presione `cargar-python`: NetLogo lee `resultados_python.csv` y dibuja las graficas `SIR
   Python` y las de comparacion.
3. (Opcional) Presione `exportar-netlogo` para guardar `resultados_netlogo.csv` con la serie de
   NetLogo, en el mismo formato.
4. Si aparece *"Archivo no encontrado"*, el modelo `.nlogo` no esta guardado en la misma carpeta
   que el CSV (vea el Paso 1).

> El codigo NetLogo es el del proyecto original: solo se le agregaron comentarios. Las
> instrucciones sobre Java se conservan porque el modelo original comparaba tres plataformas,
> pero este proyecto **solo incluye la parte de Python**.

---

## 8. Como leer el codigo (orden recomendado)

Empiece por abajo (lo mas simple) y suba hacia la capa que usa a las demas:

1. `sir/dominio/estados.py` : los tres estados.
2. `sir/dominio/configuracion.py` : parametros y reglas de validez.
3. `sir/dominio/registro_sir.py` : una fila de resultados.
4. `sir/dominio/ecuaciones.py` y `sir/dominio/reglas.py` : las matematicas.
5. `sir/aplicacion/simulador.py` : como avanza el tiempo y como cambian las personas.
6. `sir/aplicacion/solucion_euler.py` y `sir/aplicacion/verificador.py`.
7. `sir/infraestructura/exportador_csv.py` y `sir/infraestructura/graficador.py`.
8. `sir/presentacion/consola.py` : como se coordina todo.
9. `main.py` : como se arranca.

Conceptos de Python que aparecen (todos explicados en los comentarios): variables, `if / elif /
else`, `for`, `while`, listas, funciones, clases con `__init__`, `try / except`, `import`.

Un detalle especial: el metodo `proceso_simulacion` de `simulador.py` usa la palabra `yield`.
Es la forma en que SimPy "pausa" la simulacion hasta que avanza el reloj; el comentario de ese
metodo lo explica.

---

## 9. Problemas frecuentes

| Sintoma                                                        | Causa y solucion |
|----------------------------------------------------------------|------------------|
| `python` no se reconoce como comando                           | Pruebe `python3` o `py`. Si no funciona, reinstale Python marcando "Add python.exe to PATH". |
| `ModuleNotFoundError: No module named 'simpy'` (o `matplotlib`) | Falta instalar las dependencias o el entorno no esta activado. Repita los Pasos 4 y 5. |
| `ModuleNotFoundError: No module named 'sir'`                   | Ejecute los comandos **desde la carpeta `proyecto_sir`** (donde esta `main.py`). |
| PowerShell: "la ejecucion de scripts esta deshabilitada"       | Vea la nota del Paso 4 o use CMD con `activate.bat`. |
| `No such file or directory` al crear el entorno                | Esta en otra carpeta. Use `cd` hasta `proyecto_sir`. |
| El programa repite una pregunta                                | Escribio un valor no valido (letras, beta mayor que 1...). Lea el mensaje y corrija. |
| NetLogo: "Archivo no encontrado"                               | Guarde el `.nlogo` en la misma carpeta que el CSV (carpeta `netlogo/`). |
| NetLogo: "Encabezado inesperado"                               | El CSV fue modificado. Vuelva a generarlo con `python main.py`. |
| Quiero empezar de cero                                         | Borre la carpeta `entorno_sir` y repita los Pasos 3 a 5. |
