'use strict';

const BAR_THEORY = '#3b4b61'; // Color de las barras teóricas.
const BAR_SIMULATED = '#42d3d8'; // Color de las barras simuladas.
const BARS_METRICS = [ // Cada métrica relaciona la clave teórica con la simulada.
  { label: 'ρ', theory: 'rho', simulated: 'utilization' }, // Utilización.
  { label: 'L', theory: 'L', simulated: 'avg_system' }, // Paquetes en el sistema.
  { label: 'Lq', theory: 'Lq', simulated: 'avg_queue' }, // Paquetes en cola.
  { label: 'W', theory: 'W', simulated: 'mean_system' }, // Tiempo en el sistema.
  { label: 'Wq', theory: 'Wq', simulated: 'mean_wait' }, // Tiempo de espera.
];
let barScenarios = null; // Última respuesta de /api/scenarios para redibujar.

/**
 * Formatea una métrica con uno o dos decimales según su magnitud.
 * @param {number|null} value - Valor a mostrar.
 * @returns {string} Valor formateado o guion si no es válido.
 */
const barFmt = value => {
  if (value == null || !Number.isFinite(value)) return '—'; // Valor ausente o inválido.
  return Number(value).toFixed(Math.abs(value) >= 10 ? 1 : 2); // Menos decimales si es grande.
};

/**
 * Dibuja las barras teóricas y simuladas de un escenario.
 * @param {HTMLCanvasElement} canvas - Lienzo donde se pinta el gráfico.
 * @param {Object} scenario - Escenario con las secciones theory y simulated.
 */
function drawScenarioBars(canvas, scenario) {
  const rect = canvas.getBoundingClientRect(); // Tamaño visible en CSS.
  const dpr = window.devicePixelRatio || 1; // Densidad de píxeles de la pantalla.
  const width = Math.max(240, rect.width); // Ancho mínimo para mantener legibilidad.
  const height = 250; // Altura lógica del lienzo.
  canvas.width = width * dpr; // Ancho físico del canvas.
  canvas.height = height * dpr; // Alto físico del canvas.
  const ctx = canvas.getContext('2d'); // Contexto de dibujo 2D.
  ctx.scale(dpr, dpr); // Escala para que las coordenadas sean CSS px.
  ctx.clearRect(0, 0, width, height); // Limpia el fotograma anterior.

  const left = 12, right = width - 8, top = 34, bottom = height - 34; // Márgenes.
  const plotWidth = right - left, plotHeight = bottom - top; // Área útil.
  const groupWidth = plotWidth / BARS_METRICS.length; // Ancho por métrica.
  const barWidth = Math.min(18, Math.max(8, groupWidth * 0.26)); // Ancho adaptable.
  const gap = 3; // Separación entre barra teórica y simulada.

  ctx.font = '9px ui-sans-serif,system-ui'; // Fuente de etiquetas.
  ctx.textAlign = 'center'; // Texto centrado en cada grupo.

  BARS_METRICS.forEach((metric, index) => {
    const theory = scenario.theory[metric.theory]; // Valor analítico.
    const simulated = scenario.simulated[metric.simulated]; // Valor de SimPy.
    const values = [theory, simulated].filter(Number.isFinite); // Solo valores válidos.
    const maximum = values.length ? Math.max(...values) : 0; // Escala local de la métrica.
    const center = left + groupWidth * (index + 0.5); // Centro del grupo.
    // Altura proporcional al máximo del grupo; ambas barras comparten escala.
    const theoryHeight = Number.isFinite(theory) && maximum > 0
      ? (theory / maximum) * (plotHeight - 18) : 0;
    const simulatedHeight = Number.isFinite(simulated) && maximum > 0
      ? (simulated / maximum) * (plotHeight - 18) : 0;

    ctx.fillStyle = BAR_THEORY; // Barra teórica.
    ctx.fillRect(center - barWidth - gap / 2, bottom - theoryHeight, barWidth, theoryHeight);
    ctx.fillStyle = BAR_SIMULATED; // Barra simulada.
    ctx.fillRect(center + gap / 2, bottom - simulatedHeight, barWidth, simulatedHeight);

    ctx.fillStyle = '#a9b9cb'; // Color de los valores numéricos.
    ctx.fillText(barFmt(theory), center - barWidth / 2 - gap / 2, bottom - theoryHeight - 5);
    ctx.fillText(barFmt(simulated), center + barWidth / 2 + gap / 2, bottom - simulatedHeight - 5);
    ctx.fillStyle = '#8c9eb2'; // Color de la etiqueta de la métrica.
    ctx.fillText(metric.label, center, bottom + 16);
  });

  ctx.strokeStyle = '#27384c'; // Línea base del gráfico.
  ctx.beginPath();
  ctx.moveTo(left, bottom);
  ctx.lineTo(right, bottom);
  ctx.stroke();

  ctx.textAlign = 'left'; // Leyenda alineada a la izquierda.
  ctx.fillStyle = BAR_THEORY;
  ctx.fillRect(left, 10, 10, 10); // Muestra de color teórico.
  ctx.fillStyle = '#a9b9cb';
  ctx.fillText('Teórico', left + 15, 19);
  ctx.fillStyle = BAR_SIMULATED;
  ctx.fillRect(left + 75, 10, 10, 10); // Muestra de color simulado.
  ctx.fillStyle = '#a9b9cb';
  ctx.fillText('Simulado', left + 90, 19);
}

/**
 * Reemplaza el contenido de #barCharts por una tarjeta por escenario.
 * @param {Array<Object>} scenarios - Escenarios devueltos por la API.
 */
function renderScenarioBars(scenarios) {
  const container = document.getElementById('barCharts'); // Contenedor de tarjetas.
  container.replaceChildren(); // Elimina gráficos anteriores.
  scenarios.forEach(scenario => {
    const card = document.createElement('div'); // Tarjeta del escenario.
    card.className = 'bar-scenario';
    const title = document.createElement('h3'); // Nombre del escenario.
    title.textContent = scenario.scenario;
    const meta = document.createElement('p'); // Parámetros λ y μ.
    meta.className = 'bar-meta';
    meta.textContent = `λ=${scenario.arrival_rate} · μ=${scenario.service_rate}`;
    const canvas = document.createElement('canvas'); // Lienzo del gráfico.
    canvas.setAttribute('role', 'img'); // Accesibilidad: se comporta como imagen.
    canvas.setAttribute('aria-label', `Gráfico de barras de ${scenario.scenario}`);
    card.append(title, meta, canvas); // Construye la tarjeta.
    container.append(card); // Añade la tarjeta al contenedor.
    drawScenarioBars(canvas, scenario); // Dibuja con el tamaño ya insertado.
  });
}

/**
 * Lee duración y semilla del formulario y actualiza la etiqueta T/semilla.
 * @returns {URLSearchParams} Parámetros para /api/scenarios.
 */
function scenarioParams() {
  const durationInput = document.getElementById('duration'); // Campo T.
  const seedInput = document.getElementById('seed'); // Campo semilla.
  const duration = durationInput ? Number(durationInput.value) : 120; // Default 120.
  const seed = seedInput ? Number(seedInput.value) : 42; // Default 42.
  const meta = document.getElementById('barsMeta'); // Etiqueta visible.
  if (meta) meta.textContent = `T=${duration} · semilla=${seed}`; // Refleja los valores.
  return new URLSearchParams({ duration, seed }); // Query string de la petición.
}

/** Solicita los tres escenarios con los parámetros actuales y los dibuja. */
async function loadScenarioBars() {
  const container = document.getElementById('barCharts'); // Contenedor de gráficos.
  container.textContent = 'Calculando escenarios…'; // Mensaje mientras se calcula.
  try {
    const response = await fetch('/api/scenarios?' + scenarioParams()); // Petición GET.
    const scenarios = await response.json(); // Respuesta JSON.
    if (!response.ok) throw new Error(scenarios.error || 'Error al calcular escenarios');
    barScenarios = scenarios; // Guarda para redibujar al cambiar el tamaño.
    renderScenarioBars(scenarios); // Construye las tarjetas.
  } catch (error) {
    container.textContent = error.message; // Muestra el error en la interfaz.
  }
}

// Al cambiar el tamaño, redibuja con los datos ya cargados.
window.addEventListener('resize', () => {
  if (!barScenarios) return; // Nada que redibujar todavía.
  document.querySelectorAll('#barCharts canvas').forEach((canvas, index) => {
    drawScenarioBars(canvas, barScenarios[index]); // Recalcula el tamaño del canvas.
  });
});

document.getElementById('run').addEventListener('click', loadScenarioBars); // Nueva simulación.
document.getElementById('compare').addEventListener('click', loadScenarioBars); // Comparación.
loadScenarioBars(); // Carga inicial al abrir la página.
