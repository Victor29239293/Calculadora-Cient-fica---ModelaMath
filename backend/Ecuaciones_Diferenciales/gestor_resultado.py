
class ResultadosEDOManager:
    """
    Administra los resultados de métodos numéricos para ecuaciones diferenciales ordinarias (EDO).
    Permite almacenar, filtrar y recuperar historiales de xs, ys y metadatos.
    """
    _historial = []  # lista de dicts: {"metodo": str, "xs": list, "ys": list, ...}

    @classmethod
    def guardar(cls, metodo: str, xs: list, ys: list):
        """
        Guarda un nuevo resultado en el historial.
        :param metodo: Nombre del método (e.g., 'Euler', 'RK4').
        :param xs: Lista de valores x.
        :param ys: Lista de valores y.
        """
        entry = {
            "metodo": metodo,
            "xs": list(xs),
            "ys": list(ys)
        }
        cls._historial.append(entry)

    @classmethod
    def obtener_todos(cls) -> list:
        """
        Retorna todo el historial de resultados.
        """
        return list(cls._historial)

    @classmethod
    def filtrar_por_metodo(cls, metodo: str) -> list:
        """
        Filtra el historial por nombre de método.
        :param metodo: Nombre del método a filtrar.
        :return: Lista de entradas que coinciden.
        """
        return [e for e in cls._historial if e["metodo"] == metodo]
