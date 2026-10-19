'use strict';

/**
 * Atajo para obtener un elemento del DOM por su id.
 * @param {string} id - Identificador del elemento.
 * @returns {HTMLElement|null} Elemento encontrado o null.
 */
const $ = id => document.getElementById(id);

let data = null; // Última simulación recibida de /api/simulate.
let clock = 0; // Tiempo de animación actual.
let eventIndex = 0; // Siguiente evento pendiente de aplicar.
let playing = true; // Indica si la animación avanza.
let lastFrame = 0; // Marca temporal del fotograma anterior.
let lastDraw = 0; // Último instante en que se redibujaron los gráficos.

// Nombres legibles para el registro de eventos.
const names = {
  arrival: 'Llegada',
  service_start: 'Comienza servicio',
  departure: 'Salida',
  end: 'Fin de simulación',
};

/** Formatea un número con decimales fijos; null/NaN se muestran como guion. */
const fmt = (n, digits = 3) => n == null || !Number.isFinite(n) ? '—' : Number(n).toFixed(digits);

/** Convierte una proporción en porcentaje con un decimal. */
const percent = n => fmt(n * 100, 1) + '%';

/**
 * Lee los parámetros actuales del formulario y los devuelve como objeto.
 * @returns {{arrival_rate: number, service_rate: number, duration: number, seed: number}}
 */
function config() {
  return {
    arrival_rate: Number($('lambda').value), // λ: llegadas por unidad de tiempo.
    service_rate: Number($('mu').value), // μ: servicios por unidad de tiempo.
    duration: Number($('duration').value), // T: horizonte simulado.
    seed: Number($('seed').value), // Semilla del generador aleatorio.
  };
}

/**
 * Solicita una simulación nueva y reinicia la animación.
 * @returns {Promise<void>}
 */
async function loadSimulation() {
  $('alert').textContent = ''; // Limpia errores anteriores.
  $('run').disabled = true; // Evita dobles peticiones.
  try {
    const response = await fetch('/api/simulate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(config()), // Envía λ, μ, T y semilla.
    });
    const result = await response.json(); // Respuesta completa de SimPy.
    if (!response.ok) throw Error(result.error || 'Error inesperado');

    data = result; // Guarda eventos, trabajos y resumen.
    clock = 0; // Reinicia el reloj de animación.
    eventIndex = 0; // Reinicia el cursor de eventos.
    playing = true; // Empieza reproduciendo.
    lastFrame = 0; // Fuerza un nuevo cálculo de delta.
    $('timeline').max = data.config.duration; // Ajusta la barra de progreso.
    $('timeline').value = 0;
    $('durationText').textContent = '/ ' + data.config.duration;
    $('play').textContent = '❚❚ Pausar';
    $('conveyor').classList.remove('paused');
    draw(true); // Primer fotograma completo.
  } catch (error) {
    $('alert').textContent = error.message; // Muestra el fallo al usuario.
  } finally {
    $('run').disabled = false; // Reactiva el botón.
  }
}

/**
 * Devuelve el último evento aplicado para el reloj actual.
 * @returns {Object|null} Estado instantáneo o null si no hay simulación.
 */
function snapshot() {
  if (!data) return null;
  // Avanza el cursor mientras el evento ya ocurrió en el tiempo de animación.
  while (eventIndex < data.events.length && data.events[eventIndex].t <= clock + 0.00000001) {
    eventIndex++;
  }
  // Si aún no hay eventos, usa un estado inicial vacío.
  return data.events[Math.max(0, eventIndex - 1)] || {
    t: 0, queue: 0, system: 0, busy: 0, arrived: 0, completed: 0,
    mean_wait: 0, mean_system: 0, avg_queue: 0, avg_system: 0, utilization: 0,
  };
}

/**
 * Calcula métricas acumuladas hasta el reloj de animación.
 * @param {Object} s - Último evento aplicado.
 * @returns {Object} Lq, L, ρ, Wq y W actualizados.
 */
function liveStats(s) {
  // Integración exacta por tramos constantes desde el último evento hasta el reloj.
  const dt = Math.max(0, clock - s.t); // Tiempo transcurrido desde el último evento.
  const t = Math.max(clock, 0.00000001); // Evita división por cero al inicio.
  // Nuevo promedio = (área previa + estado actual × dt) / tiempo total.
  const q = (s.avg_queue * s.t + dt * s.queue) / t; // Lq(t).
  const l = (s.avg_system * s.t + dt * s.system) / t; // L(t).
  const u = (s.utilization * s.t + dt * s.busy) / t; // ρ(t).
  return { Lq: q, L: l, rho: u, Wq: s.mean_wait, W: s.mean_system };
}

/**
 * Actualiza toda la interfaz con el estado correspondiente al reloj actual.
 * @param {boolean} force - Si es true, redibuja los gráficos sin esperar el throttle.
 */
function draw(force = false) {
  if (!data) return;

  const s = snapshot(); // Último evento aplicado.
  const live = liveStats(s); // Métricas ponderadas hasta el reloj actual.

  $('clock').textContent = fmt(clock, 1);
  $('timeline').value = clock;
  $('arrived').textContent = s.arrived; // Llegadas acumuladas.
  $('completed').textContent = s.completed; // Salidas acumuladas.
  $('queue').textContent = s.queue; // Cola instantánea.
  $('util').textContent = percent(live.rho); // Utilización acumulada.
  $('queueCount').textContent = s.queue;
  $('processing').textContent = s.busy ? 'SÍ' : 'NO';
  $('finished').textContent = s.completed;
  $('workState').textContent = s.busy ? '● EN SERVICIO' : '○ SERVIDOR LIBRE';
  $('status').textContent = clock >= data.config.duration
    ? '● FINALIZADO'
    : playing ? '● EJECUTANDO' : '● PAUSADO';
  $('status').style.color = clock >= data.config.duration ? '#ffc368' : '#58dab0';
  $('stationBody').parentElement.classList.toggle('active', Boolean(s.busy));

  // Busca el último service_start cuyo departure todavía no haya ocurrido.
  const start = [...data.events.slice(0, eventIndex)].reverse().find(e =>
    e.type === 'service_start' &&
    !data.events.slice(data.events.indexOf(e) + 1, eventIndex)
      .some(d => d.type === 'departure' && d.id === e.id));
  $('stationJob').textContent = s.busy && start
    ? 'PKG-' + String(start.id).padStart(3, '0')
    : 'LIBRE';

  // Reconstruye la cola FIFO a partir de las llegadas y salidas ya procesadas.
  const queued = [];
  for (let k = 0; k < eventIndex; k++) {
    const e = data.events[k];
    if (e.type === 'arrival') queued.push(e.id);
    if (e.type === 'service_start') {
      const idx = queued.indexOf(e.id);
      if (idx >= 0) queued.splice(idx, 1);
    }
  }
  const container = $('queuePacks');
  container.replaceChildren();
  // Representa como máximo nueve paquetes para no saturar la animación.
  queued.slice(0, 9).forEach((id, i) => {
    const box = document.createElement('div');
    box.className = 'package';
    box.style.left = `${Math.max(0, 61 - (Math.min(queued.length, 9) - i) * 7.4)}%`;
    const small = document.createElement('small');
    small.textContent = '#' + id;
    box.append(small);
    container.append(box);
  });
  if (queued.length > 9) {
    const extra = document.createElement('div');
    extra.className = 'package';
    extra.style.left = '1%';
    extra.textContent = '+' + (queued.length - 9);
    container.append(extra);
  }

  // Pares (etiqueta, clave teórica, clave simulada) de la tabla de métricas.
  const pairs = [
    ['ρ · utilización', 'rho', 'rho'],
    ['L · número medio en sistema', 'L', 'L'],
    ['Lq · longitud media de cola', 'Lq', 'Lq'],
    ['W · permanencia media', 'W', 'W'],
    ['Wq · espera media', 'Wq', 'Wq'],
  ];
  $('metrics').innerHTML = pairs.map(([label, theoretical, key]) => {
    const a = data.theory[theoretical]; // Valor teórico.
    const b = live[key]; // Valor simulado hasta t.
    return `<tr><td>${label}</td><td>${fmt(a)}</td><td>${fmt(b)}</td><td>${a == null ? '—' : fmt(b - a)}</td></tr>`;
  }).join('');

  // Muestra los últimos ocho eventos del registro.
  const recent = data.events.slice(Math.max(0, eventIndex - 8), eventIndex).reverse();
  $('log').innerHTML = recent.map(e => {
    const job = e.id != null ? ' · Paquete #' + e.id : '';
    const wait = e.type === 'service_start' ? ' · espera ' + fmt(e.wait, 2) : '';
    return `<div class="logline"><b>${fmt(e.t, 2)}</b> ${names[e.type]}${job}${wait}</div>`;
  }).join('');

  // Limita el redibujado de los canvas para no bloquear la animación.
  const now = performance.now();
  if (force || now - lastDraw > 90) {
    drawChart($('queueChart'), 'queue', '#42d3d8', clock);
    drawChart($('waitChart'), 'mean_wait', '#ffc368', clock, 'Espera promedio');
    lastDraw = now;
  }
}

/**
 * Dibuja una serie temporal en un canvas.
 * @param {HTMLCanvasElement} canvas - Lienzo de destino.
 * @param {string} field - Campo del evento que se representa.
 * @param {string} color - Color de la línea.
 * @param {number} until - Tiempo máximo visible.
 * @param {string} title - Título reservado para la firma; el rótulo está en el HTML.
 */
function drawChart(canvas, field, color, until, title) {
  const rect = canvas.getBoundingClientRect();
  const dpr = window.devicePixelRatio || 1; // Densidad física de píxeles.
  const w = Math.max(180, rect.width); // Ancho visible mínimo.
  const h = 210; // Alto lógico.
  canvas.width = w * dpr;
  canvas.height = h * dpr;
  const ctx = canvas.getContext('2d');
  ctx.scale(dpr, dpr);
  ctx.clearRect(0, 0, w, h);

  // Serie acumulada: solo eventos ya ocurridos hasta `until`.
  let events = data.events.filter(e => e.t <= until);
  let series = events.map(e => ({ x: e.t, y: e[field] }));
  let last = series.at(-1);
  series.push({ x: until, y: last ? last.y : 0 }); // Extiende la última muestra hasta t.

  let max = Math.max(1, ...series.map(p => p.y)); // Escala mínima para evitar cero.
  max *= 1.15; // Margen superior del 15 %.
  const left = 35, right = w - 10, top = 20, bottom = h - 27; // Márgenes.
  const width = right - left, height = bottom - top; // Área de dibujo.
  ctx.font = '11px ui-sans-serif,system-ui';
  ctx.textAlign = 'right';
  ctx.strokeStyle = '#27384c';
  ctx.fillStyle = '#8c9eb2';
  ctx.lineWidth = 1;

  // Cuadrícula horizontal y etiquetas del eje Y.
  for (let i = 0; i <= 4; i++) {
    const y = bottom - (i / 4) * height;
    ctx.beginPath();
    ctx.moveTo(left, y);
    ctx.lineTo(right, y);
    ctx.stroke();
    ctx.fillText(fmt(max * i / 4, 1), left - 8, y + 4);
  }
  // Etiquetas del eje X.
  ctx.textAlign = 'center';
  for (let i = 0; i <= 4; i++) {
    const x = left + i * width / 4;
    ctx.fillText(fmt(until * i / 4, 0), x, bottom + 17);
  }

  ctx.beginPath();
  ctx.lineWidth = 2;
  ctx.strokeStyle = color;
  series.forEach((point, index) => {
    const x = left + width * (until ? point.x / until : 0); // Tiempo → píxel.
    const y = bottom - height * point.y / max; // Valor → píxel.
    if (!index) {
      ctx.moveTo(x, y);
    } else if (field === 'queue') {
      // La cola es constante entre eventos: dibuja un escalón.
      const previous = series[index - 1];
      ctx.lineTo(x, bottom - height * previous.y / max);
      ctx.lineTo(x, y);
    } else {
      ctx.lineTo(x, y);
    }
  });
  ctx.stroke();

  // Rellena el área bajo la curva con un degradado.
  const grad = ctx.createLinearGradient(0, top, 0, bottom);
  grad.addColorStop(0, color + '33');
  grad.addColorStop(1, color + '02');
  ctx.lineTo(right, bottom);
  ctx.lineTo(left, bottom);
  ctx.closePath();
  ctx.fillStyle = grad;
  ctx.fill();
}

/**
 * Bucle de animación: avanza el reloj y solicita el siguiente fotograma.
 * @param {number} now - Marca temporal en milisegundos.
 */
function frame(now) {
  if (!lastFrame) lastFrame = now;
  const delta = Math.min((now - lastFrame) / 1000, .1); // Segundos, con tope de 100 ms.
  lastFrame = now;
  if (data && playing && clock < data.config.duration) {
    // La velocidad del selector multiplica el tiempo real transcurrido.
    clock = Math.min(data.config.duration, clock + delta * Number($('speed').value));
    if (clock === data.config.duration) {
      playing = false;
      $('play').textContent = '▶ Reproducir';
      $('conveyor').classList.add('paused');
    }
    draw();
  }
  requestAnimationFrame(frame); // Mantiene el bucle activo.
}

$('run').addEventListener('click', loadSimulation); // Nueva simulación.
$('scenario').addEventListener('change', e => {
  if (e.target.value !== 'custom') {
    $('lambda').value = e.target.value; // λ del escenario predefinido.
    $('mu').value = 3; // μ fija de los tres escenarios.
    loadSimulation();
  }
});
for (const id of ['lambda', 'mu']) {
  $(id).addEventListener('input', () => {
    $('scenario').value = 'custom'; // Un cambio manual deja de ser un escenario fijo.
  });
}

$('play').addEventListener('click', () => {
  if (!data) return;
  if (clock >= data.config.duration) {
    clock = 0; // Si terminó, vuelve al inicio.
    eventIndex = 0;
  }
  playing = !playing; // Alterna pausa/reproducción.
  $('play').textContent = playing ? '❚❚ Pausar' : '▶ Reproducir';
  $('conveyor').classList.toggle('paused', !playing);
  draw(true);
});

$('restart').addEventListener('click', () => {
  clock = 0;
  eventIndex = 0;
  playing = true;
  $('play').textContent = '❚❚ Pausar';
  $('conveyor').classList.remove('paused');
  draw(true);
});

$('timeline').addEventListener('input', e => {
  clock = Number(e.target.value); // Salta al instante elegido.
  eventIndex = 0; // Recalcula los eventos necesarios.
  draw(true);
});

$('export').addEventListener('click', () => {
  if (!data) return;
  const cols = ['id', 'arrival', 'start', 'departure', 'wait', 'service', 'system'];
  // Convierte puntos decimales a comas para que Excel los reconozca.
  let rows = [
    cols.join(';'),
    ...data.jobs.map(j => cols.map(k =>
      Number.isFinite(j[k]) ? String(j[k]).replace('.', ',') : j[k]).join(';')),
  ];
  let blob = new Blob(['\ufeff' + rows.join('\n')], { type: 'text/csv;charset=utf-8' }); // BOM UTF-8.
  let url = URL.createObjectURL(blob);
  let a = document.createElement('a');
  a.href = url;
  a.download = 'simulacion_mm1_paquetes.csv';
  a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000); // Libera el blob después de descargar.
});

$('compare').addEventListener('click', async () => {
  const b = $('compare');
  b.disabled = true;
  $('comparisonResults').textContent = 'Calculando los tres escenarios…';
  try {
    const c = config(); // Duración y semilla actuales.
    const params = new URLSearchParams({ duration: c.duration, seed: c.seed });
    const response = await fetch('/api/scenarios?' + params); // Comparación en servidor.
    const r = await response.json();
    if (!response.ok) throw Error('Error en comparación');
    // Tabla resumen: teoría y simulación para cada escenario.
    $('comparisonResults').innerHTML = `
      <table>
        <thead><tr><th>Escenario</th><th>λ</th><th>μ</th><th>ρ teórico</th><th>Lq teórico</th><th>Lq simulado</th><th>Wq teórico</th><th>Wq simulado</th></tr></thead>
        <tbody>${r.map(s => `<tr><td>${s.scenario}</td><td>${fmt(s.arrival_rate, 1)}</td><td>${fmt(s.service_rate, 1)}</td><td>${percent(s.theory.rho)}</td><td>${fmt(s.theory.Lq)}</td><td>${fmt(s.simulated.avg_queue)}</td><td>${fmt(s.theory.Wq)}</td><td>${fmt(s.simulated.mean_wait)}</td></tr>`).join('')}</tbody>
      </table>
      <p class="footnote">Comparación con T=${c.duration} y semilla=${c.seed}. Los valores simulados varían con la duración y la semilla; el escenario próximo a saturación requiere horizontes mayores para converger.</p>`;
  } catch (err) {
    $('comparisonResults').textContent = err.message; // Error visible para el usuario.
  } finally {
    b.disabled = false;
  }
});

window.addEventListener('resize', () => draw(true)); // Redibuja al cambiar el tamaño.
requestAnimationFrame(frame); // Inicia la animación.
loadSimulation(); // Carga una simulación al abrir la página.
