"""Genera los PNG de barras por escenario que falten en analysis/output."""
import math
from pathlib import Path

from application.use_cases import SCENARIOS, compare
from domain.models import DEFAULT_DURATION, DEFAULT_SEED

OUTPUT_DIR = Path(__file__).resolve().parent / 'output' / 'barras_escenarios'  # Destino de PNG/CSV.
WIDTH, HEIGHT = 1650, 660  # Tamaño fijo de cada imagen en píxeles.

THEORY_COLOR = '#30475e'  # Azul oscuro para las barras teóricas.
SIMULATED_COLOR = '#2fcbd0'  # Cian para las barras simuladas.
GRID_COLOR = '#dfe4ea'  # Líneas de referencia del gráfico.
TEXT_COLOR = '#1f2937'  # Texto principal.
MUTED_COLOR = '#6b7280'  # Etiquetas secundarias.
BACKGROUND = '#ffffff'  # Fondo blanco de las imágenes.

LEFT_METRIC = ('Utilización ρ', 'rho', 'utilization')  # (etiqueta, clave teórica, clave simulada).
RIGHT_METRICS = (
    ('L · sistema', 'L', 'avg_system'),  # Paquetes medios en el sistema.
    ('Lq · cola', 'Lq', 'avg_queue'),  # Paquetes medios en cola.
    ('W · permanencia', 'W', 'mean_system'),  # Tiempo medio en el sistema.
    ('Wq · espera', 'Wq', 'mean_wait'),  # Tiempo medio de espera.
)
ALL_METRICS = (LEFT_METRIC,) + RIGHT_METRICS  # Métricas incluidas en el CSV.

FONT_REGULAR = (  # Rutas candidatas para la fuente normal.
    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
    '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
    'C:/Windows/Fonts/arial.ttf',
    '/System/Library/Fonts/Supplemental/Arial.ttf',
)
FONT_BOLD = (  # Rutas candidatas para la fuente en negrita.
    '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
    '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf',
    'C:/Windows/Fonts/arialbd.ttf',
    '/System/Library/Fonts/Supplemental/Arial Bold.ttf',
)


def _load_pillow():
    """Importa Pillow solo cuando hace falta generar imágenes.

    Devuelve:
        tuple: Clases Image, ImageDraw e ImageFont de Pillow.

    Lanza:
        RuntimeError: Si Pillow no está instalado.
    """
    try:
        from PIL import Image, ImageDraw, ImageFont  # Dependencia opcional.
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            'Pillow es necesario para generar los gráficos; instala requirements.txt.'
        ) from exc
    return Image, ImageDraw, ImageFont


def _font(ImageFont, size, bold=False):
    """Busca una fuente del sistema y devuelve la primera disponible.

    Parámetros:
        ImageFont: Módulo ImageFont de Pillow.
        size: Tamaño en píxeles.
        bold: Si es True, prioriza las fuentes en negrita.
    """
    candidates = FONT_BOLD + FONT_REGULAR if bold else FONT_REGULAR  # Orden de búsqueda.
    for name in candidates:
        if Path(name).is_file():  # Solo intenta rutas existentes.
            try:
                return ImageFont.truetype(name, size)  # Carga la fuente TrueType.
            except OSError:
                pass  # Si falla, prueba la siguiente ruta.
    return ImageFont.load_default()  # Último recurso: fuente básica de Pillow.


def _slug(text):
    """Convierte un nombre de escenario en un fragmento seguro para el archivo."""
    replacements = str.maketrans('áéíóúüñ', 'aeiouun')  # Elimina tildes y diéresis.
    return '_'.join(text.lower().translate(replacements).replace('·', '').split())


def _chart_path(output_dir, index, name):
    """Construye la ruta `escenario_N_nombre.png` para un escenario."""
    return output_dir / f'escenario_{index}_{_slug(name)}.png'  # Nombre estable y legible.


def _nice_max(value):
    """Redondea el máximo del eje a 1, 2, 2.5, 5 o 10 por una potencia de diez."""
    if value <= 0:
        return 1  # Evita divisiones por cero en escalas vacías.
    exponent = math.floor(math.log10(value))  # Potencia de diez del valor.
    base = 10 ** exponent  # Escala base: 0.1, 1, 10, etc.
    for factor in (1, 2, 2.5, 5, 10):
        candidate = factor * base  # Siguiente límite "bonito".
        if value <= candidate:
            return candidate  # Primer límite que contiene el valor.
    return 10 * base  # Cierre defensivo; normalmente no se alcanza.


def _center_text(draw, center_x, y, text, font, fill):
    """Dibuja texto centrado horizontalmente en `center_x`."""
    box = draw.textbbox((0, 0), text, font=font)  # Caja real del texto.
    draw.text((center_x - (box[2] - box[0]) / 2, y), text, font=font, fill=fill)


def _right_text(draw, right_x, center_y, text, font, fill):
    """Dibuja texto alineado a la derecha y centrado verticalmente."""
    box = draw.textbbox((0, 0), text, font=font)  # Dimensiones del texto.
    draw.text((right_x - (box[2] - box[0]), center_y - (box[3] - box[1]) / 2),
              text, font=font, fill=fill)


def _value_text(value):
    """Formatea una métrica para mostrarla encima de su barra."""
    return '—' if value is None else f'{value:.3f}'  # Tres decimales o guion.


def _pair(scenario, metric):
    """Extrae el par (teórico, simulado) de una métrica de un escenario."""
    _, theory_key, simulated_key = metric  # La etiqueta no se usa aquí.
    return scenario['theory'][theory_key], scenario['simulated'][simulated_key]


def _draw_axes(draw, plot, maximum, font):
    """Dibuja la cuadrícula horizontal y las etiquetas del eje Y.

    Parámetros:
        draw: Lienzo ImageDraw.
        plot: Rectángulo (x0, y0, x1, y1) del área de datos.
        maximum: Valor superior del eje Y.
        font: Fuente para las etiquetas.
    """
    x0, y0, x1, y1 = plot  # Límites del área de dibujo.
    for step in range(5):
        value = maximum * step / 4  # Cinco marcas, de 0 a maximum.
        y = y1 - (y1 - y0) * step / 4  # Interpolación lineal en píxeles.
        draw.line((x0, y, x1, y), fill=GRID_COLOR, width=1)  # Línea horizontal.
        _right_text(draw, x0 - 10, y, f'{value:g}', font, MUTED_COLOR)  # Etiqueta del eje.
    draw.line((x0, y0, x0, y1), fill=GRID_COLOR, width=1)  # Eje Y.


def _draw_left_panel(draw, scenario, ImageFont):
    """Dibuja el panel izquierdo con la utilización ρ."""
    x0, y0, x1, y1 = 70, 120, 420, 600  # Marco del panel.
    plot = (120, 160, 395, 535)  # Zona útil para las barras.
    title_font = _font(ImageFont, 20)  # Título del panel.
    axis_font = _font(ImageFont, 14)  # Marcas del eje.
    value_font = _font(ImageFont, 14)  # Valores sobre las barras.
    label_font = _font(ImageFont, 16)  # Leyendas inferiores.
    _center_text(draw, (x0 + x1) / 2, 85, LEFT_METRIC[0], title_font, TEXT_COLOR)
    theory, simulated = _pair(scenario, LEFT_METRIC)  # ρ teórico y simulado.
    maximum = _nice_max(max(value for value in (theory, simulated, 0.01) if value is not None))
    _draw_axes(draw, plot, maximum, axis_font)  # Escala vertical común.
    center = (plot[0] + plot[2]) / 2  # Centro de la pareja de barras.
    bar_width, gap = 50, 24  # Ancho de barra y separación entre ambas.
    for value, color, label, side in (
        (theory, THEORY_COLOR, 'Teórico', -1),  # Barra izquierda.
        (simulated, SIMULATED_COLOR, 'Simulado', 1),  # Barra derecha.
    ):
        left = center - bar_width - gap / 2 if side < 0 else center + gap / 2
        height = 0 if value is None else (value / maximum) * (plot[3] - plot[1])  # Altura proporcional.
        draw.rectangle((left, plot[3] - height, left + bar_width, plot[3]), fill=color)
        _center_text(draw, left + bar_width / 2, plot[3] - height - 22,
                     _value_text(value), value_font, TEXT_COLOR)  # Valor numérico.
        _center_text(draw, left + bar_width / 2, plot[3] + 12, label, label_font, MUTED_COLOR)


def _draw_right_panel(draw, scenario, ImageFont):
    """Dibuja el panel derecho con L, Lq, W y Wq."""
    x0, y0, x1, y1 = 490, 120, 1580, 600  # Marco del panel.
    plot = (560, 160, 1560, 535)  # Zona útil para las barras.
    title_font = _font(ImageFont, 20)  # Título del panel.
    axis_font = _font(ImageFont, 14)  # Marcas del eje.
    value_font = _font(ImageFont, 14)  # Valores sobre las barras.
    label_font = _font(ImageFont, 16)  # Etiquetas de cada grupo.
    legend_font = _font(ImageFont, 15)  # Leyenda teórico/simulado.
    _center_text(draw, (x0 + x1) / 2, 85, 'Métricas de cola y tiempos', title_font, TEXT_COLOR)
    pairs = [_pair(scenario, metric) for metric in RIGHT_METRICS]  # Pares teóricos/simulados.
    maximum = _nice_max(max((value for pair in pairs for value in pair if value is not None),
                            default=0.01))  # Máximo común para comparar escalas.
    _draw_axes(draw, plot, maximum, axis_font)  # Cuadrícula y eje Y.
    group_width = (plot[2] - plot[0]) / len(RIGHT_METRICS)  # Ancho reservado a cada métrica.
    bar_width, gap = 38, 8  # Tamaño de barra y separación dentro del grupo.
    for index, (metric, (theory, simulated)) in enumerate(zip(RIGHT_METRICS, pairs)):
        center = plot[0] + group_width * (index + 0.5)  # Centro del grupo actual.
        for value, color, side in (
            (theory, THEORY_COLOR, -1),  # Barra teórica.
            (simulated, SIMULATED_COLOR, 1),  # Barra simulada.
        ):
            left = center - bar_width - gap / 2 if side < 0 else center + gap / 2
            height = 0 if value is None else (value / maximum) * (plot[3] - plot[1])  # Altura.
            draw.rectangle((left, plot[3] - height, left + bar_width, plot[3]), fill=color)
            _center_text(draw, left + bar_width / 2, plot[3] - height - 20,
                         _value_text(value), value_font, TEXT_COLOR)  # Valor numérico.
        _center_text(draw, center, plot[3] + 12, metric[0], label_font, MUTED_COLOR)  # Etiqueta.

    legend_x, legend_y = 1320, 92  # Posición de la leyenda.
    draw.rectangle((legend_x, legend_y, legend_x + 14, legend_y + 14), fill=THEORY_COLOR)
    draw.text((legend_x + 20, legend_y - 1), 'Teórico', font=legend_font, fill=TEXT_COLOR)
    draw.rectangle((legend_x + 100, legend_y, legend_x + 114, legend_y + 14), fill=SIMULATED_COLOR)
    draw.text((legend_x + 120, legend_y - 1), 'Simulado', font=legend_font, fill=TEXT_COLOR)


def _draw_scenario(Image, ImageDraw, ImageFont, scenario, path):
    """Compone una imagen completa para un escenario y la guarda en `path`."""
    image = Image.new('RGB', (WIDTH, HEIGHT), BACKGROUND)  # Lienzo blanco.
    draw = ImageDraw.Draw(image)  # Objeto para dibujar formas y texto.
    title_font = _font(ImageFont, 28, bold=True)  # Fuente del título.
    title = (f"{scenario['scenario']} — λ={scenario['arrival_rate']:g}, "
             f"μ={scenario['service_rate']:g}, T={DEFAULT_DURATION:g}, semilla={DEFAULT_SEED}")
    _center_text(draw, WIDTH / 2, 34, title, title_font, TEXT_COLOR)  # Título superior.
    _draw_left_panel(draw, scenario, ImageFont)  # Panel de utilización.
    _draw_right_panel(draw, scenario, ImageFont)  # Panel de colas y tiempos.
    image.save(path)  # Guarda el PNG en disco.


def _write_csv(path, scenarios):
    """Escribe el resumen teoría/simulación en CSV compatible con Excel."""
    lines = ['Escenario;Indicador;Teorico;Simulado;Error_rel_pct']  # Cabecera del CSV.
    for scenario in scenarios:
        for label, theory_key, simulated_key in ALL_METRICS:
            theory = scenario['theory'][theory_key]  # Valor analítico.
            simulated = scenario['simulated'][simulated_key]  # Valor simulado.
            # Error relativo porcentual: (simulado − teórico) / teórico × 100.
            relative = 0.0 if theory in (None, 0) or simulated is None else (
                (simulated - theory) / theory * 100
            )
            theory_text = '' if theory is None else f'{theory:.4f}'  # Celda vacía si no existe.
            simulated_text = '' if simulated is None else f'{simulated:.4f}'
            lines.append(f"{scenario['scenario']};{label};{theory_text};{simulated_text};{relative:+.2f}")
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')  # Guarda con salto final.


def ensure_scenario_charts(output_dir=None):
    """Genera solo los archivos que falten y devuelve las rutas creadas.

    Parámetros:
        output_dir: Directorio alternativo; por defecto usa OUTPUT_DIR.

    Devuelve:
        list[Path]: Archivos PNG/CSV creados durante esta llamada.
    """
    output = Path(output_dir) if output_dir is not None else OUTPUT_DIR  # Destino efectivo.
    output.mkdir(parents=True, exist_ok=True)  # Crea la carpeta si no existe.
    expected = [
        (_chart_path(output, index, scenario['name']), scenario['name'])
        for index, scenario in enumerate(SCENARIOS, start=1)  # Un PNG por escenario.
    ]
    missing = [(path, name) for path, name in expected if not path.exists()]  # Solo faltantes.
    csv_path = output / 'teoria_vs_sim.csv'  # Resumen tabular.
    if not missing and csv_path.exists():
        return []  # Nada que generar: se conservan los archivos existentes.

    scenarios = compare()  # Calcula los datos una sola vez para PNG y CSV.
    created = []  # Rutas generadas en esta ejecución.
    if missing:
        Image, ImageDraw, ImageFont = _load_pillow()  # Carga Pillow solo si hace falta.
        by_name = {scenario['scenario']: scenario for scenario in scenarios}  # Búsqueda por nombre.
        for path, name in missing:
            _draw_scenario(Image, ImageDraw, ImageFont, by_name[name], path)  # Dibuja el PNG.
            created.append(path)
    if not csv_path.exists():
        _write_csv(csv_path, scenarios)  # Crea el CSV solo si falta.
        created.append(csv_path)
    return created


def main():
    """Genera los archivos faltantes desde la línea de comandos."""
    created = ensure_scenario_charts()  # Aplica la generación condicional.
    if created:
        print('Archivos generados:')
        for path in created:
            print(f'  {path}')
    else:
        print(f'Los gráficos de barras ya existen en {OUTPUT_DIR}')


if __name__ == '__main__':
    main()
