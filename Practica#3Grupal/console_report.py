"""Entrada de consola: tablas y generación de gráficos sin abrir la web."""
from analysis.barras import ensure_scenario_charts
from presentation.console import main as print_tables


def main():
    """Imprime las tablas y genera los gráficos que falten."""
    print_tables()  # Salida de consola con teoría y simulación.
    created = ensure_scenario_charts()  # Solo crea PNG/CSV ausentes.
    if created:
        print(f'Archivos de análisis generados en {created[0].parent}:')
        for path in created:
            print(f'  {path.name}')  # Muestra cada archivo nuevo.


if __name__ == '__main__':
    main()
