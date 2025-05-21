import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from tkinter import StringVar, IntVar, BooleanVar
from tkinter.filedialog import asksaveasfilename
from backend.bk_grafico2D import generar_eje_x, evaluar_funcion

class Graficas2DPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color="#121212")

        ctk.CTkLabel(
            self,
            text="📈 Gráficas de Funciones 2D",
            font=("Segoe UI", 26, "bold"),
            text_color="#6c63ff"
        ).pack(pady=10)

        # Frame de entrada básica
        input_frame = ctk.CTkFrame(self)
        input_frame.pack(pady=10)

        self.entrada_funcion = ctk.CTkEntry(
            input_frame,
            placeholder_text="Ingresa la función de x, ejemplo: sin(x)*x",
            width=350
        )
        self.entrada_funcion.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.rango_inicio = ctk.CTkEntry(
            input_frame,
            placeholder_text="Inicio X",
            width=100
        )
        self.rango_inicio.grid(row=1, column=0, padx=10)

        self.rango_fin = ctk.CTkEntry(
            input_frame,
            placeholder_text="Fin X",
            width=100
        )
        self.rango_fin.grid(row=1, column=1, padx=10)

        ctk.CTkButton(
            self,
            text="Graficar",
            command=self.graficar_funcion
        ).pack(pady=5)

        # Opciones avanzadas
        adv_frame = ctk.CTkFrame(self, fg_color="#23272a", corner_radius=10)
        adv_frame.pack(pady=10, fill="x", padx=20)

        # Resolución (número de puntos)
        ctk.CTkLabel(adv_frame, text="Resolución:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
        self.resol_var = IntVar(value=500)
        ctk.CTkSlider(
            adv_frame,
            from_=100,
            to=2000,
            number_of_steps=19,
            variable=self.resol_var,
            width=200
        ).grid(row=0, column=1, padx=5)

        # Color de línea
        ctk.CTkLabel(adv_frame, text="Color:", font=("Arial", 12)).grid(row=0, column=2, padx=5)
        self.color_var = StringVar(value="blue")
        ctk.CTkOptionMenu(
            adv_frame,
            values=["blue", "red", "green", "cyan", "magenta", "yellow", "black"],
            variable=self.color_var
        ).grid(row=0, column=3, padx=5)

        # Estilo de línea
        ctk.CTkLabel(adv_frame, text="Estilo de línea:", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5)
        self.style_var = StringVar(value="-")
        ctk.CTkOptionMenu(
            adv_frame,
            values=["-", "--", "-.", ":"],
            variable=self.style_var
        ).grid(row=1, column=1, padx=5)

        # Mostrar grid
        self.grid_var = BooleanVar(value=True)
        ctk.CTkCheckBox(
            adv_frame,
            text="Mostrar grid",
            variable=self.grid_var
        ).grid(row=1, column=2, padx=5)

        # Botón para guardar imagen
        ctk.CTkButton(
            adv_frame,
            text="Guardar imagen",
            command=self.guardar_imagen
        ).grid(row=1, column=3, padx=5)

        # Frame para la gráfica
        self.canvas_frame = ctk.CTkFrame(self)
        self.canvas_frame.pack(pady=10, fill="both", expand=True)
        self.canvas_frame.grid_rowconfigure(0, weight=1)
        self.canvas_frame.grid_columnconfigure(0, weight=1)

    def graficar_funcion(self):
        # Limpiar gráfico previo
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        try:
            inicio = float(self.rango_inicio.get())
            fin = float(self.rango_fin.get())
            funcion_str = self.entrada_funcion.get()
            resol = self.resol_var.get()
            color = self.color_var.get()
            style = self.style_var.get()
            show_grid = self.grid_var.get()

            x = generar_eje_x(inicio, fin, num_puntos=resol)
            y = evaluar_funcion(funcion_str, x)
        except Exception as e:
            CTkMessagebox(title="Error", message=str(e), icon="cancel")
            return

        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
        ax.plot(x, y, color=color, linestyle=style, label=f"f(x) = {funcion_str}")
        ax.set_title("Gráfica de f(x)")
        if show_grid:
            ax.grid(True)
        ax.legend()
        fig.tight_layout()
        fig.subplots_adjust(left=0.1, right=0.95, top=0.9, bottom=0.1)

        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        widget = canvas.get_tk_widget()
        widget.grid(row=0, column=0, sticky="nsew")

    def guardar_imagen(self):
        # Solicita ruta y guarda la figura actual como PNG
        path = asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png")]
        )
        if path:
            fig = plt.gcf()
            fig.savefig(path)
            CTkMessagebox(title="Éxito", message=f"Imagen guardada en:\n{path}", icon="check")