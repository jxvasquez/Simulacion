"""Adaptador de consola: muestra en texto las tablas de la interfaz web."""
from application.use_cases import compare
from domain.models import DEFAULT_DURATION, DEFAULT_SEED


def _fmt(value, digits=3):
    """Formatea un número con los decimales indicados; None se muestra como guion."""
    if value is None:
        return '—'  # Valor no definido (por ejemplo, sistema inestable).
    return f'{value:.{digits}f}'  # Redondeo fijo para alinear la tabla.


def _percent(value):
    """Convierte una proporción en un porcentaje con un decimal."""
    if value is None:
        return '—'  # Utilización no disponible.
    return f'{value * 100:.1f}%'  # De 0..1 a 0..100 %.


def _diff(theory, simulated):
    """Calcula la diferencia simulado − teórico para una métrica."""
    if theory is None or simulated is None:
        return '—'  # No se puede restar si falta algún valor.
    return _fmt(simulated - theory)  # Diferencia con el formato de la tabla.


def _print_table(headers, rows):
    """Imprime una tabla ASCII de ancho fijo.

    Parámetros:
        headers: Nombres de las columnas.
        rows: Filas con valores ya convertidos a texto.
    """
    widths = [len(header) for header in headers]  # Ancho inicial de cada columna.
    for row in rows:
        for index, cell in enumerate(row):
            widths[index] = max(widths[index], len(cell))  # Ajusta al valor más largo.
    border = '+' + '+'.join('-' * (width + 2) for width in widths) + '+'  # Línea separadora.
    print(border)
    print('| ' + ' | '.join(header.ljust(width) for header, width in zip(headers, widths)) + ' |')
    print(border)
    for row in rows:
        print('| ' + ' | '.join(cell.ljust(width) for cell, width in zip(row, widths)) + ' |')
    print(border)


def _print_metrics(scenario):
    """Imprime la comparación teórica/simulada de un escenario."""
    theory = scenario['theory']  # Indicadores analíticos.
    simulated = scenario['simulated']  # Indicadores medidos en SimPy.
    rows = [
        ['ρ · utilización', _fmt(theory['rho']), _fmt(simulated['utilization']),
         _diff(theory['rho'], simulated['utilization'])],  # Ocupación media.
        ['L · número medio en sistema', _fmt(theory['L']), _fmt(simulated['avg_system']),
         _diff(theory['L'], simulated['avg_system'])],  # Paquetes en el sistema.
        ['Lq · longitud media de cola', _fmt(theory['Lq']), _fmt(simulated['avg_queue']),
         _diff(theory['Lq'], simulated['avg_queue'])],  # Paquetes esperando.
        ['W · permanencia media', _fmt(theory['W']), _fmt(simulated['mean_system']),
         _diff(theory['W'], simulated['mean_system'])],  # Tiempo total.
        ['Wq · espera media', _fmt(theory['Wq']), _fmt(simulated['mean_wait']),
         _diff(theory['Wq'], simulated['mean_wait'])],  # Tiempo en cola.
    ]
    _print_table(['Indicador', 'Teórico', 'Simulado', 'Diferencia'], rows)


def _print_comparison(scenarios):
    """Imprime el resumen global de los tres escenarios."""
    rows = [
        [
            scenario['scenario'],  # Nombre del escenario.
            _fmt(scenario['arrival_rate'], 1),  # λ con un decimal.
            _fmt(scenario['service_rate'], 1),  # μ con un decimal.
            _percent(scenario['theory']['rho']),  # ρ teórico en porcentaje.
            _fmt(scenario['theory']['Lq']),  # Lq teórico.
            _fmt(scenario['simulated']['avg_queue']),  # Lq simulado.
            _fmt(scenario['theory']['Wq']),  # Wq teórico.
            _fmt(scenario['simulated']['mean_wait']),  # Wq simulado.
        ]
        for scenario in scenarios
    ]
    _print_table(
        ['Escenario', 'λ', 'μ', 'ρ teórico', 'Lq teórico', 'Lq simulado', 'Wq teórico', 'Wq simulado'],
        rows,
    )


def main():
    """Punto de entrada de la salida por consola."""
    scenarios = compare()  # Ejecuta los tres escenarios con T y semilla por defecto.
    print('QueueLab · tablas de simulación M/M/1')
    print(f'Escenarios de application/use_cases.py (SCENARIOS) · T={DEFAULT_DURATION:g}, semilla={DEFAULT_SEED}')
    print()
    for index, scenario in enumerate(scenarios, start=1):
        print(f"{index}. {scenario['scenario']} (λ={scenario['arrival_rate']}, μ={scenario['service_rate']})")
        _print_metrics(scenario)  # Detalle de teoría frente a simulación.
        print()
    print(f'Comparación global (T={DEFAULT_DURATION:g}, semilla={DEFAULT_SEED})')
    _print_comparison(scenarios)  # Resumen de los tres escenarios.
