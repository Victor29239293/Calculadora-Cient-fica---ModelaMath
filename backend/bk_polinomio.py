import numpy as np

def generar_coeficientes(grado: int) -> list[float]:

    return [0.0] * (grado + 1)


def evaluar_polinomio(coefs: list[float], x: float) -> float:

    return float(np.polyval(coefs, x))


def derivar_polinomio(coefs: list[float]) -> list[float]:

    return np.polyder(coefs).tolist()


def integrar_polinomio(coefs: list[float]) -> list[float]:

    return np.polyint(coefs).tolist()


def formatear_polinomio(coefs, latex=False):
    """
    Devuelve el polinomio como string normal o LaTeX.
    """
    grado = len(coefs) - 1
    terms = []
    for i, coef in enumerate(coefs):
        if coef == 0:
            continue
        power = grado - i

        # Formato para LaTeX
        if latex:
            # Coeficiente
            if coef == 1 and power > 0:
                coef_str = ""
            elif coef == -1 and power > 0:
                coef_str = "-"
            else:
                coef_str = f"{coef:g}"
            # Potencia
            if power == 0:
                term = f"{coef_str}"
            elif power == 1:
                term = f"{coef_str}x"
            else:
                term = f"{coef_str}x^{{{power}}}"
        else:
            # Formato normal
            if coef == 1 and power > 0:
                coef_str = ""
            elif coef == -1 and power > 0:
                coef_str = "-"
            else:
                coef_str = f"{coef:g}"
            if power == 0:
                term = f"{coef_str}"
            elif power == 1:
                term = f"{coef_str}x"
            else:
                term = f"{coef_str}x^{power}"

        terms.append(term)

    if not terms:
        return "0"

    # Unir términos con signos
    equation = terms[0]
    for term in terms[1:]:
        if term.startswith('-'):
            equation += f" {term}"
        else:
            equation += f" + {term}"

    return equation
