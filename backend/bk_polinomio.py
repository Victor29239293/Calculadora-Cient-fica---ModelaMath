import numpy as np

def generar_coeficientes(grado: int) -> list[float]:

    return [0.0] * (grado + 1)


def evaluar_polinomio(coefs: list[float], x: float) -> float:

    return float(np.polyval(coefs, x))


def derivar_polinomio(coefs: list[float]) -> list[float]:

    return np.polyder(coefs).tolist()


def integrar_polinomio(coefs: list[float]) -> list[float]:

    return np.polyint(coefs).tolist()


def formatear_polinomio(coefs: list[float]) -> str:

    cadena = "f(x) = "
    grado = len(coefs) - 1
    for i, coef in enumerate(coefs):
        if abs(coef) < 1e-8:
            continue
        signo = '+' if coef >= 0 and i != 0 else ''
        potencia = grado - i
        if potencia == 0:
            cadena += f"{signo}{coef:.2f}"
        elif potencia == 1:
            cadena += f"{signo}{coef:.2f}x"
        else:
            cadena += f"{signo}{coef:.2f}x^{potencia}"
    return cadena
