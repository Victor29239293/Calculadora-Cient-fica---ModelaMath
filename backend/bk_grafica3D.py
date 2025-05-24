import numpy as np

def generar_malla(x0: float, x1: float, y0: float, y1: float, num: int = 150) -> tuple[np.ndarray, np.ndarray]:

    if x0 >= x1 or y0 >= y1:
        raise ValueError("Los rangos deben cumplir: Xmin < Xmax y Ymin < Ymax.")
    x = np.linspace(x0, x1, num)
    y = np.linspace(y0, y1, num)
    return np.meshgrid(x, y)


def evaluar_funcion_3d(func_str: str, X: np.ndarray, Y: np.ndarray) -> np.ndarray:

    context = {
        "sin": np.sin,
        "cos": np.cos,
        "tan": np.tan,
        "exp": np.exp,
        "log": np.log,
        "sqrt": np.sqrt,
        "abs": np.abs,
    }
    globals_dict = {"__builtins__": None}
    globals_dict.update(context)
    try:
        func = eval("lambda x, y: " + func_str, globals_dict)
    except Exception as e:
        raise ValueError(f"Error al parsear la función: {e}")
    try:
        Z = func(X, Y)
    except Exception as e:
        raise ValueError(f"Error al evaluar la función: {e}")
    return Z
