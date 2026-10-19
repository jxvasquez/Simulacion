# QueueLab: simulador M/M/1 animado

Proyecto de la **Práctica 003 de Simulación (15-16/10/2026)**. Implementa una cola M/M/1 FIFO con **SimPy**, muestra una cinta transportadora animada y permite ver métricas, eventos y gráficos sincronizados con el tiempo *simulado*.

---

## Autores

- Miguel Armas
- Royel Jima
- Anita Panamito
- Jostin Vasquez

## Ejecutar

Se requiere Python 3.10+.

```bash
cd "Practica#3Grupal"
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows PowerShell:
# .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

Abrir **http://127.0.0.1:8501** en el navegador. Todo funciona localmente. La aplicación no requiere Internet ni servicios en la nube.

Al iniciar, `main.py` imprime en la consola las tablas de los tres escenarios (`T=120`, semilla `42`), genera los gráficos de barras que falten en `analysis/output/barras_escenarios/` y después arranca el servidor. Para ejecutar solo el reporte de consola: `python console_report.py`; para generar únicamente los gráficos: `python -m analysis.barras`.

**Pruebas**: `python -m unittest discover -s tests -v`. Incluye cuatro pruebas de teoría y dos de integración; estas últimas se omiten si SimPy no está instalado.

## Arquitectura por capas

```text
Practica#3Grupal/
├── main.py                         # Punto de entrada: reporte de consola y servidor
├── console_report.py               # Reporte de consola y generación de gráficos
├── domain/
│   ├── models.py                   # Config, Theory y validación
│   └── queueing.py                 # Fórmulas teóricas M/M/1
├── application/
│   └── use_cases.py                # simulate(), compare() y escenarios fijos
├── infrastructure/
│   └── simpy_engine.py             # MM1Engine: simulación de eventos discretos
├── analysis/
│   ├── barras.py                   # Genera los PNG de barras que falten
│   └── output/barras_escenarios/   # Gráficos y CSV teoría vs. simulación
├── presentation/
│   ├── server.py                   # Servidor HTTP con http.server
│   ├── console.py                  # Tablas de consola
│   └── static/
│       ├── index.html              # Interfaz
│       ├── styles.css              # Cinta animada y diseño responsivo
│       ├── barras.css              # Estilos de las barras por escenario
│       ├── app.js                  # Reproductor, canvas, tabla, comparación y CSV
│       └── barras.js               # Barras teórico vs simulado en la web
├── tests/
│   ├── __init__.py
│   ├── test_domain.py              # Pruebas de fórmulas y validación
│   └── test_integration.py         # Reproducibilidad, conservación y FIFO
└── requirements.txt
```

Dependencias: `presentation → application → domain`; `application → infrastructure` (adaptador SimPy); `infrastructure → domain`; `analysis → application`. El navegador consulta la API sin conocer SimPy. Para sustituir SimPy por otro motor, cambiar `MM1Engine` sin modificar el modelo matemático. Los gráficos PNG usan Pillow (incluido en `requirements.txt`).

## API local

`presentation/server.py` usa `http.server` de la biblioteca estándar:

- `POST /api/simulate`: recibe `{"arrival_rate", "service_rate", "duration", "seed"}`, valida la configuración y devuelve `config`, `theory`, `events`, `jobs` y `summary`.
- `GET /api/scenarios?duration=120&seed=42`: ejecuta los escenarios fijos (2, 3), (2.5, 3) y (2.9, 3) con la duración y semilla indicadas; si se omiten, usa `120` y `42`. La web envía los valores actuales del formulario; alimenta la comparación global y las barras.
- `GET /` y rutas estáticas: sirven `presentation/static/`.

Los errores de validación de `Config` se devuelven como HTTP 400.

## Funcionalidad

- Eventos `arrival`, `service_start`, `departure` y `end`.
- Intervalos entre llegadas `Exp(λ)` y tiempos de servicio `Exp(μ)` con semilla aleatoria reproducible.
- Recurso SimPy de capacidad uno y disciplina FIFO.
- Escenarios predefinidos (2, 3), (2.5, 3), (2.9, 3) y configuración personalizada.
- Validación: λ y μ en (0, 100], duración en [1, 10000], semilla en [0, 2³²−1].
- Cinta transportadora animada que representa la cola y la estación de servicio.
- Reloj de simulación, pausar, continuar, reiniciar, cambiar velocidad y navegar por la línea temporal.
- Gráficas Canvas en vivo de longitud de cola y espera promedio, sin CDN.
- Tablas en consola para los tres escenarios, con los valores por defecto de la aplicación web (`T=120`, semilla `42`).
- Generación automática de los PNG de barras por escenario en `analysis/output/barras_escenarios/`; solo crea los archivos que falten.
- Gráficos de barras en la web, uno por escenario, con teoría vs. simulación generados desde `/api/scenarios` con la duración y semilla del formulario.
- Conteo de llegadas, atendidos, cola y utilización, más un registro de los últimos ocho eventos.
- Tabla dinámica que contrasta **ρ, L, Lq, W y Wq** teóricos con sus estimaciones simuladas.
- Comparación de los tres escenarios de la guía desde la propia web.
- Exportación CSV de los paquetes atendidos con columnas `id`, `arrival`, `start`, `departure`, `wait`, `service` y `system`.

## Fórmulas

Para `λ < μ`, `ρ=λ/μ`, `L=λ/(μ−λ)`, `Lq=λ²/[μ(μ−λ)]`, `W=1/(μ−λ)`, `Wq=λ/[μ(μ−λ)]`. Si `λ ≥ μ`, el sistema se marca como inestable y las métricas de estado estacionario quedan en `None`.

> **Corrección de la guía**: una línea del fundamento teórico invierte ρ; el pseudocódigo de la misma guía sí indica `ρ=λ/μ`. Aquí se usa la fórmula correcta.

## Estadística simulada

- `Lq_sim = (∫Q(t)dt)/T`; `L_sim = (∫N(t)dt)/T`.
- `ρ_sim = (tiempo ocupado del servidor)/T`.
- `Wq_sim` y `W_sim`: promedios de los paquetes cuyo servicio **terminó** al finalizar el horizonte, para evitar contabilizar tiempos incompletos como cero.
- `throughput = paquetes completados/T`. `pending = llegadas − completados`.
- Gráficas y promedios en vivo utilizan el historial de eventos producido por SimPy; la reproducción visual **no es una segunda simulación** y no modifica los resultados.

**Limitaciones experimentales:** se detienen las llegadas y la observación al alcanzar el horizonte `T`, aunque queden paquetes pendientes. Las métricas teóricas son de largo plazo y pueden diferir, especialmente con `λ ≈ μ`, por transitorios, varianza aleatoria y censura de servicios pendientes. Con la duración por defecto (`120`) la comparación es rápida, pero el escenario cerca de saturación es muy ruidoso; aumentar `T` reduce el error. Para estimaciones mejores: más duración, varias semillas, intervalos de confianza y/o un periodo de calentamiento. Las unidades de tasas y tiempo son arbitrarias pero coherentes (p. ej., paquetes/minuto y minutos). No confundir velocidad de reproducción con tiempo de simulación.
