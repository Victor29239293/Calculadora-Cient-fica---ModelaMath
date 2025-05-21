import numpy as np

def generar_vector_aleatorio(dim: int, low: int = -10, high: int = 10) -> np.ndarray:

    if dim <= 0:
        raise ValueError("La dimensión debe ser mayor a 0.")
    return np.random.randint(low, high, size=dim)


def sumar(a: np.ndarray, b: np.ndarray) -> np.ndarray:

    if a.shape != b.shape:
        raise ValueError("Los vectores deben tener la misma dimensión para sumar.")
    return a + b


def restar(a: np.ndarray, b: np.ndarray) -> np.ndarray:

    if a.shape != b.shape:
        raise ValueError("Los vectores deben tener la misma dimensión para restar.")
    return a - b


def producto_punto(a: np.ndarray, b: np.ndarray) -> float:

    if a.shape != b.shape:
        raise ValueError("Los vectores deben tener la misma dimensión para calcular el producto punto.")
    return float(np.dot(a, b))


def producto_cruzado(a: np.ndarray, b: np.ndarray) -> np.ndarray:

    if a.shape != (3,) or b.shape != (3,):
        raise ValueError("El producto cruzado solo está definido para vectores de dimensión 3.")
    return np.cross(a, b)


def magnitud(a: np.ndarray) -> float:

    if a.ndim != 1:
        raise ValueError("La magnitud solo se calcula para vectores unidimensionales.")
    return float(np.linalg.norm(a))
