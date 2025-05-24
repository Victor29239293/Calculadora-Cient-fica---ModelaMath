import re
import sympy as sp
from sympy import Function, symbols, Derivative, Eq
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application
)
from math import isfinite


_transformations = standard_transformations + (implicit_multiplication_application,)


def euler_method(f_str, x0, y0, h, n):
    f_expr = sp.sympify(f_str)
    f = sp.lambdify(("x", "y"), f_expr, modules=["math", "sympy"])
    xs, ys = [x0], [y0]
    for _ in range(n):
        xi, yi = xs[-1], ys[-1]
        yi_new = yi + h * f(xi, yi)
        xs.append(xi + h)
        ys.append(yi_new)
    return xs, ys


def heun_method(f_str, x0, y0, h, n):
    f_expr = sp.sympify(f_str)
    f = sp.lambdify(("x", "y"), f_expr, modules=["math", "sympy"])
    xs, ys = [x0], [y0]
    for _ in range(n):
        xi, yi = xs[-1], ys[-1]
        y_pred = yi + h * f(xi, yi)
        yi_new = yi + h * (f(xi, yi) + f(xi + h, y_pred)) / 2
        xs.append(xi + h)
        ys.append(yi_new)
    return xs, ys


def rk4_method(f_str, x0, y0, h, n):
    f_expr = sp.sympify(f_str)
    f = sp.lambdify(("x", "y"), f_expr, modules=["math", "sympy"])
    xs, ys = [x0], [y0]
    for _ in range(n):
        xi, yi = xs[-1], ys[-1]
        k1 = h * f(xi, yi)
        k2 = h * f(xi + h/2, yi + k1/2)
        k3 = h * f(xi + h/2, yi + k2/2)
        k4 = h * f(xi + h,   yi + k3)
        yi_new = yi + (k1 + 2*k2 + 2*k3 + k4) / 6
        xs.append(xi + h)
        ys.append(yi_new)
    return xs, ys


def taylor2_method(f_str, df_str, x0, y0, xf, n):
    f_expr  = sp.sympify(f_str)
    df_expr = sp.sympify(df_str)
    f  = sp.lambdify(("x", "y"), f_expr,  modules=["math","sympy"])
    df = sp.lambdify(("x", "y"), df_expr, modules=["math","sympy"])
    h = (xf - x0) / n
    xs, ys = [x0], [y0]
    for _ in range(n):
        xi, yi = xs[-1], ys[-1]
        yi_new = yi + h*f(xi, yi) + (h**2/2)*df(xi, yi)
        xs.append(xi + h)
        ys.append(yi_new)
    return xs, ys



def analytic_solver(equation_str: str, condiciones=None):

    x = symbols('x')
    y = Function('y')

    # 1) reemplazar primas
    s = equation_str.strip()
    s = re.sub(r"y''",      r"Derivative(y(x),(x,2))", s)
    s = re.sub(r"y'",       r"Derivative(y(x),x)",     s)

    s = re.sub(r"(?<!\w)y(?!\()", "y(x)", s)


    local_dict = {'x': x, 'y': y, 'Derivative': Derivative}
    try:
        if '=' in s:
            lhs, rhs = s.split('=', 1)
            lhs_e = parse_expr(lhs,  local_dict=local_dict, transformations=_transformations)
            rhs_e = parse_expr(rhs,  local_dict=local_dict, transformations=_transformations)
            eq = Eq(lhs_e, rhs_e)
        else:
            expr = parse_expr(s, local_dict=local_dict, transformations=_transformations)
            eq = Eq(expr, 0)
    except Exception as err:
        raise ValueError(f"Error parseando la ecuación: {err}")

    ics = {}
    if condiciones:
        x0 = condiciones[0]
        if len(condiciones) >= 2:
            ics[x0] = condiciones[1] 
        if len(condiciones) == 3:
            ics[ Derivative(y(x), x).subs(x, x0) ] = condiciones[2]  


    try:
        sol = sp.dsolve(eq, y(x), ics=ics) if ics else sp.dsolve(eq, y(x))
        return sol
    except Exception as err:
        raise ValueError(f"Error al resolver analíticamente: {err}")