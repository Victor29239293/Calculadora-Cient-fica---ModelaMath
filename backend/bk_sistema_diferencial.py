import numpy as np
try:
    from scipy.linalg import expm
except ImportError:
    expm = None


def _parse_coeffs(eq_str):
    s = eq_str.replace(" ", "").replace("-", "+-")
    terms = s.split("+")
    ax = ay = 0.0
    for term in terms:
        if term.endswith("*x"):
            ax = float(term.replace("*x", ""))
        elif term.endswith("*y"):
            ay = float(term.replace("*y", ""))
    return ax, ay

def solve_system(f1_str, f2_str, x0, y0, T, h, metodo):
    def dxdt(x, y): return eval(f1_str)
    def dydt(x, y): return eval(f2_str)

    t_vals = np.arange(0, T + h, h)
    x_vals = [x0]
    y_vals = [y0]


    if metodo == "Analítico":
        if expm is None:
            raise ImportError("Método analítico requiere 'scipy'.")
        a, b = _parse_coeffs(f1_str)
        c, d = _parse_coeffs(f2_str)
        A = np.array([[a, b], [c, d]])
        x_vals, y_vals = [], []
        x0_vec = np.array([[x0], [y0]])
        for t in t_vals:
            sol = expm(A * t).dot(x0_vec)
            x_vals.append(float(sol[0]))
            y_vals.append(float(sol[1]))
        return t_vals, x_vals, y_vals

    for i in range(1, len(t_vals)):
        xp, yp = x_vals[-1], y_vals[-1]
        if metodo == "Euler":
            xn = xp + h * dxdt(xp, yp)
            yn = yp + h * dydt(xp, yp)

        elif metodo == "Runge-Kutta 4":
            k1x = h * dxdt(xp, yp)
            k1y = h * dydt(xp, yp)
            k2x = h * dxdt(xp + k1x/2, yp + k1y/2)
            k2y = h * dydt(xp + k1x/2, yp + k1y/2)
            k3x = h * dxdt(xp + k2x/2, yp + k2y/2)
            k3y = h * dydt(xp + k2x/2, yp + k2y/2)
            k4x = h * dxdt(xp + k3x, yp + k3y)
            k4y = h * dydt(xp + k3x, yp + k3y)
            xn = xp + (k1x + 2*k2x + 2*k3x + k4x) / 6
            yn = yp + (k1y + 2*k2y + 2*k3y + k4y) / 6

        else:
            raise ValueError(f"Método no soportado: {metodo}")

        x_vals.append(xn)
        y_vals.append(yn)

    return t_vals, x_vals, y_vals


def eigen_decomposition(f1_str, f2_str):
    a, b = _parse_coeffs(f1_str)
    c, d = _parse_coeffs(f2_str)
    A = np.array([[a, b], [c, d]])
    vals, vecs = np.linalg.eig(A)
    return vals, vecs
