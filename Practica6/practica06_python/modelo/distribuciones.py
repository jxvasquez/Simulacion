# ============================================================
# MODELO - Funciones matematicas para calcular valores p
# ============================================================
# Se implementan "a mano" (sin scipy) para que Python y Java
# usen EXACTAMENTE las mismas formulas y den los mismos resultados.
# Responsabilidad unica: aqui solo hay calculos de probabilidad.
# ============================================================

import math


def log_gamma(x):
    """Logaritmo de la funcion Gamma (aproximacion de Lanczos)."""
    coeficientes = [76.18009172947146, -86.50532032941677,
                    24.01409824083091, -1.231739572450155,
                    0.1208650973866179e-2, -0.5395239384953e-5]
    y = x
    tmp = x + 5.5
    tmp -= (x + 0.5) * math.log(tmp)
    serie = 1.000000000190015
    for c in coeficientes:
        y += 1
        serie += c / y
    return -tmp + math.log(2.5066282746310005 * serie / x)


def _gamma_inferior_por_serie(a, x):
    """Gamma incompleta regularizada inferior P(a, x) usando una serie."""
    suma = 1.0 / a
    termino = suma
    n = a
    for _ in range(1000):
        n += 1
        termino *= x / n
        suma += termino
        if abs(termino) < abs(suma) * 1e-15:
            break
    return suma * math.exp(-x + a * math.log(x) - log_gamma(a))


def _gamma_superior_por_fraccion(a, x):
    """Gamma incompleta regularizada superior Q(a, x) usando fraccion continua."""
    minimo = 1e-300
    b = x + 1 - a
    c = 1.0 / minimo
    d = 1.0 / b
    h = d
    for i in range(1, 1000):
        an = -i * (i - a)
        b += 2
        d = an * d + b
        if abs(d) < minimo:
            d = minimo
        c = b + an / c
        if abs(c) < minimo:
            c = minimo
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1) < 1e-15:
            break
    return math.exp(-x + a * math.log(x) - log_gamma(a)) * h


def valor_p_chi_cuadrado(estadistico, grados_libertad):
    """Probabilidad de obtener un chi2 mayor o igual al calculado."""
    if estadistico <= 0:
        return 1.0
    a = grados_libertad / 2.0
    x = estadistico / 2.0
    # Se elige el metodo que converge mejor segun el valor de x
    if x < a + 1:
        return 1.0 - _gamma_inferior_por_serie(a, x)
    return _gamma_superior_por_fraccion(a, x)


def valor_p_kolmogorov(d, n):
    """Valor p aproximado de la prueba KS (distribucion de Kolmogorov)."""
    raiz_n = math.sqrt(n)
    # Correccion de Stephens para muestras finitas
    lam = (raiz_n + 0.12 + 0.11 / raiz_n) * d
    if lam < 1e-10:
        return 1.0
    suma = 0.0
    signo = 1.0
    for j in range(1, 101):
        termino = signo * math.exp(-2.0 * j * j * lam * lam)
        suma += termino
        if abs(termino) < 1e-12:
            break
        signo = -signo
    p = 2.0 * suma
    # El valor p siempre debe estar entre 0 y 1
    return max(0.0, min(1.0, p))
