# backend/Ecuaciones_Diferenciales/graficasEDO.py
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def mostrar_grafica(sol, condiciones, parent_frame, variable=None):
    """
    Grafica la solución analítica de una EDO, sustituyendo
    constantes que queden (C1, C2, ...) a 0 para que Matplotlib
    sólo reciba floats.
    """
    # 1) Extraer la expresión y(x)
    if isinstance(sol, sp.Eq):
        expr = sol.rhs
    else:
        expr = sol

    # 2) Determinar símbolo independiente
    x = variable if variable is not None else sp.symbols('x')

    # 3) Sustituir constantes de integración por 0
    constantes = [s for s in expr.free_symbols if s != x]
    if constantes:
        expr = expr.subs({c: 0 for c in constantes})

    # 4) Construir función numérica
    f_num = sp.lambdify(x, expr, modules=["math"])

    # 5) Dominio de graficación
    if condiciones and len(condiciones) >= 1:
        x0 = condiciones[0]
        xf = x0 + 10
    else:
        x0, xf = 0, 10

    xs = np.linspace(x0, xf, 200)
    # 6) Evaluar punto a punto, garantizando floats
    ys = [f_num(xi) for xi in xs]

    # 7) Dibujar con Matplotlib
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(xs, ys, label="Solución Analítica")
    ax.set_xlabel("x")
    ax.set_ylabel("y(x)")
    ax.grid(True)
    ax.legend()

    # 8) Insertar en Tkinter
    canvas = FigureCanvasTkAgg(fig, master=parent_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True, pady=5)
