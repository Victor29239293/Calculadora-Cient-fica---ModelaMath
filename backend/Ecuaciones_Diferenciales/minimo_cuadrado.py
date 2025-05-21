import numpy as np
import matplotlib.pyplot as plt

class MinimosCuadrados:
    """
    Proporciona ajuste de mínimos cuadrados lineal.
    """
    @staticmethod
    def ajustar_lineal(xs: list, ys: list) -> dict:
        """
        Ajusta una línea y = a*x + b a los datos.
        :param xs: Lista de valores x.
        :param ys: Lista de valores y.
        :return: Diccionario con 'a', 'b', 'xs', 'ys_originales', 'ys_ajustados'
        """
        x_arr = np.array(xs, dtype=float)
        y_arr = np.array(ys, dtype=float)
        n = len(x_arr)
        x_mean = x_arr.mean()
        y_mean = y_arr.mean()
        # coeficiente a
        a = ((x_arr - x_mean) * (y_arr - y_mean)).sum() / ((x_arr - x_mean)**2).sum()
        # ordenada b
        b = y_mean - a * x_mean
        # valores ajustados
        ys_ajust = a * x_arr + b
        return {
            "a": float(a),
            "b": float(b),
            "xs": list(x_arr),
            "ys_originales": list(y_arr),
            "ys_ajustados": list(ys_ajust)
        }

    @staticmethod
    def graficar_ajuste(xs, ys_originales, ys_ajustados):
        import numpy as np
        xs = np.array(xs)
        ys_originales = np.array(ys_originales)
        ys_ajustados = np.array(ys_ajustados)

        # Ordena los valores para la línea de ajuste
        orden = np.argsort(xs)
        xs_ord = xs[orden]
        ys_ajustados_ord = ys_ajustados[orden]

        fig, ax = plt.subplots(figsize=(7, 4))
        ax.scatter(xs, ys_originales, color="#2980b9", label="Datos originales", s=60, zorder=3)
        ax.plot(xs_ord, ys_ajustados_ord, color="#e74c3c", label="Recta de ajuste", linewidth=2, zorder=2)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title("Ajuste por Mínimos Cuadrados")
        ax.legend()
        ax.grid(True, linestyle="--", alpha=0.7)
        fig.tight_layout()
        return fig