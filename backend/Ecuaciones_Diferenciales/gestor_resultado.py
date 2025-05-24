
class ResultadosEDOManager:

    _historial = []  

    @classmethod
    def guardar(cls, metodo: str, xs: list, ys: list):

        entry = {
            "metodo": metodo,
            "xs": list(xs),
            "ys": list(ys)
        }
        cls._historial.append(entry)

    @classmethod
    def obtener_todos(cls) -> list:

        return list(cls._historial)

    @classmethod
    def filtrar_por_metodo(cls, metodo: str) -> list:

        return [e for e in cls._historial if e["metodo"] == metodo]
