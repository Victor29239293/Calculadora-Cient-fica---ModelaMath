def guardar_resultado_metodo(metodo: str, f_str: str, x0: float, y0: float, x_final: float, n: int, xs: list, ys: list):
    """
    Etiqueta y almacena metadatos del resultado en el historial.
    :param metodo: Nombre del método (e.g., 'EULER').
    :param f_str: Cadena original de la función f(x,y).
    :param x0: Valor inicial de x.
    :param y0: Valor inicial de y.
    :param x_final: Valor final de x.
    :param n: Número de pasos.
    :param xs: Lista de valores x.
    :param ys: Lista de valores y.
    """
    # registra en el gestor de resultados
    from backend.Ecuaciones_Diferenciales.gestor_resultado import ResultadosEDOManager
    ResultadosEDOManager.guardar(metodo, xs, ys)
    # opcional: imprimir o loggear etiqueta en GUI
    print(f"Método {metodo}: f={f_str}, x0={x0}, y0={y0}, x_final={x_final}, pasos={n}")
