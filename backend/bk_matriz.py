import numpy as np

def crear_matriz_aleatoria(filas: int,
                           columnas: int,
                           low: int = 0,
                           high: int = 10) -> np.ndarray:
    return np.random.randint(low, high, size=(filas, columnas))


def sumar(A: np.ndarray, B: np.ndarray) -> np.ndarray:

    if A.shape != B.shape:
        raise ValueError("Dimensiones no coinciden para la suma.")
    return A + B


def restar(A: np.ndarray, B: np.ndarray) -> np.ndarray:

    if A.shape != B.shape:
        raise ValueError("Dimensiones no coinciden para la resta.")
    return A - B


def multiplicar(A: np.ndarray, B: np.ndarray) -> np.ndarray:

    if A.shape[1] != B.shape[0]:
        raise ValueError("Columnas de A deben igualar filas de B para multiplicar.")
    return A @ B


def transpuesta(A: np.ndarray) -> np.ndarray:

    return A.T


def determinante(A: np.ndarray) -> float:

    if A.shape[0] != A.shape[1]:
        raise ValueError("Solo se puede calcular determinante de matriz cuadrada.")
    return float(np.linalg.det(A))


def inversa(A: np.ndarray) -> np.ndarray:

    if A.shape[0] != A.shape[1]:
        raise ValueError("Solo se puede calcular inversa de matriz cuadrada.")
    det = np.linalg.det(A)
    if np.isclose(det, 0):
        raise np.linalg.LinAlgError("La matriz es singular (determinante cero).")
    return np.linalg.inv(A)


def resolver_sistema(A: np.ndarray, b: np.ndarray) -> np.ndarray:

    if A.shape[0] != A.shape[1]:
        raise ValueError("A debe ser cuadrada para resolver el sistema.")
    if A.shape[0] != b.shape[0]:
        raise ValueError("La dimensión de b no coincide con A.")
    return np.linalg.solve(A, b)

