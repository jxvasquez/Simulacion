"""Servidor HTTP local (stdlib); adaptador web que delega al caso de uso."""
import json
import mimetypes
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import parse_qs, urlparse
from application.use_cases import compare, simulate
from domain.models import Config, DEFAULT_DURATION, DEFAULT_SEED

STATIC = Path(__file__).parent / 'static'  # Directorio de HTML, CSS y JavaScript.


class Handler(BaseHTTPRequestHandler):
    """Atiende la API JSON y sirve los archivos estáticos de la interfaz."""

    def json(self, obj, code=200):
        """Envía una respuesta JSON con el código HTTP indicado.

        Parámetros:
            obj: Objeto serializable a JSON.
            code: Código de estado HTTP de la respuesta.
        """
        data = json.dumps(obj, ensure_ascii=False, allow_nan=False).encode('utf8')
        self.send_response(code)  # Código HTTP de la respuesta.
        self.send_header('Content-Type', 'application/json; charset=utf-8')  # Tipo JSON.
        self.send_header('Content-Length', str(len(data)))  # Longitud exacta del cuerpo.
        self.end_headers()  # Cierra las cabeceras.
        self.wfile.write(data)  # Escribe el cuerpo JSON.

    def do_POST(self):
        """Procesa `/api/simulate` con los parámetros del formulario."""
        if urlparse(self.path).path != '/api/simulate':  # Solo existe esta ruta POST.
            return self.json({'error': 'Ruta no encontrada'}, 404)
        try:
            size = int(self.headers.get('Content-Length', '0'))  # Tamaño declarado.
            if size <= 0 or size > 65536:  # Evita cuerpos vacíos o demasiado grandes.
                raise ValueError('Tamaño de solicitud inválido')
            data = json.loads(self.rfile.read(size))  # Lee y decodifica el JSON.
            cfg = Config(
                float(data['arrival_rate']),  # λ enviada por el navegador.
                float(data['service_rate']),  # μ enviada por el navegador.
                float(data['duration']),  # Horizonte T del formulario.
                int(data['seed']),  # Semilla del formulario.
            )
            return self.json(simulate(cfg))  # Ejecuta el caso de uso.
        except (KeyError, ValueError, TypeError) as exc:
            return self.json({'error': str(exc)}, 400)  # Datos inválidos o incompletos.

    def do_GET(self):
        """Responde a la comparación de escenarios y a los archivos estáticos."""
        url = urlparse(self.path)
        route = url.path  # Ruta solicitada, sin query string.
        if route == '/api/scenarios':
            try:
                query = parse_qs(url.query)  # Parámetros duration y seed.
                duration = float(query.get('duration', [DEFAULT_DURATION])[0])
                seed = int(query.get('seed', [DEFAULT_SEED])[0])
                return self.json(compare(duration, seed))  # Compara los tres escenarios.
            except (ValueError, TypeError) as exc:
                return self.json({'error': str(exc)}, 400)  # Query inválida.
        if route == '/':  # La raíz sirve la página principal.
            route = '/index.html'
        path = (STATIC / route.lstrip('/')).resolve()  # Ruta absoluta del recurso.
        if not path.is_relative_to(STATIC.resolve()) or not path.is_file():
            self.send_error(404)  # Evita salir del directorio estático.
            return
        data = path.read_bytes()  # Contenido binario del archivo.
        self.send_response(200)  # Recurso encontrado.
        self.send_header('Content-Type', mimetypes.guess_type(path.name)[0] or 'application/octet-stream')
        self.send_header('Content-Length', str(len(data)))  # Longitud del recurso.
        self.end_headers()  # Cierra las cabeceras.
        self.wfile.write(data)  # Envía el archivo al navegador.


def serve(host='127.0.0.1', port=8501):
    """Arranca el servidor HTTP local en host:port.

    Parámetros:
        host: Interfaz de escucha; por defecto solo local.
        port: Puerto HTTP; por defecto 8501.
    """
    print(f'Simulador disponible en http://{host}:{port}')
    ThreadingHTTPServer((host, port), Handler).serve_forever()  # Atiende peticiones.
