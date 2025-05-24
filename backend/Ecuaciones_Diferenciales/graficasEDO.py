# backend/Ecuaciones_Diferenciales/graficasEDO.py
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def mostrar_grafica(sol, condiciones, parent_frame, variable=None):

    if isinstance(sol, sp.Eq):
        expr = sol.rhs
    else:
        expr = sol

    x = variable if variable is not None else sp.symbols('x')

    constantes = [s for s in expr.free_symbols if s != x]
    if constantes:
        expr = expr.subs({c: 0 for c in constantes})

    f_num = sp.lambdify(x, expr, modules=["math"])

    if condiciones and len(condiciones) >= 1:
        x0 = condiciones[0]
        xf = x0 + 10
    else:
        x0, xf = 0, 10

    xs = np.linspace(x0, xf, 200)

    ys = [f_num(xi) for xi in xs]


    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(xs, ys, label="Solución Analítica")
    ax.set_xlabel("x")
    ax.set_ylabel("y(x)")
    ax.grid(True)
    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=parent_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True, pady=5)
