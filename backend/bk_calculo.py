import sympy as sp
from sympy import simplify, diff, integrate, sympify
from sympy.abc import x
import numpy as np


def derivar_funcion_pasos(expr_str: str) -> tuple[sp.Expr, str]:
    """
    Devuelve la derivada simbólica y un resumen de pasos.
    """
    funcion = sympify(expr_str)
    derivada = diff(funcion, x)
    pasos = (
        f"🧮 Función original: {funcion}\n"
        f"📈 Derivada simbólica: {derivada}\n"
        "(Simplificado automáticamente)"
    )
    return simplify(derivada), pasos


def integrar_funcion(expr_str: str, a: str = None, b: str = None) -> tuple[str, str]:
    """
    Realiza la integral indefinida o definida y devuelve resultado y pasos.
    """
    funcion = sympify(expr_str)
    reporte = f"🧮 Función original: {funcion}\n"
    if a is not None and b is not None:
        a_sym, b_sym = sympify(a), sympify(b)
        integral_def = integrate(funcion, (x, a_sym, b_sym))
        resultado = f"∫_{{{a}}}^{{{b}}} {funcion} dx = {simplify(integral_def)}"
        reporte += f"📏 Integral definida de {funcion} entre {a} y {b}: {integral_def}\n"
    else:
        integral_inf = integrate(funcion, x)
        resultado = f"∫ {funcion} dx = {simplify(integral_inf)} + C"
        reporte += f"📏 Integral indefinida: {integral_inf} + C\n"
    return resultado, reporte


def generar_datos_grafica(expr_str: str,
                           x_min: float = -10,
                           x_max: float = 10,
                           num_puntos: int = 400) -> tuple[np.ndarray, np.ndarray]:
    """
    Genera puntos (x, y) para graficar la función simbólica.
    """
    funcion = sympify(expr_str)
    f_lamb = sp.lambdify(x, funcion, modules=["numpy"])
    xs = np.linspace(x_min, x_max, num_puntos)
    ys = f_lamb(xs)
    return xs, ys