"""Entrada principal: informe por consola y servidor web local."""
from console_report import main as run_console_report  # Tablas + gráficos faltantes.
from presentation.server import serve  # Interfaz HTTP.

if __name__ == '__main__':
    run_console_report()  # Muestra resultados antes de abrir la web.
    serve()  # Inicia la aplicación en 127.0.0.1:8501.
