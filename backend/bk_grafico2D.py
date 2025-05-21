import numpy as np

def generar_eje_x(inicio: float, fin: float, num_puntos: int = 500) -> np.ndarray:

    if inicio >= fin:
        raise ValueError("El rango de X debe ser: inicio < fin.")
    return np.linspace(inicio, fin, num_puntos)


def evaluar_funcion(funcion_str: str, x: np.ndarray) -> np.ndarray:

    context = {
        "sin": np.sin,
        "cos": np.cos,
        "tan": np.tan,
        "exp": np.exp,
        "log": np.log,
        "sqrt": np.sqrt,
    }
    globals_dict = {"__builtins__": None}
    globals_dict.update(context)
    try:
        func = eval("lambda x: " + funcion_str, globals_dict)
    except Exception as e:
        raise ValueError(f"Error al parsear la función: {e}")
    try:
        y = func(x)
    except Exception as e:
        raise ValueError(f"Error al evaluar la función: {e}")
    return y