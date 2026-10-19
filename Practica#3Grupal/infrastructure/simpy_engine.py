"""Adaptador de SimPy: eventos y estadísticas observables de una sola estación FIFO."""
import random
import simpy
from domain.models import Config


class MM1Engine:
    """Motor SimPy para una cola M/M/1 con un servidor y disciplina FIFO."""

    def run(self, config: Config) -> dict:
        """Simula el sistema hasta el horizonte indicado en la configuración.

        Parámetros:
            config: Tasas λ y μ, duración total y semilla aleatoria.

        Devuelve:
            dict: Eventos, trabajos individuales y resumen de indicadores.
        """
        config.validate()
        rng = random.Random(config.seed)  # Generador aislado y reproducible.
        env = simpy.Environment()  # Reloj de eventos discretos.
        server = simpy.Resource(env, capacity=1)  # Un servidor; cola FIFO.
        events = []  # Historial de cambios de estado para la animación.
        arrived = 0  # Número acumulado de llegadas.
        completed = 0  # Número acumulado de servicios terminados.
        total_wait = 0.0  # Suma de esperas de los paquetes atendidos.
        total_system = 0.0  # Suma de permanencias en el sistema.
        total_service = 0.0  # Suma de tiempos de servicio.
        queue_area = 0.0  # Integral de la longitud de cola en el tiempo.
        system_area = 0.0  # Integral del número de paquetes en el sistema.
        busy_area = 0.0  # Tiempo acumulado con el servidor ocupado.
        previous_time = 0.0  # Último instante en que se actualizaron las áreas.
        previous_queue = 0  # Longitud de cola en el último evento.
        previous_system = 0  # Paquetes en el sistema en el último evento.
        previous_busy = 0  # 1 si el servidor estaba ocupado; 0 si estaba libre.
        wait_samples = []  # Esperas individuales para análisis adicional.
        jobs = []  # Registro de cada paquete atendido.

        def emit(kind, job_id=None, wait=None, service=None):
            """Registra un evento y actualiza las áreas antes de la instantánea.

            Parámetros:
                kind: Tipo de evento (`arrival`, `service_start`, `departure`, `end`).
                job_id: Identificador del paquete implicado, si aplica.
                wait: Espera acumulada por el paquete, si aplica.
                service: Tiempo de servicio sorteado, si aplica.
            """
            nonlocal queue_area, system_area, busy_area, previous_time
            nonlocal previous_queue, previous_system, previous_busy

            # El estado anterior permanece constante desde el último evento hasta ahora.
            dt = max(0.0, env.now - previous_time)  # Tiempo transcurrido entre eventos.
            queue_area += dt * previous_queue  # ∫ Q(t) dt para Lq.
            system_area += dt * previous_system  # ∫ L(t) dt para L.
            busy_area += dt * previous_busy  # ∫ ocupación(t) dt para ρ.
            previous_time = float(env.now)  # Nuevo instante de referencia.
            previous_queue = len(server.queue)  # Cola observable en este evento.
            previous_busy = int(server.count > 0)  # 1 si hay servicio activo.
            previous_system = arrived - completed  # Paquetes dentro del sistema.
            t = float(env.now)  # Tiempo actual en formato float.

            events.append({
                't': round(t, 7),  # Instante del evento.
                'type': kind,  # Tipo de transición.
                'id': job_id,  # Paquete asociado.
                'queue': previous_queue,  # Longitud instantánea de la cola.
                'system': previous_system,  # Paquetes en el sistema.
                'busy': previous_busy,  # Estado del servidor.
                'arrived': arrived,  # Llegadas acumuladas.
                'completed': completed,  # Salidas acumuladas.
                'mean_wait': total_wait / completed if completed else 0.0,  # Wq media.
                'mean_system': total_system / completed if completed else 0.0,  # W media.
                'mean_service': total_service / completed if completed else 0.0,  # S media.
                'avg_queue': queue_area / t if t else 0.0,  # Lq ponderada por tiempo.
                'avg_system': system_area / t if t else 0.0,  # L ponderada por tiempo.
                'utilization': busy_area / t if t else 0.0,  # ρ acumulada.
                'throughput': completed / t if t else 0.0,  # Salidas por unidad de tiempo.
                'wait': wait,  # Espera del paquete en este evento.
                'service': service,  # Servicio sorteado del paquete.
            })

        def customer(jid):
            """Ciclo de vida de un paquete: llegada, espera, servicio y salida."""
            nonlocal arrived, completed, total_wait, total_system, total_service

            arrival = env.now  # Instante de llegada del paquete.
            arrived += 1  # Contabiliza la llegada antes de solicitar el servidor.
            with server.request() as request:  # Entra en la cola FIFO del recurso.
                emit('arrival', jid)  # Registra la llegada a la cola.
                yield request  # Espera hasta que el servidor quede libre.
                wait = float(env.now - arrival)  # Wq = inicio de servicio - llegada.
                service = rng.expovariate(config.service_rate)  # Servicio ~ Exp(μ).
                emit('service_start', jid, wait=wait, service=service)  # Inicio.
                yield env.timeout(service)  # Ocupa el servidor durante el servicio.

            # Tras liberar el recurso, contar la salida sin dobles conteos.
            completed += 1  # Servicio terminado.
            total_wait += wait  # Acumula esperas para la media Wq.
            total_system += env.now - arrival  # Acumula permanencias para W.
            total_service += service  # Acumula servicios para la media S.
            wait_samples.append(wait)  # Guarda la muestra individual.
            jobs.append({
                'id': jid,  # Identificador del paquete.
                'arrival': arrival,  # Instante de llegada.
                'start': arrival + wait,  # Instante de inicio de servicio.
                'departure': float(env.now),  # Instante de salida.
                'wait': wait,  # Espera en cola.
                'service': service,  # Duración del servicio.
                'system': float(env.now - arrival),  # Tiempo total en el sistema.
            })
            emit('departure', jid, wait=wait, service=service)  # Registra la salida.

        def source():
            """Genera llegadas exponenciales hasta agotar el horizonte T."""
            jid = 0  # Identificador incremental de paquetes.
            while True:
                delay = rng.expovariate(config.arrival_rate)  # Tiempo entre llegadas ~ Exp(λ).
                if env.now + delay >= config.duration:  # No generar fuera del horizonte.
                    return
                yield env.timeout(delay)  # Avanza hasta la próxima llegada.
                jid += 1  # Asigna identificador al nuevo paquete.
                env.process(customer(jid))  # Lanza el ciclo de vida del paquete.

        env.process(source())  # Activa la fuente de llegadas.
        env.run(until=config.duration)  # Ejecuta la simulación hasta T.
        emit('end')  # Cierre explícito del registro de eventos.
        return {
            'events': events,  # Serie temporal de estados para la interfaz.
            'jobs': jobs,  # Detalle individual de cada paquete atendido.
            'summary': {  # Indicadores agregados de todo el horizonte.
                'arrived': arrived,  # Llegadas totales.
                'completed': completed,  # Servicios terminados.
                'pending': arrived - completed,  # Paquetes aún en el sistema.
                'mean_wait': total_wait / completed if completed else 0,  # Wq observada.
                'mean_system': total_system / completed if completed else 0,  # W observada.
                'mean_service': total_service / completed if completed else 0,  # S observada.
                'avg_queue': queue_area / config.duration,  # Lq = ∫Q dt / T.
                'avg_system': system_area / config.duration,  # L = ∫N dt / T.
                'utilization': busy_area / config.duration,  # ρ = tiempo ocupado / T.
                'throughput': completed / config.duration,  # X = salidas / T.
                'max_queue': max((e['queue'] for e in events), default=0),  # Máximo de cola.
                'wait_samples': wait_samples,  # Muestras individuales de espera.
            },
        }
